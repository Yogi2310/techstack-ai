import { queue, updateQueueBadge } from '../store.js';
import { formatNumber, timeAgo, truncate, platformLabel, showToast } from '../utils/helpers.js';
import { renderVideoModal } from './VideoModal.js';
import { showDownloadModal } from './DownloadModal.js';

export function renderVideoCard(video, rank) {
  const card = document.createElement('div');
  card.className = 'video-card';
  card.dataset.id = video.id;

  const inQueue = queue.getAll().find(i => i.id === video.id);
  const platform = video.platform || 'youtube';

  const badgeClass = `badge-${platform}`;
  const platformName = platformLabel(platform);

  card.innerHTML = `
    <div class="card-thumbnail">
      <img 
        src="${video.thumbnail || '/placeholder.svg'}" 
        alt="${video.title}"
        loading="lazy"
        onerror="this.src='https://placehold.co/480x270/1a1a2e/8b5cf6?text=Anime'"
      />
      <div class="play-overlay">
        <div class="play-btn-large">▶</div>
      </div>
      ${video.duration ? `<span class="card-duration">${video.duration}</span>` : ''}
      <span class="card-platform-badge ${badgeClass}">${platformName}</span>
      ${rank !== undefined && rank < 10 ? `<span class="trending-rank">#${rank + 1}</span>` : ''}
    </div>
    <div class="card-body">
      <div class="card-title">${truncate(video.title, 80)}</div>
      <div class="card-meta">
        <div class="card-stats">
          ${video.views ? `<span class="card-stat">👁 ${formatNumber(video.views)}</span>` : ''}
          ${video.likes ? `<span class="card-stat">❤️ ${formatNumber(video.likes)}</span>` : ''}
          ${video.publishedAt ? `<span class="card-stat">🕐 ${timeAgo(video.publishedAt)}</span>` : ''}
        </div>
        <div class="card-actions">
          <button class="action-btn ${inQueue ? 'queued' : ''}" data-action="queue" title="${inQueue ? 'In Queue' : 'Add to Queue'}">
            ${inQueue ? '✅' : '⬇'}
          </button>
          <button class="action-btn" data-action="download" title="Download">📥</button>
        </div>
      </div>
    </div>
  `;

  // Click card → open modal
  card.querySelector('.card-thumbnail').addEventListener('click', () => {
    renderVideoModal(video);
  });
  card.querySelector('.card-title').addEventListener('click', () => {
    renderVideoModal(video);
  });

  // Queue button
  card.querySelector('[data-action="queue"]').addEventListener('click', (e) => {
    e.stopPropagation();
    const btn = e.currentTarget;
    const added = queue.add(video);
    if (added) {
      btn.textContent = '✅';
      btn.classList.add('queued');
      showToast(`Added to queue`, 'success');
      updateQueueBadge();
    } else {
      showToast('Already in queue', 'info');
    }
  });

  // Download button — opens the full download modal
  card.querySelector('[data-action="download"]').addEventListener('click', async (e) => {
    e.stopPropagation();
    await showDownloadModal(video);
  });

  return card;
}

export function renderSkeletonCards(count = 8) {
  return Array.from({ length: count }, () => {
    const el = document.createElement('div');
    el.className = 'skeleton-card';
    el.innerHTML = `
      <div class="skeleton skeleton-thumb"></div>
      <div class="skeleton-body">
        <div class="skeleton skeleton-line"></div>
        <div class="skeleton skeleton-line short"></div>
      </div>
    `;
    return el;
  });
}
