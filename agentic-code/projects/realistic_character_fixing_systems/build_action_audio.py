import os, sys, wave, math, json
import numpy as np
import win32com.client, pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\realistic_character_fixing_systems"
audio_dir = os.path.join(proj_dir, "audio")
os.makedirs(audio_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# Script Lines & Action Timeline
# -----------------------------------------------------------------------------
script_scenes = [
    {
        "id": 1,
        "name": "act1_alarm_approach",
        "text": "Critical alert. Server zero four connection pool crashed. Autonomous agent dispatched to station one.",
        "action": "walk_to_server"
    },
    {
        "id": 2,
        "name": "act2_fix_server",
        "text": "Scanning hardware. Memory leak detected in connection handler. Injecting zero-downtime hotfix now.",
        "action": "scan_and_patch"
    },
    {
        "id": 3,
        "name": "act3_console_tests",
        "text": "Moving to the central cyber console. Rewriting integration tests. All regression suites passing green.",
        "action": "walk_and_type"
    },
    {
        "id": 4,
        "name": "act4_deploy",
        "text": "Routing patch through production pipeline. Pulling the master deployment lever. Patch deployed to global edge.",
        "action": "walk_and_deploy"
    },
    {
        "id": 5,
        "name": "act5_victory_cta",
        "text": "Full infrastructure restored in under forty-five seconds. Zero humans woken up. Are you still fixing bugs manually? Drop your thoughts below!",
        "action": "victory_pose"
    }
]

pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 0  # Energetic clear pace

sr = 44100
pause_between = 0.5
current_time = 0.3

timeline = []
all_speech_samples = [np.zeros(int(current_time * sr), dtype=np.float32)]

print("[+] Synthesizing narration clips...")
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
        t_len = int(dur * sr)
        x_o = np.linspace(0, 1, len(data))
        x_t = np.linspace(0, 1, t_len)
        data = np.interp(x_t, x_o, data).astype(np.float32)
        
    dur = len(data) / float(sr)
    start_t = current_time
    end_t = start_t + dur
    
    timeline.append({
        "id": sc["id"],
        "name": sc["name"],
        "start": start_t,
        "end": end_t,
        "duration": dur,
        "action": sc["action"]
    })
    
    all_speech_samples.append(data)
    all_speech_samples.append(np.zeros(int(pause_between * sr), dtype=np.float32))
    current_time = end_t + pause_between

full_speech = np.concatenate(all_speech_samples)
total_duration = len(full_speech) / float(sr)
print(f"Total Speech Duration: {total_duration:.2f}s")

# -----------------------------------------------------------------------------
# Procedural SFX Generation (Footsteps, Keyboard Clicks, Scanner, Zap, Chimes)
# -----------------------------------------------------------------------------
print("[+] Generating procedural interactive SFX...")
sfx_layer = np.zeros(len(full_speech), dtype=np.float32)

def add_sfx(sound, t_start, vol=1.0):
    s_idx = int(t_start * sr)
    e_idx = min(s_idx + len(sound), len(sfx_layer))
    if s_idx < len(sfx_layer):
        sfx_layer[s_idx:e_idx] += sound[:e_idx - s_idx] * vol

def make_footstep(dur=0.06):
    t = np.linspace(0, dur, int(sr * dur), False)
    noise = np.random.uniform(-1, 1, len(t))
    thump = np.sin(2 * np.pi * 90 * t)
    env = np.exp(-t * 80.0)
    return (noise * 0.4 + thump * 0.6) * env * 0.35

def make_keyclick(dur=0.03):
    t = np.linspace(0, dur, int(sr * dur), False)
    click = np.sin(2 * np.pi * 1400 * t) + np.sin(2 * np.pi * 3200 * t) * 0.5
    env = np.exp(-t * 180.0)
    return click * env * 0.3

def make_laser_scan(dur=2.5):
    t = np.linspace(0, dur, int(sr * dur), False)
    freq = 600 + 400 * np.sin(2 * np.pi * 3.0 * t)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    buzz = 0.5 * np.sin(phase) + 0.3 * np.sign(np.sin(phase * 1.5))
    env = np.minimum(t / 0.1, 1.0) * np.minimum((dur - t) / 0.2, 1.0)
    return buzz * env * 0.25

def make_zap(dur=0.3):
    t = np.linspace(0, dur, int(sr * dur), False)
    freq = 1800 * np.exp(-t * 15.0)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    noise = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 20.0)
    return (np.sin(phase) * 0.7 + noise * 0.3) * 0.45

def make_chime(freq=880.0, dur=1.2):
    t = np.linspace(0, dur, int(sr * dur), False)
    h1 = np.sin(2 * np.pi * freq * t) * np.exp(-t * 3.0)
    h2 = 0.5 * np.sin(2 * np.pi * freq * 2.0 * t) * np.exp(-t * 4.5)
    h3 = 0.25 * np.sin(2 * np.pi * freq * 3.0 * t) * np.exp(-t * 6.0)
    return (h1 + h2 + h3) * 0.4

def make_clunk(dur=0.35):
    t = np.linspace(0, dur, int(sr * dur), False)
    body = np.sin(2 * np.pi * 120 * t) * np.exp(-t * 18.0)
    metal = np.sin(2 * np.pi * 650 * t) * np.exp(-t * 35.0) * 0.5
    return (body + metal) * 0.5

# 1. Footsteps during walk phases
# Scene 1 walk to server: 1.5s to 5.5s
for step_t in np.arange(1.2, 5.2, 0.32):
    add_sfx(make_footstep(), step_t, vol=0.5)

# Scene 2 scan laser: 8.5s to 12.0s
add_sfx(make_laser_scan(3.0), 8.8, vol=0.4)
# Zap on patch injection: 13.5s
add_sfx(make_zap(0.35), 13.8, vol=0.6)
# Server online chime: 14.5s
add_sfx(make_chime(659.25, 1.2), 14.6, vol=0.5)  # E5
add_sfx(make_chime(880.00, 1.4), 14.8, vol=0.6)  # A5

# Scene 3 walk to center console: 17.0s to 20.5s
for step_t in np.arange(17.2, 20.2, 0.32):
    add_sfx(make_footstep(), step_t, vol=0.5)

# Scene 3 typing burst on console: 21.0s to 26.5s
for click_t in np.arange(21.2, 26.8, 0.085):
    if np.random.rand() > 0.15:
        add_sfx(make_keyclick(), click_t, vol=0.45)

# Test passed chimes:
add_sfx(make_chime(523.25, 0.8), 24.0, vol=0.4) # C5
add_sfx(make_chime(659.25, 0.8), 25.2, vol=0.4) # E5
add_sfx(make_chime(783.99, 1.0), 26.4, vol=0.5) # G5

# Scene 4 walk to deploy pillar: 28.5s to 32.0s
for step_t in np.arange(28.8, 31.8, 0.32):
    add_sfx(make_footstep(), step_t, vol=0.5)

# Lever pull mechanical clunk: 33.2s
add_sfx(make_clunk(0.4), 33.2, vol=0.7)
# Rocket / deployment power beam whoosh & chime: 34.5s
add_sfx(make_chime(1046.5, 1.8), 34.8, vol=0.65) # C6

# Scene 5 walk back to center: 36.5s to 39.5s
for step_t in np.arange(36.8, 39.8, 0.32):
    add_sfx(make_footstep(), step_t, vol=0.5)

# Victory powerup chord: 41.5s
add_sfx(make_chime(523.25, 1.8), 41.5, vol=0.4)
add_sfx(make_chime(659.25, 1.8), 41.6, vol=0.45)
add_sfx(make_chime(783.99, 2.0), 41.7, vol=0.5)
add_sfx(make_chime(1046.5, 2.2), 41.8, vol=0.6)

# -----------------------------------------------------------------------------
# Background Music Generation (Upbeat Modern Tech Groove)
# -----------------------------------------------------------------------------
print("[+] Generating dynamic tech groove BGM...")
def synth_piano_chord(freqs, duration, vel=0.18):
    t = np.linspace(0, duration, int(sr * duration), False)
    chord = np.zeros(len(t), dtype=np.float32)
    for f in freqs:
        note = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 2.5)
        chord += note
    att = np.minimum(t / 0.015, 1.0)
    return chord * att * vel

chords = [
    [110.0, 164.81, 196.00, 246.94],  # Am7/9
    [87.31, 130.81, 164.81, 220.00],  # Fmaj7
    [65.41, 130.81, 196.00, 246.94],  # Cmaj7
    [98.00, 146.83, 196.00, 261.63],  # Gsus4
    [110.0, 146.83, 174.61, 220.00],  # Dm7
    [82.41, 123.47, 164.81, 246.94]   # Em7
]

bgm = np.zeros(len(full_speech), dtype=np.float32)
step_len = 2.4
cur_b_t = 0.0
c_i = 0
while cur_b_t < total_duration:
    ch = chords[c_i % len(chords)]
    chord_wave = synth_piano_chord(ch, step_len + 0.8, vel=0.18)
    s_idx = int(cur_b_t * sr)
    e_idx = min(s_idx + len(chord_wave), len(bgm))
    bgm[s_idx:e_idx] += chord_wave[:e_idx - s_idx]
    
    # Rhythmic pulse on every beat (0.6s)
    for b_offset in [0.0, 0.6, 1.2, 1.8]:
        pulse_idx = int((cur_b_t + b_offset) * sr)
        if pulse_idx < len(bgm):
            p_len = int(0.12 * sr)
            pt = np.linspace(0, 0.12, p_len, False)
            kick = np.sin(2 * np.pi * 65.0 * np.exp(-pt * 30.0) * pt) * np.exp(-pt * 25.0) * 0.12
            pe_idx = min(pulse_idx + p_len, len(bgm))
            bgm[pulse_idx:pe_idx] += kick[:pe_idx - pulse_idx]
            
    cur_b_t += step_len
    c_i += 1

# Master Mix
master = full_speech * 0.96 + sfx_layer * 0.85 + bgm * 0.18

# Fade in / out
fade_in = int(0.3 * sr)
fade_out = int(1.2 * sr)
master[:fade_in] *= np.linspace(0, 1, fade_in)
master[-fade_out:] *= np.linspace(1, 0, fade_out)

peak = np.max(np.abs(master))
if peak > 0.95:
    master = master * (0.95 / peak)

master_wav = os.path.join(audio_dir, "master_action_audio.wav")
master_int = (master * 32767).astype(np.int16)
with wave.open(master_wav, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(master_int.tobytes())

print(f"Master Action Audio Created: {master_wav}")
print(f"Total Duration: {total_duration:.2f}s")

timeline_path = os.path.join(proj_dir, "action_timeline.json")
with open(timeline_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total_duration": total_duration,
        "timeline": timeline
    }, f, indent=2)
print(f"Action Timeline saved to {timeline_path}")
