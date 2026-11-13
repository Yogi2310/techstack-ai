"""
Audio Production Pipeline for 'The Midnight Colossus of Blackwood Creek' 60s Horror Short
Synthesizes cinematic narration via gTTS with neural pitch/tempo formatting,
and composites procedural horror soundscapes (wind, bell tolls, heartbeat, earthquake stomps, monster roar).
"""
import os
import sys
import subprocess
import numpy as np
import wave
import json

from gtts import gTTS

AUDIO_DIR = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short\audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

beats = [
    {
        "id": "beat1_midnight_rule",
        "text": "Rule number one of Blackwood Creek: When the village bells strike thirteen at midnight... you do not stay out in the mist.",
        "target_dur": 11.0,
        "mood": "eerie_wind_bells"
    },
    {
        "id": "beat2_hermit_warning",
        "text": "Old man Miller slammed open his shutter, tossing down a rusted iron key. Kid! Get inside the cabin right now! He smells you... and he's off the chain!",
        "target_dur": 11.0,
        "mood": "panic_shutter_whisper"
    },
    {
        "id": "beat3_shadow_tremor",
        "text": "Then, the street went dead silent. The puddles began to ripple. An immense shadow stretched forty feet across the gravel road.",
        "target_dur": 11.0,
        "mood": "dead_silence_heartbeat"
    },
    {
        "id": "beat4_titan_rises",
        "text": "Rising out of the black pines was the Colossus of Hollow Creek. Two burning red eyes staring down through the fog... and a jaw of jagged razor fangs.",
        "target_dur": 11.0,
        "mood": "colossus_reveal_drone"
    },
    {
        "id": "beat5_screaming_escape",
        "text": "With a bone-shattering roar, it charged! I lunged for the cabin door as its razor claws slammed into the dirt behind me! Did I make it inside in time? Comment for Part Two!",
        "target_dur": 11.6,
        "mood": "chase_earthquake_screaming_cut"
    }
]

print("1. Synthesizing voiceover tracks with gTTS...")
for b in beats:
    raw_mp3 = os.path.join(AUDIO_DIR, f"{b['id']}_raw.mp3")
    processed_wav = os.path.join(AUDIO_DIR, f"{b['id']}.wav")
    
    tts = gTTS(text=b["text"], lang="en", tld="com", slow=False)
    tts.save(raw_mp3)
    
    # Process audio with ffmpeg: atempo=1.12, crisp highpass and bass presence for spooky narration
    cmd = [
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "atempo=1.12,highpass=f=90,lowpass=f=7500,volume=1.4",
        "-ar", "44100", "-ac", "2", processed_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Generated: {processed_wav}")

# 2. Generate procedural horror sound effects
print("\n2. Generating procedural horror sound elements...")
SR = 44100
total_duration = sum(b["target_dur"] for b in beats) # ~55.6s
total_samples = int(total_duration * SR)

def create_wave(samples):
    return np.zeros(samples, dtype=np.float32)

sfx_track = np.zeros((total_samples, 2), dtype=np.float32)

t = np.linspace(0, total_duration, total_samples, endpoint=False)

# Atmospheric wind & sub-bass drone
wind = np.sin(2 * np.pi * 55 * t) * 0.15 + np.sin(2 * np.pi * 38 * t) * 0.2
noise = np.random.normal(0, 0.05, total_samples).astype(np.float32)
# Low-pass filter noise for wind rumble
wind_noise = np.convolve(noise, np.ones(500)/500, mode='same')
sfx_track[:, 0] += wind + wind_noise * 1.5
sfx_track[:, 1] += wind + wind_noise * 1.5

# Beat 1: Distant bell tolls (at t=1.0s, 3.5s, 6.0s, 8.5s)
bell_times = [1.0, 3.5, 6.0, 8.5]
for bt in bell_times:
    idx = int(bt * SR)
    bell_len = int(3.5 * SR)
    if idx + bell_len < total_samples:
        tb = np.linspace(0, 3.5, bell_len, endpoint=False)
        decay = np.exp(-1.2 * tb)
        bell = (np.sin(2 * np.pi * 220 * tb) + 0.5 * np.sin(2 * np.pi * 440 * tb) + 0.25 * np.sin(2 * np.pi * 880 * tb)) * decay * 0.35
        sfx_track[idx:idx+bell_len, 0] += bell
        sfx_track[idx:idx+bell_len, 1] += bell

# Beat 3: Heartbeat starts at t=22s
# Two thumps: 0.0s and 0.25s every 0.9s
hb_start = 22.0
hb_end = 55.0
current_hb = hb_start
while current_hb < hb_end:
    hb_rate = 0.85 if current_hb < 44.0 else 0.55 # accelerates in climax!
    for sub in [0.0, 0.22]:
        idx = int((current_hb + sub) * SR)
        hb_len = int(0.25 * SR)
        if idx + hb_len < total_samples:
            th = np.linspace(0, 0.25, hb_len, endpoint=False)
            decay = np.exp(-18 * th)
            thump = np.sin(2 * np.pi * 50 * th) * decay * 0.55
            sfx_track[idx:idx+hb_len, 0] += thump
            sfx_track[idx:idx+hb_len, 1] += thump
    current_hb += hb_rate

# Beat 4 & 5: Colossus Stomps (t=33s, 37s, 41s, 44s, 47s, 50s, 53s)
stomp_times = [33.0, 37.0, 41.0, 44.5, 47.5, 50.5, 53.0]
for st in stomp_times:
    idx = int(st * SR)
    stomp_len = int(1.2 * SR)
    if idx + stomp_len < total_samples:
        ts = np.linspace(0, 1.2, stomp_len, endpoint=False)
        decay = np.exp(-4.5 * ts)
        # Deep sub-bass impact (30Hz -> 60Hz) + gravel crunch
        stomp = (np.sin(2 * np.pi * 45 * ts) * 0.7 + np.random.normal(0, 0.25, stomp_len) * 0.4) * decay
        sfx_track[idx:idx+stomp_len, 0] += stomp
        sfx_track[idx:idx+stomp_len, 1] += stomp

# Monster Roar / Riser at t=44.0s
idx_roar = int(44.0 * SR)
roar_len = int(3.5 * SR)
if idx_roar + roar_len < total_samples:
    tr = np.linspace(0, 3.5, roar_len, endpoint=False)
    freq = np.linspace(80, 220, roar_len)
    decay = np.exp(-0.8 * tr) * (1.0 - np.exp(-5.0 * tr))
    roar = (np.sin(2 * np.pi * freq * tr) * 0.45 + np.random.normal(0, 0.35, roar_len) * 0.35) * decay
    sfx_track[idx_roar:idx_roar+roar_len, 0] += roar
    sfx_track[idx_roar:idx_roar+roar_len, 1] += roar

# Clip and normalize SFX
sfx_track = np.clip(sfx_track, -0.9, 0.9)
sfx_wav = os.path.join(AUDIO_DIR, "horror_sfx_ambience.wav")
sfx_int16 = (sfx_track * 32767).astype(np.int16)
with wave.open(sfx_wav, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(sfx_int16.tobytes())
print(f"Generated Horror SFX Ambience: {sfx_wav}")

# 3. Assemble Master Audio Timeline
print("\n3. Compositing Master Audio with Voiceover...")
# Create silent canvas
master_wav = os.path.join(AUDIO_DIR, "horror_master_audio.wav")

timeline = []
cur_time = 0.0

inputs = ["-i", sfx_wav]
filter_complex = ["[0:a]volume=0.85[sfx];"]
mix_inputs = ["[sfx]"]

for i, b in enumerate(beats):
    voice_file = os.path.join(AUDIO_DIR, f"{b['id']}.wav")
    inputs.extend(["-i", voice_file])
    input_idx = i + 1
    
    # get duration
    with wave.open(voice_file, 'r') as wf:
        dur = wf.getnframes() / float(wf.getframerate())
    
    delay_ms = int(cur_time * 1000)
    filter_complex.append(f"[{input_idx}:a]adelay={delay_ms}|{delay_ms},volume=1.45[v{i}];")
    mix_inputs.append(f"[v{i}]")
    
    timeline.append({
        "beat": b["id"],
        "scene_index": i + 1,
        "start": round(cur_time, 2),
        "end": round(cur_time + b["target_dur"], 2),
        "voice_dur": round(dur, 2),
        "text": b["text"]
    })
    
    cur_time += b["target_dur"]

filter_complex.append(f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[outa]")

cmd_master = ["ffmpeg", "-y"] + inputs + [
    "-filter_complex", "".join(filter_complex),
    "-map", "[outa]",
    "-t", str(round(cur_time, 2)),
    "-ar", "44100", "-ac", "2",
    master_wav
]

subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"Master Audio generated: {master_wav} (Duration: {cur_time:.2f}s)")

# Save timeline JSON
timeline_path = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short\short_timeline.json"
with open(timeline_path, 'w', encoding='utf-8') as f:
    json.dump({
        "total_duration": round(cur_time, 2),
        "beats": timeline
    }, f, indent=2)

print(f"Saved timeline to: {timeline_path}")
