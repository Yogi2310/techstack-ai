import { getTrendingAnime as getYouTubeTrending, getShortsAnime, searchAnimeVideos } from '../api/invidious.js';
import { getAllSubreddits } from '../api/reddit.js';
import { getTrendingAnime as getAniListTrending } from '../api/anilist.js';
import { renderVideoCard, renderSkeletonCards } from './VideoCard.js';
import { formatNumber, debounce, showToast } from '../utils/helpers.js';
import { queue } from '../store.js';

let currentTab = 'all';
let allVideos = [];
let isLoading = false;

const YOUTUBE_QUERIES = ['anime amv 2026', 'anime edit 4k', 'anime trending', 'anime fight scene'];

export async function renderDashboard(container) {
  container.innerHTML = `
    <div class="page-header">
      <h1 class="page-title"><span>🔥 Trending</span> Anime</h1>
      <div class="search-bar" style="width:280px">
        <span class="search-icon">🔍</span>
        <input type="text" id="search-input" placeholder="Search anime videos…" autocomplete="off" />
      </div>
    </div>

    <div class="platform-tabs">
      <button class="tab-btn active" data-tab="all">🌐 All Sources</button>
      <button class="tab-btn" data-tab="youtube"><span class="tab-icon">▶</span>YouTube</button>
      <button class="tab-btn" data-tab="shorts"><span class="tab-icon">⚡</span>Shorts</button>
      <button class="tab-btn" data-tab="reddit"><span class="tab-icon">🤖</span>Reddit</button>
      <button class="tab-btn" data-tab="anilist"><span class="tab-icon">🌸</span>AniList</button>
    </div>

    <div class="stats-row" id="stats-row">
      <div class="stat-card"><span class="stat-icon">📺</span><div><div class="stat-value" id="stat-total">—</div><div class="stat-label">Videos Found</div></div></div>
      <div class="stat-card"><span class="stat-icon">⬇️</span><div><div class="stat-value" id="stat-queue">${queue.count()}</div><div class="stat-label">In Queue</div></div></div>
      <div class="stat-card"><span class="stat-icon">🌐</span><div><div class="stat-value" id="stat-sources">4</div><div class="stat-label">Free Feeds</div></div></div>
      <div class="stat-card"><span class="stat-icon">🕐</span><div><div class="stat-value" id="stat-updated">—</div><div class="stat-label">Last Updated</div></div></div>
    </div>

    <div class="videos-container">
      <div class="section-title" id="section-title">Loading trending anime…</div>
      <div class="video-grid" id="video-grid"></div>
    </div>
  `;

  setupTabs(container);
  setupSearch();
  await loadAllSources();
}

async function loadAllSources() {
  if (isLoading) return;
  isLoading = true;

  const grid = document.getElementById('video-grid');
  const sectionTitle = document.getElementById('section-title');

  // Show skeletons
  grid.innerHTML = '';
  renderSkeletonCards(16).forEach(el => grid.appendChild(el));
  sectionTitle.textContent = 'Fetching from all sources…';

  try {
    const [ytVideos, shortsVideos, redditVideos, anilistVideos] = await Promise.allSettled([
      getYouTubeTrending(YOUTUBE_QUERIES[Math.floor(Math.random() * YOUTUBE_QUERIES.length)]),
      getShortsAnime(),
      getAllSubreddits(),
      getAniListTrending(1, 20),
    ]);

    const yt = ytVideos.status === 'fulfilled' ? ytVideos.value : [];
    const sh = shortsVideos.status === 'fulfilled' ? shortsVideos.value : [];
    const rd = redditVideos.status === 'fulfilled' ? redditVideos.value : [];
    const al = anilistVideos.status === 'fulfilled' ? anilistVideos.value : [];

    allVideos = shuffle([...yt.slice(0, 15), ...sh.slice(0, 15), ...rd.slice(0, 15), ...al.slice(0, 15)]);

    if (yt.length === 0 && sh.length === 0 && rd.length === 0 && al.length === 0) {
      showToast('Some sources are unavailable. Retrying…', 'warning');
    }

    renderVideos(allVideos);

    // Update stats
    updateStat('stat-total', formatNumber(allVideos.length));
    updateStat('stat-updated', 'Just now');

    sectionTitle.textContent = `${allVideos.length} Trending Videos & Shorts — All Sources`;
  } catch (err) {
    console.error(err);
    showToast('Failed to load some sources', 'error');
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1"><div class="empty-icon">😵</div><div class="empty-title">Failed to fetch</div><div class="empty-desc">Check your connection or try again</div></div>`;
  } finally {
    isLoading = false;
  }
}

function renderVideos(videos) {
  const grid = document.getElementById('video-grid');
  if (!grid) return;
  grid.innerHTML = '';

  if (!videos.length) {
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1"><div class="empty-icon">🎌</div><div class="empty-title">No videos found</div><div class="empty-desc">Try a different filter or search term</div></div>`;
    return;
  }

  videos.forEach((v, i) => {
    grid.appendChild(renderVideoCard(v, i));
  });
}

function filterByTab(tab) {
  currentTab = tab;
  let filtered = allVideos;
  if (tab !== 'all') filtered = allVideos.filter(v => v.platform === tab);
  renderVideos(filtered);

  const title = document.getElementById('section-title');
  const labels = {
    all: 'All Sources',
    youtube: 'YouTube Trending',
    shorts: 'YouTube Shorts',
    reddit: 'Reddit Trending',
    anilist: 'AniList Trending'
  };
  if (title) title.textContent = `${filtered.length} Videos — ${labels[tab] || tab}`;
}

function setupTabs(container) {
  container.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterByTab(btn.dataset.tab);
    });
  });
}

function setupSearch() {
  const input = document.getElementById('search-input');
  if (!input) return;
  const handleSearch = debounce(async (q) => {
    if (!q.trim()) { renderVideos(allVideos); return; }
    const grid = document.getElementById('video-grid');
    renderSkeletonCards(6).forEach(el => { grid.innerHTML = ''; grid.appendChild(el); });

    try {
      const results = await searchAnimeVideos(q);
      const redditMatch = allVideos.filter(v => v.platform === 'reddit' && v.title.toLowerCase().includes(q.toLowerCase()));
      renderVideos([...results, ...redditMatch]);
    } catch {
      const local = allVideos.filter(v => v.title.toLowerCase().includes(q.toLowerCase()));
      renderVideos(local);
    }
  }, 600);

  input.addEventListener('input', (e) => handleSearch(e.target.value));
}

function updateStat(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
