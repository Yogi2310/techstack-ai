class WorkoutAudioSynth {
  constructor() {
    this.ctx = null;
    this.destNode = null;
    
    // Master Gains
    this.musicGain = null;
    this.sfxGain = null;
    
    // Scheduler variables
    this.bpm = 124;
    this.isPlaying = false;
    this.nextNoteTime = 0.0;
    this.stepIndex = 0; // 16 steps per bar
    this.timerId = null;
    
    // Volumes (0.0 to 1.0)
    this.musicVolume = 0.4;
    this.sfxVolume = 0.6;
  }

  init() {
    if (this.ctx) return;
    
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContextClass();
    
    // MediaStream output destination for video recorder
    this.destNode = this.ctx.createMediaStreamDestination();
    
    // Setup gain nodes
    this.musicGain = this.ctx.createGain();
    this.sfxGain = this.ctx.createGain();
    
    this.musicGain.gain.setValueAtTime(this.musicVolume, this.ctx.currentTime);
    this.sfxGain.gain.setValueAtTime(this.sfxVolume, this.ctx.currentTime);
    
    // Connect Gains to both the hardware speakers (for preview) and the recorder stream
    this.musicGain.connect(this.ctx.destination);
    this.musicGain.connect(this.destNode);
    
    this.sfxGain.connect(this.ctx.destination);
    this.sfxGain.connect(this.destNode);
  }

  getAudioStream() {
    this.init();
    return this.destNode.stream;
  }

  setBpm(bpm) {
    this.bpm = Math.max(60, Math.min(200, bpm));
  }

  setVolumes(musicVol, sfxVol) {
    this.musicVolume = musicVol;
    this.sfxVolume = sfxVol;
    
    if (this.musicGain && this.ctx) {
      this.musicGain.gain.setValueAtTime(this.musicVolume, this.ctx.currentTime);
    }
    if (this.sfxGain && this.ctx) {
      this.sfxGain.gain.setValueAtTime(this.sfxVolume, this.ctx.currentTime);
    }
  }

  // ── Synthesized Instruments ──
  
  // 1. Kick Drum
  playKick(time) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    
    osc.connect(gain);
    gain.connect(this.musicGain);
    
    osc.frequency.setValueAtTime(150, time);
    // Sweep frequency down to 45Hz exponentially (classic punchy kick)
    osc.frequency.exponentialRampToValueAtTime(45, time + 0.12);
    
    gain.gain.setValueAtTime(1.0, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + 0.15);
    
    osc.start(time);
    osc.stop(time + 0.16);
  }

  // 2. Offbeat Synth Bass
  playBassNote(time, pitchHz, duration) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();
    
    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);
    
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(pitchHz, time);
    
    // Low pass filter envelope to make it warm/bouncy
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(300, time);
    filter.frequency.exponentialRampToValueAtTime(100, time + duration);
    
    gain.gain.setValueAtTime(0.8, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + duration);
    
    osc.start(time);
    osc.stop(time + duration + 0.05);
  }

  // 3. Hi-Hat (Synthesized via white noise burst)
  playHiHat(time) {
    if (!this.ctx) return;
    
    const bufferSize = this.ctx.sampleRate * 0.05; // Short 50ms burst
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    
    // Fill buffer with random white noise
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }
    
    const noiseSource = this.ctx.createBufferSource();
    noiseSource.buffer = buffer;
    
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.setValueAtTime(7000, time); // Cut out low-end noise
    
    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.3, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + 0.04);
    
    noiseSource.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);
    
    noiseSource.start(time);
    noiseSource.stop(time + 0.05);
  }

  // ── SFX Instruments ──

  // countdown tick metronome
  playTick() {
    this.init();
    if (!this.ctx || this.sfxVolume <= 0) return;
    
    const time = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    
    osc.connect(gain);
    gain.connect(this.sfxGain);
    
    osc.frequency.setValueAtTime(880, time); // A5 note
    gain.gain.setValueAtTime(0.7, time);
    gain.gain.exponentialRampToValueAtTime(0.01, time + 0.08);
    
    osc.start(time);
    osc.stop(time + 0.1);
  }

  // rep completed gong/buzzer
  playRepChime() {
    this.init();
    if (!this.ctx || this.sfxVolume <= 0) return;
    
    const time = this.ctx.currentTime;
    // Play a dual-tone chord (C5 + G5)
    [523.25, 783.99].forEach((pitch, i) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      
      osc.connect(gain);
      gain.connect(this.sfxGain);
      
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(pitch, time);
      
      gain.gain.setValueAtTime(0.4, time);
      gain.gain.exponentialRampToValueAtTime(0.01, time + 0.35);
      
      osc.start(time);
      osc.stop(time + 0.4);
    });
  }

  // workout complete chime arpeggio
  playSuccessChime() {
    this.init();
    if (!this.ctx || this.sfxVolume <= 0) return;
    
    const now = this.ctx.currentTime;
    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6 arpeggio
    
    notes.forEach((pitch, i) => {
      const time = now + i * 0.1;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      
      osc.connect(gain);
      gain.connect(this.sfxGain);
      
      osc.type = 'sine';
      osc.frequency.setValueAtTime(pitch, time);
      
      gain.gain.setValueAtTime(0.5, time);
      gain.gain.exponentialRampToValueAtTime(0.01, time + 0.25);
      
      osc.start(time);
      osc.stop(time + 0.3);
    });
  }

  // ── Beat Loop Scheduler ──
  scheduler() {
    if (!this.isPlaying) return;
    
    while (this.nextNoteTime < this.ctx.currentTime + 0.1) {
      this.scheduleNextStep(this.stepIndex, this.nextNoteTime);
      
      // Advance step time
      const secondsPerBeat = 60.0 / this.bpm;
      const secondsPerStep = secondsPerBeat / 4.0; // 16th notes
      this.nextNoteTime += secondsPerStep;
      
      this.stepIndex = (this.stepIndex + 1) % 16;
    }
    
    this.timerId = setTimeout(() => this.scheduler(), 25);
  }

  scheduleNextStep(step, time) {
    // 16-step grid
    // Four-on-the-floor kick
    if (step === 0 || step === 4 || step === 8 || step === 12) {
      this.playKick(time);
    }
    
    // Bouncy house hi-hats on offbeats
    if (step === 2 || step === 6 || step === 10 || step === 14) {
      this.playHiHat(time);
    }
    
    // Offbeat bass line (driving rhythm)
    if (step === 2 || step === 6 || step === 10 || step === 14) {
      // Alternating root note (D1 = 36.7Hz, A1 = 55.0Hz)
      const isAlt = (step === 6 || step === 14);
      this.playBassNote(time, isAlt ? 55.0 : 73.4, 0.12);
    }
  }

  startBeat() {
    this.init();
    if (this.isPlaying) return;
    
    // Resume audio context if suspended (browser security)
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
    
    this.isPlaying = true;
    this.stepIndex = 0;
    this.nextNoteTime = this.ctx.currentTime + 0.05;
    this.scheduler();
  }

  stopBeat() {
    this.isPlaying = false;
    if (this.timerId) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
  }
}

const audioSynth = new WorkoutAudioSynth();
