import { queue, updateQueueBadge } from '../store.js';
import { downloadVideo } from '../utils/downloader.js';
import { showDownloadModal } from './DownloadModal.js';
import { formatNumber, timeAgo, truncate, showToast } from '../utils/helpers.js';

export function renderQueue(container) {
  const items = queue.getAll();

  container.innerHTML = `
    <div class="queue-container">
      <div class="page-header" style="padding:0 0 0 0;margin-bottom:24px">
        <h1 class="page-title"><span>⬇️ Download</span> Queue</h1>
        <div style="display:flex;gap:10px">
          ${items.length ? `<button class="btn btn-danger btn-sm" id="clear-queue-btn">🗑 Clear All</button>` : ''}
          <button class="btn btn-primary btn-sm" id="download-all-btn" ${!items.length ? 'disabled style="opacity:0.5"' : ''}>📥 Download All</button>
        </div>
      </div>

      ${!items.length ? `
        <div class="empty-state">
          <div class="empty-icon">📭</div>
          <div class="empty-title">Queue is empty</div>
          <div class="empty-desc">Go to Trending and add videos to your download queue</div>
        </div>
      ` : `
        <div class="queue-list" id="queue-list">
          ${items.map(item => renderQueueItem(item)).join('')}
        </div>
      `}
    </div>
  `;

  // Clear all
  const clearBtn = document.getElementById('clear-queue-btn');
  if (clearBtn) {
    clearBtn.onclick = () => {
      if (confirm('Clear all items from queue?')) {
        queue.clear();
        renderQueue(container);
        showToast('Queue cleared', 'info');
      }
    };
  }

  // Download all directly via backend
  const dlAllBtn = document.getElementById('download-all-btn');
  if (dlAllBtn && items.length) {
    dlAllBtn.onclick = async () => {
      showToast('Starting downloads for queue items…', 'info');
      for (const item of items) {
        if (item.url) {
          showToast(`Downloading: ${truncate(item.title, 35)}…`, 'info');
          const res = await downloadVideo(item.url);
          if (res.success) {
            showToast(`Saved: ${truncate(item.title, 30)} 🎉`, 'success', 4000);
          } else {
            showToast(`Failed: ${res.error || 'Download error'}`, 'error', 4000);
          }
        }
      }
    };
  }

  // Individual item buttons
  document.querySelectorAll('[data-remove]').forEach(btn => {
    btn.onclick = () => {
      queue.remove(btn.dataset.remove);
      updateQueueBadge();
      renderQueue(container);
      showToast('Removed from queue', 'info');
    };
  });

  document.querySelectorAll('[data-download]').forEach(btn => {
    btn.onclick = async () => {
      const url = btn.dataset.download;
      const item = items.find(i => i.url === url || i.id === url);
      if (item) {
        await showDownloadModal(item);
      } else {
        await showDownloadModal({ title: 'Video', url, thumbnail: '' });
      }
    };
  });
}

function renderQueueItem(item) {
  const platform = item.platform || 'youtube';
  const platformColors = { youtube: '#ff0000', reddit: '#ff4500', anilist: '#02a9f4' };
  const color = platformColors[platform] || '#8b5cf6';

  return `
    <div class="queue-item" data-id="${item.id}">
      <div class="queue-thumb">
        <img src="${item.thumbnail || ''}" alt="${item.title}" 
          onerror="this.src='https://placehold.co/120x68/1a1a2e/8b5cf6?text=Anime'"
          loading="lazy" />
      </div>
      <div class="queue-info">
        <div class="queue-title" title="${item.title}">${truncate(item.title, 70)}</div>
        <div class="queue-source" style="color:${color}">📡 ${item.source || platform}</div>
        <div class="queue-status status-queued">⏳ Ready to download</div>
      </div>
      <div class="queue-actions">
        <button class="btn btn-primary btn-sm" data-download="${item.url}" title="Download">📥</button>
        <button class="btn btn-secondary btn-sm" data-remove="${item.id}" title="Remove">✕</button>
      </div>
    </div>
  `;
}
