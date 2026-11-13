// Download Modal — shows quality picker, progress bar, and fallback options
import { checkServer, getVideoInfo, downloadWithProgress, openWebDownloader, openCobaltDirect, searchYouTube } from '../utils/downloader.js';
import { searchAnimeVideos } from '../api/invidious.js';
import { showToast } from '../utils/helpers.js';

let serverStatus = null;

// Check server once on first use
async function ensureServerStatus() {
  if (serverStatus === null) serverStatus = await checkServer();
  return serverStatus;
}

export async function showDownloadModal(video) {
  // Remove existing modal if any
  document.getElementById('dl-modal-overlay')?.remove();

  const overlay = document.createElement('div');
  overlay.id = 'dl-modal-overlay';
  overlay.style.cssText = `position:fixed;inset:0;background:rgba(0,0,0,0.75);backdrop-filter:blur(8px);z-index:300;display:flex;align-items:center;justify-content:center;padding:20px`;

  const panel = document.createElement('div');
  panel.style.cssText = `background:var(--bg-secondary);border:1px solid var(--border-glow);border-radius:var(--radius-xl);width:min(520px,95vw);overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,0.7)`;

  panel.innerHTML = `
    <div style="padding:20px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between">
      <div style="display:flex;align-items:center;gap:10px">
        <span style="font-size:22px">⬇️</span>
        <span style="font-size:16px;font-weight:700">Download Video</span>
      </div>
      <button id="dl-close" style="width:32px;height:32px;border-radius:8px;background:var(--bg-card-hover);color:var(--text-secondary);font-size:18px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:1px solid var(--border)">✕</button>
    </div>

    <!-- Video info -->
    <div style="display:flex;gap:12px;padding:16px 24px;border-bottom:1px solid var(--border)">
      <img src="${video.thumbnail}" style="width:80px;height:45px;border-radius:8px;object-fit:cover;flex-shrink:0;background:#1a1a2e"
        onerror="this.src='https://placehold.co/80x45/1a1a2e/8b5cf6?text=Anime'" />
      <div style="min-width:0">
        <div style="font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${video.title}</div>
        <div style="font-size:11px;color:var(--text-muted);margin-top:4px">📡 ${video.source || video.platform}</div>
      </div>
    </div>

    <!-- Server status + content -->
    <div id="dl-body" style="padding:20px 24px">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px">
        <div id="dl-server-dot" style="width:10px;height:10px;border-radius:50%;background:var(--text-muted);flex-shrink:0"></div>
        <span id="dl-server-label" style="font-size:12px;color:var(--text-muted)">Checking download server…</span>
      </div>

      <!-- Quality selector (shown when server is up) -->
      <div id="dl-quality-section" style="display:none">
        <div style="font-size:12px;font-weight:600;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px">Quality</div>
        <div id="dl-quality-btns" style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px">
          ${['1080','720','480','360'].map(q => `
            <button class="dl-quality-btn" data-q="${q}" style="padding:8px 16px;border-radius:8px;border:1px solid var(--border);background:var(--bg-card);color:var(--text-secondary);font-size:13px;font-weight:600;cursor:pointer;transition:all 0.2s">
              ${q}p
            </button>
          `).join('')}
        </div>
        <button id="dl-start-btn" class="btn btn-primary" style="width:100%;justify-content:center;padding:13px;font-size:15px">
          ⬇️ Download with yt-dlp
        </button>
      </div>

      <!-- Progress (shown during download) -->
      <div id="dl-progress-section" style="display:none">
        <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px">
          <span id="dl-status-text">Starting…</span>
          <span id="dl-pct-text" style="color:var(--purple-light);font-weight:700">0%</span>
        </div>
        <div style="height:8px;background:var(--border);border-radius:4px;overflow:hidden;margin-bottom:8px">
          <div id="dl-prog-fill" style="height:100%;width:0%;background:linear-gradient(90deg,var(--purple),var(--cyan));border-radius:4px;transition:width 0.3s"></div>
        </div>
        <div id="dl-speed-text" style="font-size:11px;color:var(--text-muted)">Connecting…</div>
      </div>

      <!-- Done state -->
      <div id="dl-done-section" style="display:none;text-align:center;padding:16px 0">
        <div style="font-size:40px;margin-bottom:12px">✅</div>
        <div style="font-size:16px;font-weight:700;margin-bottom:6px">Download Complete!</div>
        <div id="dl-done-path" style="font-size:12px;color:var(--text-muted);word-break:break-all"></div>
      </div>

      <!-- Fallback options (shown when server is NOT running) -->
      <div id="dl-fallback-section" style="display:none">
        <div style="padding:12px 14px;background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.25);border-radius:var(--radius);margin-bottom:16px">
          <div style="font-size:13px;font-weight:600;color:var(--yellow);margin-bottom:4px">⚡ Start the Download Server</div>
          <div style="font-size:12px;color:var(--text-secondary);margin-bottom:8px">For the best experience, run the local server (uses yt-dlp, saves to Downloads folder):</div>
          <code style="display:block;background:var(--bg-primary);padding:8px 12px;border-radius:6px;font-size:11px;color:var(--cyan)">node server.js</code>
        </div>

        <div style="font-size:12px;font-weight:600;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px">Or use a web downloader:</div>
        <div style="display:flex;flex-direction:column;gap:8px" id="dl-web-options"></div>
      </div>
    </div>
  `;

  overlay.appendChild(panel);
  document.body.appendChild(overlay);

  // Close on overlay click or X
  overlay.addEventListener('click', (e) => { if (e.target === overlay) cleanup(); });
  document.getElementById('dl-close').addEventListener('click', cleanup);

  // Quality button selection
  let selectedQuality = '720';
  panel.querySelectorAll('.dl-quality-btn').forEach(btn => {
    if (btn.dataset.q === '720') applyActiveStyle(btn);
    btn.addEventListener('click', () => {
      panel.querySelectorAll('.dl-quality-btn').forEach(b => removeActiveStyle(b));
      applyActiveStyle(btn);
      selectedQuality = btn.dataset.q;
    });
  });

  // ── Check server and render appropriate UI ──
  const status = await checkServer();

  const dot = document.getElementById('dl-server-dot');
  const label = document.getElementById('dl-server-label');

  if (status.available) {
    dot.style.background = 'var(--green)';
    dot.style.boxShadow = '0 0 8px var(--green)';
    label.style.color = 'var(--green)';
    label.textContent = `✅ Server ready — yt-dlp ${status.ytdlp}`;

    document.getElementById('dl-quality-section').style.display = 'block';

    document.getElementById('dl-start-btn').addEventListener('click', () => {
      startDownload(video, selectedQuality, panel, cleanup);
    });
  } else {
    dot.style.background = 'var(--yellow)';
    label.style.color = 'var(--yellow)';
    label.textContent = '⚠️ Local server not running';

    document.getElementById('dl-fallback-section').style.display = 'block';
    renderWebOptions(video.url, document.getElementById('dl-web-options'));
  }

  function cleanup() {
    document.getElementById('dl-modal-overlay')?.remove();
  }
}

async function startDownload(videoObjOrUrl, quality, panel, cleanup) {
  let targetUrl = typeof videoObjOrUrl === 'string' ? videoObjOrUrl : videoObjOrUrl?.url;
  let title = typeof videoObjOrUrl === 'object' ? videoObjOrUrl?.title : '';

  document.getElementById('dl-quality-section').style.display = 'none';
  document.getElementById('dl-progress-section').style.display = 'block';

  const fill = document.getElementById('dl-prog-fill');
  const pct = document.getElementById('dl-pct-text');
  const statusTxt = document.getElementById('dl-status-text');
  const speedTxt = document.getElementById('dl-speed-text');

  if (!targetUrl || targetUrl.includes('anilist.co')) {
    statusTxt.textContent = 'Finding anime trailer on YouTube…';
    try {
      const res = await searchYouTube((title || 'anime') + ' trailer');
      if (res && res.url) {
        targetUrl = res.url;
      }
    } catch {
      try {
        const results = await searchAnimeVideos((title || 'anime') + ' trailer');
        if (results.length > 0 && results[0].url) {
          targetUrl = results[0].url;
        }
      } catch {}
    }
  }

  downloadWithProgress(targetUrl, quality, {
    onProgress: ({ progress, speed, eta }) => {
      fill.style.width = `${progress}%`;
      pct.textContent = `${progress.toFixed(1)}%`;
      if (speed) speedTxt.textContent = `⚡ ${speed}${eta ? ' — ETA ' + eta : ''}`;
    },
    onStatus: (msg) => { statusTxt.textContent = msg.slice(0, 60); },
    onDone: (result) => {
      if (result.success) {
        document.getElementById('dl-progress-section').style.display = 'none';
        const doneSection = document.getElementById('dl-done-section');
        doneSection.style.display = 'block';

        if (result.filename) {
          const fileUrl = `http://127.0.0.1:3001/api/file/${encodeURIComponent(result.filename)}`;
          doneSection.innerHTML = `
            <div style="font-size:40px;margin-bottom:12px">✅</div>
            <div style="font-size:16px;font-weight:700;margin-bottom:6px">Download Complete!</div>
            <div style="font-size:12px;color:var(--text-muted);word-break:break-all;margin-bottom:16px">📁 Saved to: ${result.downloadsDir || result.path || 'Downloads/AniTrend'}</div>
            <a href="${fileUrl}" download="${result.filename}" class="btn btn-primary" style="display:inline-flex;justify-content:center">
              💾 Save MP4 File to Computer
            </a>
          `;

          // Automatically trigger browser download prompt
          try {
            const link = document.createElement('a');
            link.href = fileUrl;
            link.download = result.filename;
            document.body.appendChild(link);
            link.click();
            link.remove();
          } catch {}
        }
        showToast('Download complete! File saved 🎉', 'success', 5000);
      } else {
        statusTxt.textContent = '❌ ' + (result.error || 'Download failed');
        pct.textContent = 'Error';
        showToast('Download failed: ' + result.error, 'error');
      }
    },
    onError: (err) => {
      statusTxt.textContent = '❌ ' + err;
      showToast('Download error: ' + err, 'error');
    },
  });
}

function renderWebOptions(url, container) {
  const isYouTube = url.includes('youtu');

  const options = [
    {
      label: 'Cobalt.tools (Cleanest — Copy & Open)',
      icon: '🌀',
      color: '#06b6d4',
      desc: 'No ads — copies video link & opens cobalt.tools',
      enabled: true,
      action: () => openCobaltDirect(url),
    },
    {
      label: 'SSYouTube (Fastest — URL trick)',
      icon: '⚡',
      color: '#ff0000',
      desc: 'Adds "ss" before youtube.com — opens instantly',
      enabled: isYouTube,
      action: () => openWebDownloader(url, 'ssyt'),
    },
    {
      label: 'SaveFrom.net',
      icon: '💾',
      color: '#22c55e',
      desc: 'Supports YouTube, Vimeo, Instagram',
      enabled: true,
      action: () => openWebDownloader(url, 'savefrom'),
    },
    {
      label: 'Loader.to',
      icon: '🔄',
      color: '#06b6d4',
      desc: 'Multi-format: MP4, MP3, WebM, 4K',
      enabled: true,
      action: () => openWebDownloader(url, 'loader'),
    },
    {
      label: 'y2mate.com',
      icon: '▶',
      color: '#8b5cf6',
      desc: 'YouTube downloader with quality options',
      enabled: isYouTube,
      action: () => openWebDownloader(url, 'y2mate'),
    },
  ];

  options.filter(o => o.enabled).forEach(opt => {
    const btn = document.createElement('button');
    btn.style.cssText = `display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:var(--radius);background:var(--bg-card);border:1px solid var(--border);color:var(--text-primary);cursor:pointer;transition:all 0.2s;text-align:left;width:100%`;
    btn.innerHTML = `
      <span style="font-size:20px;flex-shrink:0">${opt.icon}</span>
      <div>
        <div style="font-size:13px;font-weight:600">${opt.label}</div>
        <div style="font-size:11px;color:var(--text-muted);margin-top:2px">${opt.desc}</div>
      </div>
      <span style="margin-left:auto;font-size:12px;color:var(--text-muted)">Open →</span>
    `;
    btn.addEventListener('mouseenter', () => { btn.style.borderColor = opt.color; btn.style.background = 'var(--bg-card-hover)'; });
    btn.addEventListener('mouseleave', () => { btn.style.borderColor = 'var(--border)'; btn.style.background = 'var(--bg-card)'; });
    btn.addEventListener('click', () => {
      opt.action();
      showToast(`Opening ${opt.label}…`, 'info');
    });
    container.appendChild(btn);
  });
}

function applyActiveStyle(btn) {
  btn.style.background = 'linear-gradient(135deg,var(--purple),var(--pink))';
  btn.style.borderColor = 'transparent';
  btn.style.color = 'white';
}
function removeActiveStyle(btn) {
  btn.style.background = 'var(--bg-card)';
  btn.style.borderColor = 'var(--border)';
  btn.style.color = 'var(--text-secondary)';
}
