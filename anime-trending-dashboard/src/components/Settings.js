import { settings, queue } from '../store.js';
import { showToast } from '../utils/helpers.js';

export function renderSettings(container) {
  const s = settings.get();

  container.innerHTML = `
    <div class="settings-container">
      <div class="page-header" style="padding:0;margin-bottom:28px">
        <h1 class="page-title"><span>⚙️ Settings</span></h1>
      </div>

      <!-- API Keys -->
      <div class="settings-section">
        <div class="settings-title">🔑 API Keys</div>

        ${renderApiItem({
          name: 'Invidious (YouTube)',
          tag: 'FREE', tagClass: 'api-free',
          desc: 'Open-source YouTube frontend — no API key required! Works out of the box.',
          placeholder: 'No key needed ✅',
          key: '',
          readonly: true,
          value: 'Uses public instances automatically',
          note: 'Data Source: YouTube trending anime videos',
        })}

        ${renderApiItem({
          name: 'Reddit API',
          tag: 'FREE', tagClass: 'api-free',
          desc: 'Reddit JSON API — completely free with no authentication needed.',
          placeholder: 'No key needed ✅',
          key: '',
          readonly: true,
          value: 'Fetches from r/anime, r/AnimeMemes, r/AnimeEdits',
          note: 'Data Source: Reddit trending anime posts',
        })}

        ${renderApiItem({
          name: 'AniList GraphQL',
          tag: 'FREE', tagClass: 'api-free',
          desc: 'AniList API — free with no authentication required.',
          placeholder: 'No key needed ✅',
          key: '',
          readonly: true,
          value: 'No key needed',
          note: 'Data Source: Trending seasonal anime metadata',
        })}

        ${renderApiItem({
          name: 'YouTube Client ID (for Upload)',
          tag: 'OPTIONAL', tagClass: 'api-optional',
          desc: 'Required only for uploading videos to YouTube. Get from Google Cloud Console.',
          placeholder: 'Paste your OAuth2 Client ID here…',
          key: 'youtubeClientId',
          readonly: false,
          value: s.youtubeClientId || '',
          note: 'Free — 10,000 units/day. Get it at console.cloud.google.com',
        })}
      </div>

      <!-- Preferences -->
      <div class="settings-section">
        <div class="settings-title">🎛️ Preferences</div>

        <div class="settings-item">
          <div class="settings-item-header">
            <div class="settings-key-name">Default Upload Privacy</div>
          </div>
          <select class="form-select" id="pref-privacy" style="max-width:220px">
            <option value="private" ${s.defaultPrivacy==='private'?'selected':''}>🔒 Private</option>
            <option value="unlisted" ${s.defaultPrivacy==='unlisted'?'selected':''}>🔗 Unlisted</option>
            <option value="public" ${s.defaultPrivacy==='public'?'selected':''}>🌐 Public</option>
          </select>
        </div>

        <div class="settings-item">
          <div class="settings-item-header">
            <div class="settings-key-name">Auto-add Tags from Source</div>
            <label class="toggle">
              <input type="checkbox" id="pref-autotags" ${s.autoAddTags?'checked':''} />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="settings-key-desc">Automatically extract hashtags from source video title and description</div>
        </div>
      </div>

      <!-- Data & Storage -->
      <div class="settings-section">
        <div class="settings-title">💾 Data & Storage</div>
        <div class="settings-item">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
            <div>
              <div class="settings-key-name">Download Queue</div>
              <div class="settings-key-desc">${queue.count()} items in queue — stored in browser localStorage</div>
            </div>
            <button class="btn btn-danger btn-sm" id="clear-queue-settings">🗑 Clear Queue</button>
          </div>
        </div>
        <div class="settings-item">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
            <div>
              <div class="settings-key-name">All Settings</div>
              <div class="settings-key-desc">Reset everything to default</div>
            </div>
            <button class="btn btn-danger btn-sm" id="reset-settings">↩ Reset All</button>
          </div>
        </div>
      </div>

      <!-- About -->
      <div class="settings-section">
        <div class="settings-title">ℹ️ About AniTrend</div>
        <div class="settings-item" style="line-height:1.7;font-size:13px;color:var(--text-secondary)">
          <strong style="color:var(--text-primary)">AniTrend</strong> is a free anime video dashboard that aggregates trending content from multiple platforms using <strong>100% free APIs</strong>.<br><br>
          <strong>Free Sources:</strong> Invidious (YouTube proxy), Reddit JSON API, AniList GraphQL<br>
          <strong>Download:</strong> cobalt.tools (free, supports YT/Reddit/Twitter/Instagram)<br>
          <strong>Upload:</strong> YouTube Data API v3 (free 10k units/day)<br><br>
          <em style="color:var(--text-muted)">⚠️ Only download and re-upload content you have rights to use.</em>
        </div>
      </div>

      <button class="btn btn-primary" id="save-settings-btn" style="margin-top:8px">💾 Save Settings</button>
    </div>
  `;

  setupSettingsEvents();
}

function renderApiItem({ name, tag, tagClass, desc, placeholder, key, readonly, value, note }) {
  return `
    <div class="settings-item">
      <div class="settings-item-header">
        <div class="settings-key-name">${name}</div>
        <span class="api-tag ${tagClass}">${tag}</span>
      </div>
      <div class="settings-key-desc">${desc}</div>
      <div class="key-input-row">
        <input type="${readonly ? 'text' : 'password'}" class="form-input" 
          placeholder="${placeholder}" 
          value="${value}"
          ${readonly ? 'readonly style="opacity:0.5;cursor:default"' : ''}
          ${key ? `data-key="${key}"` : ''}
        />
      </div>
      ${note ? `<div style="font-size:11px;color:var(--text-muted);margin-top:6px">💡 ${note}</div>` : ''}
    </div>
  `;
}

function setupSettingsEvents() {
  document.getElementById('save-settings-btn')?.addEventListener('click', () => {
    const updates = {};
    document.querySelectorAll('[data-key]').forEach(el => {
      if (el.value) updates[el.dataset.key] = el.value;
    });

    const privacy = document.getElementById('pref-privacy');
    const autoTags = document.getElementById('pref-autotags');
    if (privacy) updates.defaultPrivacy = privacy.value;
    if (autoTags) updates.autoAddTags = autoTags.checked;

    settings.set(updates);
    showToast('Settings saved!', 'success');
  });

  document.getElementById('clear-queue-settings')?.addEventListener('click', () => {
    if (confirm('Clear download queue?')) {
      queue.clear();
      showToast('Queue cleared', 'info');
      renderSettings(document.getElementById('main-content'));
    }
  });

  document.getElementById('reset-settings')?.addEventListener('click', () => {
    if (confirm('Reset all settings to default?')) {
      localStorage.clear();
      showToast('Settings reset', 'info');
      renderSettings(document.getElementById('main-content'));
    }
  });
}
