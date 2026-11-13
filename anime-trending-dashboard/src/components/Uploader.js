import { queue } from '../store.js';
import { showToast, truncate } from '../utils/helpers.js';

export function renderUploader(container) {
  const queueItems = queue.getAll();

  container.innerHTML = `
    <div class="upload-container">
      <div class="page-header" style="padding:0;margin-bottom:28px">
        <h1 class="page-title"><span>📤 YouTube</span> Uploader</h1>
      </div>

      <!-- OAuth Notice -->
      <div class="upload-card" style="margin-bottom:20px;background:linear-gradient(135deg,rgba(139,92,246,0.1),rgba(236,72,153,0.05));border-color:rgba(139,92,246,0.3)">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
          <span style="font-size:28px">🔐</span>
          <div>
            <div style="font-weight:700;font-size:16px">YouTube OAuth2 Login</div>
            <div style="font-size:13px;color:var(--text-secondary);margin-top:4px">Connect your YouTube channel to enable uploading. Uses free YouTube Data API v3.</div>
          </div>
        </div>
        <div style="display:flex;gap:10px;align-items:center">
          <button class="btn btn-primary" id="yt-auth-btn">🔗 Connect YouTube Channel</button>
          <span id="yt-auth-status" style="font-size:13px;color:var(--text-muted)">Not connected</span>
        </div>
        <div style="margin-top:12px;padding:12px;background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.2);border-radius:var(--radius)">
          <div style="font-size:12px;color:var(--yellow)">⚠️ You need a <strong>YouTube Data API v3 Client ID</strong> from Google Cloud Console (free). Go to Settings to add it first.</div>
        </div>
      </div>

      <!-- Upload Form -->
      <div class="upload-card">
        <div style="font-size:16px;font-weight:700;margin-bottom:20px;display:flex;align-items:center;gap:8px">
          📋 Video Details
        </div>

        <!-- Select from queue -->
        ${queueItems.length > 0 ? `
          <div class="form-group">
            <label class="form-label">📥 Load from Download Queue</label>
            <select class="form-select" id="queue-select">
              <option value="">— Select a downloaded video —</option>
              ${queueItems.map(i => `<option value="${i.id}" data-title="${i.title}">${truncate(i.title, 60)}</option>`).join('')}
            </select>
          </div>
        ` : ''}

        <div class="form-group">
          <label class="form-label" for="upload-title">Video Title</label>
          <input type="text" class="form-input" id="upload-title" maxlength="100" placeholder="Enter video title…" />
          <div class="char-count"><span id="title-count">0</span>/100</div>
        </div>

        <div class="form-group">
          <label class="form-label" for="upload-desc">Description</label>
          <textarea class="form-textarea" id="upload-desc" maxlength="5000" placeholder="Video description, credits, links…"></textarea>
          <div class="char-count"><span id="desc-count">0</span>/5000</div>
        </div>

        <div class="form-group">
          <label class="form-label" for="upload-tags">Tags (comma-separated)</label>
          <input type="text" class="form-input" id="upload-tags" placeholder="anime, amv, animeedit, trending…" />
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
          <div class="form-group">
            <label class="form-label" for="upload-category">Category</label>
            <select class="form-select" id="upload-category">
              <option value="24">Entertainment</option>
              <option value="10">Music</option>
              <option value="22">People & Blogs</option>
              <option value="20">Gaming</option>
              <option value="1">Film & Animation</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label" for="upload-privacy">Privacy</label>
            <select class="form-select" id="upload-privacy">
              <option value="private">🔒 Private</option>
              <option value="unlisted">🔗 Unlisted</option>
              <option value="public">🌐 Public</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="upload-file">Video File</label>
          <div style="border:2px dashed var(--border);border-radius:var(--radius);padding:32px;text-align:center;cursor:pointer;transition:var(--transition)" id="drop-zone">
            <div style="font-size:40px;margin-bottom:10px">🎬</div>
            <div style="font-weight:600;margin-bottom:6px">Drag & drop video file here</div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:16px">MP4, MOV, AVI — up to 256GB</div>
            <input type="file" id="upload-file" accept="video/*" style="display:none" />
            <button class="btn btn-secondary btn-sm" onclick="document.getElementById('upload-file').click()">Browse Files</button>
          </div>
          <div id="file-chosen" style="font-size:13px;color:var(--green);margin-top:8px;display:none"></div>
        </div>

        <div style="margin-top:8px">
          <button class="btn btn-primary" id="upload-btn" style="width:100%;justify-content:center;padding:14px">
            🚀 Upload to YouTube
          </button>
          <div id="upload-progress" style="display:none;margin-top:16px">
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px">
              <span>Uploading…</span><span id="upload-pct">0%</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" id="upload-fill" style="width:0%"></div></div>
          </div>
        </div>
      </div>

      <!-- Instructions -->
      <div class="upload-card" style="margin-top:20px">
        <div style="font-size:15px;font-weight:700;margin-bottom:16px">📖 How to Set Up YouTube Upload</div>
        <div style="display:flex;flex-direction:column;gap:12px">
          ${[
            ['1', '🌐', 'Go to Google Cloud Console', 'console.cloud.google.com', 'https://console.cloud.google.com'],
            ['2', '📁', 'Create a new project', 'e.g. "AniTrend Upload"', ''],
            ['3', '🔧', 'Enable YouTube Data API v3', 'In APIs & Services > Library', ''],
            ['4', '🔑', 'Create OAuth2 Client ID', 'Application type: Web Application', ''],
            ['5', '⚙️', 'Add Client ID to Settings', 'Paste it in the Settings page', ''],
          ].map(([num, icon, title, desc, link]) => `
            <div style="display:flex;gap:12px;align-items:flex-start">
              <div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,var(--purple),var(--pink));display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0">${num}</div>
              <div>
                <div style="font-weight:600;font-size:14px">${icon} ${title}</div>
                <div style="font-size:12px;color:var(--text-muted)">${link ? `<a href="${link}" target="_blank" style="color:var(--cyan)">${desc}</a>` : desc}</div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;

  setupUploaderEvents();
}

function setupUploaderEvents() {
  // Char counters
  const titleInput = document.getElementById('upload-title');
  const descInput = document.getElementById('upload-desc');
  if (titleInput) titleInput.oninput = () => { document.getElementById('title-count').textContent = titleInput.value.length; };
  if (descInput) descInput.oninput = () => { document.getElementById('desc-count').textContent = descInput.value.length; };

  // Queue select auto-fill
  const queueSel = document.getElementById('queue-select');
  if (queueSel) {
    queueSel.onchange = () => {
      const opt = queueSel.selectedOptions[0];
      if (opt?.dataset.title && titleInput) {
        titleInput.value = opt.dataset.title;
        titleInput.dispatchEvent(new Event('input'));
      }
    };
  }

  // File chooser
  const fileInput = document.getElementById('upload-file');
  const fileChosen = document.getElementById('file-chosen');
  if (fileInput) {
    fileInput.onchange = () => {
      const file = fileInput.files[0];
      if (file) { fileChosen.style.display = 'block'; fileChosen.textContent = `✅ Selected: ${file.name}`; }
    };
  }

  // Drop zone drag effects
  const dropZone = document.getElementById('drop-zone');
  if (dropZone) {
    dropZone.ondragover = (e) => { e.preventDefault(); dropZone.style.borderColor = 'var(--purple)'; };
    dropZone.ondragleave = () => { dropZone.style.borderColor = 'var(--border)'; };
    dropZone.ondrop = (e) => {
      e.preventDefault();
      dropZone.style.borderColor = 'var(--border)';
      const file = e.dataTransfer.files[0];
      if (file && fileInput && fileChosen) {
        const dt = new DataTransfer(); dt.items.add(file); fileInput.files = dt.files;
        fileChosen.style.display = 'block'; fileChosen.textContent = `✅ Selected: ${file.name}`;
      }
    };
  }

  // Auth button
  const authBtn = document.getElementById('yt-auth-btn');
  if (authBtn) {
    authBtn.onclick = () => {
      showToast('Add your YouTube Client ID in Settings first', 'info', 4000);
      document.querySelector('[data-view="settings"]')?.click();
    };
  }

  // Upload button
  const uploadBtn = document.getElementById('upload-btn');
  if (uploadBtn) {
    uploadBtn.onclick = () => {
      showToast('Connect your YouTube channel first (see Settings)', 'warning');
    };
  }
}
