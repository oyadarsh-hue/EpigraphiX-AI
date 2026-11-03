/* ============================================================================
   EPIGRAPHIX-AI — ULTRA-FAST BIDIRECTIONAL SCROLL & TEXT CHOREOGRAPHY ENGINE
   Zero layout-thrashing, pre-cached DOM nodes, millisecond/microsecond speed
   ============================================================================ */
(function () {
  'use strict';

  const REALM_STAGES = [
    { name: 'PALM-LEAF STUDIO', wipe: 'iris' },
    { name: 'SAUVOLA FIBER LAB', wipe: 'diagonal' },
    { name: '3D RAKING RELIEF', wipe: 'diamond' },
    { name: 'TRIE LEXICON LAB', wipe: 'split' },
    { name: '5-MODEL MANIFOLD', wipe: 'octagon' },
    { name: 'ARCHIVAL FOLIO VAULT', wipe: 'horizon' }
  ];

  const ROTATING_PHRASES = [
    '⚡ 12-Stage Hyperspectral Palm-Leaf Restoration',
    '📜 354-Word Classical Malayalam & Grantha Trie',
    '🔬 Sauvola O(1) + FANI Neural Fiber Inpainting',
    '🧬 5-Model SVM • GNB • RF • k-NN • CNN Manifold'
  ];

  const CIPHER_GLYPHS = 'മലയാളംലിപിശ്രീ0123456789ABCDEF◈⚡';
  const RAINBOW_STOPLIST = ['#22d3ee', '#34d399', '#fbbf24', '#fb7185', '#c084fc'];

  // 1. Split headings ([data-split-chars]) & paragraphs ([data-anim-words]) once at boot
  function prepareSplitTypography() {
    document.querySelectorAll('[data-split-chars]').forEach((el) => {
      if (el.dataset.splitReady === '1') return;
      const text = el.textContent.trim();
      el.dataset.splitReady = '1';
      el.setAttribute('aria-label', text);
      const frag = document.createDocumentFragment();
      let charIdx = 0;
      const words = text.split(/(\s+)/);
      words.forEach((token) => {
        if (/^\s+$/.test(token)) {
          frag.appendChild(document.createTextNode(' '));
          return;
        }
        const wordWrap = document.createElement('span');
        wordWrap.style.display = 'inline-block';
        wordWrap.style.whiteSpace = 'nowrap';
        const segments = (typeof Intl !== 'undefined' && Intl.Segmenter)
          ? Array.from(new Intl.Segmenter('ml', { granularity: 'grapheme' }).segment(token), s => s.segment)
          : Array.from(token);
        segments.forEach((ch) => {
          const span = document.createElement('span');
          span.className = 'split-char';
          span.textContent = ch;
          span.style.setProperty('--char-i', String(Math.min(charIdx, 26)));
          charIdx++;
          wordWrap.appendChild(span);
        });
        frag.appendChild(wordWrap);
      });
      el.textContent = '';
      el.appendChild(frag);
    });

    document.querySelectorAll('[data-anim-words]').forEach((el) => {
      if (el.dataset.wordsReady === '1') return;
      const text = el.textContent.trim();
      el.dataset.wordsReady = '1';
      const frag = document.createDocumentFragment();
      text.split(/\s+/).forEach((word, idx, arr) => {
        const span = document.createElement('span');
        span.className = 'anim-word';
        span.textContent = word;
        span.style.setProperty('--word-i', String(Math.min(idx, 32)));
        frag.appendChild(span);
        if (idx < arr.length - 1) frag.appendChild(document.createTextNode(' '));
      });
      el.textContent = '';
      el.appendChild(frag);
    });

    document.querySelectorAll('[data-manifesto-words]').forEach((el) => {
      if (el.dataset.manifestoReady === '1') return;
      const text = el.textContent.trim();
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

  // 2. Ultra-fast 6-frame (~85ms) cipher scramble
  function scrambleElementText(el, targetText) {
    if (!el) return;
    if (el._scrambleRaf) cancelAnimationFrame(el._scrambleRaf);
    let frame = 0;
    const totalFrames = 6;
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
        if (ch === ' ' || ch === '•' || i < revealCount) {
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

  // 3. Geometric clip-path generator for full-bleed background world transitions
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
    const telemetryPill = document.getElementById('realm-telemetry-pill');
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleLabel = document.getElementById('theme-toggle-label');
    const heroRotatingEl = document.getElementById('hero-rotating-phrase');

    // Pre-cache all animated scroll items so the rAF loop runs in microseconds
    const scrollCards = Array.from(document.querySelectorAll('[data-scroll-card]'));
    const fanDecks = Array.from(document.querySelectorAll('[data-fan-deck]')).map((deck) => {
      const cards = deck.querySelectorAll('.collector-frame-card');
      return {
        el: deck,
        left: cards[0] || null,
        center: cards[1] || null,
        right: cards[2] || null,
        shutters: Array.from(deck.querySelectorAll('.aperture-shutter'))
      };
    });
    const kineticTracks = Array.from(document.querySelectorAll('[data-kinetic-track]')).map((track, idx) => ({
      el: track,
      dir: idx % 2 === 0 ? -1 : 1,
      offset: 0
    }));
    const manifestoEl = document.querySelector('[data-manifesto-words]');
    const manifestoWords = manifestoEl ? Array.from(manifestoEl.querySelectorAll('.manifesto-word')) : [];

    // Bidirectional IntersectionObservers (trigger EVERY TIME scrolling down OR up + refresh!)
    const splitObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('text-in-view');
        } else {
          entry.target.classList.remove('text-in-view');
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -4% 0px' });

    document.querySelectorAll('[data-split-chars]').forEach((el) => splitObserver.observe(el));

    const wordsObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('words-in-view');
        } else {
          entry.target.classList.remove('words-in-view');
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -4% 0px' });

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
    }, { threshold: 0.15 });

    document.querySelectorAll('[data-scramble]').forEach((el) => scrambleObserver.observe(el));

    // Rotating Hero Epigraphy Phrase
    let phraseIdx = 0;
    if (heroRotatingEl) {
      setInterval(() => {
        phraseIdx = (phraseIdx + 1) % ROTATING_PHRASES.length;
        heroRotatingEl.style.opacity = '0';
        heroRotatingEl.style.transform = 'translate3d(0, -6px, 0)';
        setTimeout(() => {
          heroRotatingEl.textContent = ROTATING_PHRASES[phraseIdx];
          heroRotatingEl.style.opacity = '1';
          heroRotatingEl.style.transform = 'translate3d(0, 0, 0)';
        }, 105);
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

    // Specimen Vault Filter Pills
    const vaultCards = Array.from(document.querySelectorAll('.vault-plate-card'));
    document.querySelectorAll('[data-vault-filter]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const cat = btn.getAttribute('data-vault-filter');
        vaultCards.forEach((card) => {
          const match = cat === 'all' || card.getAttribute('data-category') === cat;
          card.classList.toggle('is-hidden', !match);
        });
      });
    });

    // 1.65x Optical Loupe Lightbox for Collector Frames, Specimen Plates & IEEE Paper Pages
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
    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateOnScroll() {
      ticking = false;
      const scrollY = window.scrollY;
      const vh = Math.max(1, window.innerHeight);
      const maxScroll = Math.max(1, document.documentElement.scrollHeight - vh);
      const globalProgress = Math.max(0, Math.min(1, scrollY / maxScroll));
      const velocity = scrollY - lastScrollY;
      lastScrollY = scrollY;

      if (progressBar) {
        progressBar.style.transform = `scaleX(${globalProgress.toFixed(4)})`;
      }

      // 1. Multi-World Full-Bleed Background Morphing (Bidirectional)
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
            const panY = (localT * -16).toFixed(1);
            layer.style.transform = `translate3d(0, ${panY}px, 0) scale(${(1.03 + localT * 0.025).toFixed(3)})`;
          } else if (i === baseIdx + 1) {
            layer.style.opacity = localT > 0.002 ? '1' : '0';
            const stageCfg = REALM_STAGES[i] || REALM_STAGES[0];
            layer.style.clipPath = computeWipeClip(stageCfg.wipe, localT);
            const panY = ((1 - localT) * 16).toFixed(1);
            layer.style.transform = `translate3d(0, ${panY}px, 0) scale(${(1.055 - localT * 0.025).toFixed(3)})`;
          } else {
            layer.style.opacity = '0';
          }
        }

        const nearestIdx = Math.min(REALM_STAGES.length - 1, Math.round(scaled));
        if (nearestIdx !== activeStageIdx) {
          activeStageIdx = nearestIdx;
          if (telemetryPill && REALM_STAGES[nearestIdx]) {
            scrambleElementText(telemetryPill, `◈ ${REALM_STAGES[nearestIdx].name}`);
          }
        }
      }

      // 2. 3-Frame Scroll Fan-Out Collector Decks + Iridescent Aperture Shutters
      for (let i = 0; i < fanDecks.length; i++) {
        const d = fanDecks[i];
        const rect = d.el.getBoundingClientRect();
        const centerDist = (vh * 0.55 - (rect.top + rect.height * 0.5)) / (vh * 0.72);
        const spread = Math.max(0, Math.min(1, 1 - Math.abs(centerDist) * 0.92));
        const inBand = rect.bottom > vh * 0.08 && rect.top < vh * 0.92;

        if (d.left) {
          d.left.style.transform = `translate3d(${(-spread * 16).toFixed(1)}px, ${((1 - spread) * 14).toFixed(1)}px, 0) rotate(${(-spread * 2.6).toFixed(2)}deg) scale(${(0.95 + spread * 0.05).toFixed(3)})`;
          d.left.style.opacity = (0.45 + spread * 0.55).toFixed(2);
        }
        if (d.center) {
          d.center.style.transform = `translate3d(0, ${((1 - spread) * -10).toFixed(1)}px, 0) scale(${(0.96 + spread * 0.06).toFixed(3)})`;
          d.center.style.opacity = (0.55 + spread * 0.45).toFixed(2);
        }
        if (d.right) {
          d.right.style.transform = `translate3d(${(spread * 16).toFixed(1)}px, ${((1 - spread) * 14).toFixed(1)}px, 0) rotate(${(spread * 2.6).toFixed(2)}deg) scale(${(0.95 + spread * 0.05).toFixed(3)})`;
          d.right.style.opacity = (0.45 + spread * 0.55).toFixed(2);
        }
        for (let s = 0; s < d.shutters.length; s++) {
          d.shutters[s].classList.toggle('shutter-open', inBand);
        }
      }

      // 3. Continuous Bidirectional Card Glide & Scale
      for (let i = 0; i < scrollCards.length; i++) {
        const card = scrollCards[i];
        const rect = card.getBoundingClientRect();
        if (rect.bottom < -120 || rect.top > vh + 120) continue;
        const enterRatio = Math.max(0, Math.min(1, (vh - rect.top) / (vh * 0.42)));
        const yShift = ((1 - enterRatio) * 18).toFixed(1);
        const sc = (0.975 + enterRatio * 0.025).toFixed(3);
        card.style.transform = `translate3d(0, ${yShift}px, 0) scale(${sc})`;
        card.style.opacity = (0.38 + enterRatio * 0.62).toFixed(2);
      }

      // 4. Velocity-Reactive Kinetic Ribbons
      const deltaShift = Math.max(-28, Math.min(28, velocity * 0.45));
      for (let i = 0; i < kineticTracks.length; i++) {
        const kt = kineticTracks[i];
        kt.offset = (kt.offset + kt.dir * (0.65 + Math.abs(deltaShift) * 0.18)) % 420;
        kt.el.style.transform = `translate3d(${kt.offset.toFixed(1)}px, 0, 0)`;
      }

      // 5. Scroll-Scrubbed Rainbow Manifesto Word Illumination
      if (manifestoEl && manifestoWords.length > 0) {
        const mRect = manifestoEl.getBoundingClientRect();
        const mProg = Math.max(0, Math.min(1, (vh * 0.85 - mRect.top) / (vh * 0.62)));
        const litCount = Math.round(mProg * manifestoWords.length);
        for (let w = 0; w < manifestoWords.length; w++) {
          const wordEl = manifestoWords[w];
          const isLit = w < litCount;
          wordEl.classList.toggle('lit', isLit);
          wordEl.style.color = isLit ? wordEl.dataset.color : '';
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
