import os, sys, wave, json
import numpy as np
import win32com.client, pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\3_free_ai_tools_short"
audio_dir = os.path.join(proj_dir, "audio")
os.makedirs(audio_dir, exist_ok=True)

script_scenes = [
    {
        "id": 1,
        "name": "beat1_hook",
        "tool": "HOOK",
        "text": "If you are still writing boilerplate code by hand in 2026, stop. These three free AI tools feel illegal for developers."
    },
    {
        "id": 2,
        "name": "beat2_antigravity",
        "tool": "ANTIGRAVITY AGENT",
        "text": "Number one: Antigravity Code Agent. It does not just suggest lines. It clones your repository, debugs failing unit tests, and patches microservices autonomously."
    },
    {
        "id": 3,
        "name": "beat3_bolt_cursor",
        "tool": "BOLT & CURSOR",
        "text": "Number two: Bolt dot new and Cursor. Full stack cloud prototyping directly inside your browser with instant zero config deployments in sixty seconds."
    },
    {
        "id": 4,
        "name": "beat4_gemini_flash",
        "tool": "GEMINI 3.1 FLASH",
        "text": "Number three: Gemini Three Flash. A one million token context window that ingests entire multi gigabyte codebases in two seconds flat."
    },
    {
        "id": 5,
        "name": "beat5_cta",
        "tool": "SUBSCRIBE",
        "text": "Save ten hours every single week. Which one are you testing first? Subscribe to TechStack AI for daily developer hacks!"
    }
]

pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 1  # Fast, punchy Shorts pacing (+1)

sr = 44100
pause_between = 0.35
current_time = 0.2

timeline = []
all_speech_samples = [np.zeros(int(current_time * sr), dtype=np.float32)]

print("[+] Synthesizing punchy voiceover clips for Shorts...")
for sc in script_scenes:
    wav_path = os.path.join(audio_dir, f"{sc['name']}.wav")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    stream.Open(wav_path, 3, False)
    speaker.AudioOutputStream = stream
    speaker.Speak(sc["text"])
    stream.Close()
    
    with wave.open(wav_path, 'r') as wf:
        n = wf.getnframes()
        orig_sr = wf.getframerate()
        raw = wf.readframes(n)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        
    if orig_sr != sr:
        dur = len(data) / orig_sr
        target_len = int(dur * sr)
        x_old = np.linspace(0, 1, len(data))
        x_new = np.linspace(0, 1, target_len)
        data = np.interp(x_new, x_old, data).astype(np.float32)
        
    start_t = current_time
    clip_dur = len(data) / sr
    end_t = start_t + clip_dur
    
    timeline.append({
        "id": sc["id"],
        "name": sc["name"],
        "tool": sc["tool"],
        "start": round(start_t, 2),
        "end": round(end_t, 2),
        "duration": round(clip_dur, 2),
        "text": sc["text"]
    })
    
    all_speech_samples.append(data)
    all_speech_samples.append(np.zeros(int(pause_between * sr), dtype=np.float32))
    current_time = end_t + pause_between

pythoncom.CoUninitialize()

# Add 2.0s padding at end for final punchy screen
all_speech_samples.append(np.zeros(int(2.0 * sr), dtype=np.float32))
full_speech = np.concatenate(all_speech_samples)
total_duration = len(full_speech) / sr
print(f"[+] Total Shorts Duration: {total_duration:.2f}s ({len(full_speech)} samples)")

# Save timeline
timeline_path = os.path.join(proj_dir, "short_timeline.json")
with open(timeline_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total_duration": round(total_duration, 2),
        "sample_rate": sr,
        "scenes": timeline
    }, f, indent=2)
print(f"[+] Saved timeline JSON to: {timeline_path}")

# -----------------------------------------------------------------------------
# Dynamic Sound Effects & Upbeat Synthwave Beat
# -----------------------------------------------------------------------------
sfx_track = np.zeros(len(full_speech), dtype=np.float32)

def add_sfx(sound_arr, start_sec, vol=1.0):
    s_idx = int(start_sec * sr)
    e_idx = s_idx + len(sound_arr)
    if s_idx >= len(sfx_track):
        return
    if e_idx > len(sfx_track):
        e_idx = len(sfx_track)
        sound_arr = sound_arr[:e_idx - s_idx]
    sfx_track[s_idx:e_idx] += sound_arr * vol

def make_whoosh(dur=0.35):
    t = np.linspace(0, dur, int(sr * dur), False)
    noise = np.random.uniform(-0.25, 0.25, len(t))
    env = np.sin(np.pi * (t / dur)) ** 2
    return (noise * env).astype(np.float32)

def make_pop():
    dur = 0.05
    t = np.linspace(0, dur, int(sr * dur), False)
    sine = np.sin(2 * np.pi * (800 - 600 * (t / dur)) * t) * np.exp(-t * 80.0)
    return (sine * 0.4).astype(np.float32)

def make_bell(freq=1200):
    dur = 0.8
    t = np.linspace(0, dur, int(sr * dur), False)
    tone = (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)) * np.exp(-t * 5.0)
    return (tone * 0.35).astype(np.float32)

# Schedule whooshes and pop sounds at transitions
for sc in timeline:
    add_sfx(make_whoosh(), sc["start"] - 0.15, vol=0.6)
    add_sfx(make_pop(), sc["start"] + 0.05, vol=0.8)
    if sc["id"] in [2, 3, 4]:
        add_sfx(make_bell(1046.50), sc["start"] + 0.6, vol=0.5)

# Fast Upbeat Electronic Drum & Bass / Synth Groove (130 BPM)
bpm = 130.0
beat_len = 60.0 / bpm  # ~0.4615s
bgm = np.zeros(len(full_speech), dtype=np.float32)

cur_t = 0.0
b_count = 0
while cur_t < total_duration:
    idx = int(cur_t * sr)
    # Kick on beats 0, 2 (or four on the floor)
    k_len = int(0.12 * sr)
    if idx + k_len < len(bgm):
        kt = np.linspace(0, 0.12, k_len, False)
        kick = np.sin(2 * np.pi * 90.0 * np.exp(-kt * 35.0) * kt) * np.exp(-kt * 28.0) * 0.18
        bgm[idx:idx + k_len] += kick

    # Snare / Clap on beat 1, 3
    if b_count % 2 == 1:
        s_len = int(0.15 * sr)
        if idx + s_len < len(bgm):
            st = np.linspace(0, 0.15, s_len, False)
            noise = np.random.uniform(-0.15, 0.15, s_len) * np.exp(-st * 25.0)
            tone = np.sin(2 * np.pi * 220 * st) * np.exp(-st * 30.0) * 0.08
            bgm[idx:idx + s_len] += (noise + tone) * 0.22

    cur_t += beat_len
    b_count += 1

# Ambient Bassline & Arp Chords
chords = [
    [130.81, 164.81, 196.00], # C
    [110.00, 146.83, 174.61], # Dm
    [87.31, 130.81, 174.61],  # F
    [98.00, 146.83, 196.00]   # G
]
c_len = beat_len * 4.0
cur_c_t = 0.0
c_i = 0
while cur_c_t < total_duration:
    ch = chords[c_i % len(chords)]
    dur_samples = int(c_len * sr)
    t_ch = np.linspace(0, c_len, dur_samples, False)
    chord_wave = np.zeros(dur_samples, dtype=np.float32)
    for f in ch:
        chord_wave += (np.sin(2 * np.pi * f * t_ch) + 0.25 * np.sin(4 * np.pi * f * t_ch)) * 0.03
    s_i = int(cur_c_t * sr)
    e_i = min(s_i + dur_samples, len(bgm))
    bgm[s_i:e_i] += chord_wave[:e_i - s_i]
    cur_c_t += c_len
    c_i += 1

# Master Mix
master = (full_speech * 0.88) + (sfx_track * 0.95) + (bgm * 0.75)
peak = np.max(np.abs(master))
if peak > 0.95:
    master = master * (0.95 / peak)

master_path = os.path.join(audio_dir, "short_master_audio.wav")
scaled = (master * 32767.0).astype(np.int16)
with wave.open(master_path, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(scaled.tobytes())

print(f"[+] Master Shorts audio mix rendered: {master_path}")
