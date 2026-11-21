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

  /* ---------- brand-card logo animations ---------- */
  document.querySelectorAll('.brand-card').forEach(card => {
    const v = card.querySelector('.hover-vid'); if (!v) return;
    let ok = true;
    v.querySelector('source')?.addEventListener('error', () => { ok = false; v.remove(); });
    const play = () => { if (!ok) return; v.play().then(() => card.classList.add('is-playing')).catch(() => {}); };
    const stop = () => { card.classList.remove('is-playing'); v.pause(); };
    if (window.matchMedia('(hover: hover)').matches) {
      card.addEventListener('mouseenter', play); card.addEventListener('mouseleave', stop);
      card.addEventListener('focus', play); card.addEventListener('blur', stop);
    } else if ('IntersectionObserver' in window) {
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
