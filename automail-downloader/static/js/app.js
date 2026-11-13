/* ============================================================
   AutoMail Downloader — Frontend App
   ============================================================ */
(function () {
  'use strict';

  // ── State ──────────────────────────────────────────────────────────────────
  const S = {
    connected:  false,
    emails:     [],
    downloads:  [],
    dlProgress: {},   // url → progress
    stats: { emails: 0, urls: 0, files: 0, hits: 0 },
  };

  const $ = id => document.getElementById(id);
  const el = (tag, cls, html) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  };

  // ── Init ───────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    bindNav();
    bindConnect();
    bindEmailActions();
    bindDownloadActions();
    bindCacheActions();
    checkStatus();
  });

  // ── Navigation ─────────────────────────────────────────────────────────────
  function bindNav() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', () => switchView(btn.dataset.view));
    });
    $('hamburger').addEventListener('click', () => $('sidebar').classList.toggle('open'));
    document.addEventListener('click', e => {
      if (!e.target.closest('.sidebar') && !e.target.closest('.hamburger')) {
        $('sidebar').classList.remove('open');
      }
    });
  }

  const VIEW_TITLES = { emails: '📬 Emails', downloads: '📁 Downloads', cache: '🗄️ Cache' };
  function switchView(view) {
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const btn = document.querySelector(`.nav-btn[data-view="${view}"]`);
    if (btn) btn.classList.add('active');
    $(`view${cap(view)}`).classList.add('active');
    $('topbarTitle').textContent = VIEW_TITLES[view] || view;

    if (view === 'downloads') loadDownloads();
    if (view === 'cache') loadCacheStats();
  }

  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  // ── Status check ───────────────────────────────────────────────────────────
  async function checkStatus() {
    try {
      const d = await api('/api/status');
      if (d.connected) {
        setConnected(d.email, d.host);
        $('autoPollToggle').checked = d.auto_poll;
        $('pollInterval').value = String(d.poll_interval || 300);
      }
    } catch (_) {}
  }

  // ── Connection ─────────────────────────────────────────────────────────────
  function bindConnect() {
    // Auto-fill host when email changes
    $('fieldEmail').addEventListener('blur', async () => {
      const email = $('fieldEmail').value.trim();
      if (!email || $('fieldHost').value) return;
      try {
        const d = await api('/api/guess-host', 'POST', { email });
        $('fieldHost').value = d.host;
        $('fieldPort').value = d.port;
      } catch (_) {}
    });

    $('btnConnect').addEventListener('click', async () => {
      const btn = $('btnConnect');
      btn.textContent = 'Connecting…';
      btn.disabled = true;
      try {
        const d = await api('/api/connect', 'POST', {
          email:    $('fieldEmail').value.trim(),
          password: $('fieldPassword').value.trim(),
          host:     $('fieldHost').value.trim(),
          port:     $('fieldPort').value,
        });
        if (d.connected) {
          setConnected(d.email, d.host);
          toast('✅ Connected to ' + d.email, 'success');
          loadFolders();
          fetchEmails();
        } else {
          toast('❌ ' + (d.error || 'Connection failed'), 'error');
        }
      } catch (e) {
        toast('❌ ' + e.message, 'error');
      } finally {
        btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg> Connect`;
        btn.disabled = false;
      }
    });

    $('btnDisconnect').addEventListener('click', async () => {
      await api('/api/disconnect', 'POST', {});
      setDisconnected();
      toast('🔌 Disconnected', 'info');
    });

    // Auto-poll toggle
    $('autoPollToggle').addEventListener('change', async () => {
      const enable = $('autoPollToggle').checked;
      const interval = parseInt($('pollInterval').value);
      await api('/api/autopoll', 'POST', { enable, interval });
      toast(enable ? `🔄 Auto-refresh every ${interval}s` : '⏸ Auto-refresh off', 'info');
    });
    $('pollInterval').addEventListener('change', async () => {
      if ($('autoPollToggle').checked) {
        const interval = parseInt($('pollInterval').value);
        await api('/api/autopoll', 'POST', { enable: true, interval });
      }
    });
  }

  function setConnected(email, host) {
    S.connected = true;
    $('connFormWrap').style.display = 'none';
    $('connStatus').style.display = 'flex';
    $('connEmail').textContent = email;
    $('connHost').textContent  = host;
    $('autopollRow').style.display = 'flex';
  }
  function setDisconnected() {
    S.connected = false;
    $('connFormWrap').style.display = 'block';
    $('connStatus').style.display = 'none';
    $('autopollRow').style.display = 'none';
    S.emails = [];
    renderEmails([]);
  }

  // ── Folders ────────────────────────────────────────────────────────────────
  async function loadFolders() {
    try {
      const d = await api('/api/folders');
      const sel = $('folderSelect');
      sel.innerHTML = '';
      (d.folders || ['INBOX']).forEach(f => {
        const o = document.createElement('option');
        o.value = f; o.textContent = f;
        sel.appendChild(o);
      });
    } catch (_) {}
  }

  // ── Email actions ──────────────────────────────────────────────────────────
  function bindEmailActions() {
    $('btnFetch').addEventListener('click', fetchEmails);
    $('btnRefreshDl').addEventListener('click', loadDownloads);
  }

  async function fetchEmails() {
    if (!S.connected) { toast('⚠️ Connect to a mailbox first', 'error'); return; }
    const btn = $('btnFetch');
    btn.textContent = 'Fetching…';
    btn.disabled = true;
    try {
      const folder  = $('folderSelect').value || 'INBOX';
      const limit   = parseInt($('limitSelect').value);
      const unread  = $('unreadOnly').checked;
      const d = await api(`/api/emails?folder=${encodeURIComponent(folder)}&limit=${limit}&unread=${unread}`);
      S.emails = d.emails || [];
      renderEmails(S.emails);
      updateStats();
      toast(`✅ Loaded ${S.emails.length} emails`, 'success');
    } catch (e) {
      toast('❌ ' + e.message, 'error');
    } finally {
      btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/></svg> Fetch Emails`;
      btn.disabled = false;
    }
  }

  // ── Render emails ──────────────────────────────────────────────────────────
  function renderEmails(emails) {
    const list  = $('emailList');
    const empty = $('emailEmpty');

    if (!emails.length) {
      list.innerHTML = '';
      list.appendChild(empty);
      empty.style.display = 'flex';
      return;
    }
    empty.style.display = 'none';

    // Remove old cards (keep empty)
    [...list.children].forEach(c => { if (c !== empty) c.remove(); });

    emails.forEach(em => {
      const card = buildEmailCard(em);
      list.appendChild(card);
    });
  }

  const FILE_ICONS = {
    pdf: '📄', zip: '🗜️', rar: '🗜️', mp4: '🎬', mp3: '🎵',
    jpg: '🖼️', jpeg: '🖼️', png: '🖼️', gif: '🖼️', webp: '🖼️',
    doc: '📝', docx: '📝', xls: '📊', xlsx: '📊', ppt: '📊',
    txt: '📃', csv: '📊', exe: '⚙️', apk: '📱', default: '🔗',
  };
  function fileIcon(url) {
    const ext = url.split('?')[0].split('.').pop().toLowerCase();
    return FILE_ICONS[ext] || FILE_ICONS.default;
  }
  function isVideoUrl(url) {
    return /youtube\.com|youtu\.be|vimeo\.com|dailymotion|tiktok|instagram|twitter\.com|x\.com/i.test(url);
  }

  function buildEmailCard(em) {
    const card = el('div', 'email-card');
    const initial = (em.sender || '?').replace(/.*</, '').replace(/>.*/, '').charAt(0).toUpperCase();
    const urlChip = em.url_count ? `<span class="chip chip-url">🔗 ${em.url_count} URL${em.url_count > 1 ? 's' : ''}</span>` : '';
    const attChip = em.attachments?.length ? `<span class="chip chip-attach">📎 ${em.attachments.length}</span>` : '';
    const cached  = em.cached ? `<span class="chip chip-cached">⚡ Cached</span>` : '';

    // Header
    const header = el('div', 'email-header');
    header.innerHTML = `
      <div class="email-avatar">${initial}</div>
      <div class="email-meta">
        <div class="email-subject">${esc(em.subject)}</div>
        <div class="email-from">${esc(em.sender)}</div>
        <div class="email-date">${esc(em.date)}</div>
      </div>
      <div class="email-chips">
        ${urlChip}${attChip}${cached}
        <span class="chip chip-expand" id="chipExpand-${em.msg_id}">▼</span>
      </div>`;
    card.appendChild(header);

    // Collapsible body
    const body = el('div', 'email-body');
    body.style.display = 'none';
    card.appendChild(body);

    // Body preview
    if (em.body_preview) {
      const prev = el('div', 'email-preview');
      prev.textContent = em.body_preview;
      body.appendChild(prev);
    }

    // URL section
    if (em.urls && em.urls.length) {
      const sec = el('div', 'url-section');
      const titleRow = el('div', 'url-section-title');
      titleRow.innerHTML = `<span>🔗 ${em.urls.length} URLs found</span>`;
      const dlAll = el('button', 'btn-dl-all', '⬇️ Download All');
      titleRow.appendChild(dlAll);
      sec.appendChild(titleRow);

      const urlEls = [];
      em.urls.forEach(url => {
        const row = buildUrlRow(url);
        urlEls.push({ url, row });
        sec.appendChild(row);
      });

      dlAll.addEventListener('click', () => {
        urlEls.forEach(({ url }) => startDownload(url));
      });

      body.appendChild(sec);
    }

    // Attachments
    if (em.attachments && em.attachments.length) {
      const sec = el('div', 'attach-section');
      sec.innerHTML = `<div class="attach-title">📎 Attachments (email server — no direct download)</div>`;
      em.attachments.forEach(name => {
        const row = el('div', 'attach-row', `📎 ${esc(name)}`);
        sec.appendChild(row);
      });
      body.appendChild(sec);
    }

    // Toggle expand
    header.addEventListener('click', () => {
      const open = body.style.display !== 'none';
      body.style.display = open ? 'none' : 'block';
      card.classList.toggle('open', !open);
      const chip = $(`chipExpand-${em.msg_id}`);
      if (chip) chip.textContent = open ? '▼' : '▲';
    });

    return card;
  }

  function buildUrlRow(url) {
    const row = el('div', 'url-row');
    const icon = isVideoUrl(url) ? '🎬' : fileIcon(url);
    row.innerHTML = `
      <span class="url-icon">${icon}</span>
      <span class="url-text"><a href="${esc(url)}" target="_blank" rel="noopener">${esc(url)}</a></span>
      <div class="url-actions">
        <button class="btn-dl" data-url="${esc(url)}">⬇️ Download</button>
      </div>`;

    // Progress bar
    const pb = el('div', 'url-progress');
    const fill = el('div', 'url-progress-fill');
    pb.appendChild(fill);
    pb.style.display = 'none';
    row.appendChild(pb);

    row.querySelector('.btn-dl').addEventListener('click', () => {
      startDownload(url, row, fill, pb);
    });
    return row;
  }

  // ── Download ───────────────────────────────────────────────────────────────
  async function startDownload(url, rowEl, fillEl, pbEl) {
    const btn = rowEl ? rowEl.querySelector('.btn-dl') : null;
    if (btn) { btn.classList.add('downloading'); btn.textContent = '⏳ Starting…'; }
    if (pbEl) pbEl.style.display = 'block';

    try {
      const d = await api('/api/download', 'POST', { url });

      if (d.status === 'cached') {
        if (btn) { btn.classList.remove('downloading'); btn.classList.add('cached'); btn.textContent = '✅ Cached'; }
        toast(`✅ Already cached: ${d.filename}`, 'success');
        updateStats();
        return;
      }

      const urlHash = d.url_hash;
      pollDownload(url, urlHash, btn, fillEl, pbEl);
    } catch (e) {
      if (btn) { btn.classList.add('error'); btn.textContent = '❌ Error'; }
      toast('❌ Download failed: ' + e.message, 'error');
    }
  }

  function pollDownload(url, urlHash, btn, fillEl, pbEl) {
    const interval = setInterval(async () => {
      try {
        const prog = await api(`/api/download/progress/${urlHash}`);
        const pct = prog.percent || 0;

        if (fillEl) fillEl.style.width = pct + '%';
        if (btn) {
          if (prog.status === 'downloading') {
            btn.textContent = `⬇️ ${Math.round(pct)}%`;
          }
        }

        if (prog.status === 'done') {
          clearInterval(interval);
          if (btn) { btn.classList.remove('downloading'); btn.classList.add('done'); btn.textContent = '✅ Done'; }
          if (pbEl) pbEl.style.display = 'none';
          toast(`✅ Downloaded: ${prog.filename}`, 'success');
          updateDownloadBadge();
          updateStats();
        } else if (prog.status === 'error') {
          clearInterval(interval);
          if (btn) { btn.classList.add('error'); btn.textContent = '❌ Error'; }
          toast('❌ ' + (prog.error || 'Download failed'), 'error');
        }
      } catch (_) { clearInterval(interval); }
    }, 1200);
  }

  // ── Downloads view ─────────────────────────────────────────────────────────
  function bindDownloadActions() {
    $('btnRefreshDl').addEventListener('click', loadDownloads);
  }

  async function loadDownloads() {
    try {
      const d = await api('/api/downloads');
      S.downloads = d.downloads || [];
      renderDownloads(S.downloads);
      updateDownloadBadge();
    } catch (_) {}
  }

  function renderDownloads(files) {
    const list  = $('dlList');
    const empty = $('dlEmpty');
    if (!files.length) {
      list.innerHTML = '';
      list.appendChild(empty);
      empty.style.display = 'flex';
      return;
    }
    empty.style.display = 'none';
    [...list.children].forEach(c => { if (c !== empty) c.remove(); });

    files.forEach(f => {
      const ext = (f.ext || 'file').toLowerCase();
      const icon = FILE_ICONS[ext] || '📄';
      const row = el('div', 'dl-item');
      row.innerHTML = `
        <div class="dl-icon">${icon}</div>
        <div class="dl-info">
          <div class="dl-name">${esc(f.filename)}</div>
          <div class="dl-meta">📦 ${f.size_mb} MB &nbsp;•&nbsp; .${esc(f.ext || 'file')}</div>
        </div>
        <div class="dl-btns">
          <a class="btn-save-dl" href="/api/file/${encodeURIComponent(f.filename)}" download title="Save to Computer">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7,10 12,15 17,10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Save
          </a>
          <button class="btn-del-dl" data-fn="${esc(f.filename)}" title="Delete">🗑️</button>
        </div>`;
      row.querySelector('.btn-del-dl').addEventListener('click', () => deleteDownload(f.filename, row));
      list.appendChild(row);
    });
  }

  async function deleteDownload(filename, rowEl) {
    if (!confirm(`Delete "${filename}"?`)) return;
    try {
      await api(`/api/file/${encodeURIComponent(filename)}`, 'DELETE');
      rowEl.remove();
      toast('🗑️ Deleted', 'info');
      updateDownloadBadge();
    } catch (e) {
      toast('❌ ' + e.message, 'error');
    }
  }

  function updateDownloadBadge() {
    fetch('/api/downloads')
      .then(r => r.json())
      .then(d => {
        const count = (d.downloads || []).length;
        const badge = $('dlBadge');
        badge.textContent = count;
        badge.style.display = count ? 'flex' : 'none';
      }).catch(() => {});
  }

  // ── Cache view ─────────────────────────────────────────────────────────────
  function bindCacheActions() {
    $('btnClearCache').addEventListener('click', async () => {
      if (!confirm('Clear all cache? This will not delete downloaded files.')) return;
      await api('/api/cache/clear', 'DELETE');
      toast('🗑️ Cache cleared', 'info');
      loadCacheStats();
    });
  }

  async function loadCacheStats() {
    try {
      const d = await api('/api/cache/stats');
      $('ccEmailsCached').textContent = d.emails_cached ?? 0;
      $('ccDlCached').textContent     = d.downloads_cached ?? 0;
      $('ccEmailHits').textContent    = d.email_hits ?? 0;
      $('ccEmailMisses').textContent  = d.email_misses ?? 0;
      $('ccDlHits').textContent       = d.download_hits ?? 0;
      $('ccDlMisses').textContent     = d.download_misses ?? 0;
      $('ccTotalMb').textContent      = d.total_cached_mb ?? 0;
      $('statHits').textContent = (d.email_hits ?? 0) + (d.download_hits ?? 0);
    } catch (_) {}
  }

  // ── Sidebar stats ──────────────────────────────────────────────────────────
  function updateStats() {
    S.stats.emails = S.emails.length;
    S.stats.urls   = S.emails.reduce((a, e) => a + (e.url_count || 0), 0);
    $('statEmails').textContent = S.stats.emails;
    $('statUrls').textContent   = S.stats.urls;
    loadCacheStats();
    fetch('/api/downloads').then(r => r.json()).then(d => {
      $('statFiles').textContent = (d.downloads || []).length;
    }).catch(() => {});
  }

  // ── API helper ─────────────────────────────────────────────────────────────
  async function api(path, method = 'GET', body) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body !== undefined) opts.body = JSON.stringify(body);
    const resp = await fetch(path, opts);
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || `HTTP ${resp.status}`);
    return data;
  }

  // ── Toast ──────────────────────────────────────────────────────────────────
  let _toastTimer;
  function toast(msg, type = 'info') {
    const t = $('toast');
    t.textContent = msg;
    t.className = `toast ${type} show`;
    clearTimeout(_toastTimer);
    _toastTimer = setTimeout(() => t.classList.remove('show'), 3500);
  }

  // ── Escape ─────────────────────────────────────────────────────────────────
  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

})();
