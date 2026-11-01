(function () {
  'use strict';

  // Route every outbound HTTP(S) link through the site's central /go/bonus endpoint.
  function routeExternalLink(anchor) {
    if (!anchor || !anchor.hasAttribute('href')) return;
    var href = anchor.getAttribute('href');
    if (!href || href.charAt(0) === '#' || /^(mailto:|tel:|javascript:|data:|blob:)/i.test(href)) return;
    try {
      var destination = new URL(href, window.location.href);
      if ((destination.protocol === 'http:' || destination.protocol === 'https:') &&
          destination.origin !== window.location.origin) {
        anchor.setAttribute('href', '/go/bonus');
        anchor.removeAttribute('target');
      }
    } catch (e) {}
  }

  function routeExternalLinks(root) {
    if (!root) return;
    if (root.matches && root.matches('a[href]')) routeExternalLink(root);
    if (root.querySelectorAll) root.querySelectorAll('a[href]').forEach(routeExternalLink);
  }

  routeExternalLinks(document);
  if (window.MutationObserver && document.documentElement) {
    var outboundObserver = new MutationObserver(function (records) {
      records.forEach(function (record) {
        if (record.type === 'attributes') routeExternalLink(record.target);
        else record.addedNodes.forEach(routeExternalLinks);
      });
    });
    outboundObserver.observe(document.documentElement, {
      childList: true, subtree: true, attributes: true, attributeFilter: ['href']
    });
  }

  var menuBtn = document.getElementById('mobile-menu-btn');
  var mobileMenu = document.getElementById('mobile-menu');
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', function () {
      var open = mobileMenu.classList.toggle('hidden') === false;
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileMenu.classList.add('hidden');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Hide the header on downward scroll, but reveal it after even small
  // accumulated upward movement. Mobile browsers often emit many tiny scroll
  // deltas, so compare against a direction anchor instead of the last event.
  var lobbyHeader = document.querySelector('.lobby-header');
  if (lobbyHeader) {
    var previousScrollY = window.scrollY || window.pageYOffset;
    var directionAnchorY = previousScrollY;
    var lastScrollDirection = 0;
    var scrollFramePending = false;
    var hideThreshold = 8;
    var revealThreshold = 2;

    function updateHeaderForScroll() {
      var currentScrollY = Math.max(0, window.scrollY || window.pageYOffset);
      var mobileMenuOpen = mobileMenu && !mobileMenu.classList.contains('hidden');
      var delta = currentScrollY - previousScrollY;

      if (currentScrollY <= 80 || mobileMenuOpen) {
        lobbyHeader.classList.remove('is-scroll-hidden');
        directionAnchorY = currentScrollY;
        lastScrollDirection = 0;
      } else if (Math.abs(delta) >= 1) {
        var direction = delta > 0 ? 1 : -1;
        if (direction !== lastScrollDirection) {
          lastScrollDirection = direction;
          directionAnchorY = previousScrollY;
        }

        if (direction === 1 && currentScrollY - directionAnchorY >= hideThreshold) {
          lobbyHeader.classList.add('is-scroll-hidden');
        } else if (direction === -1 && directionAnchorY - currentScrollY >= revealThreshold) {
          lobbyHeader.classList.remove('is-scroll-hidden');
        }
      }

      previousScrollY = currentScrollY;
      scrollFramePending = false;
    }

    function scheduleHeaderUpdate() {
      if (scrollFramePending) return;
      scrollFramePending = true;
      window.requestAnimationFrame(updateHeaderForScroll);
    }

    window.addEventListener('scroll', scheduleHeaderUpdate, { passive: true });
    if (menuBtn) {
      menuBtn.addEventListener('click', function () {
        window.requestAnimationFrame(updateHeaderForScroll);
      });
    }
  }

  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (!href || href === '#') return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* Horizontal lobby rails */
  document.querySelectorAll('[data-scroll]').forEach(function (button) {
    button.addEventListener('click', function () {
      var track = document.getElementById(button.getAttribute('data-scroll'));
      if (!track) return;
      var direction = Number(button.getAttribute('data-dir') || 1);
      var step = Math.min(Math.max(220, track.clientWidth * 0.72), 520);
      track.scrollBy({ left: direction * step, behavior: 'smooth' });
    });
  });

  /* Small interactive favorite buttons — visual only */
  document.querySelectorAll('.game-fav').forEach(function (button) {
    button.addEventListener('click', function () {
      var active = button.classList.toggle('is-saved');
      button.textContent = active ? '★' : '☆';
      button.setAttribute('aria-pressed', String(active));
      button.style.color = active ? '#ffd22b' : '';
    });
  });

  /* Local game search */
  var search = document.getElementById('lobby-search');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.lobby-game-card[data-search]'));
  if (search && cards.length) {
    var noResults = document.createElement('div');
    noResults.className = 'lobby-no-results';
    noResults.textContent = 'Keine passenden Spiele in dieser Auswahl gefunden.';
    noResults.hidden = true;

    var track = cards[0].closest('.lobby-track');
    if (track) track.parentNode.insertBefore(noResults, track.nextSibling);
    var lang = (document.documentElement.getAttribute('lang') || 'de').slice(0,2);
    var noResultText = { de: 'Keine passenden Spiele in dieser Auswahl gefunden.', en: 'No matching games were found in this selection.', fr: 'Aucun jeu correspondant dans cette sélection.', es: 'No hay juegos que coincidan en esta selección.' };
    noResults.textContent = noResultText[lang] || noResultText.en;

    search.addEventListener('input', function () {
      var query = search.value.trim().toLowerCase();
      var visible = 0;
      cards.forEach(function (card) {
        var matches = !query || card.getAttribute('data-search').indexOf(query) !== -1;
        card.classList.toggle('search-hidden', !matches);
        if (matches) visible += 1;
      });
      noResults.hidden = visible !== 0 || !query;
    });
  }

  /* Search the complete catalogue across localized metadata, with relevance ranking. */
  var catalogueSearch = document.getElementById('slot-catalog-search');
  var catalogueGrid = document.getElementById('slot-catalog-grid');
  if (catalogueSearch && catalogueGrid) {
    var catalogueCards = Array.prototype.slice.call(catalogueGrid.querySelectorAll('.slot-game-card'));
    var catalogueCount = document.getElementById('slot-catalog-results');
    var catalogueEmpty = document.getElementById('slot-catalog-empty');
    var catalogueClear = document.getElementById('slot-catalog-clear');
    var catalogueLang = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
    var countLabels = {
      de: ['Spiel', 'Spiele'], en: ['game', 'games'], pl: ['gra', 'gier'],
      es: ['juego', 'juegos'], pt: ['jogo', 'jogos'], ja: ['件', '件']
    };

    function normalizeCatalogueSearch(value) {
      var text = String(value || '').toLocaleLowerCase();
      if (typeof text.normalize === 'function') {
        text = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      }
      return text.replace(/[’‘]/g, "'")
        .replace(/[^\p{L}\p{N}' ]+/gu, ' ')
        .replace(/\s+/g, ' ').trim();
    }

    function editDistanceAtMostOne(a, b) {
      if (Math.abs(a.length - b.length) > 1) return false;
      var i = 0, j = 0, edits = 0;
      while (i < a.length && j < b.length) {
        if (a[i] === b[j]) { i++; j++; continue; }
        if (++edits > 1) return false;
        if (a.length > b.length) i++;
        else if (b.length > a.length) j++;
        else { i++; j++; }
      }
      return edits + ((i < a.length || j < b.length) ? 1 : 0) <= 1;
    }

    var searchableCards = catalogueCards.map(function (card, index) {
      var title = normalizeCatalogueSearch(card.querySelector('h3') ? card.querySelector('h3').textContent : '');
      var provider = normalizeCatalogueSearch(card.querySelector('.slot-game-card-provider') ? card.querySelector('.slot-game-card-provider').textContent : '');
      var text = normalizeCatalogueSearch(card.getAttribute('data-search') || '');
      return {
        element: card, index: index, title: title, provider: provider, text: text,
        words: text.split(' ').filter(Boolean)
      };
    });

    function scoreCard(item, query, terms) {
      if (!query) return 0;
      if (item.title === query) return 1000;
      if (item.title.indexOf(query) === 0) return 900;
      if (item.title.indexOf(query) !== -1) return 800;
      if (item.provider === query) return 700;
      if (item.provider.indexOf(query) !== -1) return 650;
      if (item.text.indexOf(query) !== -1) return 600;

      var score = 0;
      for (var i = 0; i < terms.length; i++) {
        var term = terms[i];
        var found = false;
        for (var j = 0; j < item.words.length; j++) {
          var word = item.words[j];
          if (word === term) { score += 30; found = true; break; }
          if (word.indexOf(term) === 0) { score += 24; found = true; break; }
          if (term.length >= 5 && editDistanceAtMostOne(term, word)) {
            score += 12; found = true; break;
          }
        }
        if (!found) return -1;
      }
      return score;
    }

    function filterCatalogue() {
      var query = normalizeCatalogueSearch(catalogueSearch.value);
      var terms = query ? query.split(' ').filter(Boolean) : [];
      var ranked = searchableCards.map(function (item) {
        return { item: item, score: scoreCard(item, query, terms) };
      }).filter(function (entry) { return !query || entry.score >= 0; });

      ranked.sort(function (a, b) {
        return b.score - a.score || a.item.index - b.item.index;
      });

      var visible = ranked.length;
      searchableCards.forEach(function (entry) { entry.element.hidden = true; });
      ranked.forEach(function (entry) {
        entry.item.element.hidden = false;
        catalogueGrid.appendChild(entry.item.element);
      });

      if (catalogueCount) {
        var labels = countLabels[catalogueLang] || countLabels.en;
        catalogueCount.textContent = visible + ' ' + (visible === 1 ? labels[0] : labels[1]);
      }
      if (catalogueEmpty) catalogueEmpty.hidden = visible !== 0;
      if (catalogueClear) catalogueClear.hidden = query.length === 0;
      catalogueSearch.setAttribute('aria-invalid', String(visible === 0 && query.length > 0));
    }

    catalogueSearch.addEventListener('input', filterCatalogue);
    if (catalogueClear) {
      catalogueClear.addEventListener('click', function () {
        catalogueSearch.value = '';
        filterCatalogue();
        catalogueSearch.focus();
      });
    }
    catalogueSearch.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && catalogueSearch.value) {
        catalogueSearch.value = '';
        filterCatalogue();
      }
    });
    filterCatalogue();
  }
  /* Random game button */
  var randomBtn = document.getElementById('random-game');
  if (randomBtn && cards.length) {
    randomBtn.addEventListener('click', function () {
      var visibleCards = cards.filter(function (card) {
        return !card.classList.contains('search-hidden');
      });
      var pool = visibleCards.length ? visibleCards : cards;
      var chosen = pool[Math.floor(Math.random() * pool.length)];
      var track = chosen.closest('.lobby-track');

      if (track) {
        track.scrollTo({ left: Math.max(0, chosen.offsetLeft - track.offsetLeft - 20), behavior: 'smooth' });
      }
      chosen.animate([
        { transform: 'translateY(0)' },
        { transform: 'translateY(-6px)' },
        { transform: 'translateY(0)' }
      ], { duration: 420, easing: 'ease-out' });
    });
  }

  /* Category chips */
  document.querySelectorAll('.lobby-category-chip[href^="#"]').forEach(function (chip) {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.lobby-category-chip').forEach(function (item) {
        item.classList.remove('is-active');
      });
      chip.classList.add('is-active');
    });
  });

  /* Promo-code copy buttons */
  document.querySelectorAll('[data-copy-code]').forEach(function (button) {
    button.addEventListener('click', function () {
      var code = button.getAttribute('data-copy-code') || '';
      var status = button.parentElement.querySelector('.promo-code-status');
      var copyLabel = button.getAttribute('data-copy-label') || 'Copy code';
      var copiedLabel = button.getAttribute('data-copied-label') || 'Copied';
      var failLabel = button.getAttribute('data-copy-fail-label') || 'Copy manually';

      function showResult(success) {
        if (status) status.textContent = success ? copiedLabel : failLabel + ': ' + code;
        button.textContent = success ? copiedLabel : failLabel;
        button.setAttribute('aria-label', (success ? copiedLabel : failLabel) + ': ' + code);
        window.setTimeout(function () {
          button.textContent = copyLabel;
          button.setAttribute('aria-label', copyLabel + ': ' + code);
          if (status) status.textContent = '';
        }, 2200);
      }

      if (navigator.clipboard && window.isSecureContext && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(function () { showResult(true); }).catch(function () { fallbackCopy(); });
      } else {
        fallbackCopy();
      }

      function fallbackCopy() {
        var field = document.createElement('textarea');
        field.value = code;
        field.setAttribute('readonly', '');
        field.style.position = 'absolute';
        field.style.left = '-9999px';
        document.body.appendChild(field);
        field.select();
        var success = false;
        try { success = document.execCommand('copy'); } catch (e) { success = false; }
        document.body.removeChild(field);
        showResult(success);
      }
    });
  });

  /* Cookie consent */
  var banner = document.getElementById('cookie-banner');
  var accept = document.getElementById('cookie-accept');
  var decline = document.getElementById('cookie-decline');
  var settings = document.getElementById('cookie-settings');
  var panel = document.getElementById('cookie-settings-panel');
  var saveSettings = document.getElementById('cookie-save-settings');
  var analytics = document.getElementById('cookie-analytics');
  var marketing = document.getElementById('cookie-marketing');

  function readPrefs() {
    try {
      var raw = localStorage.getItem('cookie_preferences');
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  var gaId = banner ? banner.getAttribute('data-ga-id') : '';
  var gaLoaded = false;

  function loadGoogleAnalytics() {
    if (!gaId || !/^G-[A-Z0-9]+$/.test(gaId)) return;
    window['ga-disable-' + gaId] = false;
    if (!gaLoaded) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
      window.gtag('consent', 'default', {
        analytics_storage: 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied'
      });
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gaId);
      document.head.appendChild(script);
      window.gtag('js', new Date());
      window.gtag('consent', 'update', { analytics_storage: 'granted' });
      window.gtag('config', gaId);
      gaLoaded = true;
    } else if (window.gtag) {
      window.gtag('consent', 'update', { analytics_storage: 'granted' });
    }
  }

  function updateAnalyticsConsent(granted) {
    if (granted) {
      loadGoogleAnalytics();
    } else if (gaId && gaLoaded && window.gtag) {
      window['ga-disable-' + gaId] = true;
      window.gtag('consent', 'update', {
        analytics_storage: 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied'
      });
    }
  }

  function savePrefs(prefs) {
    try { localStorage.setItem('cookie_preferences', JSON.stringify(prefs)); } catch (e) {}
    updateAnalyticsConsent(prefs.analytics === true);
    if (banner) banner.classList.add('hidden');
    if (panel) panel.classList.add('hidden');
    if (settings) settings.setAttribute('aria-expanded', 'false');
  }

  if (banner) {
    var prefs = readPrefs();
    if (!prefs) {
      banner.classList.remove('hidden');
    } else {
      if (analytics) analytics.checked = prefs.analytics === true;
      if (marketing) marketing.checked = prefs.marketing === true;
      updateAnalyticsConsent(prefs.analytics === true);
    }
    if (accept) accept.addEventListener('click', function () { savePrefs({ necessary: true, analytics: true, marketing: true }); });
    if (decline) decline.addEventListener('click', function () { savePrefs({ necessary: true, analytics: false, marketing: false }); });
    if (settings) settings.addEventListener('click', function () {
      var isHidden = panel.classList.toggle('hidden');
      settings.setAttribute('aria-expanded', String(!isHidden));
    });
    if (saveSettings) saveSettings.addEventListener('click', function () {
      savePrefs({ necessary: true, analytics: !!(analytics && analytics.checked), marketing: !!(marketing && marketing.checked) });
    });
  }

  /* Track affiliate redirect clicks only after analytics consent. */
  document.addEventListener('click', function (event) {
    var link = event.target.closest ? event.target.closest('a[href]') : null;
    if (!link || !window.gtag || !gaLoaded || !gaId || window['ga-disable-' + gaId]) return;
    try {
      var target = new URL(link.href, window.location.href);
      if (target.origin === window.location.origin && /^\/go(?:\/|$)/.test(target.pathname)) {
        window.gtag('event', 'affiliate_click', {
          link_url: target.pathname,
          link_text: (link.textContent || '').trim().slice(0, 100)
        });
      }
    } catch (e) {}
  });

  /* Localized bonus wagering calculator on every language version. */
  document.querySelectorAll('[data-wager-calculator]').forEach(function (calculator) {
    var form = calculator.querySelector('[data-wager-form]');
    var result = calculator.querySelector('[data-wager-result]');
    var recommendation = calculator.querySelector('[data-wager-cta]');
    if (!form || !result) return;

    var lang = calculator.getAttribute('data-calculator-lang') || 'en';
    var locales = { de: 'de-DE', en: 'en-IE', pl: 'pl-PL', es: 'es-ES', pt: 'pt-PT', ja: 'ja-JP' };
    var locale = locales[lang] || 'en-IE';

    function currency(value) {
      return new Intl.NumberFormat(locale, {
        style: 'currency', currency: 'EUR', maximumFractionDigits: 2
      }).format(value);
    }

    form.addEventListener('input', function () {
      if (recommendation) recommendation.hidden = true;
    });
    form.addEventListener('change', function () {
      if (recommendation) recommendation.hidden = true;
    });

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;

      var deposit = Number(form.elements.deposit.value);
      var bonus = Number(form.elements.bonus.value);
      var wager = Number(form.elements.wager.value);
      var contribution = Number(form.elements.contribution.value);
      var basis = form.elements.basis.value;
      if (![deposit, bonus, wager, contribution].every(Number.isFinite) ||
          deposit < 0 || bonus < 0 || wager < 0 || contribution < 1 ||
          deposit > 100000 || bonus > 100000 || wager > 1000 || contribution > 100) {
        result.textContent = calculator.getAttribute('data-error');
        if (recommendation) recommendation.hidden = true;
        return;
      }

      var base = basis === 'deposit_bonus' ? deposit + bonus : bonus;
      var turnover = base * wager;
      var estimatedStakes = turnover / (contribution / 100);
      var baseLabel = basis === 'deposit_bonus'
        ? calculator.getAttribute('data-base-deposit')
        : calculator.getAttribute('data-base-bonus');
      var number = new Intl.NumberFormat(locale, { maximumFractionDigits: 1 }).format(wager);
      result.textContent = calculator.getAttribute('data-turnover-label') + currency(turnover) +
        '. ' + baseLabel + ' (' + currency(base) + ') × ' + number + '.' +
        calculator.getAttribute('data-at-weight') + contribution +
        calculator.getAttribute('data-weight-tail') + currency(estimatedStakes) +
        calculator.getAttribute('data-stakes-tail');
      if (recommendation) recommendation.hidden = false;
    });
  });
})();
