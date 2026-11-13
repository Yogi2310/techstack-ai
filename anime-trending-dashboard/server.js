// AniTrend Download Server — powered by yt-dlp
// Run with: node server.js
// Runs on http://localhost:3001

import express from 'express';
import cors from 'cors';
import { spawn, exec } from 'child_process';
import path from 'path';
import fs from 'fs';
import os from 'os';

const app = express();
const PORT = 3001;

// Downloads go to user's Downloads folder
const DOWNLOADS_DIR = path.join(os.homedir(), 'Downloads', 'AniTrend');
if (!fs.existsSync(DOWNLOADS_DIR)) fs.mkdirSync(DOWNLOADS_DIR, { recursive: true });

app.use(cors());
app.use(express.json());
app.use('/downloads', express.static(DOWNLOADS_DIR));

// ─── GET /api/file/:filename — download file directly in browser ─────────
app.get('/api/file/:filename', (req, res) => {
  const safeName = path.basename(req.params.filename);
  const filePath = path.join(DOWNLOADS_DIR, safeName);
  if (fs.existsSync(filePath)) {
    res.download(filePath, safeName);
  } else {
    res.status(404).json({ error: 'File not found' });
  }
});

// ─── GET /api/info — get video metadata ────────────────────────────────────
app.get('/api/info', async (req, res) => {
  const { url } = req.query;
  if (!url) return res.status(400).json({ error: 'url is required' });

  const args = ['--dump-json', '--no-playlist', url];

  runYtDlp(args, (err, output) => {
    if (err) return res.status(500).json({ error: err.message, detail: err.stderr });
    try {
      const info = JSON.parse(output);
      res.json({
        id: info.id,
        title: info.title,
        thumbnail: info.thumbnail,
        duration: info.duration,
        uploader: info.uploader,
        view_count: info.view_count,
        like_count: info.like_count,
        upload_date: info.upload_date,
        webpage_url: info.webpage_url,
        formats: (info.formats || [])
          .filter(f => f.ext && f.height)
          .map(f => ({ format_id: f.format_id, ext: f.ext, height: f.height, fps: f.fps, filesize: f.filesize }))
          .sort((a, b) => (b.height || 0) - (a.height || 0))
          .slice(0, 8),
      });
    } catch {
      res.status(500).json({ error: 'Failed to parse yt-dlp output' });
    }
  });
});

// ─── GET /api/feed — fetch trending videos or shorts via yt-dlp ───────────
app.get('/api/feed', (req, res) => {
  const type = req.query.type || 'trending';
  const query = type === 'shorts'
    ? 'ytsearch12:anime edit shorts #animeshorts'
    : 'ytsearch12:anime amv fight scene trailer 2026';

  const proc = spawn('yt-dlp', ['--dump-json', '--no-playlist', query]);
  let stdout = '';
  proc.stdout.on('data', d => stdout += d);

  proc.on('close', (code) => {
    if (!stdout.trim()) return res.json([]);
    try {
      const items = stdout.trim().split('\n').filter(Boolean).map(line => {
        try {
          const info = JSON.parse(line);
          const isShort = type === 'shorts' || (info.duration && info.duration <= 60);
          return {
            id: info.id,
            platform: isShort ? 'shorts' : 'youtube',
            title: info.title,
            thumbnail: info.thumbnail || `https://i.ytimg.com/vi/${info.id}/hqdefault.jpg`,
            channelName: info.uploader || info.channel || '',
            views: info.view_count || 0,
            likes: info.like_count || 0,
            duration: formatSec(info.duration || 0),
            publishedAt: info.upload_date ? `${info.upload_date.slice(0,4)}-${info.upload_date.slice(4,6)}-${info.upload_date.slice(6,8)}` : '',
            url: info.webpage_url || `https://www.youtube.com/watch?v=${info.id}`,
            embedUrl: `https://www.youtube.com/embed/${info.id}`,
            description: info.description ? info.description.slice(0, 150) : '',
            source: isShort ? 'YouTube Shorts' : 'YouTube',
          };
        } catch { return null; }
      }).filter(Boolean);
      res.json(items);
    } catch { res.json([]); }
  });
  proc.on('error', () => res.json([]));
});

function formatSec(s) {
  if (!s) return '';
  const m = Math.floor(s / 60), sec = s % 60;
  return `${m}:${String(sec).padStart(2,'0')}`;
}

// ─── GET /api/search — search YouTube via yt-dlp ───────────────────────────
app.get('/api/search', (req, res) => {
  const { q } = req.query;
  if (!q) return res.status(400).json({ error: 'q is required' });

  const proc = spawn('yt-dlp', ['--dump-json', '--no-playlist', `ytsearch1:${q}`]);
  let stdout = '', stderr = '';
  proc.stdout.on('data', d => stdout += d);
  proc.stderr.on('data', d => stderr += d);
  proc.on('close', (code) => {
    if (code !== 0) return res.status(500).json({ error: stderr || 'yt-dlp search failed', code });
    try {
      const info = JSON.parse(stdout.trim());
      res.json({
        id: info.id,
        title: info.title,
        thumbnail: info.thumbnail,
        url: info.webpage_url || `https://www.youtube.com/watch?v=${info.id}`,
      });
    } catch { res.status(500).json({ error: 'Parse error' }); }
  });
  proc.on('error', (e) => res.status(500).json({ error: e.message }));
});

// ─── POST /api/download — download a video ────────────────────────────────
app.post('/api/download', (req, res) => {
  const { url, quality = '720', format = 'mp4' } = req.body;
  if (!url) return res.status(400).json({ error: 'url is required' });

  const safeTitle = `anitrend_${Date.now()}`;
  const outputTemplate = path.join(DOWNLOADS_DIR, `${safeTitle}.%(ext)s`);

  // Build yt-dlp args
  const args = [
    '--no-playlist',
    '-f', `best[height<=${quality}][ext=mp4]/best[height<=${quality}]/bestvideo[height<=${quality}]+bestaudio/best`,
    '--output', outputTemplate,
    '--progress',
    '--newline',
    url,
  ];

  console.log(`\n▶ Downloading: ${url}`);
  console.log(`  Quality: ${quality}p | Output: ${DOWNLOADS_DIR}\n`);

  const ytdlp = spawn('yt-dlp', args);
  let lastProgress = '';
  let finalFile = '';

  // Stream progress back via SSE if client wants, otherwise buffer
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  const send = (data) => res.write(`data: ${JSON.stringify(data)}\n\n`);

  ytdlp.stdout.on('data', (chunk) => {
    const line = chunk.toString().trim();
    if (!line) return;

    // Parse download progress lines
    const pctMatch = line.match(/(\d+\.?\d*)%/);
    const speedMatch = line.match(/at\s+([\d.]+\w+\/s)/);
    const etaMatch = line.match(/ETA\s+([\d:]+)/);
    const destMatch = line.match(/Destination:\s+(.+)/);
    const mergeMatch = line.match(/\[Merger\].*"(.+?)"/);

    if (destMatch) finalFile = destMatch[1];
    if (mergeMatch) finalFile = mergeMatch[1];

    if (pctMatch) {
      const progress = parseFloat(pctMatch[1]);
      lastProgress = `${progress.toFixed(1)}%`;
      send({ type: 'progress', progress, speed: speedMatch?.[1] || '', eta: etaMatch?.[1] || '' });
    } else if (line.includes('[download]') || line.includes('[ffmpeg]') || line.includes('[Merger]')) {
      send({ type: 'status', message: line.replace(/\[.*?\]\s*/, '') });
    }
    console.log(line);
  });

  ytdlp.stderr.on('data', (chunk) => {
    const line = chunk.toString().trim();
    if (line) { send({ type: 'warning', message: line }); console.error(line); }
  });

  let isFinished = false;

  ytdlp.on('close', (code) => {
    isFinished = true;
    if (code === 0) {
      // Find the actual downloaded file
      const files = fs.readdirSync(DOWNLOADS_DIR)
        .filter(f => f.startsWith(safeTitle))
        .map(f => path.join(DOWNLOADS_DIR, f));

      const file = files[0] || finalFile;
      const filename = file ? path.basename(file) : 'video.mp4';

      send({ type: 'done', success: true, filename, path: file, downloadsDir: DOWNLOADS_DIR });
      console.log(`\n✅ Done! Saved to: ${file || DOWNLOADS_DIR}`);
    } else {
      send({ type: 'done', success: false, error: `yt-dlp exited with code ${code}` });
    }
    res.end();
  });

  ytdlp.on('error', (err) => {
    isFinished = true;
    send({ type: 'done', success: false, error: err.message });
    res.end();
  });

  // Kill yt-dlp if client disconnects prematurely
  req.on('aborted', () => { if (!isFinished) { try { ytdlp.kill('SIGTERM'); } catch {} } });
});

// ─── GET /api/status ───────────────────────────────────────────────────────
app.get('/api/status', (req, res) => {
  // Check yt-dlp version
  exec('yt-dlp --version', (err, stdout) => {
    res.json({
      server: 'AniTrend Download Server',
      status: 'running',
      ytdlp: err ? 'not found' : stdout.trim(),
      downloadsDir: DOWNLOADS_DIR,
      port: PORT,
    });
  });
});

// ─── Helpers ───────────────────────────────────────────────────────────────
function runYtDlp(args, cb) {
  const proc = spawn('yt-dlp', args);
  let stdout = '', stderr = '';
  proc.stdout.on('data', d => stdout += d);
  proc.stderr.on('data', d => stderr += d);
  proc.on('close', code => {
    if (code !== 0) cb(new Error(stderr || `Exit ${code}`), null);
    else cb(null, stdout.trim());
  });
  proc.on('error', cb);
}

// ─── Start ─────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log('\n╔═══════════════════════════════════════╗');
  console.log('║   AniTrend Download Server            ║');
  console.log(`║   http://localhost:${PORT}               ║`);
  console.log('║   Powered by yt-dlp ✅                ║');
  console.log(`║   Downloads → ${DOWNLOADS_DIR.slice(0, 24)}...  ║`);
  console.log('╚═══════════════════════════════════════╝\n');
});
