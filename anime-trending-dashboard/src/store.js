// Global state — backed by localStorage

const STORAGE_KEYS = {
  queue: 'anitrend_queue',
  settings: 'anitrend_settings',
  history: 'anitrend_history',
};

function load(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; }
}
function save(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch {}
}

// --- Download Queue ---
export const queue = {
  getAll: () => load(STORAGE_KEYS.queue, []),
  add(video) {
    const items = this.getAll();
    if (items.find(i => i.id === video.id)) return false;
    items.unshift({ ...video, status: 'queued', addedAt: Date.now(), progress: 0 });
    save(STORAGE_KEYS.queue, items);
    updateQueueBadge();
    return true;
  },
  remove(id) {
    const items = this.getAll().filter(i => i.id !== id);
    save(STORAGE_KEYS.queue, items);
    updateQueueBadge();
  },
  update(id, updates) {
    const items = this.getAll().map(i => i.id === id ? { ...i, ...updates } : i);
    save(STORAGE_KEYS.queue, items);
  },
  clear() { save(STORAGE_KEYS.queue, []); updateQueueBadge(); },
  count: () => load(STORAGE_KEYS.queue, []).length,
};

// --- Settings ---
export const settings = {
  get: () => load(STORAGE_KEYS.settings, {
    youtubeApiKey: '',
    youtubeClientId: '',
    defaultPrivacy: 'private',
    defaultCategory: '24',
    autoAddTags: true,
    fetchInterval: 30,
    darkMode: true,
    activeTab: 'youtube',
  }),
  set(updates) {
    const current = this.get();
    save(STORAGE_KEYS.settings, { ...current, ...updates });
  },
  getValue: (key) => settings.get()[key],
};

// --- History ---
export const history = {
  getAll: () => load(STORAGE_KEYS.history, []),
  add(video) {
    const items = this.getAll().filter(i => i.id !== video.id);
    items.unshift({ ...video, viewedAt: Date.now() });
    save(STORAGE_KEYS.history, items.slice(0, 100)); // keep last 100
  },
};

// --- UI helpers ---
function updateQueueBadge() {
  const badge = document.getElementById('queue-badge');
  const count = queue.count();
  if (badge) {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'inline-flex' : 'none';
  }
}

// Initialize badge on load
document.addEventListener('DOMContentLoaded', updateQueueBadge);
export { updateQueueBadge };
