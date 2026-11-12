/* JagX Pulse — a JagX & JRILICENSE newsroom.
   Loads the edition from data/stories.json and renders the front page,
   section filters, search, the Latest and Most read rails, and article pages. */
(function () {
  'use strict';

  var SECTIONS = [
    { id: 'all', label: 'All' },
    { id: 'world', label: 'World' },
    { id: 'africa', label: 'Africa' },
    { id: 'nigeria', label: 'Nigeria' },
    { id: 'business', label: 'Business' },
    { id: 'tech', label: 'Tech' },
    { id: 'sports', label: 'Sports' },
    { id: 'entertainment', label: 'Entertainment' },
    { id: 'health', label: 'Health' },
    { id: 'science', label: 'Science' }
  ];

  var DATA_URL = 'data/stories.json';
  var READS_KEY = 'jagx-pulse-reads';
  var state = { stories: [], edition: null, section: 'all', query: '' };

  var $ = function (id) { return document.getElementById(id); };

  /* ---------- helpers ---------- */

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function fmtDate(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var hh = String(d.getHours()).padStart(2, '0');
    var mm = String(d.getMinutes()).padStart(2, '0');
    return d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear() + ' · ' + hh + ':' + mm + ' WAT';
  }

  function ageLabel(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    var mins = Math.floor((Date.now() - d.getTime()) / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return mins + ' min ago';
    var hrs = Math.floor(mins / 60);
    if (hrs < 24) return hrs + (hrs === 1 ? ' hour ago' : ' hours ago');
    var days = Math.floor(hrs / 24);
    if (days === 1) return 'yesterday';
    if (days < 30) return days + ' days ago';
    var mo = Math.floor(days / 30);
    return mo + (mo === 1 ? ' month ago' : ' months ago');
  }

  function reads() {
    try { return JSON.parse(localStorage.getItem(READS_KEY) || '{}'); } catch (e) { return {}; }
  }

  function bumpRead(slug) {
    try {
      var r = reads();
      r[slug] = (r[slug] || 0) + 1;
      localStorage.setItem(READS_KEY, JSON.stringify(r));
    } catch (e) { /* storage unavailable — the rail just falls back to recency */ }
  }

  function cardHTML(s, opts) {
    opts = opts || {};
    var img = s.image ? '<img src="' + esc(s.image) + '" alt="' + esc(s.title) + '" loading="lazy" decoding="async" width="720" height="405">' : '';
    return '' +
      '<article class="card">' +
        '<a class="card__link" href="#/story/' + esc(s.slug) + '">' +
          '<div class="card__media">' + img + '</div>' +
          '<div class="card__body">' +
            '<span class="tag">' + esc(s.sectionLabel || s.section) + '</span>' +
            '<h3 class="card__title">' + esc(s.title) + '</h3>' +
            (opts.hideSummary ? '' : '<p class="card__sum">' + esc(s.summary) + '</p>') +
            '<div class="card__meta">' +
              '<span class="src">' + esc(s.source) + '</span>' +
              '<span class="card__dates">' +
                '<span>Published ' + esc(fmtDate(s.published)) + '</span>' +
                '<span>Added ' + esc(fmtDate(s.added)) + ' · <span class="age">' + esc(ageLabel(s.published)) + '</span></span>' +
              '</span>' +
            '</div>' +
          '</div>' +
        '</a>' +
      '</article>';
  }

  /* ---------- rendering ---------- */

  function renderCats() {
    var host = $('cats');
    if (!host) return;
    host.innerHTML = SECTIONS.map(function (s) {
      return '<button class="cat" type="button" data-section="' + s.id + '" aria-pressed="' +
        (state.section === s.id ? 'true' : 'false') + '">' + esc(s.label) + '</button>';
    }).join('');
    var foot = $('footCats');
    if (foot) {
      foot.innerHTML = SECTIONS.filter(function (s) { return s.id !== 'all'; }).map(function (s) {
        return '<li><a href="#/section/' + s.id + '">' + esc(s.label) + '</a></li>';
      }).join('');
    }
  }

  function filtered() {
    var q = state.query.trim().toLowerCase();
    return state.stories.filter(function (s) {
      if (state.section !== 'all' && s.section !== state.section) return false;
      if (!q) return true;
      return (s.title + ' ' + s.summary + ' ' + s.source + ' ' + (s.sectionLabel || '')).toLowerCase().indexOf(q) !== -1;
    });
  }

  function renderHome() {
    var list = filtered();
    var hero = list[0];
    var heroSlot = $('heroSlot');
    if (heroSlot) {
      heroSlot.innerHTML = hero ? (
        '<article class="hero">' +
          '<div class="hero__media">' +
            (hero.image ? '<img src="' + esc(hero.image) + '" alt="' + esc(hero.title) + '" width="900" height="506">' : '') +
          '</div>' +
          '<div class="hero__body">' +
            '<span class="hero__flag">Lead story · ' + esc(hero.sectionLabel || hero.section) + '</span>' +
            '<h1 class="hero__title"><a href="#/story/' + esc(hero.slug) + '">' + esc(hero.title) + '</a></h1>' +
            '<p class="hero__sum">' + esc(hero.summary) + '</p>' +
            '<div class="hero__meta">' +
              '<span>Source <b>' + esc(hero.source) + '</b></span>' +
              '<span>Published <b>' + esc(fmtDate(hero.published)) + '</b></span>' +
              '<span>Added <b>' + esc(fmtDate(hero.added)) + '</b></span>' +
              '<span><b>' + esc(ageLabel(hero.published)) + '</b></span>' +
            '</div>' +
          '</div>' +
        '</article>'
      ) : '';
    }

    var latest = $('latestTrack');
    if (latest) latest.innerHTML = list.slice(0, 12).map(function (s) { return cardHTML(s, { hideSummary: true }); }).join('');

    var r = reads();
    var mostRead = state.stories.slice().sort(function (a, b) {
      var d = (r[b.slug] || 0) - (r[a.slug] || 0);
      if (d !== 0) return d;
      return new Date(b.published) - new Date(a.published);
    }).slice(0, 12);
    var readTrack = $('readTrack');
    if (readTrack) readTrack.innerHTML = mostRead.map(function (s) { return cardHTML(s, { hideSummary: true }); }).join('');

    var grid = $('grid');
    if (grid) grid.innerHTML = list.map(function (s) { return cardHTML(s); }).join('');

    var empty = $('empty');
    if (empty) empty.hidden = list.length > 0;

    var note = $('feedNote');
    if (note) {
      var bits = [];
      if (state.section !== 'all') bits.push(SECTIONS.filter(function (s) { return s.id === state.section; })[0].label);
      if (state.query.trim()) bits.push('“' + state.query.trim() + '”');
      note.textContent = list.length + (list.length === 1 ? ' story' : ' stories') + (bits.length ? ' · ' + bits.join(' · ') : '');
    }
  }

  function renderArticle(slug) {
    var s = state.stories.filter(function (x) { return x.slug === slug; })[0];
    var host = $('articleView');
    if (!host) return;
    if (!s) {
      host.innerHTML = '<div class="article"><a class="article__back" href="#/">← Back to the front page</a>' +
        '<h1 class="article__title">That story is not in this edition</h1>' +
        '<p class="article__lead">It may have moved. Use the search box or the section filters to find it.</p></div>';
      return;
    }
    bumpRead(s.slug);
    var related = state.stories.filter(function (x) { return x.section === s.section && x.slug !== s.slug; }).slice(0, 3);
    host.innerHTML = '' +
      '<div class="article">' +
        '<a class="article__back" href="#/">← Back to the front page</a>' +
        '<span class="article__tag">' + esc(s.sectionLabel || s.section) + '</span>' +
        '<h1 class="article__title">' + esc(s.title) + '</h1>' +
        '<div class="article__meta">' +
          '<span>Source <b>' + esc(s.source) + '</b></span>' +
          '<span>Published <b>' + esc(fmtDate(s.published)) + '</b></span>' +
          '<span>Added to JagX Pulse <b>' + esc(fmtDate(s.added)) + '</b></span>' +
          '<span><b>' + esc(ageLabel(s.published)) + '</b></span>' +
        '</div>' +
        (s.image ? '<figure class="article__figure"><img src="' + esc(s.image) + '" alt="' + esc(s.title) + '" width="900" height="506">' +
          '<figcaption>' + esc(s.title) + ' — image via ' + esc(s.source) + '</figcaption></figure>' : '') +
        '<p class="article__lead">' + esc(s.summary) + '</p>' +
        '<div class="article__body">' +
          '<p>This is the summary JagX Pulse holds for this story. The full report is published by ' + esc(s.source) +
          ', and the link below opens it at the source.</p>' +
          '<p>JagX Pulse carries the headline, what the story is about, the source, the date it was published and the date it was added to this edition — so a reader arriving later can always tell how old a story is. Older editions stay online with their original dates.</p>' +
        '</div>' +
        '<div class="article__source">' +
          '<p>Read the full story at the source:</p>' +
          '<a href="' + esc(s.url) + '" target="_blank" rel="noopener noreferrer">' + esc(s.source) + ' — ' + esc(s.title) + '</a>' +
        '</div>' +
        (related.length ? '<section class="article__related"><div class="rail__head"><h2>More in ' +
          esc(s.sectionLabel || s.section) + '</h2></div><div class="grid">' +
          related.map(function (x) { return cardHTML(x); }).join('') + '</div></section>' : '') +
      '</div>';
  }

  function route() {
    var hash = location.hash || '#/';
    var mStory = hash.match(/^#\/story\/(.+)$/);
    var mSection = hash.match(/^#\/section\/([a-z]+)$/);
    var home = $('homeView'), art = $('articleView');

    if (mStory) {
      if (home) home.hidden = true;
      if (art) art.hidden = false;
      renderArticle(decodeURIComponent(mStory[1]));
      window.scrollTo(0, 0);
      return;
    }
    if (mSection) {
      state.section = mSection[1];
      state.query = '';
      var q = $('q'); if (q) q.value = '';
      renderCats();
    }
    if (home) home.hidden = false;
    if (art) art.hidden = true;
    renderHome();
  }

  /* ---------- edition bar ---------- */

  function renderEdition() {
    var e = state.edition || {};
    var up = $('edUpdated');
    if (up) up.textContent = 'Last updated ' + (e.updatedLabel || fmtDate(e.updated));
    var c = $('edCount');
    if (c) c.textContent = state.stories.length + ' stories in this edition';
    var v = $('edVersion');
    if (v) v.textContent = 'Edition ' + (e.edition || 1) + ' · ' + (e.refreshSchedule || '7 refreshes a day');
    var f = $('footStamp');
    if (f) f.textContent = 'Last updated ' + (e.updatedLabel || fmtDate(e.updated));
  }

  /* ---------- events ---------- */

  function wire() {
    document.addEventListener('click', function (ev) {
      var cat = ev.target.closest ? ev.target.closest('.cat') : null;
      if (cat) {
        state.section = cat.getAttribute('data-section');
        state.query = '';
        var q = $('q'); if (q) q.value = '';
        renderCats();
        if (location.hash.indexOf('#/story/') === 0) location.hash = '#/';
        else renderHome();
        return;
      }
      var foot = ev.target.closest ? ev.target.closest('#footCats a') : null;
      if (foot) { /* hash routing handles it */ }
    });

    var form = $('searchForm');
    if (form) {
      form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var q = $('q');
        state.query = q ? q.value : '';
        if (location.hash.indexOf('#/story/') === 0) location.hash = '#/';
        else renderHome();
      });
    }

    var input = $('q');
    if (input) {
      input.addEventListener('input', function () {
        state.query = input.value;
        if (location.hash.indexOf('#/story/') === 0) location.hash = '#/';
        else renderHome();
      });
    }

    document.addEventListener('keydown', function (ev) {
      if (ev.key === '/' && document.activeElement !== input) {
        ev.preventDefault();
        if (input) input.focus();
      }
    });

    window.addEventListener('hashchange', route);
  }

  /* ---------- PWA install ---------- */

  var deferred = null;
  window.addEventListener('beforeinstallprompt', function (ev) {
    ev.preventDefault();
    deferred = ev;
    var b = $('installBtn');
    if (b) b.hidden = false;
  });

  function wireInstall() {
    var b = $('installBtn');
    if (!b) return;
    b.addEventListener('click', function () {
      if (!deferred) return;
      deferred.prompt();
      deferred.userChoice.then(function () {
        deferred = null;
        b.hidden = true;
      });
    });
    window.addEventListener('appinstalled', function () { b.hidden = true; });
  }

  /* ---------- boot ---------- */

  function boot() {
    renderCats();
    wire();
    wireInstall();

    fetch(DATA_URL, { cache: 'no-cache' })
      .then(function (r) {
        if (!r.ok) throw new Error('edition ' + r.status);
        return r.json();
      })
      .then(function (data) {
        state.edition = data;
        state.stories = (data.stories || []).slice().sort(function (a, b) {
          return new Date(b.published) - new Date(a.published);
        });
        renderEdition();
        route();
      })
      .catch(function () {
        var up = $('edUpdated');
        if (up) up.textContent = 'Edition unavailable offline';
        var grid = $('grid');
        if (grid) grid.innerHTML = '<p class="empty">The edition could not be loaded. Reconnect and reload — the last edition you read stays available offline.</p>';
      });

    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function () {
        navigator.serviceWorker.register('sw.js').catch(function () { /* offline reading simply stays unavailable */ });
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
