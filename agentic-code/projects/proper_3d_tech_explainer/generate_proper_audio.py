import os, sys, wave, math, subprocess
import numpy as np
import win32com.client, pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\proper_3d_tech_explainer"
audio_dir = os.path.join(proj_dir, "audio")
sfx_dir = os.path.join(proj_dir, "sfx")

os.makedirs(audio_dir, exist_ok=True)

# Scene Script Lines
script_scenes = [
    {
        "id": 1,
        "name": "scene1_catastrophe",
        "text": "It's two A M. Your production database just crashed, your server is throwing five hundred errors, and your lead developer is dead asleep.",
        "sfx": [("clock_tick.wav", 0.5, 0.4), ("horror_sting.wav", 5.5, 0.6)]
    },
    {
        "id": 2,
        "name": "scene2_team_myth",
        "text": "Most founders think hiring ten more developers solves the problem. But adding headcount doesn't speed up delivery. It adds standups, merge conflicts, and endless Slack ping-pong.",
        "sfx": [("vine_boom.wav", 9.5, 0.8)]
    },
    {
        "id": 3,
        "name": "scene3_agent_enters",
        "text": "Now look at this. While humans sleep, an autonomous A I agent detects the exception, spins up a sandbox, isolates the failing unit test, and writes the patch.",
        "sfx": [("anime_riser.wav", 0.2, 0.5)]
    },
    {
        "id": 4,
        "name": "scene4_zero_handoff",
        "text": "No waiting for code reviews. No arguing in pull requests. The agent tests its own fix, verifies regression safety, and deploys directly to production.",
        "sfx": [("sparkle_chime.wav", 8.0, 0.6)]
    },
    {
        "id": 5,
        "name": "scene5_ten_x_shift",
        "text": "In 2026, the most dangerous startups aren't fifty-person engineering departments. They are solo founders orchestrating fleets of autonomous agents shipping ten times faster.",
        "sfx": [("dbz_aura.wav", 1.0, 0.5)]
    },
    {
        "id": 6,
        "name": "scene6_cta",
        "text": "So the real question isn't whether A I replaces programmers. It's whether you're building with agents, or competing against them. Which side are you on? Comment below!",
        "sfx": []
    }
]

pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 0  # Natural energetic conversational pace

sr = 44100
pause_between = 0.55  # 550ms natural pause between scenes
current_time = 0.4    # 400ms lead

timeline = []
all_speech_samples = []

# Lead silence
all_speech_samples.append(np.zeros(int(current_time * sr), dtype=np.float32))

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
        
    # Resample to 44100
    if orig_sr != sr:
        dur = len(data) / orig_sr
        target_len = int(dur * sr)
        x_orig = np.linspace(0, 1, len(data))
        x_target = np.linspace(0, 1, target_len)
        data = np.interp(x_target, x_orig, data).astype(np.float32)
        
    clip_dur = len(data) / float(sr)
    start_t = current_time
    end_t = start_t + clip_dur
    
    timeline.append({
        "id": sc["id"],
        "name": sc["name"],
        "start": start_t,
        "end": end_t,
        "duration": clip_dur,
        "sfx": sc["sfx"]
    })
    
    all_speech_samples.append(data)
    all_speech_samples.append(np.zeros(int(pause_between * sr), dtype=np.float32))
    current_time = end_t + pause_between

full_speech = np.concatenate(all_speech_samples)
total_duration = len(full_speech) / float(sr)
print(f"Total Speech Duration: {total_duration:.2f}s")

# -----------------------------------------------------------------------------
# Generate Warm Modern Tech BGM (Piano + Ambient Pads)
# -----------------------------------------------------------------------------
print("[+] Generating ambient chord progression BGM...")
def synth_note(freq, duration, vel=0.25):
    t = np.linspace(0, duration, int(sr * duration), False)
    h1 = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.2)
    h2 = 0.55 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 3.5)
    h3 = 0.28 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 5.0)
    h4 = 0.12 * np.sin(2 * np.pi * 4 * freq * t) * np.exp(-t * 7.2)
    att = np.minimum(t / 0.02, 1.0)
    return (h1 + h2 + h3 + h4) * att * vel

chords = [
    [110.0, 130.81, 164.81, 196.00, 246.94],  # Am9
    [87.31, 130.81, 164.81, 220.00],          # Fmaj7
    [65.41, 98.00, 164.81, 246.94],           # Cmaj7
    [98.00, 146.83, 196.00, 261.63],          # Gsus4
    [110.0, 164.81, 220.00, 261.63],          # Am7
    [73.42, 110.00, 146.83, 220.00]           # Dm7
]

bgm_samples = np.zeros(len(full_speech), dtype=np.float32)
chord_dur = 3.6
cur_bgm_t = 0.0
c_idx = 0

while cur_bgm_t < total_duration:
    ch = chords[c_idx % len(chords)]
    for n_i, freq in enumerate(ch):
        offset = n_i * 0.07
        n_dur = chord_dur + 1.4 - offset
        note = synth_note(freq, n_dur, vel=0.20)
        s_idx = int((cur_bgm_t + offset) * sr)
        e_idx = min(s_idx + len(note), len(bgm_samples))
        bgm_samples[s_idx:e_idx] += note[:e_idx - s_idx]
    cur_bgm_t += chord_dur
    c_idx += 1

# Sub-bass pad
t_arr = np.linspace(0, total_duration, len(bgm_samples), False)
sub_bass = 0.05 * np.sin(2 * np.pi * 55.0 * t_arr) * np.sin(2 * np.pi * 0.2 * t_arr)
bgm_samples += sub_bass

# Normalize BGM
bgm_max = np.max(np.abs(bgm_samples))
if bgm_max > 0:
    bgm_samples = (bgm_samples / bgm_max) * 0.22  # Soft, sits comfortably below speech

# -----------------------------------------------------------------------------
# Layer Sound Effects (SFX) at exact scene timestamps
# -----------------------------------------------------------------------------
print("[+] Layering SFX...")
sfx_layer = np.zeros(len(full_speech), dtype=np.float32)

for sc in timeline:
    scene_start = sc["start"]
    for sfx_name, rel_time, vol in sc["sfx"]:
        sfx_path = os.path.join(sfx_dir, sfx_name)
        if not os.path.exists(sfx_path):
            continue
        try:
            with wave.open(sfx_path, 'r') as wf:
                sfx_n = wf.getnframes()
                sfx_sr = wf.getframerate()
                sfx_raw = wf.readframes(sfx_n)
                sfx_data = np.frombuffer(sfx_raw, dtype=np.int16).astype(np.float32) / 32768.0
            # Resample if needed
            if sfx_sr != sr:
                sfx_dur = len(sfx_data) / sfx_sr
                t_len = int(sfx_dur * sr)
                x_o = np.linspace(0, 1, len(sfx_data))
                x_t = np.linspace(0, 1, t_len)
                sfx_data = np.interp(x_t, x_o, sfx_data).astype(np.float32)
                
            abs_time = scene_start + rel_time
            s_idx = int(abs_time * sr)
            e_idx = min(s_idx + len(sfx_data), len(sfx_layer))
            sfx_layer[s_idx:e_idx] += sfx_data[:e_idx - s_idx] * vol
            print(f"  Applied {sfx_name} at t={abs_time:.2f}s (vol: {vol})")
        except Exception as e:
            print(f"  Error loading {sfx_name}: {e}")

# -----------------------------------------------------------------------------
# Final Master Mix (Voice-First Audio Mix)
# -----------------------------------------------------------------------------
print("[+] Performing final master mix...")
master = full_speech * 0.98 + bgm_samples * 0.15 + sfx_layer * 0.65

# Smooth Fade in / out
fade_in = int(0.4 * sr)
fade_out = int(1.2 * sr)
master[:fade_in] *= np.linspace(0, 1, fade_in)
master[-fade_out:] *= np.linspace(1, 0, fade_out)

# Limiter to avoid clipping
peak = np.max(np.abs(master))
if peak > 0.95:
    master = master * (0.95 / peak)

master_wav = os.path.join(audio_dir, "master_audio_with_sfx.wav")
master_int = (master * 32767).astype(np.int16)
with wave.open(master_wav, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(master_int.tobytes())

print(f"\n✅ Master Audio with SFX Created: {master_wav}")
print(f"   Duration: {total_duration:.2f}s ({len(master)} samples)")

# Output timeline JSON for renderer
import json
timeline_path = os.path.join(proj_dir, "timeline.json")
with open(timeline_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total_duration": total_duration,
        "timeline": timeline
    }, f, indent=2)
print(f"✅ Timeline saved to {timeline_path}")
