import { queue, updateQueueBadge } from '../store.js';
import { showDownloadModal } from './DownloadModal.js';
import { showToast, formatNumber, timeAgo, truncate } from '../utils/helpers.js';

export function renderVideoModal(video) {
  const { overlay, modal } = openModalElements();

  const hasEmbed = !!video.embedUrl;
  const isAniList = video.platform === 'anilist';

  // Determine download capability
  const isYouTubeUrl = video.url?.includes('youtube') || video.url?.includes('youtu.be');
  const isRedditUrl = video.url?.includes('reddit');
  const canDirectDownload = isYouTubeUrl || isRedditUrl;

  // For AniList: build a YouTube search URL for trailer
  const ytSearchUrl = isAniList
    ? `https://www.youtube.com/results?search_query=${encodeURIComponent(video.title + ' official trailer anime')}`
    : '';

  // Trailer embed URL for AniList
  const trailerEmbed = isAniList && video.trailerUrl ? video.trailerUrl : '';

  // Effective embed URL
  const embedUrl = trailerEmbed || (hasEmbed ? video.embedUrl : '');
  const inQueue = queue.getAll().find(i => i.id === video.id);

  modal.innerHTML = `
    <div class="modal-header">
      <div style="display:flex;align-items:center;gap:10px;flex:1;min-width:0">
        ${isAniList && video.score ? `<span style="background:linear-gradient(135deg,#8b5cf6,#ec4899);color:white;font-size:11px;font-weight:700;padding:3px 9px;border-radius:99px;flex-shrink:0">⭐ ${video.score}/100</span>` : ''}
        <h2 style="font-size:16px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${truncate(video.title, 100)}</h2>
      </div>
      <button class="modal-close" id="modal-close-btn">✕</button>
    </div>
    <div class="modal-body">

      ${embedUrl ? `
        <div class="modal-video-frame">
          <iframe src="${embedUrl}?autoplay=0&rel=0" allowfullscreen
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            loading="lazy"></iframe>
        </div>
      ` : video.thumbnail ? `
        <div class="modal-video-frame" style="position:relative;background:#0a0a0f">
          <img src="${video.thumbnail}" style="width:100%;height:100%;object-fit:contain" alt="${video.title}" />
          <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">
            <a href="${video.url}" target="_blank" class="btn btn-primary">▶ Open on ${video.source}</a>
          </div>
        </div>
      ` : ''}

      <div class="modal-info">

        <!-- Stats Row -->
        <div class="modal-stats">
          ${video.views   ? `<span class="modal-stat">👁 ${formatNumber(video.views)}</span>` : ''}
          ${video.likes   ? `<span class="modal-stat">❤️ ${formatNumber(video.likes)}</span>` : ''}
          ${video.score   ? `<span class="modal-stat">⭐ ${video.score}/100</span>` : ''}
          ${video.comments? `<span class="modal-stat">💬 ${formatNumber(video.comments)}</span>` : ''}
          ${video.duration? `<span class="modal-stat">⏱ ${video.duration}</span>` : ''}
          ${video.publishedAt ? `<span class="modal-stat">📅 ${timeAgo(video.publishedAt)}</span>` : ''}
          ${video.season && video.seasonYear ? `<span class="modal-stat">📺 ${video.season} ${video.seasonYear}</span>` : ''}
          ${video.source  ? `<span class="modal-stat">📡 ${video.source}</span>` : ''}
        </div>

        ${video.channelName ? `<div style="font-size:13px;color:var(--text-secondary)">By <strong style="color:var(--purple-light)">${video.channelName}</strong></div>` : ''}

        <!-- Genres -->
        ${video.genres?.length ? `
          <div style="display:flex;gap:6px;flex-wrap:wrap">
            ${video.genres.slice(0,6).map(g => `
              <span style="font-size:11px;padding:3px 10px;border-radius:99px;
                background:rgba(139,92,246,0.15);color:var(--purple-light);
                border:1px solid rgba(139,92,246,0.3)">${g}</span>
            `).join('')}
          </div>
        ` : ''}

        <!-- Description -->
        ${video.description ? `
          <p style="font-size:13px;color:var(--text-secondary);line-height:1.6;max-height:80px;overflow:hidden;position:relative">
            ${truncate(video.description, 280)}
          </p>
        ` : ''}

        <!-- Action Buttons -->
        <div class="modal-actions">

          ${canDirectDownload ? `
            <button class="btn btn-primary" id="modal-download-btn">
              ⬇️ Download Video
            </button>
          ` : ''}

          ${isAniList ? `
            <button class="btn btn-primary" id="modal-yt-search-btn">
              🔍 Find on YouTube
            </button>
          ` : ''}

          <button class="btn btn-secondary" id="modal-queue-btn">
            ${inQueue ? '✅ In Queue' : '+ Add to Queue'}
          </button>

          <a href="${video.url}" target="_blank" class="btn btn-secondary">
            🔗 Open Source
          </a>
        </div>

        <!-- AniList extra: how to download guidance -->
        ${isAniList ? `
          <div style="margin-top:12px;padding:12px 14px;background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.2);border-radius:var(--radius);font-size:12px;color:var(--text-secondary)">
            💡 <strong style="color:var(--purple-light)">How to download:</strong>
            Click <em>"Find on YouTube"</em> to search for this anime's trailer or clips,
            then click the 📥 Download button on the video card!
          </div>
        ` : ''}

      </div>
    </div>
  `;

  // === Event Listeners ===

  document.getElementById('modal-close-btn').onclick = closeModalElements;
  overlay.onclick = (e) => { if (e.target === overlay) closeModalElements(); };

  // Direct download (YouTube/Reddit) — opens the full download modal
  const dlBtn = document.getElementById('modal-download-btn');
  if (dlBtn) {
    dlBtn.onclick = async () => {
      closeModalElements(); // close video modal first
      await showDownloadModal(video);
    };
  }

  // AniList → search on YouTube
  const ytBtn = document.getElementById('modal-yt-search-btn');
  if (ytBtn) {
    ytBtn.onclick = () => {
      window.open(ytSearchUrl, '_blank');
      showToast('YouTube search opened — find the clip, then use cobalt.tools to download!', 'info', 5000);
    };
  }

  // Add to queue
  const qBtn = document.getElementById('modal-queue-btn');
  if (qBtn) {
    qBtn.onclick = () => {
      const added = queue.add(video);
      if (added) {
        qBtn.textContent = '✅ In Queue';
        showToast(`"${truncate(video.title, 40)}" added to queue!`, 'success');
        updateQueueBadge();
      } else {
        showToast('Already in queue', 'info');
      }
    };
  }
}

// ===== Helpers =====
function openModalElements() {
  const overlay = document.getElementById('modal-overlay');
  const modal = document.getElementById('video-modal');
  overlay.style.display = 'block';
  modal.style.display = 'block';
  return { overlay, modal };
}

function closeModalElements() {
  document.getElementById('modal-overlay').style.display = 'none';
  document.getElementById('video-modal').style.display = 'none';
  document.getElementById('video-modal').innerHTML = '';
}
