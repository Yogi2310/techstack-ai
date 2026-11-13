const canvas = document.getElementById('workoutCanvas');
const ctx = canvas.getContext('2d');

// State Variables
let targetReps = 6;
let durationSecs = 10;
let speedMult = 1.0;
let bgContrast = 0.45;
let timerStart = null;
let animationFrameId = null;

let isRecording = false;
let mediaRecorder = null;
let recordedChunks = [];
let recordStartTime = 0;

// Text overlays
let textTitle = "PERFECT PUSHUPS";
let textTip = "KEEP BACK STRAIGHT & TUCK ELBOWS";
let textHandle = "@CYBERFITNESS";

// Scaling logic
function resizeCanvas() {
  // Always lock resolution to standard vertical HD (1080 x 1920)
  canvas.width = 1080;
  canvas.height = 1920;
  
  // Calculate scaled height based on screen size
  const parent = document.getElementById('previewShell');
  const parentHeight = parent.clientHeight || 720;
  const scale = parentHeight / 1920;
  
  canvas.style.width = (1080 * scale) + 'px';
  canvas.style.height = (1920 * scale) + 'px';
}

// ── Event Presets Setup ──
const PRESETS = {
  pushup: {
    title: 'PERFECT PUSHUPS',
    tip: 'KEEP BACK STRAIGHT & TUCK ELBOWS',
    reps: 6,
    duration: 10,
    speed: 1.0,
    bpm: 124
  },
  squat: {
    title: 'DEEP SQUATS',
    tip: 'LOWER HIPS PAST KNEES & KEEP CHEST UP',
    reps: 5,
    duration: 10,
    speed: 1.0,
    bpm: 118
  },
  pullup: {
    title: 'STRICT PULLUPS',
    tip: 'CHIN ABOVE BAR & CONTROL THE DESCENT',
    reps: 4,
    duration: 12,
    speed: 0.8,
    bpm: 128
  },
  curl: {
    title: 'BICEP PEAK CURLS',
    tip: 'KEEP ELBOWS LOCKED & SQUEEZE BICEPS',
    reps: 6,
    duration: 10,
    speed: 1.2,
    bpm: 130
  },
  plank: {
    title: 'ABS PLANK HOVER',
    tip: 'ENGAGE CORE & DO NOT LET HIPS SAG',
    reps: 1,
    duration: 10,
    speed: 1.0,
    bpm: 120
  },
  deadlift: {
    title: 'BARBELL DEADLIFT',
    tip: 'DRIVE THROUGH HEELS & KEEP BACK FLAT',
    reps: 5,
    duration: 12,
    speed: 0.9,
    bpm: 116
  },
  shoulderpress: {
    title: 'OVERHEAD PRESS',
    tip: 'PRESS STRAIGHT UP & LOCK OUT ARMS',
    reps: 6,
    duration: 10,
    speed: 1.0,
    bpm: 122
  },
  lunge: {
    title: 'WALKING LUNGES',
    tip: 'FRONT KNEE OVER ANKLE & DROP BACK KNEE',
    reps: 6,
    duration: 12,
    speed: 0.9,
    bpm: 118
  },
  crunch: {
    title: 'AB CRUNCHES',
    tip: 'CURL SHOULDERS UP & SQUEEZE ABS',
    reps: 8,
    duration: 10,
    speed: 1.3,
    bpm: 126
  },
  jumpingjack: {
    title: 'JUMPING JACKS',
    tip: 'FULL ARM EXTENSION & LAND SOFT',
    reps: 10,
    duration: 10,
    speed: 1.5,
    bpm: 140
  },
  mountainclimber: {
    title: 'MOUNTAIN CLIMBERS',
    tip: 'KEEP HIPS LOW & DRIVE KNEES FAST',
    reps: 10,
    duration: 10,
    speed: 1.6,
    bpm: 145
  },
  tricepdip: {
    title: 'BENCH TRICEP DIPS',
    tip: 'LOWER UNTIL 90° BEND & PRESS UP',
    reps: 6,
    duration: 10,
    speed: 1.0,
    bpm: 124
  },
  lateralraise: {
    title: 'LATERAL RAISES',
    tip: 'RAISE TO SHOULDER HEIGHT & CONTROL DOWN',
    reps: 7,
    duration: 10,
    speed: 1.1,
    bpm: 120
  },
  bentoverrow: {
    title: 'BENT-OVER ROWS',
    tip: 'SQUEEZE SHOULDER BLADES & PULL TO WAIST',
    reps: 6,
    duration: 10,
    speed: 1.0,
    bpm: 122
  },
  jumpsquat: {
    title: 'EXPLOSIVE JUMP SQUATS',
    tip: 'SQUAT DEEP THEN EXPLODE UPWARD',
    reps: 6,
    duration: 10,
    speed: 1.2,
    bpm: 138
  }
};

function selectPreset(presetKey) {
  // Toggle active preset button class
  document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById(`btn-${presetKey}`).classList.add('active');
  
  // Load settings
  const config = PRESETS[presetKey];
  
  document.getElementById('inp-title').value = config.title;
  document.getElementById('inp-tip').value = config.tip;
  
  document.getElementById('inp-duration').value = config.duration;
  document.getElementById('inp-reps').value = config.reps;
  document.getElementById('inp-speed').value = Math.round(config.speed * 10);
  document.getElementById('inp-bpm').value = config.bpm;
  
  // Update state & UI
  animator.setExercise(presetKey);
  syncStateFromUI();
  
  // Sound play on change
  audioSynth.playTick();
}

function syncStateFromUI() {
  textTitle = document.getElementById('inp-title').value.toUpperCase();
  textTip = document.getElementById('inp-tip').value.toUpperCase();
  textHandle = document.getElementById('inp-handle').value.toUpperCase();
  
  bgContrast = parseInt(document.getElementById('rng-bg').value) / 100;
  document.getElementById('val-bg').textContent = Math.round(bgContrast * 100) + '%';
  
  durationSecs = parseInt(document.getElementById('inp-duration').value);
  document.getElementById('val-duration').textContent = durationSecs + 's';
  
  targetReps = parseInt(document.getElementById('inp-reps').value);
  document.getElementById('val-reps').textContent = targetReps;
  
  const rawSpeed = parseInt(document.getElementById('inp-speed').value);
  speedMult = rawSpeed / 10;
  document.getElementById('val-speed').textContent = speedMult.toFixed(1) + 'x';
  
  const bpm = parseInt(document.getElementById('inp-bpm').value);
  document.getElementById('val-bpm').textContent = bpm;
  
  const mVol = parseInt(document.getElementById('inp-music-vol').value) / 100;
  document.getElementById('val-music-vol').textContent = Math.round(mVol * 100) + '%';
  
  const sVol = parseInt(document.getElementById('inp-sfx-vol').value) / 100;
  document.getElementById('val-sfx-vol').textContent = Math.round(sVol * 100) + '%';
  
  // Apply values to models
  audioSynth.setBpm(bpm);
  audioSynth.setVolumes(mVol, sVol);
}

function updateText() { syncStateFromUI(); }
function updateAesthetics() { syncStateFromUI(); }
function updateTiming() { syncStateFromUI(); }
function updateAudio() { syncStateFromUI(); }

function changeTheme(swatch) {
  document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
  swatch.classList.add('active');
  const color = swatch.dataset.color;
  animator.setGlowColor(color);
  
  // Apply root custom property for UI coherence
  document.documentElement.style.setProperty('--active-glow', color);
  audioSynth.playTick();
}

// ── Drawing Layout Overlays on Canvas ──
function drawLayoutOverlays(time, activeProgress, currentRep) {
  const w = canvas.width;
  const h = canvas.height;
  
  // 1. Dark vignette overlays for text legibility
  ctx.save();
  const topGrad = ctx.createLinearGradient(0, 0, 0, h * 0.22);
  topGrad.addColorStop(0, 'rgba(0,0,0,0.85)');
  topGrad.addColorStop(1, 'transparent');
  ctx.fillStyle = topGrad;
  ctx.fillRect(0, 0, w, h * 0.22);

  const bottomGrad = ctx.createLinearGradient(0, h * 0.75, 0, h);
  bottomGrad.addColorStop(0, 'transparent');
  bottomGrad.addColorStop(1, 'rgba(0,0,0,0.9)');
  ctx.fillStyle = bottomGrad;
  ctx.fillRect(0, h * 0.75, w, h * 0.25);
  ctx.restore();

  // 2. HEADER TEXT (Space Grotesk style)
  ctx.save();
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  // Outer text shadow glow
  ctx.shadowColor = animator.glowColor;
  ctx.shadowBlur = 15;
  ctx.fillStyle = '#ffffff';
  ctx.font = `900 80px ${animator.glowColor === '#facc15' ? 'Space Grotesk' : 'Outfit'}`;
  ctx.fillText(textTitle, w/2, h * 0.12);
  ctx.restore();

  // 3. RETENTION TIMER PROGRESS BAR (Horizontal, top edge)
  ctx.save();
  const pct = Math.min(1.0, time / durationSecs);
  ctx.fillStyle = 'rgba(255,255,255,0.06)';
  ctx.fillRect(0, 0, w, 15);
  ctx.fillStyle = animator.glowColor;
  ctx.shadowColor = animator.glowColor;
  ctx.shadowBlur = 10;
  ctx.fillRect(0, 0, w * pct, 15);
  ctx.restore();

  // 4. REP DIAL DISPLAY (Premium circle overlay, top-left)
  ctx.save();
  const dialX = 160;
  const dialY = 260;
  const dialR = 85;
  
  // Backdrop
  ctx.shadowColor = 'rgba(0,0,0,0.5)';
  ctx.shadowBlur = 20;
  ctx.fillStyle = 'rgba(12, 12, 18, 0.75)';
  ctx.strokeStyle = 'rgba(255,255,255,0.08)';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(dialX, dialY, dialR, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();
  
  // Progress Ring
  const repProgress = animator.activeExercise === 'plank' ? pct : activeProgress;
  ctx.strokeStyle = animator.glowColor;
  ctx.shadowColor = animator.glowColor;
  ctx.shadowBlur = 8;
  ctx.lineWidth = 6;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.arc(dialX, dialY, dialR, -Math.PI / 2, -Math.PI / 2 + (repProgress * Math.PI * 2));
  ctx.stroke();
  
  // Texts inside ring
  ctx.shadowBlur = 0;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  if (animator.activeExercise === 'plank') {
    ctx.fillStyle = '#ffffff';
    ctx.font = '800 36px Outfit';
    ctx.fillText('HOLD', dialX, dialY - 12);
    ctx.fillStyle = varColorText();
    ctx.font = '700 24px Outfit';
    ctx.fillText(Math.round(pct * 100) + '%', dialX, dialY + 22);
  } else {
    ctx.fillStyle = '#ffffff';
    ctx.font = '800 48px Outfit';
    ctx.fillText(currentRep, dialX, dialY - 10);
    ctx.fillStyle = varColorText();
    ctx.font = '600 22px Outfit';
    ctx.fillText(`OF ${targetReps}`, dialX, dialY + 24);
  }
  ctx.restore();

  // 5. INSTRUCTION BOX (Bottom Glassmorphic Pill)
  ctx.save();
  const boxW = w * 0.86;
  const boxH = 140;
  const boxX = (w - boxW) / 2;
  const boxY = h * 0.81;
  const radius = 24;
  
  // Pill shadow and backfill
  ctx.shadowColor = 'rgba(0,0,0,0.6)';
  ctx.shadowBlur = 30;
  ctx.fillStyle = 'rgba(10, 10, 15, 0.85)';
  
  // Draw rounded rect
  ctx.beginPath();
  ctx.moveTo(boxX + radius, boxY);
  ctx.lineTo(boxX + boxW - radius, boxY);
  ctx.quadraticCurveTo(boxX + boxW, boxY, boxX + boxW, boxY + radius);
  ctx.lineTo(boxX + boxW, boxY + boxH - radius);
  ctx.quadraticCurveTo(boxX + boxW, boxY + boxH, boxX + boxW - radius, boxY + boxH);
  ctx.lineTo(boxX + radius, boxY + boxH);
  ctx.quadraticCurveTo(boxX, boxY + boxH, boxX, boxY + boxH - radius);
  ctx.lineTo(boxX, boxY + radius);
  ctx.quadraticCurveTo(boxX, boxY, boxX + radius, boxY);
  ctx.fill();
  
  // Glowing left border tag
  ctx.fillStyle = animator.glowColor;
  ctx.shadowColor = animator.glowColor;
  ctx.shadowBlur = 8;
  ctx.beginPath();
  ctx.moveTo(boxX, boxY + radius);
  ctx.quadraticCurveTo(boxX, boxY, boxX + radius, boxY);
  ctx.lineTo(boxX + 16, boxY);
  ctx.lineTo(boxX, boxY + 40);
  ctx.fill();
  
  // Text inside Pill
  ctx.shadowBlur = 0;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  // Primary Form Tip
  ctx.fillStyle = '#ffffff';
  ctx.font = '800 36px Outfit';
  ctx.fillText(textTip, w/2, boxY + boxH * 0.5);
  ctx.restore();

  // 6. WATERMARK / HANDLE (Bottom Center)
  ctx.save();
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = 'rgba(255,255,255,0.25)';
  ctx.font = '700 28px Space Grotesk';
  ctx.fillText(textHandle, w/2, h * 0.94);
  ctx.restore();
}

function varColorText() {
  return animator.glowColor === '#facc15' ? '#f59e0b' : animator.glowColor;
}

// ── Continuous Loop ──
let lastRepCount = 0;
let lastTickCount = 0;

function drawLoop(timestamp) {
  if (!timerStart) timerStart = timestamp;
  
  // Calculate relative playback time (affected by Speed multiplier)
  let elapsedMs = (timestamp - timerStart) * speedMult;
  let elapsedSecs = elapsedMs / 1000;
  
  // Handle stopping loops
  if (elapsedSecs >= durationSecs) {
    if (isRecording) {
      stopExport();
      return;
    } else {
      // Loop preview around
      timerStart = timestamp;
      elapsedSecs = 0;
      lastRepCount = 0;
      lastTickCount = 0;
    }
  }

  // Set shared time for core calculations
  timeSecs = elapsedSecs;

  // Clear Canvas with premium dark overlay gradient
  ctx.save();
  const bgGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
  bgGrad.addColorStop(0, '#040407');
  bgGrad.addColorStop(0.5, '#07070b');
  bgGrad.addColorStop(1, '#020204');
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // Draw glowing dark background radial tint
  const rad = ctx.createRadialGradient(canvas.width/2, canvas.height*0.55, 100, canvas.width/2, canvas.height*0.55, 800);
  rad.addColorStop(0, animator.glowColor + '08'); // low-glow
  rad.addColorStop(1, 'transparent');
  ctx.fillStyle = rad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.restore();

  // Exercise Animation Progress Calculations
  const repDuration = durationSecs / targetReps;
  const activeProgress = (elapsedSecs % repDuration) / repDuration; // 0.0 to 1.0 within rep
  const currentRep = Math.floor(elapsedSecs / repDuration);

  // Trigger sound effect when rep count advances
  if (animator.activeExercise !== 'plank' && currentRep > lastRepCount && currentRep <= targetReps) {
    audioSynth.playRepChime();
    lastRepCount = currentRep;
  }
  
  // Metronome tick sound on final 3 seconds
  const remainingSecs = Math.ceil(durationSecs - elapsedSecs);
  if (remainingSecs <= 3 && remainingSecs > 0) {
    if (remainingSecs !== lastTickCount) {
      audioSynth.playTick();
      lastTickCount = remainingSecs;
    }
  }

  // Draw Character Skeleton
  animator.render(ctx, elapsedSecs, activeProgress, elapsedSecs / durationSecs);

  // Draw Layout Text & Overlays
  drawLayoutOverlays(elapsedSecs, activeProgress, currentRep);

  // Loop
  animationFrameId = requestAnimationFrame(drawLoop);
}

// ── Export Recording Engine ──
function startExport() {
  if (isRecording) return;
  
  // Initialize Synthesizer context on user interaction
  audioSynth.init();
  audioSynth.startBeat();
  
  isRecording = true;
  recordedChunks = [];
  
  // Lock interface during recording
  document.getElementById('btn-export').disabled = true;
  document.getElementById('record-bar').classList.add('active');
  
  // Extract output streams
  const canvasStream = canvas.captureStream(30);
  const audioStream = audioSynth.getAudioStream();
  
  // Combine visual track and audio track
  const combinedStream = new MediaStream([
    canvasStream.getVideoTracks()[0],
    audioStream.getAudioTracks()[0]
  ]);
  
  // Setup recorder
  let options = { mimeType: 'video/webm;codecs=vp9,opus' };
  if (!MediaRecorder.isTypeSupported(options.mimeType)) {
    options = { mimeType: 'video/webm;codecs=vp8,opus' };
  }
  
  mediaRecorder = new MediaRecorder(combinedStream, options);
  mediaRecorder.ondataavailable = (event) => {
    if (event.data && event.data.size > 0) {
      recordedChunks.push(event.data);
    }
  };
  
  mediaRecorder.onstop = () => {
    // Generate blob and download
    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `CyberFit-${animator.activeExercise}-${Date.now()}.webm`;
    a.click();
    URL.revokeObjectURL(url);
    
    // Reset buttons
    document.getElementById('btn-export').disabled = false;
    document.getElementById('record-bar').classList.remove('active');
    
    // Stop beat synth
    audioSynth.stopBeat();
    
    // Restart preview
    timerStart = null;
    animationFrameId = requestAnimationFrame(drawLoop);
  };
  
  // Start recorder
  mediaRecorder.start(100);
  recordStartTime = performance.now();
  
  // Reset preview cycle to sync timing
  timerStart = performance.now();
  lastRepCount = 0;
  lastTickCount = 0;
  
  if (animationFrameId) cancelAnimationFrame(animationFrameId);
  animationFrameId = requestAnimationFrame(recordProgressLoop);
}

function recordProgressLoop(timestamp) {
  const elapsedMs = timestamp - recordStartTime;
  const elapsedSecs = elapsedMs / 1000;
  
  // Update export progress bar
  const pct = Math.min(1.0, elapsedSecs / durationSecs);
  document.getElementById('record-text').textContent = `Exporting Short: ${elapsedSecs.toFixed(1)}s / ${durationSecs}s`;
  document.getElementById('record-fill').style.width = (pct * 100) + '%';
  
  // Draw standard frames
  drawLoop(timestamp);
}

function stopExport() {
  if (!isRecording) return;
  isRecording = false;
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }
}

// ── Startup ──
window.onload = () => {
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
  
  // Set default preset
  selectPreset('pushup');
  
  // Trigger rendering loop
  animationFrameId = requestAnimationFrame(drawLoop);
};

// ── Diagnostics & Self-Test Suite ──
function runDiagnostics() {
  const resultsDiv = document.getElementById('test-results');
  resultsDiv.style.display = 'block';
  resultsDiv.innerHTML = '<div style="color: var(--text-muted);">Running test suite...</div>';
  
  const tests = [
    {
      name: 'Canvas Context Test',
      run: () => {
        if (!canvas || !ctx) throw new Error('Canvas or Context not initialized');
        return 'Canvas 2D Context OK';
      }
    },
    {
      name: 'Exercise Presets Test',
      run: () => {
        const exercises = ['pushup', 'squat', 'pullup', 'curl', 'plank'];
        for (const ex of exercises) {
          selectPreset(ex);
          if (animator.activeExercise !== ex) throw new Error(`Failed to activate preset: ${ex}`);
        }
        selectPreset('pushup'); // restore default
        return 'All 5 exercise presets configured correctly';
      }
    },
    {
      name: 'Audio Synthesizer Test',
      run: () => {
        audioSynth.init();
        if (!audioSynth.ctx || !audioSynth.destNode) throw new Error('AudioContext failed to initialize');
        return 'Web Audio API context created';
      }
    },
    {
      name: 'MediaRecorder Support Test',
      run: () => {
        if (typeof MediaRecorder === 'undefined') throw new Error('MediaRecorder API not supported in this browser');
        const canvasStream = canvas.captureStream(30);
        const audioStream = audioSynth.getAudioStream();
        const combined = new MediaStream([
          canvasStream.getVideoTracks()[0],
          audioStream.getAudioTracks()[0]
        ]);
        let options = { mimeType: 'video/webm;codecs=vp9,opus' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
          options = { mimeType: 'video/webm;codecs=vp8,opus' };
        }
        const rec = new MediaRecorder(combined, options);
        if (!rec) throw new Error('Failed to instantiate MediaRecorder');
        return `MediaRecorder supported (${options.mimeType})`;
      }
    },
    {
      name: 'Skeletal Render Test',
      run: () => {
        animator.render(ctx, 1.5, 0.5, 0.5);
        drawLayoutOverlays(1.5, 0.5, 1);
        
        const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        let hasPixels = false;
        for (let i = 0; i < imgData.data.length; i += 1000) {
          if (imgData.data[i + 3] > 0 && (imgData.data[i] > 0 || imgData.data[i+1] > 0 || imgData.data[i+2] > 0)) {
            hasPixels = true;
            break;
          }
        }
        if (!hasPixels) throw new Error('Canvas render is completely blank or transparent');
        return 'Mannequin skeleton rendered successfully on canvas';
      }
    },
    {
      name: 'UI State Synchronization Test',
      run: () => {
        const inpTitle = document.getElementById('inp-title');
        const oldVal = inpTitle.value;
        inpTitle.value = 'DIAGNOSTIC TEST';
        syncStateFromUI();
        if (textTitle !== 'DIAGNOSTIC TEST') throw new Error('UI text state failed to sync');
        inpTitle.value = oldVal;
        syncStateFromUI();
        return 'Two-way state synchronization OK';
      }
    }
  ];

  resultsDiv.innerHTML = '';
  let failed = 0;
  tests.forEach((t, i) => {
    const item = document.createElement('div');
    item.style.padding = '4px 0';
    item.style.borderBottom = i < tests.length - 1 ? '1px solid rgba(255,255,255,0.03)' : 'none';
    item.style.display = 'flex';
    item.style.justifyContent = 'space-between';
    
    try {
      t.run();
      item.innerHTML = `<span style="color: var(--text-muted)">${t.name}</span> <span style="color: var(--neon-green)">✔ PASSED</span>`;
    } catch (e) {
      item.innerHTML = `<span style="color: var(--text-muted)">${t.name}</span> <span style="color: var(--neon-red)" title="${e.message}">✘ FAILED</span>`;
      failed++;
    }
    resultsDiv.appendChild(item);
  });
  
  const summary = document.createElement('div');
  summary.style.marginTop = '10px';
  summary.style.paddingTop = '8px';
  summary.style.borderTop = '1.5px solid var(--border-light)';
  summary.style.fontWeight = 'bold';
  summary.style.textAlign = 'center';
  
  if (failed === 0) {
    summary.innerHTML = '<span style="color: var(--neon-green)">All 6 Diagnostics Passed!</span>';
  } else {
    summary.innerHTML = `<span style="color: var(--neon-red)">${failed} test(s) failed.</span>`;
  }
  resultsDiv.appendChild(summary);
}
