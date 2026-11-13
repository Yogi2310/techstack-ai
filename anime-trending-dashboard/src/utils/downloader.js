// AniTrend Downloader — uses local yt-dlp server (server.js)
// Falls back to web-based options if server is not running

import { showToast } from './helpers.js';

let activeServer = 'http://localhost:3001';

// Check if local download server is running
export async function checkServer() {
  const hosts = ['http://localhost:3001', 'http://127.0.0.1:3001'];
  for (const host of hosts) {
    try {
      const res = await fetch(`${host}/api/status`, { signal: AbortSignal.timeout(2000) });
      if (res.ok) {
        const data = await res.json();
        activeServer = host;
        return { available: true, ytdlp: data.ytdlp, downloadsDir: data.downloadsDir };
      }
    } catch {}
  }
  return { available: false };
}

// Get video info before downloading
export async function getVideoInfo(url) {
  const res = await fetch(`${activeServer}/api/info?url=${encodeURIComponent(url)}`, {
    signal: AbortSignal.timeout(15000),
  });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}

// Search YouTube via local yt-dlp server
export async function searchYouTube(query) {
  const res = await fetch(`${activeServer}/api/search?q=${encodeURIComponent(query)}`, {
    signal: AbortSignal.timeout(12000),
  });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}

// Download with real-time progress via SSE
export function downloadWithProgress(url, quality = '720', callbacks = {}) {
  const { onProgress, onStatus, onDone, onError } = callbacks;

  fetch(`${activeServer}/api/download`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, quality }),
  }).then(async (res) => {
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Server error' }));
      onError?.(err.error || 'Download failed');
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const event = JSON.parse(line.slice(6));
          if (event.type === 'progress') onProgress?.(event);
          else if (event.type === 'status') onStatus?.(event.message);
          else if (event.type === 'warning') console.warn(event.message);
          else if (event.type === 'done') onDone?.(event);
        } catch {}
      }
    }
  }).catch(err => onError?.(err.message));
}

// Simple one-shot download (no progress tracking)
export async function downloadVideo(url, quality = '720') {
  const serverStatus = await checkServer();
  if (!serverStatus.available) {
    return { success: false, error: 'Download server not running', needsServer: true };
  }

  return new Promise((resolve) => {
    downloadWithProgress(url, quality, {
      onDone: (result) => resolve(result),
      onError: (err) => resolve({ success: false, error: err }),
    });
  });
}

// Open a web-based downloader as fallback
export function openWebDownloader(url, service = 'auto') {
  const services = {
    // Method: prepend "ss" to youtube.com → ssyoutube.com
    ssyt: (u) => u.replace('www.youtube.com', 'ssyoutube.com').replace('youtu.be/', 'ssyoutube.com/'),
    // y2mate
    y2mate: (u) => `https://www.y2mate.com/youtube/${extractYtId(u)}`,
    // loader.to
    loader: (u) => `https://loader.to/en25/${encodeURIComponent(u)}`,
    // SaveFrom.net
    savefrom: (u) => `https://en.savefrom.net/1-youtube-video-downloader/?url=${encodeURIComponent(u)}`,
  };

  const ytId = extractYtId(url);
  let target;

  if (service === 'auto') {
    // Try ssyoutube trick first (cleanest UX)
    if (url.includes('youtu')) {
      target = url
        .replace('https://www.youtube.com/watch?v=', 'https://ssyoutube.com/watch?v=')
        .replace('https://youtu.be/', 'https://ssyoutube.com/watch?v=');
    } else {
      target = `https://loader.to/en25/${encodeURIComponent(url)}`;
    }
  } else {
    target = services[service]?.(url) || url;
  }

  window.open(target, '_blank');
  return { opened: true, service: service === 'auto' ? 'ssyoutube' : service, url: target };
}

// Open cobalt.tools directly and copy the link to clipboard for convenience
export async function openCobaltDirect(url) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(url);
      showToast('Link copied to clipboard! Paste it in cobalt.tools.', 'success');
    } else {
      showToast('Opening cobalt.tools...', 'info');
    }
  } catch (err) {
    console.warn('Could not copy link to clipboard:', err);
    showToast('Opening cobalt.tools...', 'info');
  }
  window.open('https://cobalt.tools', '_blank');
}

function extractYtId(url) {
  const match = url?.match(/(?:v=|youtu\.be\/|embed\/)([a-zA-Z0-9_-]{11})/);
  return match?.[1] || '';
}
