import os, wave, math, subprocess
import numpy as np

audio_dir = r"D:\Antigravity\Pro\agentic-code\projects\ai_agents_video\audio"
clips = [f"clip{i}.wav" for i in range(1, 7)]
bgm_file = os.path.join(audio_dir, "ambient_bgm.wav")
master_out = os.path.join(audio_dir, "master_audio.wav")

sr = 44100
pause_dur = 0.45  # 450ms pause between clips
timeline = []
current_time = 0.3  # 300ms lead

all_speech = []
lead_samples = int(current_time * sr)
all_speech.append(np.zeros(lead_samples, dtype=np.float32))

for i, c in enumerate(clips):
    path = os.path.join(audio_dir, c)
    with wave.open(path, 'r') as wf:
        n = wf.getnframes()
        orig_sr = wf.getframerate()
        raw = wf.readframes(n)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        
    # Resample to 44100 if needed
    if orig_sr != sr:
        duration = len(data) / orig_sr
        target_len = int(duration * sr)
        x_orig = np.linspace(0, 1, len(data))
        x_target = np.linspace(0, 1, target_len)
        data = np.interp(x_target, x_orig, data).astype(np.float32)
        
    clip_dur = len(data) / sr
    start_t = current_time
    end_t = start_t + clip_dur
    timeline.append({
        "id": i + 1,
        "clip": c,
        "start": start_t,
        "end": end_t,
        "duration": clip_dur
    })
    
    all_speech.append(data)
    
    # Add pause between sentences
    pause_samples = int(pause_dur * sr)
    all_speech.append(np.zeros(pause_samples, dtype=np.float32))
    current_time = end_t + pause_dur

# Final speech array
speech_full = np.concatenate(all_speech)
total_duration = len(speech_full) / sr

# Load BGM
with wave.open(bgm_file, 'r') as wf:
    n_bgm = wf.getnframes()
    raw_bgm = wf.readframes(n_bgm)
    bgm_data = np.frombuffer(raw_bgm, dtype=np.int16).astype(np.float32) / 32768.0

# Match length
if len(bgm_data) < len(speech_full):
    # loop bgm
    repeats = int(np.ceil(len(speech_full) / len(bgm_data)))
    bgm_data = np.tile(bgm_data, repeats)
bgm_data = bgm_data[:len(speech_full)]

# Mix voice-first: speech 0.95, BGM 0.14
master = speech_full * 0.95 + bgm_data * 0.14

# Master fade in/out
fade_in = int(0.5 * sr)
fade_out = int(1.2 * sr)
master[:fade_in] *= np.linspace(0, 1, fade_in)
master[-fade_out:] *= np.linspace(1, 0, fade_out)

# Prevent clipping
peak = np.max(np.abs(master))
if peak > 0.95:
    master = master * (0.95 / peak)

master_int = (master * 32767).astype(np.int16)
with wave.open(master_out, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(master_int.tobytes())

print(f"Master audio created: {master_out}")
print(f"Total video duration: {total_duration:.2f}s")
print("Timeline:")
for t in timeline:
    print(f"  Clip {t['id']}: {t['start']:.2f}s -> {t['end']:.2f}s (dur: {t['duration']:.2f}s)")
