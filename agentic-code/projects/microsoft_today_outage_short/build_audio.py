import os, sys, wave, json
import numpy as np
import win32com.client, pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_today_outage_short"
audio_dir = os.path.join(proj_dir, "audio")
os.makedirs(audio_dir, exist_ok=True)

script_scenes = [
    {
        "id": 1,
        "name": "beat1_hook",
        "card_badge": "🚨 BREAKING TECH NEWS",
        "card_title": "MICROSOFT DOWN TODAY",
        "card_sub": "Teams, Outlook & Copilot Worldwide Crash",
        "text": "Microsoft just went down worldwide again today! Over one hundred and thirty thousand enterprise users were kicked out of Teams, Outlook, and Copilot. But this time... it was not a cyberattack or CrowdStrike."
    },
    {
        "id": 2,
        "name": "beat2_incident_mo",
        "card_badge": "🔍 INCIDENT MO1550821",
        "card_title": "THE FAILED HEALTH-CHECK",
        "card_sub": "Watchdog Monitors Failed Under Load",
        "text": "Microsoft tracked the chaos under incident M-O 1550821. It started when a backend cluster experienced sudden latency, causing automated health checks to fail."
    },
    {
        "id": 3,
        "name": "beat3_cascading_crash",
        "card_badge": "⚠️ CASCADING FAILURE",
        "card_title": "THE THUNDERING HERD",
        "card_sub": "Dead Nodes Killed Surviving Servers",
        "text": "Instead of throttling traffic, the orchestrator automatically pulled those servers offline! That dumped one hundred percent of global traffic onto surviving nodes, creating an instant cascading collapse!"
    },
    {
        "id": 4,
        "name": "beat4_manual_reroute",
        "card_badge": "🌐 GLOBAL TRAFFIC REROUTING",
        "card_title": "EMERGENCY NODE BYPASS",
        "card_sub": "Manual Capacity Re-injection",
        "text": "The secure handshake proxies choked. Microsoft engineers had to manually bypass broken routing and force healthy capacity back into the cluster to halt the spiral."
    },
    {
        "id": 5,
        "name": "beat5_engineering_lesson",
        "card_badge": "💡 SYSTEMS ENGINEERING LESSON",
        "card_title": "CIRCUIT BREAKER RULE",
        "card_sub": "Never Let Health Checks Kill Clusters",
        "text": "The golden rule of distributed systems: Never let your health checks kill more than twenty percent of your fleet at once. Subscribe to TechStack AI for real engineering post-mortems!"
    }
]

pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 2  # Punchy, energetic shorts pacing (+2)

sr = 44100
pause_between = 0.28
current_time = 0.2

timeline = []
all_speech_samples = [np.zeros(int(current_time * sr), dtype=np.float32)]

print("[+] Synthesizing narration for Microsoft Today Outage Short...")
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
        "card_badge": sc["card_badge"],
        "card_title": sc["card_title"],
        "card_sub": sc["card_sub"],
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
print(f"[+] Total Voice Duration: {total_duration:.2f} seconds ({len(script_scenes)} scenes)")

# --- INTENSE CYBERPUNK / SUSPENSE SOUND DESIGN ---
print("[+] Generating dramatic tech-disaster synthwave sound design...")
bpm = 132.0
beat_len = 60.0 / bpm
total_samples = len(full_speech)
t_arr = np.linspace(0, total_duration, total_samples, endpoint=False)

bgm = np.zeros(total_samples, dtype=np.float32)

# 1. Dark Pulsing Heartbeat Sub-Bass (A Minor Cyberpunk: A1, F1, D1, E1)
root_notes = [55.0, 43.65, 36.71, 41.20] # A1, F1, D1, E1
bar_len = beat_len * 4.0
sub_bass = np.zeros(total_samples, dtype=np.float32)

for bar_idx in range(int(np.ceil(total_duration / bar_len))):
    root_freq = root_notes[bar_idx % len(root_notes)]
    bar_start_t = bar_idx * bar_len
    for sixteenth in range(16):
        note_t0 = bar_start_t + sixteenth * (beat_len / 4.0)
        note_idx0 = int(note_t0 * sr)
        note_len = int((beat_len / 4.0) * 0.85 * sr)
        if note_idx0 >= total_samples:
            break
        note_idx1 = min(total_samples, note_idx0 + note_len)
        chunk_t = t_arr[note_idx0:note_idx1] - note_t0
        
        decay = np.exp(-chunk_t * 14.0)
        f = root_freq if sixteenth not in [6, 14] else root_freq * 1.5
        wave_b = (np.sin(2 * np.pi * f * chunk_t) * 0.65 +
                  np.sin(2 * np.pi * f * 2 * chunk_t) * 0.25 +
                  np.sin(2 * np.pi * f * 3 * chunk_t) * 0.1) * decay
        sub_bass[note_idx0:note_idx1] += wave_b

bgm += sub_bass * 0.22

# 2. Dramatic Industrial Drums (Punchy Kick + Sub Snare + Metallic Ticks)
kick_track = np.zeros(total_samples, dtype=np.float32)
snare_track = np.zeros(total_samples, dtype=np.float32)
hat_track = np.zeros(total_samples, dtype=np.float32)

total_beats = int(total_duration / beat_len) + 1
for b in range(total_beats):
    bt = b * beat_len
    idx0 = int(bt * sr)
    
    # Heavy Kick
    k_len = int(0.22 * sr)
    if idx0 < total_samples:
        k_idx1 = min(total_samples, idx0 + k_len)
        kt = t_arr[idx0:k_idx1] - bt
        k_pitch = 160.0 * np.exp(-kt * 35.0) + 38.0
        k_env = np.exp(-kt * 16.0)
        kick_track[idx0:k_idx1] += np.sin(2 * np.pi * k_pitch * kt) * k_env

    # Heavy Snare on beats 2 & 4
    if b % 2 == 1 and idx0 < total_samples:
        s_len = int(0.24 * sr)
        s_idx1 = min(total_samples, idx0 + s_len)
        st = t_arr[idx0:s_idx1] - bt
        s_noise = (np.random.rand(len(st)) * 2.0 - 1.0) * np.exp(-st * 20.0)
        s_tone = np.sin(2 * np.pi * 180.0 * st) * np.exp(-st * 24.0)
        snare_track[idx0:s_idx1] += (s_noise * 0.75 + s_tone * 0.45)

    # Fast tense 16th hats
    for h in [0.0, 0.25, 0.5, 0.75]:
        ht = bt + h * beat_len
        h_idx0 = int(ht * sr)
        if h_idx0 < total_samples:
            h_len = int(0.035 * sr)
            h_idx1 = min(total_samples, h_idx0 + h_len)
            htt = t_arr[h_idx0:h_idx1] - ht
            hat_env = np.exp(-htt * 95.0)
            hat_noise = (np.random.rand(len(htt)) * 2.0 - 1.0) * hat_env
            hat_track[h_idx0:h_idx1] += hat_noise * 0.25

bgm += kick_track * 0.26 + snare_track * 0.18 + hat_track * 0.08

# 3. Warning Alarm / Stuttering Glitch Synth
glitch_track = np.zeros(total_samples, dtype=np.float32)
for bar_idx in range(int(np.ceil(total_duration / bar_len))):
    bar_start_t = bar_idx * bar_len
    # Siren interval (E5 and G5)
    for s_i in range(8):
        st0 = bar_start_t + s_i * (beat_len / 2.0)
        si0 = int(st0 * sr)
        slen = int(0.18 * sr)
        if si0 >= total_samples:
            break
        si1 = min(total_samples, si0 + slen)
        st_arr = t_arr[si0:si1] - st0
        s_freq = 659.25 if s_i % 2 == 0 else 783.99  # E5 and G5
        s_env = np.exp(-st_arr * 10.0)
        glitch_track[si0:si1] += np.sin(2 * np.pi * s_freq * st_arr) * s_env

bgm += glitch_track * 0.06

# Normalize & Mix with Ducking
speech_norm = full_speech / (np.max(np.abs(full_speech)) + 1e-6) * 0.88
bgm_norm = bgm / (np.max(np.abs(bgm)) + 1e-6) * 0.20

ducking = 1.0 - np.clip(np.abs(speech_norm) * 1.5, 0.0, 0.65)
master_audio = speech_norm + (bgm_norm * ducking)
master_audio = master_audio / (np.max(np.abs(master_audio)) + 1e-6) * 0.95

# Save master WAV
out_wav = os.path.join(audio_dir, "short_master_audio.wav")
int16_audio = (master_audio * 32767.0).astype(np.int16)
with wave.open(out_wav, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(int16_audio.tobytes())

print(f"[SUCCESS] Master audio synthesized: {out_wav}")
print(f"File size: {os.path.getsize(out_wav) / 1024:.1f} KB")

# Save timeline metadata
timeline_file = os.path.join(proj_dir, "short_timeline.json")
with open(timeline_file, 'w', encoding='utf-8') as f:
    json.dump({
        "total_duration": round(total_duration, 2),
        "sample_rate": sr,
        "scenes": timeline
    }, f, indent=2)

print(f"[SUCCESS] Timeline metadata saved: {timeline_file}")
