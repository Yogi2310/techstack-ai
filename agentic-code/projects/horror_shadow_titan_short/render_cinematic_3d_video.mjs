import puppeteer from 'puppeteer-core';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';

const PROJECT_DIR = 'D:\\Antigravity\\Pro\\agentic-code\\projects\\horror_shadow_titan_short';
const HTML_FILE = `file:///${PROJECT_DIR.replace(/\\/g, '/')}/scene3d_cinematic.html?record=1`;
const AUDIO_FILE = path.join(PROJECT_DIR, 'audio', 'horror_master_audio.wav');
const OUTPUT_VIDEO = path.join(PROJECT_DIR, 'THE_MIDNIGHT_COLOSSUS_FULL_MOTION_3D.mp4');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const WIDTH = 720;
const HEIGHT = 1280;
const FPS = 24;
const DURATION = 55.60;
const TOTAL_FRAMES = Math.floor(DURATION * FPS); // 1334 frames

async function main() {
  console.log(`[1] Launching Headless Chrome for Full-Motion 3D Character Animation (${WIDTH}x${HEIGHT} @ ${FPS}fps)...`);

  const tempProfile = path.join(PROJECT_DIR, `temp_profile_full3d_${Date.now()}`);
  fs.mkdirSync(tempProfile, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: true,
    userDataDir: tempProfile,
    args: [
      '--use-gl=angle',
      '--use-angle=d3d11',
      '--enable-webgl',
      '--allow-file-access-from-files',
      '--disable-web-security',
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      `--window-size=${WIDTH},${HEIGHT}`
    ]
  });

  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err));
  await page.setViewport({ width: WIDTH, height: HEIGHT });

  console.log(`[2] Loading 3D Cinematic Scene: ${HTML_FILE}`);
  await page.goto(HTML_FILE, { waitUntil: 'load' });

  // Wait for 3D renderer function to be ready
  await page.waitForFunction(() => typeof window.renderFrameAtTime === 'function', { timeout: 15000 });
  console.log(`[2.1] 3D WebGL engine, character rigs & procedural shaders initialized!`);

  console.log(`[3] Spawning FFmpeg encoder to ${OUTPUT_VIDEO}...`);
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-loglevel', 'error',
    '-f', 'image2pipe',
    '-vcodec', 'mjpeg',
    '-r', String(FPS),
    '-i', '-',
    '-i', AUDIO_FILE,
    '-c:v', 'libx264',
    '-preset', 'veryfast',
    '-crf', '20',
    '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    OUTPUT_VIDEO
  ]);

  ffmpeg.stderr.on('data', (d) => console.error(`FFmpeg error: ${d}`));

  console.log(`[4] Rendering & Capturing ${TOTAL_FRAMES} frames of continuous character movement...`);
  const startTime = Date.now();

  for (let f = 0; f < TOTAL_FRAMES; f++) {
    const t = f / FPS;

    // Advance 3D animation simulation to time t
    await page.evaluate((timeSec) => {
      window.renderFrameAtTime(timeSec);
    }, t);

    // Capture screenshot buffer as JPEG
    const buffer = await page.screenshot({ type: 'jpeg', quality: 92 });
    ffmpeg.stdin.write(buffer);

    if (f % 120 === 0 || f === TOTAL_FRAMES - 1) {
      const pct = (((f + 1) / TOTAL_FRAMES) * 100).toFixed(1);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const fps = ((f + 1) / ((Date.now() - startTime) / 1000)).toFixed(1);
      console.log(`Progress: ${pct}% (${f + 1}/${TOTAL_FRAMES} frames) | Sim time: ${t.toFixed(1)}s | Speed: ${fps} fps | Elapsed: ${elapsed}s`);
    }
  }

  ffmpeg.stdin.end();

  await new Promise((resolve) => ffmpeg.on('close', resolve));
  await browser.close();

  try {
    fs.rmSync(tempProfile, { recursive: true, force: true });
  } catch (e) {}

  const stats = fs.statSync(OUTPUT_VIDEO);
  console.log(`[5] Video rendering completed successfully!`);
  console.log(`File: ${OUTPUT_VIDEO}`);
  console.log(`Size: ${(stats.size / (1024 * 1024)).toFixed(2)} MB`);
}

main().catch(err => {
  console.error('Fatal error during render:', err);
  process.exit(1);
});
