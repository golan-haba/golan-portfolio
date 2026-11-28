/* Golan Haba — portfolio interactions */
(() => {
  /* ---------- mobile menu ---------- */
  const menu = document.querySelector('.menu');
  const openBtn = document.querySelector('.burger');
  if (menu && openBtn) {
    const close = () => { menu.classList.remove('open'); openBtn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; };
    openBtn.addEventListener('click', () => { menu.classList.add('open'); openBtn.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; menu.querySelector('.menu-close').focus(); });
    menu.addEventListener('click', e => { if (e.target === menu || e.target.closest('.menu-close') || e.target.closest('a')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  /* ---------- coverflow carousels (mobile only — on desktop they are grids) ---------- */
  const isDesktop = window.matchMedia('(min-width: 900px)');
  document.querySelectorAll('.cf').forEach(cf => {
    const track = cf.querySelector('.cf-track');
    const items = [...track.children];
    const centerOf = el => el.offsetLeft + el.offsetWidth / 2;
    const goTo = el => track.scrollTo({ left: centerOf(el) - track.clientWidth / 2, behavior: 'smooth' });
    let focused = null;

    const update = () => {
      if (isDesktop.matches) { items.forEach(el => { el.style.transform = el.style.filter = el.style.opacity = ''; el.classList.remove('is-focus'); }); focused = null; return; }
      const mid = track.scrollLeft + track.clientWidth / 2;
      let best = null, bestD = Infinity;
      items.forEach(el => {
        const d = Math.abs(centerOf(el) - mid);
        const t = Math.min(d / (el.offsetWidth + 12), 1);
        el.style.transform = `scale(${1 - 0.2 * t})`;
        el.style.filter = t > 0.02 ? `blur(${(6 * t).toFixed(1)}px)` : 'none';
        el.style.opacity = 1 - 0.25 * t;
        if (d < bestD) { bestD = d; best = el; }
      });
      if (best !== focused) {
        items.forEach(el => el.classList.toggle('is-focus', el === best));
        // pause any video that left the centre
        items.forEach(el => { if (el !== best) el.querySelectorAll('video[data-click]').forEach(stopVideo); });
        focused = best;
      }
    };
    let raf = 0;
    track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', update);

    items.forEach(el => el.addEventListener('click', e => {
      if (!isDesktop.matches && el !== focused) { e.preventDefault(); e.stopPropagation(); goTo(el); }
    }, true));

    cf.querySelector('.cf-prev')?.addEventListener('click', () => { const i = items.indexOf(focused); goTo(items[Math.max(0, i - 1)]); });
    cf.querySelector('.cf-next')?.addEventListener('click', () => { const i = items.indexOf(focused); goTo(items[Math.min(items.length - 1, i + 1)]); });

    // start on the middle item
    const start = items[Math.floor((items.length - 1) / 2)];
    isDesktop.addEventListener?.('change', () => init());
    const init = () => { track.scrollLeft = centerOf(start) - track.clientWidth / 2; update(); };
    if (document.readyState === 'complete') init(); else window.addEventListener('load', init);
    init();
  });

  /* ---------- mobile lightbox: tap a carousel item to enlarge it, tap outside to close ---------- */
  (() => {
    const lb = document.createElement('div');
    lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<div class="lb-box"></div>';
    document.body.appendChild(lb);
    const box = lb.querySelector('.lb-box');
    let src = null, ph = null;

    const open = item => {
      const r = item.getBoundingClientRect();
      const ar = r.width / r.height;
      const maxW = window.innerWidth - 40, maxH = window.innerHeight - 80;
      const w = Math.min(maxW, maxH * ar);
      ph = document.createElement('div');
      ph.style.cssText = `width:${r.width / (parseFloat(item.style.transform?.match(/scale\(([\d.]+)/)?.[1]) || 1)}px;height:${item.offsetHeight}px`;
      src = item;
      while (item.firstChild) box.appendChild(item.firstChild);
      item.appendChild(ph);
      box.style.width = w + 'px';
      // grow from where the item was
      const to = { x: (window.innerWidth - w) / 2, y: (window.innerHeight - w / ar) / 2 };
      const s = r.width / w;
      box.style.transition = 'none';
      box.style.transform = `translate(${r.left - to.x}px, ${r.top - to.y}px) scale(${s})`;
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      requestAnimationFrame(() => requestAnimationFrame(() => { box.style.transition = ''; box.style.transform = 'none'; }));
    };
    const close = () => {
      if (!src) return;
      const r = ph.getBoundingClientRect(), b = box.getBoundingClientRect();
      box.style.transform = `translate(${r.left - b.left}px, ${r.top - b.top}px) scale(${r.width / b.width})`;
      lb.classList.add('closing');
      setTimeout(() => {
        box.querySelectorAll('video[data-click]').forEach(v => { v.pause(); v.closest('.media')?.classList.remove('playing'); });
        ph.remove();
        while (box.firstChild) src.appendChild(box.firstChild);
        lb.classList.remove('open', 'closing'); box.style.transform = ''; box.style.width = '';
        document.body.style.overflow = ''; src = ph = null;
      }, 260);
    };
    lb.addEventListener('click', e => { if (!e.target.closest('.lb-box > *')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });

    document.querySelectorAll('.cf-item, .pair-row > *').forEach(item => item.addEventListener('click', e => {
      if (isDesktop.matches || src) return;
      if (e.target.closest('.play') || item.querySelector('.media.playing')) return;
      if (item.classList.contains('cf-item') && !item.classList.contains('is-focus')) return; // side items just scroll into the centre
      e.preventDefault();
      open(item);
    }));
  })();

  /* ---------- videos ---------- */
  // If a video file is missing, keep showing its poster image instead.
  document.querySelectorAll('video').forEach(v => {
    const src = v.querySelector('source');
    const fallback = () => {
      if (!v.poster || v.closest('.inset') || v.classList.contains('hover-vid')) { v.remove(); return; }
      const img = new Image(); img.src = v.poster; img.alt = v.getAttribute('aria-label') || '';
      img.width = v.width; img.height = v.height; img.className = v.className;
      v.closest('.media')?.querySelector('.play')?.remove();
      v.replaceWith(img);
    };
    src?.addEventListener('error', fallback);
  });

  // click-to-play videos (play button)
  function stopVideo(v) { v.pause(); v.closest('.media')?.classList.remove('playing'); }
  document.querySelectorAll('.media .play').forEach(btn => {
    const media = btn.closest('.media'); const v = media.querySelector('video');
    btn.addEventListener('click', () => {
      document.querySelectorAll('video[data-click]').forEach(o => o !== v && stopVideo(o));
      v.muted = false; v.play(); media.classList.add('playing');
    });
    v.addEventListener('click', () => { if (!v.paused) stopVideo(v); });
    v.addEventListener('ended', () => stopVideo(v));
  });

  // autoplay videos only play while on screen (saves battery & data)
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    entries.forEach(e => {
      const v = e.target;
      if (e.isIntersecting) { v.play().catch(() => {}); } else { v.pause(); }
    });
  }, { threshold: 0.2 }) : null;
  document.querySelectorAll('video[autoplay]').forEach(v => io?.observe(v));


  /* ---------- home intro, stop motion like the launch video: face pops in with a poof, name is typed, role letters pop in tilted and keep boiling ---------- */
  (() => {
    const root = document.documentElement, hero = document.querySelector('.hero');
    const face = hero && hero.querySelector('.hero-face'), h1 = hero && hero.querySelector('h1'), role = hero && hero.querySelector('.role');
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!face || !h1 || !role || reduce) { root.classList.remove('intro-pending'); return; }
    const intro = root.classList.contains('intro-pending');
    try { sessionStorage.setItem('gh_intro', '1'); } catch (e) {}
    const FPS = 8, rnd = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
    const cl = x => Math.max(0, Math.min(1, x)), seg = (t, a, b) => cl((t - a) / (b - a));
    const back = x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
    const split = (el, cls) => {
      const txt = el.textContent; el.setAttribute('aria-label', txt); el.textContent = '';
      return [...txt].map(ch => { const s = document.createElement('span'); s.className = cls; s.setAttribute('aria-hidden', 'true');
        s.textContent = ch === ' ' ? ' ' : ch; el.appendChild(s); return s; });
    };
    const nameL = split(h1, 'tl'), roleL = split(role, 'rl');
    const tilt = roleL.map((_, i) => (i % 2 ? 1 : -1) * (4 + (i * 37) % 5));
    const cur = document.createElement('span'); cur.className = 'type-cur'; cur.setAttribute('aria-hidden', 'true');
    const box = face.parentElement, puffs = [];
    if (intro) for (let i = 0; i < 9; i++) { const p = document.createElement('span'); p.className = 'intro-puff'; box.appendChild(p); puffs.push(p); }
    const T_TYPE = 0.75, T_ROLE = T_TYPE + nameL.length / FPS + 0.25, T_END = T_ROLE + roleL.length / FPS + 0.5;
    let k = intro ? 0 : Math.ceil(T_END * FPS), visible = true;
    const frame = () => {
      const t = k / FPS, boil = Math.floor(k / 3);
      // face: pop in (scale with overshoot), then a gentle boil
      const sc = intro ? back(seg(t, 0, 0.42)) : 1, on = t > 0.45;
      face.style.transform = `translate(${on ? (rnd(boil) - .5) * 4 : 0}px,${on ? (rnd(boil + 7) - .5) * 4 : 0}px) scale(${sc}) rotate(${on ? (rnd(boil + 3) - .5) * 3 : 0}deg)`;
      // poof
      if (puffs.length) {
        const pp = seg(t, 0.05, 0.55), r0 = face.offsetWidth * 0.35, cx = face.offsetLeft + face.offsetWidth / 2, cy = face.offsetTop + face.offsetHeight / 2;
        puffs.forEach((p, i) => { const a = i / 9 * Math.PI * 2 + rnd(i) * .5, r = r0 + face.offsetWidth * 0.9 * pp;
          p.style.display = t >= 0.05 && t < 0.6 ? 'block' : 'none';
          p.style.left = cx + 'px'; p.style.top = cy + 'px'; p.style.width = face.offsetWidth * 0.32 + 'px';
          p.style.transform = `translate(-50%,-50%) translate(${Math.cos(a) * r}px,${Math.sin(a) * r}px) scale(${(1 - pp) * (0.8 + rnd(i + 20) * .8)})`; });
        if (t >= 0.6) { puffs.forEach(p => p.remove()); puffs.length = 0; }
      }
      // typing
      const n = Math.max(0, Math.floor((t - T_TYPE) * FPS) + 1);
      nameL.forEach((s, i) => s.style.visibility = (t >= T_TYPE && i < n) ? 'visible' : 'hidden');
      if (intro && t >= T_TYPE - 0.375 && t < T_ROLE + 0.6) {
        const last = nameL[Math.min(nameL.length, n) - 1];
        if (t >= T_TYPE && last) last.after(cur); else h1.prepend(cur);
        cur.style.visibility = (n < nameL.length && t >= T_TYPE) || Math.floor(t * 2.5) % 2 === 0 ? 'visible' : 'hidden';
      } else if (cur.isConnected) cur.remove();
      // role letters pop in one per frame, tilted, and keep boiling
      roleL.forEach((s, i) => { const st = T_ROLE + i / FPS, shown = t >= st;
        s.style.visibility = shown ? 'visible' : 'hidden';
        const ps = t < st + 1 / FPS ? 0.55 : (t < st + 2 / FPS ? 1.2 : 1);
        const jx = (rnd(boil * 7 + i) - .5) * 3, jy = (rnd(boil * 3 + i * 11) - .5) * 3, jr = (rnd(boil * 5 + i * 13) - .5) * 4;
        s.style.transform = `translate(${jx}px,${jy}px) rotate(${tilt[i] + jr}deg) scale(${ps})`; });
      root.classList.remove('intro-pending');
      k++;
    };
    frame();
    setInterval(() => { if (visible && !document.hidden) frame(); }, 1000 / FPS);
    if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(hero);
  })();

  /* ---------- brand-card logo animations ---------- */
  document.querySelectorAll('.brand-card').forEach(card => {
    const v = card.querySelector('.hover-vid'); if (!v) return;
    let ok = true;
    v.querySelector('source')?.addEventListener('error', () => { ok = false; v.remove(); });
    const play = () => { if (!ok) return; v.play().then(() => card.classList.add('is-playing')).catch(() => {}); };
    const stop = () => { card.classList.remove('is-playing'); v.pause(); };
    // the logo animations loop by themselves while the cards are on screen (desktop and mobile)
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? play() : stop()), { threshold: 0.6 }).observe(card);
    }
  });

  /* ---------- reveal on scroll ---------- */
  const rv = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); rv.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' }) : null;
  document.querySelectorAll('.reveal').forEach(el => rv ? rv.observe(el) : el.classList.add('in'));

  /* ---------- jump to a project section (projects.html#bbb etc.) ---------- */
  const jump = (smooth) => {
    const id = decodeURIComponent(location.hash.slice(1)); if (!id) return;
    const el = [...document.querySelectorAll(`[data-anchor="${id}"]`)].find(e => e.offsetParent !== null || getComputedStyle(e).position === 'absolute' && e.closest('.desk') && getComputedStyle(e.closest('.desk')).display !== 'none');
    if (!el) return;
    window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 10, behavior: smooth ? 'smooth' : 'auto' });
  };
  window.addEventListener('hashchange', () => jump(true));
  if (location.hash) window.addEventListener('load', () => setTimeout(() => jump(true), 150));

  /* ---------- floating back-to-top button ---------- */
  const fab = document.querySelector('.fab-top'), foot = document.querySelector('.site-footer');
  if (fab) {
    let footVisible = false;
    const upd = () => fab.classList.toggle('show', window.scrollY > window.innerHeight * 0.6 && !footVisible);
    if (foot && 'IntersectionObserver' in window) new IntersectionObserver(es => { footVisible = es[0].isIntersecting; upd(); }).observe(foot);
    window.addEventListener('scroll', upd, { passive: true }); upd();
    fab.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ---------- year in footer ---------- */
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
