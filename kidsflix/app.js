// ============================================
// KidsFlix App — ShortsCraft-style UI Logic
// ============================================
(function () {
  'use strict';

  // ======= STATE =======
  const state = {
    category: 'cartoon',
    contentType: 'shorts',
    language: 'all',
    duration: 'all',
    searchQuery: '',
    savedVideos: [],
    currentVideoData: null,
    theme: 'dark',
    view: 'discover',     // 'discover' | 'saved'
    sidebarOpen: false,
  };

  // ======= DOM =======
  const $ = id => document.getElementById(id);
  const $$ = sel => document.querySelectorAll(sel);

  // ======= INIT =======
  function init() {
    try {
      state.savedVideos = JSON.parse(localStorage.getItem('kidsflix_saved') || '[]');
      state.theme = localStorage.getItem('kidsflix_theme') || 'dark';
    } catch (e) {}
    applyTheme();
    bindEvents();
    renderGrid();
    renderFeatured();
    renderSavedGrid();
    updateSidebarStats();
  }

  // ======= THEME =======
  function applyTheme() {
    document.body.classList.toggle('light', state.theme === 'light');
  }

  // ======= GET VIDEOS =======
  function getVideos() {
    const pool = state.contentType === 'shorts' ? CONFIG.DEMO_SHORTS : CONFIG.DEMO_VIDEOS;
    const catData = pool[state.category] || {};
    let vids = [];
    if (state.language === 'all') {
      Object.values(catData).forEach(arr => vids = vids.concat(arr));
    } else {
      vids = catData[state.language] || [];
    }
    if (state.contentType === 'shorts' && state.duration !== 'all') {
      const f = CONFIG.DURATION_FILTERS[state.duration];
      vids = vids.filter(v => v.durationSec >= f.min && v.durationSec <= f.max);
    }
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      vids = vids.filter(v => v.title.toLowerCase().includes(q) || v.channel.toLowerCase().includes(q));
    }
    return vids;
  }

  // ======= RENDER MAIN GRID =======
  function renderGrid() {
    const grid = $('videoGrid');
    const spinner = $('loadingSpinner');
    const noRes = $('noResults');
    if (!grid) return;
    spinner.style.display = 'none';
    noRes.style.display = 'none';
    const vids = getVideos();
    if (!vids.length) {
      grid.innerHTML = '';
      noRes.style.display = 'flex';
      $('videosCount').textContent = '0 videos';
      return;
    }
    grid.style.display = 'grid';
    grid.innerHTML = vids.map(v => cardHTML(v, state.contentType === 'shorts')).join('');
    $('videosCount').textContent = `${vids.length} videos`;
    updateTitle();
    bindCardEvents(grid);
    refreshBookmarkUI();
  }

  function updateTitle() {
    const cat = { cartoon: '🎨 Cartoon', maths: '🔢 Maths' }[state.category];
    const type = state.contentType === 'shorts' ? 'Shorts' : 'Full Videos';
    $('videosTitle').textContent = `⚡ ${cat} ${type}`;
    $('sidebarCategory').textContent = state.category === 'cartoon' ? 'Cartoon' : 'Maths';
    $('sidebarType').textContent = state.contentType === 'shorts' ? 'Shorts' : 'Full Videos';
  }

  // ======= CARD HTML =======
  function cardHTML(v, isShort, savedView) {
    const thumb = `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
    const saved = state.savedVideos.find(s => s.id === v.id);
    const langKey = v.language || (state.language !== 'all' ? state.language : '');
    const chipClass = langKey === 'hindi' ? 'lang-chip-hi' : 'lang-chip-en';
    const chipLabel = langKey === 'hindi' ? '🇮🇳 Hindi' : (langKey ? '🇬🇧 English' : '');
    return `
      <div class="video-card" data-id="${v.id}" data-title="${esc(v.title)}" data-channel="${esc(v.channel)}" data-views="${v.views||''}" data-published="${v.published||''}">
        <div class="card-thumb">
          <img src="${thumb}" alt="${esc(v.title)}" loading="lazy" onerror="this.style.opacity='0'" />
          <div class="card-overlay">
            <div class="play-circle">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5,3 19,12 5,21" fill="white"/></svg>
            </div>
          </div>
          <div class="card-dur-tag">${v.duration}</div>
          ${isShort ? '<div class="card-shorts-tag">⚡ Short</div>' : ''}
        </div>
        <div class="card-body">
          <div class="card-title">${esc(v.title)}</div>
          <div class="card-channel">${esc(v.channel)}</div>
          <div class="card-stats">
            <span>👀 ${v.views||''}</span>
            <span>🕐 ${v.published||''}</span>
          </div>
        </div>
        <div class="card-footer">
          ${chipLabel ? `<span class="lang-chip ${chipClass}">${chipLabel}</span>` : '<span></span>'}
          <button class="bookmark-btn js-bm ${saved ? 'saved' : ''}" data-id="${v.id}" title="${saved ? 'Unsave' : 'Save'}">
            <svg viewBox="0 0 24 24" fill="${saved ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
            </svg>
          </button>
        </div>
      </div>`;
  }

  function esc(s) {
    return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // ======= BIND CARD EVENTS =======
  function bindCardEvents(container) {
    container.querySelectorAll('.video-card').forEach(card => {
      card.addEventListener('click', e => {
        if (e.target.closest('.js-bm')) return;
        openModal(card.dataset);
      });
    });
    container.querySelectorAll('.js-bm').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        toggleSave(btn.dataset.id, btn);
      });
    });
  }

  // ======= FEATURED SECTIONS =======
  function renderFeatured() {
    renderFeatureGrid('mathsGrid', CONFIG.MATHS_FEATURED);
    renderFeatureGrid('cartoonGrid', CONFIG.CARTOON_FEATURED);
  }

  function renderFeatureGrid(id, list) {
    const g = $(id);
    if (!g) return;
    g.innerHTML = list.map(v => {
      const thumb = `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
      const saved = state.savedVideos.find(s => s.id === v.id);
      return `
        <div class="video-card" data-id="${v.id}" data-title="${esc(v.title)}" data-channel="${esc(v.channel)}" data-views="${v.views}" data-published="${v.published}">
          <div class="card-thumb">
            <img src="${thumb}" alt="${esc(v.title)}" loading="lazy" onerror="this.style.opacity='0'" />
            <div class="card-overlay">
              <div class="play-circle">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5,3 19,12 5,21" fill="white"/></svg>
              </div>
            </div>
            <div class="card-dur-tag">${v.duration}</div>
            <div class="card-shorts-tag">⚡ Short</div>
          </div>
          <div class="card-body">
            <div class="card-title">${esc(v.title)}</div>
            <div class="card-channel">${esc(v.channel)}</div>
          </div>
          <div class="card-footer">
            <span class="lang-chip ${v.lang==='hindi'?'lang-chip-hi':'lang-chip-en'}">${v.lang==='hindi'?'🇮🇳 Hindi':'🇬🇧 English'}</span>
            <button class="bookmark-btn js-bm ${saved ? 'saved' : ''}" data-id="${v.id}">
              <svg viewBox="0 0 24 24" fill="${saved ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
              </svg>
            </button>
          </div>
        </div>`;
    }).join('');
    bindCardEvents(g);
  }

  // ======= SAVED GRID =======
  function renderSavedGrid() {
    const grid = $('savedGrid');
    const empty = $('savedEmpty');
    if (!state.savedVideos.length) {
      grid.innerHTML = '';
      empty.style.display = 'flex';
      return;
    }
    empty.style.display = 'none';
    grid.innerHTML = state.savedVideos.map(v => {
      const thumb = v.thumb || `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
      return `
        <div class="video-card" data-id="${v.id}" data-title="${esc(v.title)}" data-channel="${esc(v.channel)}" data-views="${v.views}" data-published="${v.published}">
          <div class="card-thumb">
            <img src="${thumb}" alt="${esc(v.title)}" loading="lazy" onerror="this.style.opacity='0'" />
            <div class="card-overlay">
              <div class="play-circle">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5,3 19,12 5,21" fill="white"/></svg>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="card-title">${esc(v.title)}</div>
            <div class="card-channel">${esc(v.channel)}</div>
          </div>
          <div class="card-footer">
            <span></span>
            <button class="bookmark-btn js-bm saved" data-id="${v.id}">
              <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
              </svg>
            </button>
          </div>
        </div>`;
    }).join('');
    bindCardEvents(grid);
  }

  // ======= MODAL =======
  function openModal(data) {
    state.currentVideoData = data;
    $('modalPlayer').src = `https://www.youtube.com/embed/${data.id}?autoplay=1`;
    $('modalTitle').textContent = data.title || '';
    $('modalChannel').textContent = data.channel || '';
    $('modalViews').textContent = data.views ? `👀 ${data.views}` : '';
    $('modalDate').textContent = data.published ? `🕐 ${data.published}` : '';
    $('watchOnYT').href = `https://www.youtube.com/watch?v=${data.id}`;
    syncModalSaveBtn(data.id);
    renderComments();
    $('videoModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeModal() {
    $('videoModal').classList.remove('open');
    $('modalPlayer').src = '';
    state.currentVideoData = null;
    document.body.style.overflow = '';
  }
  function syncModalSaveBtn(id) {
    const saved = state.savedVideos.find(s => s.id === id);
    const btn = $('modalSaveBtn');
    const txt = $('modalSaveText');
    if (saved) { btn.classList.add('saved'); txt.textContent = 'Saved!'; }
    else { btn.classList.remove('saved'); txt.textContent = 'Save'; }
  }
  function renderComments() {
    const pool = CONFIG.VIDEO_COMMENTS;
    const set = pool[Math.floor(Math.random() * pool.length)];
    $('commentsList').innerHTML = set.map(c => `
      <div class="comment-item">
        <div class="comment-avatar">${c.author.charAt(0)}</div>
        <div>
          <div class="comment-author">${esc(c.author)}</div>
          <div class="comment-text">${esc(c.text)}</div>
          <div class="comment-likes">👍 ${c.likes}</div>
        </div>
      </div>`).join('');
  }

  // ======= SAVE TOGGLE =======
  function toggleSave(id, btn) {
    const idx = state.savedVideos.findIndex(s => s.id === id);
    if (idx >= 0) {
      state.savedVideos.splice(idx, 1);
    } else {
      const card = document.querySelector(`.video-card[data-id="${id}"]`);
      state.savedVideos.push({
        id,
        title: card?.dataset.title || id,
        channel: card?.dataset.channel || '',
        views: card?.dataset.views || '',
        published: card?.dataset.published || '',
        thumb: `https://i.ytimg.com/vi/${id}/hqdefault.jpg`,
      });
    }
    localStorage.setItem('kidsflix_saved', JSON.stringify(state.savedVideos));
    refreshBookmarkUI();
    renderSavedGrid();
    updateSidebarStats();
    // Update sidebar saved count
    $('sidebarSavedCount').textContent = state.savedVideos.length;
    if (state.currentVideoData && state.currentVideoData.id === id) syncModalSaveBtn(id);
  }

  function refreshBookmarkUI() {
    $$('.js-bm').forEach(btn => {
      const saved = state.savedVideos.find(s => s.id === btn.dataset.id);
      btn.classList.toggle('saved', !!saved);
      btn.querySelector('svg').setAttribute('fill', saved ? 'currentColor' : 'none');
    });
  }

  function updateSidebarStats() {
    $('sidebarSavedCount').textContent = state.savedVideos.length;
    $('sidebarCategory').textContent = state.category === 'cartoon' ? 'Cartoon' : 'Maths';
    $('sidebarType').textContent = state.contentType === 'shorts' ? 'Shorts' : 'Full Videos';
  }

  // ======= BIND ALL EVENTS =======
  function bindEvents() {
    // Theme
    $('themeToggle').addEventListener('click', () => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme();
      localStorage.setItem('kidsflix_theme', state.theme);
    });

    // Sidebar toggle (mobile)
    $('sidebarToggle').addEventListener('click', () => {
      $('sidebar').classList.toggle('open');
    });

    // Nav items (sidebar)
    $$('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => {
        $$('.nav-item').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const view = btn.dataset.view;
        state.view = view;
        $('viewDiscover').style.display = view === 'discover' ? 'block' : 'none';
        $('viewSaved').style.display = view === 'saved' ? 'block' : 'none';
        // Close sidebar on mobile
        $('sidebar').classList.remove('open');
      });
    });

    // Category cards
    $$('.cat-card').forEach(card => {
      card.addEventListener('click', () => {
        $$('.cat-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        state.category = card.dataset.category;
        renderGrid();
        updateSidebarStats();
      });
    });

    // Content type pills
    $$('#contentTypePills .pill').forEach(pill => {
      pill.addEventListener('click', () => {
        $$('#contentTypePills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.contentType = pill.dataset.type;
        $('durationGroup').style.display = pill.dataset.type === 'shorts' ? 'block' : 'none';
        renderGrid();
        updateSidebarStats();
      });
    });

    // Default: shorts active
    const defaultType = document.querySelector('#contentTypePills .pill[data-type="shorts"]');
    if (defaultType) defaultType.classList.add('active');
    document.querySelector('#contentTypePills .pill[data-type="big"]')?.classList.remove('active');
    $('durationGroup').style.display = 'block';

    // Language pills
    $$('#langPills .pill').forEach(pill => {
      pill.addEventListener('click', () => {
        $$('#langPills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.language = pill.dataset.lang;
        renderGrid();
      });
    });

    // Duration pills
    $$('#durationPills .pill').forEach(pill => {
      pill.addEventListener('click', () => {
        $$('#durationPills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.duration = pill.dataset.dur;
        renderGrid();
      });
    });

    // Search
    let t;
    $('searchInput').addEventListener('input', e => {
      clearTimeout(t);
      t = setTimeout(() => { state.searchQuery = e.target.value.trim(); renderGrid(); }, 350);
    });

    // Modal close
    $('modalClose').addEventListener('click', closeModal);
    $('videoModal').addEventListener('click', e => { if (e.target === $('videoModal')) closeModal(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

    // Modal save
    $('modalSaveBtn').addEventListener('click', () => {
      if (state.currentVideoData) toggleSave(state.currentVideoData.id, null);
    });

    // Clear all saved
    $('clearAllBtn').addEventListener('click', () => {
      state.savedVideos = [];
      localStorage.removeItem('kidsflix_saved');
      renderSavedGrid();
      refreshBookmarkUI();
      updateSidebarStats();
    });

    // Sticky top bar
    window.addEventListener('scroll', () => {}, { passive: true });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
