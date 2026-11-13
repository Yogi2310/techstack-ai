// ============================================
// KidsFlix App — Full Featured with Download & Upload
// ============================================
import { generateBatch, renderPreview } from './kidsgenerator.js';

(function () {
  'use strict';

  // ======= STATE =======
  const state = {
    category:    'cartoon',
    contentType: 'shorts',
    language:    'all',
    duration:    'all',
    ageGroup:    'all',
    searchQuery: '',
    savedVideos: [],
    currentVideoData: null,
    theme: 'dark',
    view: 'discover',   // 'discover' | 'saved' | 'downloads' | 'generate'
    downloads: [],
    // Generate state
    genCategory: 'cartoon',
    genCount: 3,
    genDuration: 15,
    genResults: [],
    isGenerating: false,
  };

  const $ = id  => document.getElementById(id);
  const $$ = sel => document.querySelectorAll(sel);

  // ======= INIT =======
  function init() {
    try {
      state.savedVideos = JSON.parse(localStorage.getItem('kidsflix_saved') || '[]');
      state.theme = localStorage.getItem('kidsflix_theme') || 'dark';
    } catch (e) {}
    applyTheme();
    bindEvents();
    renderSavedGrid();
    updateSidebarStats();
    updateMyShorts();
    // Default to Generate view — this is an auto-generate app!
    switchView('generate');

    const params = new URLSearchParams(window.location.search);
    const uploadFile = params.get('upload');
    if (uploadFile) {
      history.replaceState({}, '', '/');
      switchView('downloads');
      showToast('✅ Authenticated! Ready to upload: ' + uploadFile, 'success');
    }
  }

  // ======= THEME =======
  function applyTheme() {
    document.body.classList.toggle('light', state.theme === 'light');
  }

  // ======= VIEW SWITCH =======
  function switchView(view) {
    state.view = view;
    $('viewDiscover').style.display  = view === 'discover'  ? 'block' : 'none';
    $('viewSaved').style.display     = view === 'saved'     ? 'block' : 'none';
    $('viewDownloads').style.display = view === 'downloads' ? 'block' : 'none';
    $('viewGenerate').style.display  = view === 'generate'  ? 'block' : 'none';
    $$('.nav-item').forEach(b => b.classList.remove('active'));
    const nav = document.querySelector(`.nav-item[data-view="${view}"]`);
    if (nav) nav.classList.add('active');
    if (view === 'downloads') loadDownloads();
  }

  // ======= GET VIDEOS =======
  function getVideos() {
    const pool = CONFIG.DEMO_SHORTS;
    const catData = pool[state.category] || {};
    let vids = [];
    if (state.language === 'all') {
      Object.values(catData).forEach(arr => vids = vids.concat(arr));
    } else {
      vids = catData[state.language] || [];
    }
    if (state.duration !== 'all') {
      const f = CONFIG.DURATION_FILTERS[state.duration];
      vids = vids.filter(v => v.durationSec >= f.min && v.durationSec <= f.max);
    }
    if (state.ageGroup !== 'all') {
      vids = vids.filter(v => v.age === state.ageGroup);
    }
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      vids = vids.filter(v => v.title.toLowerCase().includes(q) || v.channel.toLowerCase().includes(q));
    }
    return vids;
  }

  // ======= RENDER MAIN GRID =======
  function renderGrid() {
    const grid    = $('videoGrid');
    const spinner = $('loadingSpinner');
    const noRes   = $('noResults');
    if (!grid) return;
    spinner.style.display = 'none';
    noRes.style.display   = 'none';
    const vids = getVideos();
    $('videosCount').textContent = vids.length + ' videos';
    if (!vids.length) {
      grid.innerHTML = '';
      noRes.style.display = 'flex';
      return;
    }
    // Sort by views desc for trending detection
    const sorted = [...vids].sort((a, b) => parseMillion(b.views) - parseMillion(a.views));
    const topIds = new Set(sorted.slice(0, 3).map(v => v.id));
    grid.innerHTML = vids.map(v => cardHTML(v, true, false, topIds.has(v.id))).join('');
    updateTitle();
    bindCardEvents(grid);
    refreshBookmarkUI();
  }

  function parseMillion(str) {
    if (!str) return 0;
    return parseFloat(str.replace(/[^0-9.]/g, '')) || 0;
  }

  function updateTitle() {
    const labels = { cartoon: '🎨 Cartoon', maths: '🔢 Maths', stories: '📚 Stories', science: '🔬 Science' };
    $('videosTitle').textContent = `⚡ ${labels[state.category] || state.category} Shorts`;
    $('sidebarCategory').textContent = { cartoon:'Cartoon', maths:'Maths', stories:'Stories', science:'Science' }[state.category] || state.category;
  }

  // ======= CARD HTML =======
  function cardHTML(v, isShort, savedView, isTrending) {
    const thumb   = `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
    const saved   = state.savedVideos.find(s => s.id === v.id);
    const lang    = v.language || '';
    const chipClass = lang === 'hindi' ? 'lang-chip-hi' : (lang ? 'lang-chip-en' : '');
    const chipLabel = lang === 'hindi' ? '🇮🇳 Hindi' : (lang === 'english' ? '🇬🇧 English' : '');
    const ageLabel  = { toddler:'🐣 Toddler', kids:'⭐ Kids', tweens:'🚀 Tweens' }[v.age] || '';
    return `
      <div class="video-card" data-id="${v.id}" data-title="${esc(v.title)}" data-channel="${esc(v.channel)}" data-views="${v.views||''}" data-published="${v.published||''}">
        <div class="card-thumb">
          <img src="${thumb}" alt="${esc(v.title)}" loading="lazy" onerror="this.style.opacity='0'" />
          <div class="card-overlay">
            <div class="play-circle">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5,3 19,12 5,21" fill="white"/></svg>
            </div>
          </div>
          <div class="card-dur-tag">${v.duration || ''}</div>
          ${isShort ? '<div class="card-shorts-tag">⚡ Short</div>' : ''}
          ${isTrending ? '<div class="card-trending-tag">🔥 Trending</div>' : ''}
        </div>
        <div class="card-body">
          <div class="card-title">${esc(v.title)}</div>
          <div class="card-channel">${esc(v.channel)}</div>
          <div class="card-stats">
            <span>👀 ${v.views||''}</span>
            <span>🕐 ${v.published||''}</span>
            ${ageLabel ? `<span class="age-chip">${ageLabel}</span>` : ''}
          </div>
        </div>
        <div class="card-footer">
          ${chipLabel ? `<span class="lang-chip ${chipClass}">${chipLabel}</span>` : '<span></span>'}
          <div class="card-actions">
            <button class="action-btn download-btn js-dl" data-id="${v.id}" data-title="${esc(v.title)}" title="Download">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            </button>
            <button class="bookmark-btn js-bm ${saved ? 'saved' : ''}" data-id="${v.id}" title="${saved ? 'Unsave' : 'Save'}">
              <svg viewBox="0 0 24 24" fill="${saved ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
              </svg>
            </button>
          </div>
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
        if (e.target.closest('.js-bm') || e.target.closest('.js-dl')) return;
        openModal(card.dataset);
      });
    });
    container.querySelectorAll('.js-bm').forEach(btn => {
      btn.addEventListener('click', e => { e.stopPropagation(); toggleSave(btn.dataset.id, btn); });
    });
    container.querySelectorAll('.js-dl').forEach(btn => {
      btn.addEventListener('click', e => { e.stopPropagation(); downloadVideo(btn.dataset.id, btn.dataset.title); });
    });
  }

  // ======= FEATURED SECTIONS =======
  function renderFeatured() {
    renderFeatureGrid('mathsGrid',   CONFIG.MATHS_FEATURED);
    renderFeatureGrid('cartoonGrid', CONFIG.CARTOON_FEATURED);
    renderFeatureGrid('storiesGrid', CONFIG.STORIES_FEATURED);
    renderFeatureGrid('scienceGrid', CONFIG.SCIENCE_FEATURED);
  }

  function renderFeatureGrid(id, list) {
    const g = $(id); if (!g) return;
    g.innerHTML = list.map(v => {
      const thumb = `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
      const saved = state.savedVideos.find(s => s.id === v.id);
      return `
        <div class="video-card" data-id="${v.id}" data-title="${esc(v.title)}" data-channel="${esc(v.channel)}" data-views="${v.views}" data-published="${v.published}">
          <div class="card-thumb">
            <img src="${thumb}" alt="${esc(v.title)}" loading="lazy" onerror="this.style.opacity='0'" />
            <div class="card-overlay"><div class="play-circle"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5,3 19,12 5,21" fill="white"/></svg></div></div>
            <div class="card-dur-tag">${v.duration}</div>
            <div class="card-shorts-tag">⚡ Short</div>
          </div>
          <div class="card-body">
            <div class="card-title">${esc(v.title)}</div>
            <div class="card-channel">${esc(v.channel)}</div>
          </div>
          <div class="card-footer">
            <span class="lang-chip ${v.lang==='hindi'?'lang-chip-hi':'lang-chip-en'}">${v.lang==='hindi'?'🇮🇳 Hindi':'🇬🇧 English'}</span>
            <div class="card-actions">
              <button class="action-btn download-btn js-dl" data-id="${v.id}" data-title="${esc(v.title)}" title="Download">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              </button>
              <button class="bookmark-btn js-bm ${saved ? 'saved' : ''}" data-id="${v.id}">
                <svg viewBox="0 0 24 24" fill="${saved ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>`;
    }).join('');
    bindCardEvents(g);
  }

  // ======= SAVED GRID =======
  function renderSavedGrid() {
    const grid  = $('savedGrid');
    const empty = $('savedEmpty');
    if (!state.savedVideos.length) {
      grid.innerHTML = ''; empty.style.display = 'flex'; return;
    }
    empty.style.display = 'none';
    grid.innerHTML = state.savedVideos.map(v => {
      const thumb = v.thumb || `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
      return `
        <div class="video-card" data-id="${v.id}" data-title="${esc(v.title)}" data-channel="${esc(v.channel)}" data-views="${v.views}" data-published="${v.published}">
          <div class="card-thumb">
            <img src="${thumb}" alt="${esc(v.title)}" loading="lazy" onerror="this.style.opacity='0'" />
            <div class="card-overlay"><div class="play-circle"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5,3 19,12 5,21" fill="white"/></svg></div></div>
          </div>
          <div class="card-body">
            <div class="card-title">${esc(v.title)}</div>
            <div class="card-channel">${esc(v.channel)}</div>
          </div>
          <div class="card-footer">
            <div class="card-actions">
              <button class="action-btn download-btn js-dl" data-id="${v.id}" data-title="${esc(v.title)}" title="Download">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              </button>
              <button class="bookmark-btn js-bm saved" data-id="${v.id}">
                <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>`;
    }).join('');
    bindCardEvents(grid);
  }

  // ======= DOWNLOADS VIEW =======
  async function loadDownloads() {
    const list  = $('downloadsList');
    const empty = $('downloadsEmpty');
    if (!list) return;
    list.innerHTML = '<div class="dl-loading">⏳ Loading downloads…</div>';
    try {
      const res  = await fetch('/api/downloads');
      const data = await res.json();
      state.downloads = data.downloads || [];
    } catch (e) {
      state.downloads = [];
    }
    renderDownloadsList();
  }

  function renderDownloadsList() {
    const list  = $('downloadsList');
    const empty = $('downloadsEmpty');
    if (!state.downloads.length) {
      list.innerHTML = '';
      empty.style.display = 'flex';
      return;
    }
    empty.style.display = 'none';
    list.innerHTML = state.downloads.map(f => `
      <div class="dl-item" id="dl-${CSS.escape(f.filename)}">
        <div class="dl-thumb">
          ${f.videoId ? `<img src="https://i.ytimg.com/vi/${f.videoId}/hqdefault.jpg" alt="" loading="lazy" onerror="this.style.opacity='0'"/>` : '<div class="dl-thumb-placeholder">📹</div>'}
        </div>
        <div class="dl-info">
          <div class="dl-name">${esc(f.filename)}</div>
          <div class="dl-meta">📦 ${f.size_mb} MB ${f.uploaded ? `• <a href="${f.ytUrl}" target="_blank" rel="noopener" class="dl-yt-link">▶ View on YouTube</a>` : ''}</div>
        </div>
        <div class="dl-btns">
          ${!f.uploaded ? `
            <button class="btn-upload js-upload" data-filename="${esc(f.filename)}" data-title="${esc(f.filename.replace(/\[.*\]/,'').trim())}">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17,8 12,3 7,8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              Upload to YouTube
            </button>` : `<span class="dl-uploaded-badge">✅ Uploaded</span>`}
          <a class="btn-dl-file" href="/api/file/${encodeURIComponent(f.filename)}" download title="Save to Computer">💾</a>
          <button class="btn-delete js-del-dl" data-filename="${esc(f.filename)}">🗑️</button>
        </div>
      </div>`).join('');

    $$('.js-upload').forEach(btn => btn.addEventListener('click', () => uploadToYouTube(btn.dataset.filename, btn.dataset.title)));
    $$('.js-del-dl').forEach(btn => btn.addEventListener('click', () => deleteDownload(btn.dataset.filename)));
  }

  // ======= DOWNLOAD =======
  async function downloadVideo(videoId, title) {
    showToast(`⬇️ Starting download: ${title.slice(0,40)}…`, 'info');
    try {
      const res  = await fetch('/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ videoId, title })
      });
      const data = await res.json();
      if (data.status === 'exists') {
        showToast('✅ Already downloaded!', 'success');
        return;
      }
      pollDownloadProgress(videoId, title);
    } catch (e) {
      showToast('❌ Download failed. Is the Flask server running?', 'error');
    }
  }

  function pollDownloadProgress(videoId, title) {
    const interval = setInterval(async () => {
      try {
        const res  = await fetch(`/api/download/progress/${videoId}`);
        const prog = await res.json();
        if (prog.status === 'done') {
          clearInterval(interval);
          showToast(`✅ Downloaded! Go to Downloads tab.`, 'success');
          $('sidebarDownloadCount') && ($('sidebarDownloadCount').textContent = parseInt($('sidebarDownloadCount').textContent||'0') + 1);
        } else if (prog.status === 'error') {
          clearInterval(interval);
          showToast(`❌ Download error: ${prog.error || 'Unknown'}`, 'error');
        } else if (prog.status === 'downloading') {
          showToast(`⬇️ Downloading… ${Math.round(prog.percent)}%`, 'info', true);
        }
      } catch (e) { clearInterval(interval); }
    }, 1500);
  }

  // ======= UPLOAD =======
  async function uploadToYouTube(filename, title) {
    showToast('🚀 Starting upload to YouTube…', 'info');
    try {
      const res  = await fetch('/api/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename, title, tags: ['kids', 'cartoon', 'shorts', 'educational', 'kidsflix'] })
      });
      const data = await res.json();
      if (data.auth_required) {
        showToast('🔐 Redirecting to Google for YouTube permission…', 'info');
        setTimeout(() => { window.location.href = data.auth_url; }, 1500);
        return;
      }
      if (data.status === 'uploading') {
        pollUploadProgress(filename);
      }
    } catch (e) {
      showToast('❌ Upload failed. Is the Flask server running?', 'error');
    }
  }

  function pollUploadProgress(filename) {
    const interval = setInterval(async () => {
      try {
        const res  = await fetch(`/api/upload/progress/${encodeURIComponent(filename)}`);
        const prog = await res.json();
        if (prog.status === 'done') {
          clearInterval(interval);
          showToast(`🎉 Uploaded! <a href="${prog.video_url}" target="_blank">View on YouTube ↗</a>`, 'success');
          loadDownloads();
        } else if (prog.status === 'error') {
          clearInterval(interval);
          showToast(`❌ Upload error: ${prog.error || 'Unknown'}`, 'error');
        } else {
          showToast('🚀 Uploading to YouTube…', 'info', true);
        }
      } catch (e) { clearInterval(interval); }
    }, 2000);
  }

  async function deleteDownload(filename) {
    if (!confirm(`Delete "${filename}"?`)) return;
    await fetch(`/api/download/${encodeURIComponent(filename)}`, { method: 'DELETE' });
    showToast('🗑️ Deleted.', 'info');
    loadDownloads();
  }

  // ======= TOAST =======
  let _toastEl = null; let _toastTimer = null;
  function showToast(html, type = 'info', replace = false) {
    if (!_toastEl) {
      _toastEl = document.createElement('div');
      _toastEl.className = 'kf-toast';
      document.body.appendChild(_toastEl);
    }
    if (_toastTimer && !replace) clearTimeout(_toastTimer);
    _toastEl.innerHTML = html;
    _toastEl.className = `kf-toast kf-toast-${type} show`;
    _toastTimer = setTimeout(() => _toastEl.classList.remove('show'), 3500);
  }

  // ======= MODAL =======
  function openModal(data) {
    state.currentVideoData = data;
    $('modalPlayer').src = `https://www.youtube.com/embed/${data.id}?autoplay=1`;
    $('modalTitle').textContent   = data.title || '';
    $('modalChannel').textContent = data.channel || '';
    $('modalViews').textContent   = data.views ? `👀 ${data.views}` : '';
    $('modalDate').textContent    = data.published ? `🕐 ${data.published}` : '';
    $('watchOnYT').href           = `https://www.youtube.com/watch?v=${data.id}`;
    $('modalDownloadBtn').onclick = () => downloadVideo(data.id, data.title);
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
    $('modalSaveBtn').classList.toggle('saved', !!saved);
    $('modalSaveText').textContent = saved ? 'Saved!' : 'Save';
  }
  function renderComments() {
    const pool = CONFIG.VIDEO_COMMENTS;
    const set  = pool[Math.floor(Math.random() * pool.length)];
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
      state.savedVideos.push({ id, title: card?.dataset.title || id, channel: card?.dataset.channel || '', views: card?.dataset.views || '', published: card?.dataset.published || '', thumb: `https://i.ytimg.com/vi/${id}/hqdefault.jpg` });
    }
    localStorage.setItem('kidsflix_saved', JSON.stringify(state.savedVideos));
    refreshBookmarkUI();
    renderSavedGrid();
    updateSidebarStats();
    if (state.currentVideoData?.id === id) syncModalSaveBtn(id);
  }

  function refreshBookmarkUI() {
    $$('.js-bm').forEach(btn => {
      const saved = state.savedVideos.find(s => s.id === btn.dataset.id);
      btn.classList.toggle('saved', !!saved);
      btn.querySelector('svg').setAttribute('fill', saved ? 'currentColor' : 'none');
    });
  }

  function updateSidebarStats() {
    $('sidebarSavedCount').textContent    = state.savedVideos.length;
    $('sidebarCategory').textContent      = { cartoon:'Cartoon', maths:'Maths', stories:'Stories', science:'Science' }[state.category] || state.category;
    $('sidebarType').textContent          = 'Shorts';
  }

  // ======= EVENTS =======
  function bindEvents() {
    $('themeToggle').addEventListener('click', () => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme();
      localStorage.setItem('kidsflix_theme', state.theme);
    });

    $('sidebarToggle').addEventListener('click', () => $('sidebar').classList.toggle('open'));

    $$('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => {
        switchView(btn.dataset.view);
        $('sidebar').classList.remove('open');
      });
    });

    $$('.cat-card').forEach(card => {
      card.addEventListener('click', () => {
        $$('.cat-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        state.category = card.dataset.category;
        renderGrid();
        updateSidebarStats();
      });
    });

    $$('#contentTypePills .pill').forEach(pill => {
      pill.addEventListener('click', () => {
        $$('#contentTypePills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.contentType = pill.dataset.type;
        renderGrid();
        updateSidebarStats();
      });
    });

    $$('#langPills .pill').forEach(pill => {
      pill.addEventListener('click', () => {
        $$('#langPills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.language = pill.dataset.lang;
        renderGrid();
      });
    });

    $$('#durationPills .pill').forEach(pill => {
      pill.addEventListener('click', () => {
        $$('#durationPills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.duration = pill.dataset.dur;
        renderGrid();
      });
    });

    $$('#agePills .pill').forEach(pill => {
      pill.addEventListener('click', () => {
        $$('#agePills .pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.ageGroup = pill.dataset.age;
        renderGrid();
      });
    });

    let t;
    $('searchInput').addEventListener('input', e => {
      clearTimeout(t);
      t = setTimeout(() => { state.searchQuery = e.target.value.trim(); renderGrid(); }, 350);
    });

    $('modalClose').addEventListener('click', closeModal);
    $('videoModal').addEventListener('click', e => { if (e.target === $('videoModal')) closeModal(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

    $('modalSaveBtn').addEventListener('click', () => {
      if (state.currentVideoData) toggleSave(state.currentVideoData.id, null);
    });

    $('clearAllBtn').addEventListener('click', () => {
      state.savedVideos = [];
      localStorage.removeItem('kidsflix_saved');
      renderSavedGrid(); refreshBookmarkUI(); updateSidebarStats();
    });

    // ── Generate view controls ────────────────────────────────
    $$('.gen-cat-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        $$('.gen-cat-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.genCategory = btn.dataset.gencat;
      });
    });
    $$('.gen-count-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        $$('.gen-count-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.genCount = parseInt(btn.dataset.gencount);
      });
    });
    $$('.gen-dur-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        $$('.gen-dur-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.genDuration = parseInt(btn.dataset.gendur);
      });
    });
    $('btnGenerate').addEventListener('click', startGenerate);
    $('btnDownloadAll').addEventListener('click', downloadAll);

    // Preview modal close
    $('previewClose').addEventListener('click', closePreviewModal);
    $('previewModal').addEventListener('click', e => { if (e.target === $('previewModal')) closePreviewModal(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closePreviewModal(); });

    // CTA buttons on My Shorts view → go to Generate
    const heroBtn  = $('btnHeroGenerate');
    const emptyBtn = $('btnEmptyGenerate');
    if (heroBtn)  heroBtn.addEventListener('click',  () => switchView('generate'));
    if (emptyBtn) emptyBtn.addEventListener('click', () => switchView('generate'));
  }

  // ======= GENERATE =======
  async function startGenerate() {
    if (state.isGenerating) return;
    state.isGenerating = true;
    const btn = $('btnGenerate');
    btn.disabled = true;
    btn.style.opacity = '0.6';

    const progress = $('genProgress');
    const queue    = $('genQueue');
    progress.classList.remove('hidden');
    queue.classList.add('hidden');
    $('genQueueGrid').innerHTML = '';
    state.genResults = [];

    const renderCanvas = $('genRenderCanvas');
    const liveCanvas   = $('genLiveCanvas');

    await generateBatch(
      renderCanvas,
      state.genCategory,
      state.genCount,
      state.genDuration,
      ({ phase, current, total, text }) => {
        if (phase === 'music') {
          $('genProgressLabel').textContent = '🎵 Generating background music…';
          $('genProgressCount').textContent = `0/${total}`;
          $('genProgressFill').style.width = '5%';
          $('genLiveText').textContent = 'Composing music for ' + state.genCategory + '…';
          $('genLiveBadge').textContent = state.genCategory.toUpperCase();
        } else if (phase === 'video') {
          $('genProgressLabel').textContent = `🎥 Rendering video ${current} of ${total}…`;
          $('genProgressCount').textContent = `${current}/${total}`;
          $('genProgressFill').style.width = `${(current / total) * 90 + 5}%`;
          $('genLiveText').textContent = text ? text.replace(/\n/g, ' ') : 'Rendering…';
        } else if (phase === 'done') {
          $('genProgressFill').style.width = '100%';
        }
      }
    ).then(results => {
      state.genResults = results;
      // Accumulate all generated results for My Shorts gallery
      if (!state.allGenerated) state.allGenerated = [];
      state.allGenerated = state.allGenerated.concat(results);
      state.isGenerating = false;
      btn.disabled = false;
      btn.style.opacity = '1';
      progress.classList.add('hidden');
      renderGenQueue(results);
      queue.classList.remove('hidden');
      updateMyShorts();
    }).catch(err => {
      console.error('Generation failed:', err);
      state.isGenerating = false;
      btn.disabled = false;
      btn.style.opacity = '1';
      progress.classList.add('hidden');
      showToast('❌ Generation failed: ' + err.message, 'error');
    });
  }

  function renderGenQueue(results) {
    const grid = $('genQueueGrid');
    grid.innerHTML = results.map((r, i) => {
      const canvasId = `genPreview-${i}`;
      return `
        <div class="gen-queue-card">
          <div class="gen-queue-thumb" style="cursor:pointer;" data-preview="${i}">
            <canvas id="${canvasId}" width="1080" height="1920"></canvas>
            <div class="gen-play-overlay" data-preview="${i}">
              <div class="gen-play-circle">▶️</div>
            </div>
          </div>
          <div class="gen-queue-info">
            <div class="gen-queue-cat">${r.category.toUpperCase()}</div>
            <div class="gen-queue-text">${r.item.emoji} ${r.item.text.replace(/\n/g, ' ')}</div>
            <div class="gen-card-btns">
              <button class="gen-prev-btn" data-index="${i}">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><polygon points="5,3 19,12 5,21"/></svg>
                Preview
              </button>
              <button class="gen-dl-btn" data-index="${i}">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Download
              </button>
            </div>
          </div>
        </div>`;
    }).join('');

    results.forEach((r, i) => {
      const c = $(`genPreview-${i}`);
      if (c) renderPreview(c, r.item, r.gradient);
    });

    // Preview buttons
    grid.querySelectorAll('.gen-prev-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const i = parseInt(btn.dataset.index);
        openPreviewModal(state.genResults[i]);
      });
    });
    // Thumb click also opens preview
    grid.querySelectorAll('[data-preview]').forEach(el => {
      el.addEventListener('click', () => {
        const i = parseInt(el.dataset.preview);
        openPreviewModal(state.genResults[i]);
      });
    });

    // Download buttons
    grid.querySelectorAll('.gen-dl-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const i   = parseInt(btn.dataset.index);
        const res = state.genResults[i];
        if (!res) return;
        dlBlob(res.blob, `kidsflix-${res.category}-${i+1}-${Date.now()}.webm`);
        btn.textContent = '✅ Saved!';
        setTimeout(() => { btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download`; }, 2500);
      });
    });
  }

  function downloadAll() {
    if (!state.genResults.length) return;
    state.genResults.forEach((r, i) => {
      setTimeout(() => dlBlob(r.blob, `kidsflix-${r.category}-${i+1}-${Date.now()}.webm`), i * 800);
    });
    showToast(`⬇️ Downloading ${state.genResults.length} videos…`, 'success');
  }

  function dlBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url); }, 2000);
  }

  // ======= PREVIEW MODAL =======
  let _previewBlobUrl = null;
  function openPreviewModal(res) {
    if (!res || !res.blob) { showToast('⚠️ No video — please re-generate.', 'error'); return; }
    // Revoke old URL
    if (_previewBlobUrl) { URL.revokeObjectURL(_previewBlobUrl); _previewBlobUrl = null; }
    _previewBlobUrl = URL.createObjectURL(res.blob);
    const video = $('previewVideo');
    video.src = _previewBlobUrl;
    video.load();
    video.play().catch(() => {});
    $('previewCat').textContent   = res.category.toUpperCase();
    $('previewTitle').textContent = res.item.emoji + ' ' + res.item.text.replace(/\n/g, ' ');
    $('previewDownloadBtn').onclick = () => {
      dlBlob(res.blob, `kidsflix-${res.category}-${Date.now()}.webm`);
      showToast('✅ Downloading!', 'success');
    };
    $('previewModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closePreviewModal() {
    $('previewModal').classList.remove('open');
    const video = $('previewVideo');
    video.pause(); video.src = '';
    if (_previewBlobUrl) { URL.revokeObjectURL(_previewBlobUrl); _previewBlobUrl = null; }
    document.body.style.overflow = '';
  }

  // ======= MY SHORTS GALLERY =======
  function updateMyShorts() {
    const grid  = $('myShortGrid');
    const empty = $('myShortEmpty');
    const cnt   = $('myShortCount');
    if (!grid) return;
    const all = state.allGenerated || [];
    if (cnt) cnt.textContent = all.length + ' video' + (all.length !== 1 ? 's' : '');
    if (!all.length) {
      grid.innerHTML = '';
      if (empty) empty.style.display = 'flex';
      return;
    }
    if (empty) empty.style.display = 'none';
    const reversed = [...all].reverse();
    grid.innerHTML = reversed.map((r, i) => {
      const ci = `myShort-${r.id || i}`;
      return `
        <div class="gen-queue-card">
          <div class="gen-queue-thumb"><canvas id="${ci}" width="1080" height="1920"></canvas></div>
          <div class="gen-queue-info">
            <div class="gen-queue-cat">${r.category.toUpperCase()}</div>
            <div class="gen-queue-text">${r.item.emoji} ${r.item.text.replace(/\n/g,' ')}</div>
            <button class="gen-dl-btn" data-ridx="${i}">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Download
            </button>
          </div>
        </div>`;
    }).join('');

    reversed.forEach((r, i) => {
      const c = $(`myShort-${r.id || i}`);
      if (c) renderPreview(c, r.item, r.gradient);
    });

    grid.querySelectorAll('.gen-dl-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.ridx);
        const res = reversed[idx];
        if (res && res.blob) {
          dlBlob(res.blob, `kidsflix-${res.category}-${Date.now()}.webm`);
          btn.textContent = '✅ Saved!';
          setTimeout(() => { btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download`; }, 2500);
        } else {
          showToast('⚠️ Video not available — please re-generate.', 'error');
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
