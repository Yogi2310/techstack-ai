import os
import sys
import asyncio
import subprocess
import edge_tts
import wave
import struct
import math

OUTPUT_DIR = r"D:\Antigravity\Pro\roblox_3d_engine"
AUDIO_OUT = os.path.join(OUTPUT_DIR, "black_onion_action_audio.wav")
VOICE = "en-US-GuyNeural"

SCRIPT = (
    "Last week, I threw the Golden Cheese and got a golden dragon. "
    "But that night... the giants started throwing food back at US! "
    "A carrot the size of a skyscraper crushed our street, "
    "and my grandma had to bench-press a tank just to survive! "
    "I ran to the forbidden vault, grabbed the pulsing Black Onion, "
    "and leaped off the water tower into the storm! "
    "It hit the giant in the chest... its red eyes turned bright blue, "
    "and it rolled over like a giant puppy! "
    "But on its collar, a glowing tag read: PROPERTY OF SECTOR 9 - DO NOT RELEASE!"
)

async def generate_speech():
    mp3_temp = os.path.join(OUTPUT_DIR, "temp_onion_speech.mp3")
    wav_temp = os.path.join(OUTPUT_DIR, "temp_onion_speech.wav")
    print("[1] Synthesizing speech with edge-tts (+15% rate)...")
    comm = edge_tts.Communicate(SCRIPT, VOICE, rate="+15%", pitch="+2Hz")
    await comm.save(mp3_temp)
    
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_temp,
        "-ar", "44100", "-ac", "2",
        wav_temp
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wav_temp

def build_sound_track(speech_wav):
    print("[2] Building master cinematic sound design track...")
    with wave.open(speech_wav, 'rb') as w:
        sr = w.getframerate()
        n_frames = w.getnframes()
        channels = w.getnchannels()
        speech_bytes = w.readframes(n_frames)
    
    speech_duration = n_frames / sr
    total_duration = 38.0  # 38 seconds full-motion short
    total_samples = int(sr * total_duration)
    
    left = [0.0] * total_samples
    right = [0.0] * total_samples
    
    speech_ints = struct.unpack(f"<{n_frames * channels}h", speech_bytes)
    start_sample = int(0.5 * sr)
    for i in range(n_frames):
        if start_sample + i < total_samples:
            val_l = speech_ints[i * channels] / 32768.0
            val_r = speech_ints[i * channels + (1 if channels > 1 else 0)] / 32768.0
            left[start_sample + i] += val_l * 0.95
            right[start_sample + i] += val_r * 0.95

    # 1. Action BGM synthesizer pad (tension riser)
    for i in range(total_samples):
        t = i / sr
        vol = min(1.0, t / 3.0) * 0.10
        if t > 32.0:
            vol *= max(0.0, 1.0 - (t - 32.0) / 6.0)
        chord = math.sin(2 * math.pi * 110.0 * t) + math.sin(2 * math.pi * 146.83 * t) + math.sin(2 * math.pi * 164.81 * t)
        left[i] += chord * vol
        right[i] += chord * vol

    # 2. Skyscraper Carrot Crash BOOM at t=8.5s
    crash_start = int(8.5 * sr)
    crash_len = int(2.5 * sr)
    for i in range(crash_len):
        idx = crash_start + i
        if idx < total_samples:
            p = i / crash_len
            freq = 60 + 30 * math.exp(-p * 3)
            vol = math.exp(-p * 2.5) * 0.45
            s = math.sin(2 * math.pi * freq * (i / sr)) * vol
            left[idx] += s
            right[idx] += s

    # 3. Water Tower Jump & Hypersonic Purple Throw at t=21.0s
    throw_start = int(21.0 * sr)
    throw_len = int(2.0 * sr)
    for i in range(throw_len):
        idx = throw_start + i
        if idx < total_samples:
            p = i / throw_len
            freq = 400 + 1500 * (1 - p)
            vol = math.sin(p * math.pi) * 0.35
            s = math.sin(2 * math.pi * freq * (i / sr)) * vol
            left[idx] += s
            right[idx] += s

    # 4. Titan Impact Flash & Tamed Chimes at t=26.5s
    tamed_start = int(26.5 * sr)
    tamed_len = int(5.0 * sr)
    for i in range(tamed_len):
        idx = tamed_start + i
        if idx < total_samples:
            t_loc = i / sr
            c = (math.sin(2 * math.pi * 523.25 * t_loc) * math.exp(-t_loc * 1.2) +
                 math.sin(2 * math.pi * 659.25 * t_loc) * math.exp(-max(0, t_loc - 0.25) * 1.2) +
                 math.sin(2 * math.pi * 783.99 * t_loc) * math.exp(-max(0, t_loc - 0.5) * 1.2) +
                 math.sin(2 * math.pi * 1046.50 * t_loc) * math.exp(-max(0, t_loc - 0.75) * 1.2)) * 0.22
            left[idx] += c
            right[idx] += c

    # 5. Mystery Sector 9 Dramatic Chord at t=33.0s
    sec_start = int(33.0 * sr)
    sec_len = int(4.5 * sr)
    for i in range(sec_len):
        idx = sec_start + i
        if idx < total_samples:
            t_loc = i / sr
            dark_chord = (math.sin(2 * math.pi * 92.5 * t_loc) + math.sin(2 * math.pi * 138.59 * t_loc)) * math.exp(-t_loc * 0.6) * 0.30
            left[idx] += dark_chord
            right[idx] += dark_chord

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
    
    print(f"[OK] Master action soundtrack ready: {AUDIO_OUT} ({total_duration}s)")

if __name__ == "__main__":
    sp = asyncio.run(generate_speech())
    build_sound_track(sp)
