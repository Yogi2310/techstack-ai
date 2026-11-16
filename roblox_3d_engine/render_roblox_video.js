const puppeteer = require('D:/Antigravity/Pro/agentic-code/projects/horror_shadow_titan_short/node_modules/puppeteer-core');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const ENGINE_DIR = 'D:\\Antigravity\\Pro\\roblox_3d_engine';
const HTML_FILE = `file:///${ENGINE_DIR.replace(/\\/g, '/')}/roblox_scene.html`;
const AUDIO_FILE = path.join(ENGINE_DIR, 'pilot_audio.wav');
const OUTPUT_VIDEO = 'D:\\Antigravity\\Pro\\Riyo_3D_Roblox_Series\\master_videos\\SHORT_7_Roblox_Eli_Golden_Cheese_Full_Motion.mp4';
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const WIDTH = 720;
const HEIGHT = 1280;
const FPS = 30;
const DURATION = 24.5;
const TOTAL_FRAMES = Math.floor(DURATION * FPS); // 735 frames

async function main() {
  console.log('='.repeat(60));
  console.log(`🚀 TaleBlox 3D Full-Motion Engine: Rendering ${TOTAL_FRAMES} frames @ ${FPS}fps...`);
  console.log(`Resolution: ${WIDTH}x${HEIGHT} (9:16 vertical Shorts)`);
  console.log(`Scene: ${HTML_FILE}`);
  console.log('='.repeat(60));

  const tempProfile = path.join(ENGINE_DIR, `temp_profile_${Date.now()}`);
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
  page.on('console', msg => console.log('PAGE:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err));
  await page.setViewport({ width: WIDTH, height: HEIGHT });

  console.log(`[1] Loading WebGL Roblox 3D scene...`);
  await page.goto(HTML_FILE, { waitUntil: 'load' });

  await page.waitForFunction(() => typeof window.renderFrameAtTime === 'function', { timeout: 15000 });
  console.log(`[2] Three.js Roblox R6 Rig & Physics system initialized!`);

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
    '-preset', 'fast',
    '-crf', '19',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    OUTPUT_VIDEO
  ]);

  ffmpeg.stderr.on('data', d => console.error(`FFmpeg: ${d}`));

  console.log(`[4] Rendering & piping animation frames...`);
  const startTime = Date.now();

  for (let f = 0; f < TOTAL_FRAMES; f++) {
    const t = f / FPS;

    await page.evaluate((timeSec) => {
      window.renderFrameAtTime(timeSec);
    }, t);

    const buffer = await page.screenshot({ type: 'jpeg', quality: 90 });
    ffmpeg.stdin.write(buffer);

    if (f % 60 === 0 || f === TOTAL_FRAMES - 1) {
      const pct = (((f + 1) / TOTAL_FRAMES) * 100).toFixed(1);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const fps = ((f + 1) / Math.max(0.1, (Date.now() - startTime) / 1000)).toFixed(1);
      console.log(`Progress: ${pct}% (${f + 1}/${TOTAL_FRAMES}) | Sim: ${t.toFixed(1)}s | Render speed: ${fps} fps | Elapsed: ${elapsed}s`);
    }
  }

  ffmpeg.stdin.end();

  await new Promise(resolve => ffmpeg.on('close', resolve));
  await browser.close();

  try {
    fs.rmSync(tempProfile, { recursive: true, force: true });
  } catch (e) {}

  const stats = fs.statSync(OUTPUT_VIDEO);
  const sizeMb = (stats.size / (1024 * 1024)).toFixed(2);
  console.log('\n' + '='.repeat(60));
  console.log(`✨ FULL-MOTION 3D ROBLOX VIDEO RENDERED 100% AUTONOMOUSLY!`);
  console.log(`Output: ${OUTPUT_VIDEO}`);
  console.log(`Size: ${sizeMb} MB | Duration: ${DURATION}s`);
  console.log('='.repeat(60));
}

main().catch(err => {
  console.error('Fatal render error:', err);
  process.exit(1);
});
