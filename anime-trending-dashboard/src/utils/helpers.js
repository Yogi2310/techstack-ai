// Helper utilities

export function formatNumber(n) {
  if (!n && n !== 0) return '—';
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(1) + 'K';
  return n.toString();
}

export function timeAgo(dateStr) {
  if (!dateStr) return '';
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 30) return `${days}d ago`;
  return `${Math.floor(days / 30)}mo ago`;
}

export function truncate(str, max = 80) {
  if (!str) return '';
  return str.length > max ? str.slice(0, max) + '…' : str;
}

export function platformColor(platform) {
  const map = { youtube: '#ff0000', shorts: '#ff0050', reddit: '#ff4500', anilist: '#02a9f4' };
  return map[platform] || '#8b5cf6';
}

export function platformIcon(platform) {
  const map = { youtube: '▶', shorts: '⚡', reddit: '🤖', anilist: '🌸' };
  return map[platform] || '📺';
}

export function platformLabel(platform) {
  const map = { youtube: 'YouTube', shorts: 'Shorts', reddit: 'Reddit', anilist: 'AniList' };
  return map[platform] || platform;
}

export function showToast(message, type = 'info', duration = 3000) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span class="toast-icon">${icons[type]}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

export function openModal(videoData) {
  const overlay = document.getElementById('modal-overlay');
  const modal = document.getElementById('video-modal');
  overlay.style.display = 'block';
  modal.style.display = 'block';
  overlay.onclick = closeModal;
  return { overlay, modal };
}

export function closeModal() {
  document.getElementById('modal-overlay').style.display = 'none';
  document.getElementById('video-modal').style.display = 'none';
  document.getElementById('video-modal').innerHTML = '';
}

export function debounce(fn, delay = 300) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); };
}
