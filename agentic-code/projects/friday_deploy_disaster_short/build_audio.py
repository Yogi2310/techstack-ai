import os, sys, wave, json, subprocess
import numpy as np
from gtts import gTTS

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\friday_deploy_disaster_short"
audio_dir = os.path.join(proj_dir, "audio")
os.makedirs(audio_dir, exist_ok=True)

script_scenes = [
    {
        "id": 1,
        "name": "beat1_innocent_commit",
        "card_badge": "💀 FRIDAY 5:00 PM",
        "card_title": "THE INNOCENT COMMIT",
        "card_sub": "Pushing Straight to Production",
        "text": "It is Friday at 5 PM. Your sprint is done, the weekend is calling, and you decide to push one tiny, innocent commit straight to production."
    },
    {
        "id": 2,
        "name": "beat2_red_alert",
        "card_badge": "🚨 PRODUCTION CRASH",
        "card_title": "500 INTERNAL SERVER ERROR",
        "card_sub": "PagerDuty Explodes with Alerts",
        "text": "Two minutes later... your phone explodes with PagerDuty alerts! 500 Internal Server Error. CPU at one hundred percent. The production database is completely locked!"
    },
    {
        "id": 3,
        "name": "beat3_terminal_debug",
        "card_badge": "🔍 ROOT CAUSE FOUND",
        "card_title": "UNINDEXED SQL NESTED QUERY",
        "card_sub": "Tracing Logs in Terminal",
        "text": "You panic and open the terminal. You run kubectl logs and trace the memory leak. And then you see it: an unindexed nested query locking ten million rows!"
    },
    {
        "id": 4,
        "name": "beat4_hotfix_restart",
        "card_badge": "🛠️ EMERGENCY HOTFIX",
        "card_title": "APPLYING COMPOSITE INDEX",
        "card_sub": "Rolling Restart 3/3 Pods Ready",
        "text": "You quickly write the hotfix migration, add the composite index, kill the zombie query locks, and execute the emergency rolling restart."
    },
    {
        "id": 5,
        "name": "beat5_readonly_friday",
        "card_badge": "💡 SENIOR DEV RULE",
        "card_title": "READ-ONLY FRIDAYS",
        "card_sub": "Subscribe to TechStack AI",
        "text": "System restored! Error rate is back to zero. The golden rule of software engineering: Read-Only Fridays exist for a reason. Subscribe to TechStack AI for real developer sanity!"
    }
]

sr = 44100
pause_between = 0.28
current_time = 0.2

timeline = []
all_speech_samples = [np.zeros(int(current_time * sr), dtype=np.float32)]

print("[+] Synthesizing natural Google Neural narration for Friday Deploy Short...")
for sc in script_scenes:
    mp3_path = os.path.join(audio_dir, f"{sc['name']}_raw.mp3")
    wav_path = os.path.join(audio_dir, f"{sc['name']}.wav")
    
    tts = gTTS(sc["text"], lang="en", tld="us")
    tts.save(mp3_path)
    
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", mp3_path,
        "-filter:a", "atempo=1.18,volume=1.25,highpass=f=80,lowpass=f=12000",
        "-ar", str(sr), "-ac", "1",
        wav_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with wave.open(wav_path, 'r') as wf:
        n = wf.getnframes()
        orig_sr = wf.getframerate()
        raw = wf.readframes(n)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        
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

all_speech_samples.append(np.zeros(int(2.0 * sr), dtype=np.float32))
full_speech = np.concatenate(all_speech_samples)

total_duration = len(full_speech) / sr
print(f"[+] Total Voice Duration: {total_duration:.2f} seconds ({len(script_scenes)} scenes)")

# --- DYNAMIC SOUND DESIGN (LO-FI CHILL -> RED ALERT SIREN -> INTENSE TYPING TECHNO -> TRIUMPHANT CHORDS) ---
print("[+] Generating dynamic developer drama sound design...")
bpm = 128.0
beat_len = 60.0 / bpm
total_samples = len(full_speech)
t_arr = np.linspace(0, total_duration, total_samples, endpoint=False)

bgm = np.zeros(total_samples, dtype=np.float32)

# 1. Bassline that evolves: Lo-fi chill in Scene 1 -> Dark pulsing industrial in Scenes 2-4 -> Warm major chords in Scene 5
bar_len = beat_len * 4.0
sub_bass = np.zeros(total_samples, dtype=np.float32)

for bar_idx in range(int(np.ceil(total_duration / bar_len))):
    bar_start_t = bar_idx * bar_len
    # Minor key progression for panic, resolving to major at end
    if bar_start_t > total_duration - 10.0:
        root_freq = 65.41  # C2 major relief
    elif bar_start_t > 9.0:
        root_freq = 55.0   # A1 minor tension
    else:
        root_freq = 43.65  # F1 relaxed lo-fi
        
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
                  np.sin(2 * np.pi * f * 2 * chunk_t) * 0.25) * decay
        sub_bass[note_idx0:note_idx1] += wave_b

bgm += sub_bass * 0.22

# 2. Punchy Kick, Snare & Mechanical Keyboard Clicks
kick_track = np.zeros(total_samples, dtype=np.float32)
snare_track = np.zeros(total_samples, dtype=np.float32)
mech_click_track = np.zeros(total_samples, dtype=np.float32)

total_beats = int(total_duration / beat_len) + 1
for b in range(total_beats):
    bt = b * beat_len
    idx0 = int(bt * sr)
    
    # Kick
    k_len = int(0.20 * sr)
    if idx0 < total_samples:
        k_idx1 = min(total_samples, idx0 + k_len)
        kt = t_arr[idx0:k_idx1] - bt
        k_pitch = 150.0 * np.exp(-kt * 35.0) + 40.0
        k_env = np.exp(-kt * 16.0)
        kick_track[idx0:k_idx1] += np.sin(2 * np.pi * k_pitch * kt) * k_env

    # Snare on 2 & 4
    if b % 2 == 1 and idx0 < total_samples:
        s_len = int(0.22 * sr)
        s_idx1 = min(total_samples, idx0 + s_len)
        st = t_arr[idx0:s_idx1] - bt
        s_noise = (np.random.rand(len(st)) * 2.0 - 1.0) * np.exp(-st * 22.0)
        snare_track[idx0:s_idx1] += s_noise * 0.6

    # Mechanical keyboard clicks (blue switch clicks on rapid 16ths)
    for c_i in [0.1, 0.25, 0.45, 0.6, 0.8, 0.95]:
        ct = bt + c_i * beat_len
        c_idx0 = int(ct * sr)
        if c_idx0 < total_samples:
            c_len = int(0.015 * sr)
            c_idx1 = min(total_samples, c_idx0 + c_len)
            ctt = t_arr[c_idx0:c_idx1] - ct
            c_click = (np.random.rand(len(ctt)) * 2.0 - 1.0) * np.exp(-ctt * 280.0)
            mech_click_track[c_idx0:c_idx1] += c_click * 0.35

bgm += kick_track * 0.25 + snare_track * 0.16 + mech_click_track * 0.12

# 3. Emergency Siren & System Chimes
siren_track = np.zeros(total_samples, dtype=np.float32)
for bar_idx in range(int(np.ceil(total_duration / bar_len))):
    bar_start_t = bar_idx * bar_len
    # Siren pulses only in emergency middle section (9s to 35s)
    if 9.0 <= bar_start_t <= 35.0:
        for s_i in range(8):
            st0 = bar_start_t + s_i * (beat_len / 2.0)
            si0 = int(st0 * sr)
            slen = int(0.18 * sr)
            if si0 >= total_samples:
                break
            si1 = min(total_samples, si0 + slen)
            st_arr = t_arr[si0:si1] - st0
            s_freq = 620.0 if s_i % 2 == 0 else 780.0
            s_env = np.exp(-st_arr * 10.0)
            siren_track[si0:si1] += np.sin(2 * np.pi * s_freq * st_arr) * s_env

bgm += siren_track * 0.08

# Normalize & Mix with Speech Ducking
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

timeline_file = os.path.join(proj_dir, "short_timeline.json")
with open(timeline_file, 'w', encoding='utf-8') as f:
    json.dump({
        "total_duration": round(total_duration, 2),
        "sample_rate": sr,
        "scenes": timeline
    }, f, indent=2)

print(f"[SUCCESS] Timeline metadata saved: {timeline_file}")
