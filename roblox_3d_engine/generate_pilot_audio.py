import os
import sys
import asyncio
import subprocess
import edge_tts
import wave
import struct
import math

OUTPUT_DIR = r"D:\Antigravity\Pro\roblox_3d_engine"
AUDIO_OUT = os.path.join(OUTPUT_DIR, "pilot_audio.wav")
VOICE = "en-US-GuyNeural"

PILOT_SCRIPT = (
    "In my town, you don't buy pets... you throw food off the mountain! "
    "I trained every single day, saved up, and bought the legendary Golden Cheese. "
    "I took a deep breath, and I threw it with everything I had! "
    "Suddenly, the sky turned gold... and a giant dragon bowed right in front of me!"
)

async def generate_speech():
    mp3_temp = os.path.join(OUTPUT_DIR, "temp_speech.mp3")
    wav_temp = os.path.join(OUTPUT_DIR, "temp_speech.wav")
    print("[1] Synthesizing speech with edge-tts...")
    comm = edge_tts.Communicate(PILOT_SCRIPT, VOICE, rate="+14%", pitch="+2Hz")
    await comm.save(mp3_temp)
    
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_temp,
        "-ar", "44100", "-ac", "2",
        wav_temp
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wav_temp

def build_sound_track(speech_wav):
    print("[2] Building master audio track with cinematic SFX & musical swell...")
    # Load speech
    with wave.open(speech_wav, 'rb') as w:
        sr = w.getframerate()
        n_frames = w.getnframes()
        channels = w.getnchannels()
        speech_bytes = w.readframes(n_frames)
    
    speech_duration = n_frames / sr
    total_duration = 24.5  # target duration
    total_samples = int(sr * total_duration)
    
    # Master stereo buffer
    left = [0.0] * total_samples
    right = [0.0] * total_samples
    
    # Unpack speech into master (starts at t=0.5s)
    speech_ints = struct.unpack(f"<{n_frames * channels}h", speech_bytes)
    start_sample = int(0.5 * sr)
    for i in range(n_frames):
        if start_sample + i < total_samples:
            val_l = speech_ints[i * channels] / 32768.0
            val_r = speech_ints[i * channels + (1 if channels > 1 else 0)] / 32768.0
            left[start_sample + i] += val_l * 0.95
            right[start_sample + i] += val_r * 0.95

    # 1. Add background ambient music chord (orchestral riser)
    for i in range(total_samples):
        t = i / sr
        # Base swelling pad (C major / A minor uplifting progression)
        vol = min(1.0, t / 4.0) * 0.12
        if t > 18.0:
            vol *= max(0.0, 1.0 - (t - 18.0) / 6.0)
        chord1 = math.sin(2 * math.pi * 130.81 * t) + math.sin(2 * math.pi * 164.81 * t) + math.sin(2 * math.pi * 196.00 * t)
        left[i] += chord1 * vol
        right[i] += chord1 * vol

    # 2. Add Throw Whoosh SFX at t=10.2s
    whoosh_start = int(10.2 * sr)
    whoosh_len = int(1.2 * sr)
    for i in range(whoosh_len):
        idx = whoosh_start + i
        if idx < total_samples:
            p = i / whoosh_len
            freq = 300 + 1200 * math.sin(p * math.pi)
            vol = math.sin(p * math.pi) * 0.28
            s = math.sin(2 * math.pi * freq * (i / sr)) * vol
            left[idx] += s
            right[idx] += s

    # 3. Add Earthquake Sub-Bass Tremor at t=16.5s
    tremor_start = int(16.5 * sr)
    tremor_len = int(4.0 * sr)
    for i in range(tremor_len):
        idx = tremor_start + i
        if idx < total_samples:
            p = i / tremor_len
            freq = 45 + 15 * math.sin(i * 0.05)
            vol = math.sin(p * math.pi) * 0.35
            s = math.sin(2 * math.pi * freq * (i / sr)) * vol
            left[idx] += s
            right[idx] += s

    # 4. Add Golden Dragon Chimes at t=18.5s
    chime_start = int(18.5 * sr)
    chime_len = int(5.0 * sr)
    for i in range(chime_len):
        idx = chime_start + i
        if idx < total_samples:
            t_loc = i / sr
            # Cascading sparkling sine chimes (880Hz, 1174Hz, 1318Hz, 1760Hz)
            c = (math.sin(2 * math.pi * 880 * t_loc) * math.exp(-t_loc * 1.5) +
                 math.sin(2 * math.pi * 1174 * t_loc) * math.exp(-max(0, t_loc - 0.3) * 1.5) +
                 math.sin(2 * math.pi * 1760 * t_loc) * math.exp(-max(0, t_loc - 0.7) * 1.5)) * 0.18
            left[idx] += c
            right[idx] += c

    # Normalize & write WAV
    out_ints = []
    max_amp = max(max(abs(x) for x in left), max(abs(x) for x in right), 0.001)
    scale = min(0.96 / max_amp, 1.2)
    
    for l, r in zip(left, right):
        sl = int(max(-32767, min(32767, l * scale * 32767)))
        sr_val = int(max(-32767, min(32767, r * scale * 32767)))
        out_ints.extend([sl, sr_val])

    with wave.open(AUDIO_OUT, 'wb') as out_w:
        out_w.setnchannels(2)
        out_w.setsampwidth(2)
        out_w.setframerate(sr)
        out_w.writeframes(struct.pack(f"<{len(out_ints)}h", *out_ints))
    
    print(f"[OK] Master audio track ready: {AUDIO_OUT} ({total_duration}s)")

if __name__ == "__main__":
    sp = asyncio.run(generate_speech())
    build_sound_track(sp)
