import './styles/base.css';
import { renderDashboard } from './components/TrendingFeed.js';
import { renderQueue } from './components/DownloadQueue.js';
import { renderUploader } from './components/Uploader.js';
import { renderSettings } from './components/Settings.js';
import { updateQueueBadge } from './store.js';
import { initParticles } from './particles.js';

const views = {
  dashboard: renderDashboard,
  queue: renderQueue,
  upload: renderUploader,
  settings: renderSettings,
};

let currentView = 'dashboard';

function navigateTo(view) {
  const main = document.getElementById('main-content');
  if (!main || !views[view]) return;

  // Update nav
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.view === view);
  });

  currentView = view;
  views[view](main);
  updateQueueBadge();

  // Update URL hash
  window.location.hash = view;
}

function init() {
  // Init particles background
  initParticles();

  // Setup nav
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => navigateTo(btn.dataset.view));
  });

  // Handle hash routing
  const hash = window.location.hash.replace('#', '');
  const startView = Object.keys(views).includes(hash) ? hash : 'dashboard';
  navigateTo(startView);

  // Keyboard shortcut: Escape closes modal
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.getElementById('modal-overlay').style.display = 'none';
      document.getElementById('video-modal').style.display = 'none';
      document.getElementById('video-modal').innerHTML = '';
    }
  });
}

// Wait for DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
