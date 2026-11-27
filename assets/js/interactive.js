/* Golan Haba — interactive portfolio: scroll-driven scenes (no libraries) */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desk = matchMedia('(min-width: 900px)');
  if (reduce) root.classList.add('rm');

  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const ease = t => 1 - Math.pow(1 - t, 3);
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  let vw = innerWidth, vh = innerHeight;

  // scrolled pixels inside a pinned section, and 0..1 progress
  const scrolled = sec => -sec.getBoundingClientRect().top;
  const progress = sec => { const t = sec.offsetHeight - vh; return t > 0 ? clamp(scrolled(sec) / t) : 0; };

  /* ---------- reveal on scroll (both) ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }),
    { rootMargin: '0px 0px -12% 0px' });
  $$('.rv').forEach(el => reduce ? el.classList.add('on') : io.observe(el));

  /* ---------- videos play only while visible ---------- */
  const vio = new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? e.target.play().catch(() => {}) : e.target.pause()), { threshold: 0.25 });
  $$('video').forEach(v => vio.observe(v));

  /* ---------- scenes ---------- */
  const bar = $('.ix-bar span');
  const hero = $('.ix-hero'), hint = $('.ix-hint');
  // each piece is thrown off the frame in its own direction, spinning (x, y in viewport units, degrees, start offset)
  const throws = [['.p-face', 0.6, -0.95, 260, 0], ['.p-name', -1.15, -0.25, -35, 0.06], ['.p-role', 1.1, 0.4, 45, 0.12],
                  ['.p-scissors', -0.75, 0.7, -140, 0.18], ['.p-ruler', 0.75, -0.8, 110, 0.24]]
    .map(([sel, x, y, r, st]) => ({ el: $(sel + ' .ix-fly'), x, y, r, st })).filter(t => t.el);
  const about = $('.ix-about'), steps = $$('.ix-step');
  const bands = $$('.ix-band-t');
  const brands = $$('.ix-brand').map(sec => ({ sec, cover: $('.ix-cover', sec), track: $('.ix-track', sec), over: 0 }));
  const stack = $('.ix-stack'), cards = $$('.ix-card');
  const rot = [-9, 6, -4, 8, -7, 3, 10, -5, 5], off = [[-14, 8], [12, -6], [-6, -12], [16, 10], [-18, -4], [6, 14], [-10, 16], [14, -14], [0, 0]];
  const pars = $$('[data-speed]');
  const contact = $('.ix-contact'), cm = $('.ix-cm'), end = $('.ix-end');

  let grid = [];
  function layout() {
    vw = innerWidth; vh = innerHeight;
    // brands: section height = logo phase + horizontal travel
    brands.forEach(b => {
      if (desk.matches && !reduce) {
        b.over = Math.max(0, b.track.scrollWidth - vw);
        b.sec.style.height = (vh * 1.9 + b.over) + 'px';
      } else { b.sec.style.height = ''; b.over = 0; }
    });
    // poster grid targets
    const cols = desk.matches ? 5 : 3, rows = Math.ceil(cards.length / cols), gap = desk.matches ? 18 : 8;
    const availH = vh * (desk.matches ? 0.6 : 0.56), availW = vw * 0.9;
    const cw = Math.min((availW - gap * (cols - 1)) / cols, ((availH - gap * (rows - 1)) / rows) * 0.755);
    const ch = cw / 0.755;
    stack.style.setProperty('--cw', cw + 'px');
    grid = cards.map((_, i) => {
      const r = Math.floor(i / cols), inRow = Math.min(cols, cards.length - r * cols), c = i - r * cols;
      return [(c - (inRow - 1) / 2) * (cw + gap), (r - (rows - 1) / 2) * (ch + gap)];
    });
    update();
  }

  function update() {
    // progress bar
    const max = document.documentElement.scrollHeight - vh;
    bar.style.transform = `scaleX(${max > 0 ? clamp(scrollY / max) : 0})`;
    if (reduce) { stackAt(1); return; }

    // hero: name shrinks and lifts, tools fly out
    const hp = progress(hero);
    throws.forEach(t => {
      const k = clamp((hp - t.st) / 0.7), q = k * k; // speeds up like a flick off the table
      t.el.style.transform = q ? `translate(${t.x * vw * q}px, ${t.y * vh * q}px) rotate(${t.r * q}deg)` : '';
    });
    hint.style.opacity = 1 - clamp(hp * 6);

    // about: steps appear one by one while pinned (desktop); on mobile they reveal as they enter
    if (desk.matches) {
      const p = progress(about);
      steps.forEach((s, i) => s.classList.toggle('on', p > 0.02 + i * 0.2));
    } else {
      steps.forEach(s => { if (s.getBoundingClientRect().top < vh * 0.85) s.classList.add('on'); });
    }

    // band titles slide sideways
    bands.forEach((t, i) => {
      const r = t.parentElement.getBoundingClientRect();
      const k = clamp((vh - r.top) / (vh + r.height));
      t.style.transform = `translateX(${(i % 2 ? -1 : 1) * (0.5 - k) * vw * 0.35}px)`;
    });

    // brands: the black cover with the logo is flicked off the frame, then the work slides sideways
    brands.forEach(b => {
      if (desk.matches) {
        const s = scrolled(b.sec);
        const q = clamp(s / (vh * 0.7)), e = q * q;
        b.cover.style.transform = e ? `translate(${-e * vw * 0.15}px, ${-e * vh * 1.25}px) rotate(${-e * 14}deg)` : '';
        const p2 = clamp((s - vh * 0.7) / Math.max(1, b.over));
        b.track.style.transform = `translateX(${-p2 * b.over}px)`;
      } else {
        const r = b.cover.getBoundingClientRect();
        const k = clamp(-r.top / r.height), e = k * k;
        b.cover.style.transform = e ? `translate(${-e * vw * 0.35}px, ${e * r.height * 0.2}px) rotate(${-e * 16}deg)` : '';
      }
    });

    // poster stack fans out into a grid
    stackAt(ease(clamp((progress(stack) - 0.08) / 0.7)));

    // gentle parallax
    pars.forEach(el => {
      const sp = parseFloat(el.dataset.speed) || 0; if (!sp || !el.classList.contains('on')) return;
      const r = el.getBoundingClientRect();
      el.style.transform = `translateY(${(r.top + r.height / 2 - vh / 2) * -sp}px)`;
    });

    // contact: the CONTACT ME line draws itself
    const c = progress(contact);
    cm.style.clipPath = `inset(0 ${100 - clamp(c / 0.6) * 100}% 0 0)`;
    end.classList.toggle('on', c > 0.55);
  }

  function stackAt(e) {
    cards.forEach((card, i) => {
      const [gx, gy] = grid[i] || [0, 0];
      const sx = off[i][0] * (desk.matches ? 1 : 0.5), sy = off[i][1] * (desk.matches ? 1 : 0.5);
      const x = lerp(sx, gx, e), y = lerp(sy, gy, e), r = lerp(rot[i], 0, e), k = lerp(desk.matches ? 1.35 : 1.6, 1, e);
      card.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px) rotate(${r}deg) scale(${k})`;
      card.style.zIndex = String(i);
    });
  }

  let ticking = false;
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; update(); }); } }, { passive: true });
  addEventListener('resize', layout);
  desk.addEventListener?.('change', layout);
  addEventListener('load', layout);
  layout();
})();
