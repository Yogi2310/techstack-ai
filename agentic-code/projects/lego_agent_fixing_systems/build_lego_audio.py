import os, sys, wave, math, json
import numpy as np
import win32com.client, pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems"
audio_dir = os.path.join(proj_dir, "audio")
os.makedirs(audio_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# Script Scenes & Narrative Timeline
# -----------------------------------------------------------------------------
script_scenes = [
    {
        "id": 1,
        "name": "act1_lego_alarm_approach",
        "text": "Critical alert on the brick grid! Server Blade zero-one connection pool crashed. Autonomous LEGO agent dispatched to station one.",
        "action": "lego_walk_to_server"
    },
    {
        "id": 2,
        "name": "act2_lego_scan_server",
        "text": "Scanning hardware. Memory leak detected in brick cluster. Snapping in a hotfix brick. Daemon rebooted, status solid cyan!",
        "action": "lego_scan_and_patch"
    },
    {
        "id": 3,
        "name": "act3_lego_console_tests",
        "text": "Waddling over to the cyber slope terminal. Rapid-fire typing with C-clamp hands. All forty-two regression unit tests pass!",
        "action": "lego_walk_and_type"
    },
    {
        "id": 4,
        "name": "act4_lego_lever_deploy",
        "text": "Approaching the Technic master deployment lever. Locking yellow grip into place, pulling down. Hundred percent power locked in!",
        "action": "lego_pull_technic_lever"
    },
    {
        "id": 5,
        "name": "act5_lego_victory_ship",
        "text": "Autonomous code shipped to production while humans sleep. Build your own AI brick workforce. Subscribe for more agentic workflows!",
        "action": "lego_victory_celebration"
    }
]

pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 0  # Natural, crisp, conversational tempo

sr = 44100
pause_between = 0.5
current_time = 0.3

timeline = []
all_speech_samples = [np.zeros(int(current_time * sr), dtype=np.float32)]

print("[+] Synthesizing LEGO narration clips...")
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
        "action": sc["action"],
        "start": round(start_t, 2),
        "end": round(end_t, 2),
        "duration": round(clip_dur, 2),
        "text": sc["text"]
    })
    
    all_speech_samples.append(data)
    all_speech_samples.append(np.zeros(int(pause_between * sr), dtype=np.float32))
    current_time = end_t + pause_between

pythoncom.CoUninitialize()

# Add extra 3.5 seconds at the end for final celebratory screen
tail_pad = 3.5
all_speech_samples.append(np.zeros(int(tail_pad * sr), dtype=np.float32))
full_speech = np.concatenate(all_speech_samples)
total_duration = len(full_speech) / sr
print(f"[+] Total Voice Duration: {total_duration:.2f}s ({len(full_speech)} samples)")

# Save timeline JSON
timeline_path = os.path.join(proj_dir, "lego_action_timeline.json")
with open(timeline_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total_duration": round(total_duration, 2),
        "sample_rate": sr,
        "scenes": timeline
    }, f, indent=2)
print(f"[+] Timeline saved to {timeline_path}")

# -----------------------------------------------------------------------------
# Procedural LEGO Sound Effects
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

def make_lego_click():
    # Authentic ABS plastic resonance: high-Q snap + short burst
    dur = 0.035
    t = np.linspace(0, dur, int(sr * dur), False)
    snap = np.sin(2 * np.pi * 1750 * t) * np.exp(-t * 90.0)
    high = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 130.0) * 0.4
    noise = np.random.uniform(-0.15, 0.15, len(t)) * np.exp(-t * 150.0)
    return (snap + high + noise).astype(np.float32)

def make_lego_brick_snap():
    # Double-click snap of pressing two LEGO bricks together
    c1 = make_lego_click()
    c2 = make_lego_click() * 0.8
    pad = np.zeros(int(sr * 0.025), dtype=np.float32)
    return np.concatenate([c1, pad, c2])

def make_laser_scan(dur=2.5):
    t = np.linspace(0, dur, int(sr * dur), False)
    fm = 520.0 + 380.0 * np.sin(2 * np.pi * 3.5 * t)
    carrier = np.sin(2 * np.pi * fm * t) + 0.3 * np.sin(4 * np.pi * fm * t)
    env = np.sin(np.pi * (t / dur)) ** 0.5
    return (carrier * env * 0.25).astype(np.float32)

def make_chime(freq, dur=1.0):
    t = np.linspace(0, dur, int(sr * dur), False)
    env = np.exp(-t * 3.5)
    return (np.sin(2 * np.pi * freq * t) * env).astype(np.float32)

def make_technic_lever_snap():
    # Heavy LEGO Technic axle click + gear snap
    dur = 0.12
    t = np.linspace(0, dur, int(sr * dur), False)
    thud = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 22.0)
    click = make_lego_brick_snap()
    res = np.zeros(len(t), dtype=np.float32)
    res += thud * 0.6
    res[:min(len(click), len(res))] += click[:min(len(click), len(res))] * 0.8
    return res

# Schedule SFX across scenes based on timeline
# Act 1: Walking across studded plate to Server
act1 = timeline[0]
for step_t in np.arange(act1["start"] + 0.8, act1["end"] - 0.5, 0.35):
    add_sfx(make_lego_click(), step_t, vol=0.55)

# Act 2: Laser scan on broken server, snap in hotfix brick
act2 = timeline[1]
add_sfx(make_laser_scan(3.0), act2["start"] + 0.5, vol=0.45)
add_sfx(make_lego_brick_snap(), act2["start"] + 3.8, vol=0.75) # Hotfix brick snapped!
add_sfx(make_chime(659.25, 1.2), act2["start"] + 4.3, vol=0.5) # E5
add_sfx(make_chime(880.00, 1.4), act2["start"] + 4.5, vol=0.6) # A5

# Walk from server to cyber terminal
for step_t in np.arange(act2["end"] - 0.3, act2["end"] + 2.0, 0.35):
    add_sfx(make_lego_click(), step_t, vol=0.5)

# Act 3: Rapid typewriter typing on slope brick
act3 = timeline[2]
for click_t in np.arange(act3["start"] + 0.6, act3["end"] - 1.2, 0.09):
    if np.random.rand() > 0.15:
        add_sfx(make_lego_click(), click_t, vol=0.4)

# Test pass bells
add_sfx(make_chime(523.25, 0.8), act3["end"] - 1.0, vol=0.45) # C5
add_sfx(make_chime(659.25, 0.8), act3["end"] - 0.7, vol=0.5)  # E5
add_sfx(make_chime(783.99, 1.0), act3["end"] - 0.4, vol=0.55) # G5
add_sfx(make_chime(1046.5, 1.2), act3["end"] - 0.1, vol=0.65) # C6

# Walk to Technic lever
act4 = timeline[3]
for step_t in np.arange(act3["end"] + 0.2, act4["start"] + 1.2, 0.35):
    add_sfx(make_lego_click(), step_t, vol=0.5)

# Act 4: Technic lever snap & power surge
add_sfx(make_technic_lever_snap(), act4["start"] + 3.2, vol=0.85)
# Power charging drone
charge_t = np.linspace(0, 2.5, int(sr * 2.5), False)
charge_s = (np.sin(2 * np.pi * 95 * charge_t) + 0.4 * np.sin(2 * np.pi * 190 * charge_t)) * np.sin(np.pi * (charge_t / 2.5))
add_sfx(charge_s.astype(np.float32), act4["start"] + 3.4, vol=0.4)

# Rocket / cloud pipeline uplink launch
rocket_t = np.linspace(0, 2.5, int(sr * 2.5), False)
rocket_s = np.random.uniform(-0.35, 0.35, len(rocket_t)) * np.sin(np.pi * (rocket_t / 2.5))
add_sfx(rocket_s.astype(np.float32), act4["end"] - 1.2, vol=0.5)

# Act 5: Minifigure celebration & final victory
act5 = timeline[4]
for step_t in np.arange(act4["end"], act5["start"] + 1.2, 0.35):
    add_sfx(make_lego_click(), step_t, vol=0.5)

add_sfx(make_chime(523.25, 2.0), act5["start"] + 2.0, vol=0.45)
add_sfx(make_chime(659.25, 2.0), act5["start"] + 2.1, vol=0.5)
add_sfx(make_chime(783.99, 2.2), act5["start"] + 2.2, vol=0.55)
add_sfx(make_chime(1046.5, 2.4), act5["start"] + 2.3, vol=0.65)

# -----------------------------------------------------------------------------
# Upbeat BGM (Playful Modern Toy/Tech Synthesizer Groove)
# -----------------------------------------------------------------------------
print("[+] Generating playful LEGO tech groove BGM...")
def synth_toy_synth(freqs, duration, vel=0.15):
    t = np.linspace(0, duration, int(sr * duration), False)
    chord = np.zeros(len(t), dtype=np.float32)
    for f in freqs:
        # Square-ish harmonics with warm filter decay
        note = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 2.2)
        chord += note
    att = np.minimum(t / 0.02, 1.0)
    return chord * att * vel

chords = [
    [130.81, 164.81, 196.00, 246.94],  # Cmaj7
    [110.00, 164.81, 196.00, 246.94],  # Am7
    [87.31, 130.81, 174.61, 220.00],   # Fmaj7
    [98.00, 146.83, 196.00, 246.94],   # G
]

bgm = np.zeros(len(full_speech), dtype=np.float32)
step_len = 2.4
cur_b_t = 0.0
c_i = 0
while cur_b_t < total_duration:
    ch = chords[c_i % len(chords)]
    chord_wave = synth_toy_synth(ch, step_len + 0.6, vel=0.15)
    s_idx = int(cur_b_t * sr)
    e_idx = min(s_idx + len(chord_wave), len(bgm))
    bgm[s_idx:e_idx] += chord_wave[:e_idx - s_idx]
    
    # Four-on-the-floor gentle toy kick & hi-hat
    for b_offset in [0.0, 0.6, 1.2, 1.8]:
        pulse_idx = int((cur_b_t + b_offset) * sr)
        if pulse_idx < len(bgm):
            p_len = int(0.1 * sr)
            pt = np.linspace(0, 0.1, p_len, False)
            kick = np.sin(2 * np.pi * 75.0 * np.exp(-pt * 35.0) * pt) * np.exp(-pt * 30.0) * 0.10
            bgm[pulse_idx:min(pulse_idx + p_len, len(bgm))] += kick[:min(p_len, len(bgm) - pulse_idx)]
    cur_b_t += step_len
    c_i += 1

# Master mix
master = (full_speech * 0.88) + (sfx_track * 0.95) + (bgm * 0.75)
peak = np.max(np.abs(master))
if peak > 0.95:
    master = master * (0.95 / peak)

master_path = os.path.join(audio_dir, "lego_master_audio.wav")
scaled = (master * 32767.0).astype(np.int16)
with wave.open(master_path, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(scaled.tobytes())

print(f"[+] Master LEGO audio mix rendered successfully: {master_path}")
