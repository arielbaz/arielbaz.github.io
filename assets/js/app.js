/* ARIBAZ — interactions. Zéro dépendance, tout en progressive enhancement. */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- Thème ---------- */
  var STORAGE_KEY = 'aribaz-theme';
  var media = window.matchMedia('(prefers-color-scheme: dark)');

  function systemTheme() { return media.matches ? 'dark' : 'light'; }

  function applyTheme(theme) {
    if (theme) {
      root.setAttribute('data-theme', theme);
      root.style.colorScheme = theme;
    } else {
      root.removeAttribute('data-theme');
      root.style.colorScheme = '';
    }
    var btn = document.querySelector('[data-theme-toggle]');
    if (btn) {
      var current = theme || systemTheme();
      btn.setAttribute('aria-label', current === 'dark' ? 'Passer en thème clair' : 'Passer en thème sombre');
      btn.innerHTML = current === 'dark'
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2M12 19.5v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.5 12h2M19.5 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.5 14.2A8.6 8.6 0 0 1 9.8 3.5 8.6 8.6 0 1 0 20.5 14.2Z"/></svg>';
    }
  }

  var stored = null;
  try { stored = localStorage.getItem(STORAGE_KEY); } catch (e) {}
  applyTheme(stored);
  media.addEventListener('change', function () { if (!stored) applyTheme(null); });

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-theme-toggle]');
    if (!t) return;
    e.preventDefault();
    var next = (root.getAttribute('data-theme') || systemTheme()) === 'dark' ? 'light' : 'dark';
    stored = next;
    try { localStorage.setItem(STORAGE_KEY, next); } catch (err) {}
    applyTheme(next);
  });

  /* ---------- Navigation mobile ---------- */
  var toggle = document.querySelector('[data-nav-toggle]');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        links.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- Ombre de la navbar ---------- */
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Révélation au scroll ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealEls.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 6, 5) * 50 + 'ms';
      io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Spotlight du hero ---------- */
  var hero = document.querySelector('.hero');
  if (hero && finePointer && !reduceMotion) {
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      hero.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      hero.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });
  }

  /* ---------- Parallaxe douce des blobs ---------- */
  var heroBg = document.querySelector('.hero-bg');
  if (heroBg && !reduceMotion) {
    var ticking = false;
    var parallax = function () {
      var y = window.scrollY;
      if (y < 1100) heroBg.style.transform = 'translate3d(0,' + (y * 0.10) + 'px,0)';
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(parallax); }
    }, { passive: true });
  }

  /* ---------- Cartes : inclinaison 3D + halo ---------- */
  if (finePointer && !reduceMotion) {
    document.querySelectorAll('.post-card').forEach(function (card) {
      var raf = null;
      card.addEventListener('pointermove', function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          var r = card.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width;
          var py = (e.clientY - r.top) / r.height;
          var caps = card.closest('.card-grid');
          if (caps) caps.style.perspective = '1000px';
          card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
          card.style.setProperty('--my', (e.clientY - r.top) + 'px');
          card.style.transform = 'perspective(900px) rotateX(' + ((0.5 - py) * 5).toFixed(2) + 'deg) rotateY(' + ((px - 0.5) * 6).toFixed(2) + 'deg) translateY(-4px)';
          card.style.transition = 'transform 0.12s linear, box-shadow 0.3s ease';
          raf = null;
        });
      }, { passive: true });
      card.addEventListener('pointerleave', function () {
        card.style.transform = '';
        card.style.transition = '';
      });
    });
  }

  /* ---------- Compteurs ---------- */
  var counters = document.querySelectorAll('[data-count-to]');
  if (counters.length && 'IntersectionObserver' in window && !reduceMotion) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseInt(el.dataset.countTo, 10);
        var start = performance.now();
        var dur = 900;
        var tick = function (now) {
          var p = Math.min((now - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased);
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        cio.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- Filtre + recherche ---------- */
  var searchInput = document.querySelector('[data-search]');
  var chips = Array.prototype.slice.call(document.querySelectorAll('[data-filter]'));
  var items = Array.prototype.slice.call(document.querySelectorAll('[data-post]'));
  var countEl = document.querySelector('[data-count]');
  var emptyEl = document.querySelector('[data-empty]');
  var featuredSec = document.querySelector('[data-featured-section]');
  var activeCat = 'Tous';

  function normalize(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function applyFilters() {
    var q = normalize(searchInput ? searchInput.value.trim() : '');
    var shown = 0;
    items.forEach(function (el) {
      var cat = el.dataset.cat || '';
      var hay = normalize(el.dataset.search || el.textContent);
      var okCat = activeCat === 'Tous' || cat === activeCat;
      var okQ = !q || hay.indexOf(q) !== -1;
      var ok = okCat && okQ;
      el.hidden = !ok;
      if (ok) shown++;
    });
    var filtering = !!q || activeCat !== 'Tous';
    if (featuredSec) featuredSec.hidden = filtering;
    var total = shown + (featuredSec && !featuredSec.hidden ? 1 : 0);
    if (countEl) {
      countEl.textContent = total === 0 ? 'Aucun article' : total + (total > 1 ? ' articles' : ' article');
    }
    if (emptyEl) emptyEl.hidden = shown !== 0;
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      activeCat = chip.dataset.filter;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      applyFilters();
    });
  });

  /* filtre via l'ancre (#securite, #productivite…) */
  function applyHashFilter() {
    var hash = (location.hash || '').replace('#', '');
    if (!hash) return;
    var chip = chips.filter(function (c) { return c.dataset.slug === hash; })[0];
    if (chip) chip.click();
  }
  if (chips.length) applyHashFilter();
  window.addEventListener('hashchange', applyHashFilter);

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput.focus();
      }
    });
  }
  if (items.length) applyFilters();

  /* ---------- Progression de lecture ---------- */
  var progress = document.querySelector('.progress');
  var article = document.querySelector('.article-body');
  if (progress && article) {
    var update = function () {
      var rect = article.getBoundingClientRect();
      var total = rect.height - window.innerHeight * 0.4;
      var done = Math.min(Math.max(-rect.top + 80, 0), Math.max(total, 1));
      progress.style.width = (done / Math.max(total, 1)) * 100 + '%';
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
  }


  /* ---------- Formulaire de contact ---------- */
  var cform = document.querySelector('[data-contact-form]');
  if (cform) {
    var hint = cform.querySelector('[data-form-hint]');
    cform.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = e.submitter || cform.querySelector('[data-send]');
      var mode = btn && btn.dataset.send === 'mail' ? 'mail' : 'wa';
      var name = (cform.elements.name.value || '').trim();
      var need = cform.elements.need.value || 'Projet';
      var msg = (cform.elements.message.value || '').trim();
      if (!msg) {
        cform.elements.message.focus();
        if (hint) { hint.hidden = false; hint.textContent = 'Ajoute deux lignes de message pour que je puisse t\'aider.'; }
        return;
      }
      var text = 'Bonjour ARIBAZ,' + (name ? '\nJe m\'appelle ' + name + '.' : '') + '\nBesoin : ' + need + '\n\n' + msg;
      if (mode === 'mail') {
        location.href = 'mailto:' + (cform.dataset.mail || '') +
          '?subject=' + encodeURIComponent('Demande — ' + need) +
          '&body=' + encodeURIComponent(text);
        if (hint) { hint.hidden = false; hint.textContent = 'Ton application mail s\'ouvre avec le message pré-rempli.'; }
      } else {
        window.open((cform.dataset.wa || 'https://wa.me/') + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
        if (hint) { hint.hidden = false; hint.textContent = 'WhatsApp s\'ouvre avec le message pré-rempli : il ne reste qu\'à envoyer.'; }
      }
    });
  }


  /* ---------- Titres interactifs (lettres qui réagissent au pointeur) ----------
     - découpe les titres en mots + lettres, sans casser les dégradés (traités
       comme un bloc atomique) ;
     - ressort physique : chaque lettre rejoint sa cible avec inertie ;
     - un seul rAF partagé, arrêté dès que tout est au repos ;
     - souris, trackpad et doigt, avec repli propre si mouvement réduit. */

  function initTitleFx() {
    var motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (motionQuery.matches) return;

    var titles = document.querySelectorAll('.display, .article-hero h1, .section-head h2');
    if (!titles.length) return;

    var acts = [];

    function splitTitle(el) {
      var chars = [];
      var text = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (text.length > 130) return []; // au-delà, on laisse le titre tranquille

      function walk(node) {
        if (node.nodeType === 3) {
          var raw = node.nodeValue;
          if (!raw || !raw.trim()) return;
          var frag = document.createDocumentFragment();
          raw.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) {
              frag.appendChild(document.createTextNode(part));
              return;
            }
            var word = document.createElement('span');
            word.className = 'fx-word';
            word.setAttribute('aria-hidden', 'true');
            for (var i = 0; i < part.length; i++) {
              var c = document.createElement('span');
              c.className = 'fx-char';
              c.textContent = part.charAt(i);
              word.appendChild(c);
              chars.push(c);
            }
            frag.appendChild(word);
          });
          node.parentNode.replaceChild(frag, node);
          return;
        }
        if (node.nodeType !== 1) return;
        if (node.classList && (node.classList.contains('gradient-text') || node.classList.contains('accent'))) {
          node.classList.add('fx-char', 'fx-block');
          node.setAttribute('aria-hidden', 'true');
          chars.push(node);
          return;
        }
        if (node.tagName === 'BR' || node.tagName === 'svg') return;
        Array.prototype.slice.call(node.childNodes).forEach(walk);
      }

      Array.prototype.slice.call(el.childNodes).forEach(walk);
      el.setAttribute('aria-label', text);
      return chars;
    }

    titles.forEach(function (el) {
      if (el.closest('.article-body') || el.closest('.prose')) return;
      var chars = splitTitle(el);
      if (!chars.length) return;

      el.setAttribute('data-title-fx', '');
      var state = chars.map(function () { return { x: 0, y: 0, r: 0, vx: 0, vy: 0, vr: 0, tx: 0, ty: 0, tr: 0 }; });
      var points = null;
      var raf = null;
      var pointer = null;
      var active = false;

      function measure() {
        var base = el.getBoundingClientRect();
        points = chars.map(function (c) {
          var r = c.getBoundingClientRect();
          return { x: r.left + r.width / 2 - base.left, y: r.top + r.height / 2 - base.top };
        });
      }

      function paint() {
        raf = null;
        var moving = false;
        for (var i = 0; i < chars.length; i++) {
          var s = state[i];
          s.vx = (s.vx + (s.tx - s.x) * 0.22) * 0.74;
          s.vy = (s.vy + (s.ty - s.y) * 0.22) * 0.74;
          s.vr = (s.vr + (s.tr - s.r) * 0.22) * 0.74;
          s.x += s.vx;
          s.y += s.vy;
          s.r += s.vr;
          if (Math.abs(s.tx - s.x) > 0.02 || Math.abs(s.ty - s.y) > 0.02 || Math.abs(s.tr - s.r) > 0.02) moving = true;
          chars[i].style.transform = 'translate3d(' + s.x.toFixed(2) + 'px,' + s.y.toFixed(2) + 'px,0) rotate(' + s.r.toFixed(2) + 'deg)';
        }
        if (moving) raf = requestAnimationFrame(paint);
      }

      function kick() { if (!raf) raf = requestAnimationFrame(paint); }

      function aim(clientX, clientY) {
        if (!points) measure();
        var base = el.getBoundingClientRect();
        var px = clientX - base.left;
        var py = clientY - base.top;
        el.style.setProperty('--fx-x', px.toFixed(1) + 'px');
        el.style.setProperty('--fx-y', py.toFixed(1) + 'px');

        var R = 170;
        for (var i = 0; i < chars.length; i++) {
          var p = points[i];
          var dx = p.x - px;
          var dy = p.y - py;
          var dist = Math.sqrt(dx * dx + dy * dy) || 1;
          var s = state[i];
          if (dist < R && active) {
            var f = 1 - dist / R;
            f = f * f;
            s.tx = (dx / dist) * 9 * f;
            s.ty = (dy / dist) * 7 * f - 3 * f;
            s.tr = (dx / dist) * 3.2 * f;
          } else {
            s.tx = 0; s.ty = 0; s.tr = 0;
          }
        }
        kick();
      }

      function release() {
        active = false;
        el.classList.remove('is-hover');
        state.forEach(function (s) { s.tx = 0; s.ty = 0; s.tr = 0; });
        kick();
      }

      el.addEventListener('pointerenter', function (e) {
        if (!points) measure();
        active = true;
        el.classList.add('is-hover');
        aim(e.clientX, e.clientY);
      });

      el.addEventListener('pointermove', function (e) {
        if (e.pointerType === 'touch' && !active) return;
        aim(e.clientX, e.clientY);
      }, { passive: true });

      el.addEventListener('pointerleave', release);
      el.addEventListener('pointercancel', release);
      el.addEventListener('pointerup', function (e) {
        if (e.pointerType === 'touch') setTimeout(release, 260);
      });

      var remeasure = function () { points = null; if (active) measure(); };
      window.addEventListener('resize', remeasure, { passive: true });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);
      if ('ResizeObserver' in window) new ResizeObserver(remeasure).observe(el);

      acts.push({ el: el, release: release });
    });

    // si le système passe en « mouvement réduit » en cours de route
    var onMotionChange = function () {
      if (motionQuery.matches) acts.forEach(function (a) { a.release(); });
    };
    if (motionQuery.addEventListener) motionQuery.addEventListener('change', onMotionChange);
  }

  initTitleFx();

  /* ---------- Partage ---------- */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-share]');
    if (!btn) return;
    e.preventDefault();
    var url = btn.dataset.share || location.href;
    if (navigator.share && btn.dataset.native === '1') {
      navigator.share({ title: document.title, url: url }).catch(function () {});
      return;
    }
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(function () {
        var old = btn.getAttribute('aria-label');
        btn.setAttribute('aria-label', 'Lien copié !');
        btn.classList.add('is-copied');
        setTimeout(function () {
          btn.setAttribute('aria-label', old || 'Copier le lien');
          btn.classList.remove('is-copied');
        }, 1600);
      }).catch(function () { window.prompt('Copier ce lien :', url); });
    } else {
      window.prompt('Copier ce lien :', url);
    }
  });
})();
