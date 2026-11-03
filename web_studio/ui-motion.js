/* ============================================================================
   EPIGRAPHIX-AI — ENHANCED SCROLL & TYPOGRAPHY CHOREOGRAPHY ENGINE (v2026.2)
   120fps GPU-composited scroll-linked text masks, grapheme waves, laser rules,
   velocity-reactive ribbons, scroll-spy rail, count-ups, and border spotlights
   ============================================================================ */
(function () {
  'use strict';

  const REALM_STAGES = [
    { name: 'PALM-LEAF STUDIO', wipe: 'iris', sectionId: 'hero' },
    { name: 'SAUVOLA FIBER LAB', wipe: 'diagonal', sectionId: 'ocr' },
    { name: '3D RAKING RELIEF', wipe: 'diamond', sectionId: 'lexicon' },
    { name: 'TRIE LEXICON LAB', wipe: 'split', sectionId: 'architecture' },
    { name: '5-MODEL MANIFOLD', wipe: 'octagon', sectionId: 'vault' },
    { name: 'ARCHIVAL FOLIO VAULT', wipe: 'horizon', sectionId: 'research' }
  ];

  const ROTATING_PHRASES = [
    '⚡ 12-Stage Hyperspectral Palm-Leaf Restoration',
    '📜 354+ Root Classical Malayalam & Grantha Trie',
    '🔬 Sauvola O(1) + FANI Neural Fiber Inpainting',
    '🧬 5-Model SVM • GNB • RF • k-NN • CNN Manifold'
  ];

  const TECH_KEYWORDS = /^(sauvola|fani|trocr|trie|malayalam|grantha|thaliyola|n-gram|sandhi|svm|cnn|12-stage|12|354\+|1\.65×|hyperspectral|binarization)$/i;
  const CIPHER_GLYPHS = 'മലയാളംലിപിതാളിയോല0123456789◈⚡∆';
  const RAINBOW_STOPLIST = ['#22d3ee', '#34d399', '#fbbf24', '#fb7185', '#c084fc'];

  // 1. Split headings ([data-split-chars]), masked words ([data-anim-words]), & manifesto words
  function prepareSplitTypography() {
    const segmenter = (typeof Intl !== 'undefined' && Intl.Segmenter)
      ? new Intl.Segmenter('ml', { granularity: 'grapheme' })
      : null;

    document.querySelectorAll('[data-split-chars]').forEach((el) => {
      if (el.dataset.splitReady === '1') return;
      const text = el.textContent.replace(/\s+/g, ' ').trim();
      el.dataset.splitReady = '1';
      el.setAttribute('aria-label', text);

      const frag = document.createDocumentFragment();
      let charIdx = 0;
      const tokens = text.split(/(\s+)/);

      tokens.forEach((token) => {
        if (/^\s+$/.test(token)) {
          frag.appendChild(document.createTextNode(' '));
          return;
        }
        const wordMask = document.createElement('span');
        wordMask.className = 'split-word-mask';
        const segments = segmenter
          ? Array.from(segmenter.segment(token), (s) => s.segment)
          : Array.from(token);

        segments.forEach((ch) => {
          const span = document.createElement('span');
          span.className = 'split-char';
          span.textContent = ch;
          span.style.setProperty('--char-i', String(Math.min(charIdx, 30)));
          charIdx++;
          wordMask.appendChild(span);
        });
        frag.appendChild(wordMask);
      });

      el.textContent = '';
      el.appendChild(frag);

      // Attach scroll-scrubbed laser underline bar on section & interlude headings
      if (el.classList.contains('chapter-heading') || el.classList.contains('interlude-title')) {
        const rule = document.createElement('span');
        rule.className = 'heading-laser-rule';
        rule.setAttribute('aria-hidden', 'true');
        el.appendChild(rule);
      }
    });

    document.querySelectorAll('[data-anim-words]').forEach((el) => {
      if (el.dataset.wordsReady === '1') return;
      const text = el.textContent.replace(/\s+/g, ' ').trim();
      el.dataset.wordsReady = '1';
      const frag = document.createDocumentFragment();
      const words = text.split(/\s+/);

      words.forEach((word, idx) => {
        const mask = document.createElement('span');
        mask.className = 'word-mask';

        const span = document.createElement('span');
        const stripped = word.replace(/[.,;:—–()]/g, '');
        span.className = TECH_KEYWORDS.test(stripped) ? 'anim-word word-tech-accent' : 'anim-word';
        span.textContent = word;
        span.style.setProperty('--word-i', String(Math.min(idx, 34)));

        mask.appendChild(span);
        frag.appendChild(mask);
        if (idx < words.length - 1) frag.appendChild(document.createTextNode(' '));
      });

      el.textContent = '';
      el.appendChild(frag);
    });

    document.querySelectorAll('[data-manifesto-words]').forEach((el) => {
      if (el.dataset.manifestoReady === '1') return;
      const text = el.textContent.replace(/\s+/g, ' ').trim();
      el.dataset.manifestoReady = '1';
      const frag = document.createDocumentFragment();
      text.split(/\s+/).forEach((word, idx) => {
        const span = document.createElement('span');
        span.className = 'manifesto-word';
        span.textContent = word;
        span.dataset.color = RAINBOW_STOPLIST[idx % RAINBOW_STOPLIST.length];
        frag.appendChild(span);
      });
      el.textContent = '';
      el.appendChild(frag);
    });
  }

  // 2. Crisp 7-frame (~105ms) Malayalam/Palaeography cipher scramble
  function scrambleElementText(el, targetText) {
    if (!el || !targetText) return;
    if (el._scrambleRaf) cancelAnimationFrame(el._scrambleRaf);
    let frame = 0;
    const totalFrames = 7;
    const step = () => {
      frame++;
      if (frame >= totalFrames) {
        el.textContent = targetText;
        el._scrambleRaf = null;
        return;
      }
      const revealCount = Math.floor((frame / totalFrames) * targetText.length);
      let out = '';
      for (let i = 0; i < targetText.length; i++) {
        const ch = targetText[i];
        if (ch === ' ' || ch === '•' || ch === '◈' || i < revealCount) {
          out += ch;
        } else {
          out += CIPHER_GLYPHS[(i * 7 + frame * 5) % CIPHER_GLYPHS.length];
        }
      }
      el.textContent = out;
      el._scrambleRaf = requestAnimationFrame(step);
    };
    el._scrambleRaf = requestAnimationFrame(step);
  }

  // 3. Fast 11-frame (~175ms) numeric telemetry count-up
  function animateCountUp(el) {
    if (!el) return;
    const target = parseFloat(el.getAttribute('data-countup') || '0');
    const suffix = el.getAttribute('data-suffix') || '';
    const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    if (el._countRaf) cancelAnimationFrame(el._countRaf);
    let frame = 0;
    const total = 11;
    const tick = () => {
      frame++;
      const eased = 1 - Math.pow(1 - frame / total, 3);
      const val = target * eased;
      el.textContent = (frame >= total ? target : val).toFixed(decimals) + suffix;
      if (frame < total) {
        el._countRaf = requestAnimationFrame(tick);
      } else {
        el._countRaf = null;
      }
    };
    el._countRaf = requestAnimationFrame(tick);
  }

  // 4. Geometric clip-path generator for full-bleed 4K background world transitions
  function computeWipeClip(wipeType, t) {
    const p = Math.max(0, Math.min(1, t));
    if (p <= 0.001) return 'circle(0% at 50% 50%)';
    if (p >= 0.999) return 'none';

    switch (wipeType) {
      case 'iris':
        return `circle(${(p * 86).toFixed(1)}% at 50% 50%)`;
      case 'diagonal': {
        const sweep = p * 220;
        return `polygon(0% 0%, ${Math.min(100, sweep).toFixed(1)}% 0%, ${Math.max(0, sweep - 45).toFixed(1)}% 100%, 0% 100%)`;
      }
      case 'diamond': {
        const r = p * 115;
        return `polygon(50% ${(50 - r).toFixed(1)}%, ${(50 + r).toFixed(1)}% 50%, 50% ${(50 + r).toFixed(1)}%, ${(50 - r).toFixed(1)}% 50%)`;
      }
      case 'split': {
        const half = (1 - p) * 50;
        return `inset(${half.toFixed(1)}% 0% ${half.toFixed(1)}% 0%)`;
      }
      case 'octagon':
        return `circle(${(p * 88).toFixed(1)}% at 50% 48%)`;
      case 'horizon':
      default: {
        const top = (1 - p) * 100;
        return `inset(${top.toFixed(1)}% 0% 0% 0%)`;
      }
    }
  }

  function initMotionConservatory() {
    prepareSplitTypography();
    document.body.classList.add('page-refresh-enter');

    const bgLayers = Array.from(document.querySelectorAll('.bg-world-layer'));
    const progressBar = document.getElementById('scroll-progress-bar');
    const siteHeader = document.getElementById('site-header');
    const telemetryPill = document.getElementById('realm-telemetry-pill');
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleLabel = document.getElementById('theme-toggle-label');
    const heroRotatingEl = document.getElementById('hero-rotating-phrase');
    const heroSection = document.getElementById('hero');
    const railFill = document.getElementById('scroll-rail-fill');
    const railDots = Array.from(document.querySelectorAll('.scroll-rail-node'));
    const navPills = Array.from(document.querySelectorAll('.header-nav-pills .nav-pill'));

    // Pre-cache all animated scroll elements so the rAF loop executes in microseconds
    const splitHeadings = Array.from(document.querySelectorAll('[data-split-chars]'));
    const scrollCards = Array.from(document.querySelectorAll('[data-scroll-card]'));
    const fanDecks = Array.from(document.querySelectorAll('[data-fan-deck]')).map((deck) => {
      const cards = deck.querySelectorAll('.collector-frame-card');
      return {
        el: deck,
        left: cards[0] || null,
        center: cards[1] || null,
        right: cards[2] || null,
        shutters: Array.from(deck.querySelectorAll('.aperture-shutter')),
        scanlines: Array.from(deck.querySelectorAll('.frame-scanline'))
      };
    });
    const kineticTracks = Array.from(document.querySelectorAll('[data-kinetic-track]')).map((track, idx) => ({
      el: track,
      baseDir: idx % 2 === 0 ? -1 : 1,
      offset: 0
    }));
    const manifestoEl = document.querySelector('[data-manifesto-words]');
    const manifestoWords = manifestoEl ? Array.from(manifestoEl.querySelectorAll('.manifesto-word')) : [];
    const manifestoMeterFill = document.getElementById('manifestoProgressFill');
    const manifestoMeterVal = document.getElementById('manifestoProgressVal');

    const trackedSections = ['hero', 'ocr', 'lexicon', 'architecture', 'vault', 'research']
      .map((id) => ({ id, el: document.getElementById(id) }))
      .filter((s) => s.el);

    // Bidirectional IntersectionObservers (trigger EVERY TIME scrolling down OR up)
    const splitObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        entry.target.classList.toggle('text-in-view', entry.isIntersecting);
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -3% 0px' });
    splitHeadings.forEach((el) => splitObserver.observe(el));

    const wordsObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        entry.target.classList.toggle('words-in-view', entry.isIntersecting);
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -3% 0px' });
    document.querySelectorAll('[data-anim-words]').forEach((el) => wordsObserver.observe(el));

    const typeObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        entry.target.classList.toggle('type-in-view', entry.isIntersecting);
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('[data-typewriter]').forEach((el) => typeObserver.observe(el));

    const scrambleObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const el = entry.target;
        const orig = el.dataset.origText || el.textContent.trim();
        el.dataset.origText = orig;
        if (entry.isIntersecting) {
          scrambleElementText(el, orig);
        }
      });
    }, { threshold: 0.12 });

    document.querySelectorAll('[data-scramble]').forEach((el) => {
      const orig = el.dataset.origText || el.textContent.trim();
      el.dataset.origText = orig;
      scrambleObserver.observe(el);
      el.addEventListener('pointerenter', () => scrambleElementText(el, el.dataset.origText || orig));
    });

    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCountUp(entry.target);
        }
      });
    }, { threshold: 0.2 });
    document.querySelectorAll('[data-countup]').forEach((el) => countObserver.observe(el));

    // Subtle pointer border-spotlight on glass cards & collector frames (ZERO 3D card tilt)
    document.querySelectorAll('.colorful-card, .collector-frame-card, .vault-plate-card, .hero-stat-pill').forEach((card) => {
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--spot-x', `${(e.clientX - r.left).toFixed(0)}px`);
        card.style.setProperty('--spot-y', `${(e.clientY - r.top).toFixed(0)}px`);
      }, { passive: true });
    });

    // Rotating Hero Epigraphy Phrase
    let phraseIdx = 0;
    if (heroRotatingEl) {
      setInterval(() => {
        phraseIdx = (phraseIdx + 1) % ROTATING_PHRASES.length;
        heroRotatingEl.style.opacity = '0';
        heroRotatingEl.style.transform = 'translate3d(0, -7px, 0) scale(0.97)';
        setTimeout(() => {
          heroRotatingEl.textContent = ROTATING_PHRASES[phraseIdx];
          heroRotatingEl.style.opacity = '1';
          heroRotatingEl.style.transform = 'translate3d(0, 0, 0) scale(1)';
        }, 115);
      }, 2700);
    }

    // Ultra-Fast Celestial Light / Dark Theme Toggle (<= 190ms)
    const savedTheme = localStorage.getItem('epigraphix_theme') || 'dark';
    const applyTheme = (theme) => {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('epigraphix_theme', theme);
      if (themeToggleLabel) {
        themeToggleLabel.textContent = theme === 'dark' ? '☀️ Solar Light' : '🌙 Cosmic Dark';
      }
    };
    applyTheme(savedTheme);

    if (themeToggleBtn) {
      themeToggleBtn.addEventListener('click', () => {
        const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        if (document.startViewTransition) {
          document.startViewTransition(() => applyTheme(next));
        } else {
          applyTheme(next);
        }
      });
    }

    // Ultra-fast 150ms Cubic-Out Smooth Anchor Navigation
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        if (!targetId || targetId === '#') return;
        const targetEl = document.querySelector(targetId);
        if (!targetEl) return;
        e.preventDefault();
        const startY = window.scrollY;
        const endY = Math.max(0, targetEl.getBoundingClientRect().top + startY - 82);
        const startTime = performance.now();
        const duration = 150;
        const tickScroll = (now) => {
          const p = Math.min(1, (now - startTime) / duration);
          const eased = 1 - Math.pow(1 - p, 3);
          window.scrollTo(0, startY + (endY - startY) * eased);
          if (p < 1) requestAnimationFrame(tickScroll);
        };
        requestAnimationFrame(tickScroll);
      });
    });

    // Quick-Load Sample Manuscript Buttons & Hero Shortcuts
    document.querySelectorAll('[data-load-sample]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const sampleFile = btn.getAttribute('data-load-sample');
        if (sampleFile && typeof window.loadImage === 'function') {
          window.loadImage(sampleFile);
        }
        const ocrSec = document.getElementById('ocr');
        if (ocrSec) {
          const targetY = Math.max(0, ocrSec.getBoundingClientRect().top + window.scrollY - 82);
          window.scrollTo({ top: targetY, behavior: 'auto' });
        }
      });
    });

    const btnTriggerUpload = document.getElementById('btnQuickUpload');
    if (btnTriggerUpload) {
      btnTriggerUpload.addEventListener('click', () => {
        const fi = document.getElementById('fileInput');
        if (fi) fi.click();
      });
    }

    const heroBenchmarkBtn = document.getElementById('btnHeroBenchmark');
    if (heroBenchmarkBtn) {
      heroBenchmarkBtn.addEventListener('click', () => {
        const runBtn = document.getElementById('btnRunBenchmark');
        if (runBtn) runBtn.click();
      });
    }

    // Quick Malayalam Lexicon Root Chips
    document.querySelectorAll('[data-dict-word]').forEach((chip) => {
      chip.addEventListener('click', () => {
        const word = chip.getAttribute('data-dict-word');
        if (word && typeof window.setSearchQuery === 'function') {
          window.setSearchQuery(word);
        }
      });
    });

    // Specimen Vault Filter Pills with active highlight
    const vaultCards = Array.from(document.querySelectorAll('.vault-plate-card'));
    const vaultFilterBtns = Array.from(document.querySelectorAll('[data-vault-filter]'));
    vaultFilterBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const cat = btn.getAttribute('data-vault-filter');
        vaultFilterBtns.forEach((b) => b.classList.toggle('is-active-filter', b === btn));
        vaultCards.forEach((card) => {
          const match = cat === 'all' || card.getAttribute('data-category') === cat;
          card.classList.toggle('is-hidden', !match);
        });
      });
    });

    // 1.65x Optical Loupe Lightbox
    const lightbox = document.getElementById('loupeLightbox');
    const loupeImg = document.getElementById('loupeImage');
    const loupeTitle = document.getElementById('loupeTitle');
    const loupeClose = document.getElementById('loupeCloseBtn');
    const loupeViewport = document.getElementById('loupeViewport');

    function openLoupe(src, title) {
      if (!lightbox || !loupeImg) return;
      loupeImg.src = src;
      if (loupeTitle) loupeTitle.textContent = title || 'EpigraphiX-AI Archival Plate';
      lightbox.classList.add('active');
    }

    document.querySelectorAll('[data-loupe-src]').forEach((item) => {
      item.addEventListener('click', () => {
        openLoupe(item.getAttribute('data-loupe-src'), item.getAttribute('data-loupe-title'));
      });
    });

    if (loupeViewport && loupeImg) {
      loupeViewport.addEventListener('mousemove', (e) => {
        const rect = loupeViewport.getBoundingClientRect();
        const ox = ((e.clientX - rect.left) / rect.width) * 100;
        const oy = ((e.clientY - rect.top) / rect.height) * 100;
        loupeImg.style.transformOrigin = `${ox.toFixed(1)}% ${oy.toFixed(1)}%`;
        loupeImg.style.transform = 'scale(1.65)';
      });
      loupeViewport.addEventListener('mouseleave', () => {
        loupeImg.style.transform = 'scale(1)';
      });
    }

    if (loupeClose) loupeClose.addEventListener('click', () => lightbox.classList.remove('active'));
    if (lightbox) {
      lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) lightbox.classList.remove('active');
      });
    }

    // Continuous Bidirectional Scroll Engine (Upward + Downward + Refresh)
    let activeStageIdx = -1;
    let activeSectionId = '';
    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateOnScroll() {
      ticking = false;
      const scrollY = window.scrollY;
      const vh = Math.max(1, window.innerHeight);
      const maxScroll = Math.max(1, document.documentElement.scrollHeight - vh);
      const globalProgress = Math.max(0, Math.min(1, scrollY / maxScroll));
      const velocity = scrollY - lastScrollY;
      const scrollDir = velocity >= 0 ? 1 : -1;
      lastScrollY = scrollY;

      if (progressBar) {
        progressBar.style.transform = `scaleX(${globalProgress.toFixed(4)})`;
      }
      if (railFill) {
        railFill.style.transform = `scaleY(${globalProgress.toFixed(4)})`;
      }
      if (siteHeader) {
        siteHeader.classList.toggle('is-scrolled', scrollY > 36);
      }

      // Active Section Scroll-Spy for Header Nav Pills & Right Chapter Rail
      let currentSec = trackedSections[0] ? trackedSections[0].id : 'hero';
      for (let i = 0; i < trackedSections.length; i++) {
        const r = trackedSections[i].el.getBoundingClientRect();
        if (r.top <= vh * 0.42) {
          currentSec = trackedSections[i].id;
        }
      }
      if (currentSec !== activeSectionId) {
        activeSectionId = currentSec;
        navPills.forEach((pill) => {
          pill.classList.toggle('nav-pill-active', pill.getAttribute('href') === `#${currentSec}`);
        });
        railDots.forEach((dot) => {
          dot.classList.toggle('is-active', dot.getAttribute('href') === `#${currentSec}`);
        });
      }

      // 0. Multi-Plane Hero Depth Parallax
      if (heroSection && scrollY < vh * 1.15) {
        const hp = Math.max(0, Math.min(1, scrollY / (vh * 0.85)));
        heroSection.style.setProperty('--hero-p', hp.toFixed(3));
      }

      // 1. Multi-World Full-Bleed 4K Background Morphing (Bidirectional)
      const worldCount = bgLayers.length;
      if (worldCount > 0) {
        const scaled = globalProgress * (worldCount - 1);
        const baseIdx = Math.min(worldCount - 1, Math.floor(scaled));
        const localT = scaled - baseIdx;

        for (let i = 0; i < worldCount; i++) {
          const layer = bgLayers[i];
          if (i < baseIdx) {
            layer.style.opacity = '0';
          } else if (i === baseIdx) {
            layer.style.opacity = '1';
            layer.style.clipPath = 'none';
            const panY = (localT * -18).toFixed(1);
            layer.style.transform = `translate3d(0, ${panY}px, 0) scale(${(1.03 + localT * 0.028).toFixed(3)})`;
          } else if (i === baseIdx + 1) {
            layer.style.opacity = localT > 0.002 ? '1' : '0';
            const stageCfg = REALM_STAGES[i] || REALM_STAGES[0];
            layer.style.clipPath = computeWipeClip(stageCfg.wipe, localT);
            const panY = ((1 - localT) * 18).toFixed(1);
            layer.style.transform = `translate3d(0, ${panY}px, 0) scale(${(1.058 - localT * 0.028).toFixed(3)})`;
          } else {
            layer.style.opacity = '0';
          }
        }

        const nearestIdx = Math.min(REALM_STAGES.length - 1, Math.round(scaled));
        if (nearestIdx !== activeStageIdx) {
          activeStageIdx = nearestIdx;
          if (telemetryPill && REALM_STAGES[nearestIdx]) {
            const label = `◈ ${REALM_STAGES[nearestIdx].name}`;
            telemetryPill.dataset.origText = label;
            scrambleElementText(telemetryPill, label);
          }
        }
      }

      // 2. Scroll-Scrubbed Heading Laser Rule & Chromatic Shimmer Progress
      for (let i = 0; i < splitHeadings.length; i++) {
        const h = splitHeadings[i];
        const r = h.getBoundingClientRect();
        if (r.bottom < -60 || r.top > vh + 60) continue;
        const hp = Math.max(0, Math.min(1, (vh * 0.88 - r.top) / (vh * 0.46)));
        h.style.setProperty('--head-prog', hp.toFixed(3));
      }

      // 3. 3-Frame Scroll Fan-Out Collector Decks + Shutters + Live Optical Scanline
      for (let i = 0; i < fanDecks.length; i++) {
        const d = fanDecks[i];
        const rect = d.el.getBoundingClientRect();
        if (rect.bottom < -120 || rect.top > vh + 120) continue;
        const centerDist = (vh * 0.54 - (rect.top + rect.height * 0.5)) / (vh * 0.72);
        const spread = Math.max(0, Math.min(1, 1 - Math.abs(centerDist) * 0.9));
        const scanPos = Math.max(0, Math.min(100, ((vh - rect.top) / (vh + rect.height)) * 100));
        const inBand = rect.bottom > vh * 0.08 && rect.top < vh * 0.92;

        if (d.left) {
          d.left.style.transform = `perspective(900px) translate3d(${(-spread * 18).toFixed(1)}px, ${((1 - spread) * 16).toFixed(1)}px, 0) rotateZ(${(-spread * 2.8).toFixed(2)}deg) rotateY(${(spread * 4.5).toFixed(2)}deg) scale(${(0.94 + spread * 0.06).toFixed(3)})`;
          d.left.style.opacity = (0.42 + spread * 0.58).toFixed(2);
        }
        if (d.center) {
          d.center.style.transform = `perspective(900px) translate3d(0, ${((1 - spread) * -12).toFixed(1)}px, ${(spread * 14).toFixed(1)}px) scale(${(0.95 + spread * 0.065).toFixed(3)})`;
          d.center.style.opacity = (0.52 + spread * 0.48).toFixed(2);
        }
        if (d.right) {
          d.right.style.transform = `perspective(900px) translate3d(${(spread * 18).toFixed(1)}px, ${((1 - spread) * 16).toFixed(1)}px, 0) rotateZ(${(spread * 2.8).toFixed(2)}deg) rotateY(${(-spread * 4.5).toFixed(2)}deg) scale(${(0.94 + spread * 0.06).toFixed(3)})`;
          d.right.style.opacity = (0.42 + spread * 0.58).toFixed(2);
        }
        for (let s = 0; s < d.shutters.length; s++) {
          d.shutters[s].classList.toggle('shutter-open', inBand);
        }
        for (let l = 0; l < d.scanlines.length; l++) {
          d.scanlines[l].style.transform = `translate3d(0, ${(scanPos * 2.2).toFixed(1)}%, 0)`;
        }
      }

      // 4. Direction-Aware Continuous Bidirectional Card Glide & Scale
      for (let i = 0; i < scrollCards.length; i++) {
        const card = scrollCards[i];
        const rect = card.getBoundingClientRect();
        if (rect.bottom < -120 || rect.top > vh + 120) continue;
        const enterRatio = Math.max(0, Math.min(1, (vh - rect.top) / (vh * 0.38)));
        const exitTopRatio = Math.max(0, Math.min(1, (rect.bottom) / (vh * 0.26)));
        const vis = Math.min(enterRatio, exitTopRatio);
        const yShift = ((1 - enterRatio) * 20 - (1 - exitTopRatio) * 10).toFixed(1);
        const sc = (0.972 + vis * 0.028).toFixed(3);
        card.style.transform = `translate3d(0, ${yShift}px, 0) scale(${sc})`;
        card.style.opacity = (0.36 + vis * 0.64).toFixed(2);
      }

      // 5. Velocity & Direction-Reactive Kinetic Ribbons
      const speedBoost = Math.min(34, Math.abs(velocity) * 0.52);
      const skewDeg = Math.max(-4.5, Math.min(4.5, velocity * 0.09));
      for (let i = 0; i < kineticTracks.length; i++) {
        const kt = kineticTracks[i];
        const effectiveDir = kt.baseDir * (Math.abs(velocity) > 1.5 ? scrollDir : 1);
        kt.offset = (kt.offset + effectiveDir * (0.72 + speedBoost * 0.22)) % 440;
        kt.el.style.transform = `translate3d(${kt.offset.toFixed(1)}px, 0, 0) skewX(${skewDeg.toFixed(2)}deg)`;
      }

      // 6. Scroll-Scrubbed Rainbow Manifesto Word Illumination + Progress Readout
      if (manifestoEl && manifestoWords.length > 0) {
        const mRect = manifestoEl.getBoundingClientRect();
        const mProg = Math.max(0, Math.min(1, (vh * 0.86 - mRect.top) / (vh * 0.58)));
        const litCount = Math.round(mProg * manifestoWords.length);
        for (let w = 0; w < manifestoWords.length; w++) {
          const wordEl = manifestoWords[w];
          const isLit = w < litCount;
          const isCurrent = w === litCount - 1;
          wordEl.classList.toggle('lit', isLit);
          wordEl.classList.toggle('lit-head', isCurrent);
          wordEl.style.color = isLit ? wordEl.dataset.color : '';
        }
        if (manifestoMeterFill) {
          manifestoMeterFill.style.transform = `scaleX(${mProg.toFixed(3)})`;
        }
        if (manifestoMeterVal) {
          manifestoMeterVal.textContent = `${Math.round(mProg * 100)}% ILLUMINATED`;
        }
      }
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(updateOnScroll);
      }
    }, { passive: true });

    window.addEventListener('resize', () => requestAnimationFrame(updateOnScroll), { passive: true });
    updateOnScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMotionConservatory);
  } else {
    initMotionConservatory();
  }
})();
