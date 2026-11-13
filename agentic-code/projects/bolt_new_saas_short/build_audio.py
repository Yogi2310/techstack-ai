import os, sys, wave, json
import numpy as np
import win32com.client, pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\bolt_new_saas_short"
audio_dir = os.path.join(proj_dir, "audio")
os.makedirs(audio_dir, exist_ok=True)

script_scenes = [
    {
        "id": 1,
        "name": "beat1_hook",
        "card_badge": "🚨 3 DAYS VS 12 MINS",
        "card_title": "STOP MANUAL CONFIG",
        "card_sub": "Full-Stack SaaS Built in 12 Minutes",
        "text": "Stop spending three days configuring Docker, Webpack, and database migrations. Watch this: I just built a production full-stack web app in under twelve minutes using Bolt dot new."
    },
    {
        "id": 2,
        "name": "beat2_webcontainer",
        "card_badge": "⚡ ZERO LOCAL SETUP",
        "card_title": "WEBCONTAINER ENGINE",
        "card_sub": "No Node.js or Local Tools Required",
        "text": "You do not even need Node dot js installed. Inside a single browser tab, Bolt spins up a full WebContainer runtime with Vite, React, and Tailwind directly in memory."
    },
    {
        "id": 3,
        "name": "beat3_codegen",
        "card_badge": "🤖 FULL-STACK AI CODEGEN",
        "card_title": "PROMPT TO ARCHITECTURE",
        "card_sub": "React 19 + Supabase Auth + API Routes",
        "text": "Type what you want in plain English. It creates the database schemas, writes the authentication hooks, and live previews your application in real-time."
    },
    {
        "id": 4,
        "name": "beat4_deploy",
        "card_badge": "🚀 PRODUCTION LIVE",
        "card_title": "ONE-CLICK CLOUD DEPLOY",
        "card_sub": "Global CDN + Instant SSL in 60s",
        "text": "One click, and your entire application is deployed live to Netlify or Cloudflare Pages with SSL certificates, ready for real users."
    },
    {
        "id": 5,
        "name": "beat5_cta",
        "card_badge": "🏆 10X SPEED BOOST",
        "card_title": "WHAT WILL YOU BUILD?",
        "card_sub": "Subscribe for Daily AI Dev Hacks",
        "text": "What will you build first? Drop your project idea in the comments, and subscribe to TechStack AI for daily developer breakthroughs!"
    }
]

pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 1  # Energetic, fast Shorts pacing

sr = 44100
pause_between = 0.35
current_time = 0.2

timeline = []
all_speech_samples = [np.zeros(int(current_time * sr), dtype=np.float32)]

print("[+] Synthesizing punchy voiceover clips for Bolt.new Short...")
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

# Add 2.0s padding at end for outro victory screen
all_speech_samples.append(np.zeros(int(2.0 * sr), dtype=np.float32))
full_speech = np.concatenate(all_speech_samples)

total_duration = len(full_speech) / sr
print(f"[+] Total Voice Duration: {total_duration:.2f} seconds ({len(script_scenes)} scenes)")

# --- PROCEDURAL SYNTHWAVE / D&B BACKGROUND BEAT ---
print("[+] Generating high-energy developer synthwave background beat...")
bpm = 132.0
beat_len = 60.0 / bpm
total_samples = len(full_speech)
t_arr = np.linspace(0, total_duration, total_samples, endpoint=False)

bgm = np.zeros(total_samples, dtype=np.float32)

# 1. Bassline (Punchy rolling 80s Cyberpunk 16th notes)
root_notes = [55.0, 55.0, 65.41, 48.99] # A1, A1, C2, G1
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
        
        # Sawtooth harmonic bass with exponential filter decay
        f = root_freq if sixteenth not in [10, 14] else root_freq * 1.5
        decay = np.exp(-chunk_t * 12.0)
        wave_b = (np.sin(2 * np.pi * f * chunk_t) * 0.6 +
                  np.sin(2 * np.pi * f * 2 * chunk_t) * 0.3 +
                  np.sin(2 * np.pi * f * 3 * chunk_t) * 0.1) * decay
        sub_bass[note_idx0:note_idx1] += wave_b

bgm += sub_bass * 0.18

# 2. Tight Drum Track (Four on the Floor Kick + Snappy Snare + Shuffling Hi-Hats)
kick_track = np.zeros(total_samples, dtype=np.float32)
snare_track = np.zeros(total_samples, dtype=np.float32)
hat_track = np.zeros(total_samples, dtype=np.float32)

total_beats = int(total_duration / beat_len) + 1
for b in range(total_beats):
    bt = b * beat_len
    idx0 = int(bt * sr)
    
    # KICK on every beat (b % 1 == 0)
    k_len = int(0.18 * sr)
    if idx0 < total_samples:
        k_idx1 = min(total_samples, idx0 + k_len)
        kt = t_arr[idx0:k_idx1] - bt
        k_pitch = 140.0 * np.exp(-kt * 38.0) + 42.0
        k_env = np.exp(-kt * 18.0)
        kick_track[idx0:k_idx1] += np.sin(2 * np.pi * k_pitch * kt) * k_env

    # SNARE on beats 2 and 4 (b % 2 == 1)
    if b % 2 == 1 and idx0 < total_samples:
        s_len = int(0.20 * sr)
        s_idx1 = min(total_samples, idx0 + s_len)
        st = t_arr[idx0:s_idx1] - bt
        s_noise = (np.random.rand(len(st)) * 2.0 - 1.0) * np.exp(-st * 24.0)
        s_tone = np.sin(2 * np.pi * 185.0 * st) * np.exp(-st * 28.0)
        snare_track[idx0:s_idx1] += (s_noise * 0.7 + s_tone * 0.5)

    # HI-HATS on every 8th note
    for h in [0.0, 0.5]:
        ht = bt + h * beat_len
        h_idx0 = int(ht * sr)
        if h_idx0 < total_samples:
            h_len = int(0.045 * sr)
            h_idx1 = min(total_samples, h_idx0 + h_len)
            htt = t_arr[h_idx0:h_idx1] - ht
            hat_env = np.exp(-htt * 80.0)
            hat_noise = (np.random.rand(len(htt)) * 2.0 - 1.0) * hat_env
            hat_track[h_idx0:h_idx1] += hat_noise * 0.4

bgm += kick_track * 0.24 + snare_track * 0.16 + hat_track * 0.08

# 3. Arpeggiated Cyber Synth Chords (Lofi cyberpunk shimmer)
chord_notes = [
    [220.0, 261.63, 329.63, 392.0],  # Am7
    [174.61, 220.0, 261.63, 329.63], # Fmaj7
    [130.81, 164.81, 196.0, 246.94], # Cmaj7
    [196.0, 246.94, 293.66, 349.23]  # G7
]
arp_track = np.zeros(total_samples, dtype=np.float32)
for bar_idx in range(int(np.ceil(total_duration / bar_len))):
    bar_start_t = bar_idx * bar_len
    ch = chord_notes[bar_idx % len(chord_notes)]
    for note_idx in range(16):
        n_t0 = bar_start_t + note_idx * (beat_len / 4.0)
        n_i0 = int(n_t0 * sr)
        n_len = int((beat_len / 4.0) * 0.8 * sr)
        if n_i0 >= total_samples:
            break
        n_i1 = min(total_samples, n_i0 + n_len)
        nt = t_arr[n_i0:n_i1] - n_t0
        note_freq = ch[note_idx % len(ch)] * 2.0  # Octave up
        arp_env = np.exp(-nt * 15.0)
        arp_track[n_i0:n_i1] += np.sin(2 * np.pi * note_freq * nt) * arp_env

bgm += arp_track * 0.09

# Normalize Speech & Mix
speech_norm = full_speech / (np.max(np.abs(full_speech)) + 1e-6) * 0.85
bgm_norm = bgm / (np.max(np.abs(bgm)) + 1e-6) * 0.22

# Sidechain ducking: duck bgm whenever speech amplitude is high
ducking = 1.0 - np.clip(np.abs(speech_norm) * 1.4, 0.0, 0.65)
master_audio = speech_norm + (bgm_norm * ducking)
master_audio = master_audio / (np.max(np.abs(master_audio)) + 1e-6) * 0.94

# Save final mixed master WAV
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
