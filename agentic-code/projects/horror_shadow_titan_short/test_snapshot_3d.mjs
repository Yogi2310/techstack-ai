import puppeteer from 'puppeteer-core';
import path from 'path';
import fs from 'fs';

const PROJECT_DIR = 'D:\\Antigravity\\Pro\\agentic-code\\projects\\horror_shadow_titan_short';
const HTML_FILE = `file:///${PROJECT_DIR.replace(/\\/g, '/')}/scene3d_cinematic.html?record=1`;
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const TEST_TIMES = [
  { time: 5.0, name: 'fix_act1_walking.png' },
  { time: 16.0, name: 'fix_act2_hermit_warning.png' },
  { time: 28.0, name: 'fix_act3_tremor_rising.png' },
  { time: 39.0, name: 'fix_act4_colossus_stomp.png' },
  { time: 50.0, name: 'fix_act5_screaming_sprint.png' }
];

async function main() {
  console.log('Testing updated 3D cinematic scene rendering...');
  const tempProfile = path.join(PROJECT_DIR, `temp_profile_snapfix_${Date.now()}`);
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
      '--window-size=720,1280'
    ]
  });

  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err));
  await page.setViewport({ width: 720, height: 1280 });

  console.log(`Navigating to ${HTML_FILE}...`);
  await page.goto(HTML_FILE, { waitUntil: 'load' });
  await page.waitForFunction(() => typeof window.renderFrameAtTime === 'function', { timeout: 15000 });

  for (const item of TEST_TIMES) {
    console.log(`Capturing frame at ${item.time}s (${item.name})...`);
    await page.evaluate((t) => window.renderFrameAtTime(t), item.time);
    const savePath = path.join(PROJECT_DIR, item.name);
    await page.screenshot({ path: savePath, type: 'png' });
    console.log(`Saved: ${savePath}`);
  }

  await browser.close();
  try { fs.rmSync(tempProfile, { recursive: true, force: true }); } catch (e) {}
  console.log('All updated test snapshots captured successfully!');
}

main().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
