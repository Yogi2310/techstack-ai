import os
import sys
import asyncio
import subprocess
import edge_tts
import wave
import struct
import math

OUTPUT_DIR = r"D:\Antigravity\Pro\roblox_3d_engine"
AUDIO_OUT = os.path.join(OUTPUT_DIR, "scale_comparison_audio.wav")
VOICE = "en-US-GuyNeural"

SCRIPT = (
    "TaleBlox Scale Comparison! Who is the BIGGEST in our town? "
    "At 0.3 meters: Kevin the Frog! "
    "At 1.5 meters: Eli in his blue hoodie! "
    "At 28 meters: The Skyscraper Carrot! "
    "At 55 meters: The Mythical Golden Dragon! "
    "At 180 meters: The Mountain Colossus! "
    "And at 850 meters: The Sector 9 Titan! "
    "Who would win? Drop your vote below!"
)

async def generate_speech():
    mp3_temp = os.path.join(OUTPUT_DIR, "temp_scale_speech.mp3")
    wav_temp = os.path.join(OUTPUT_DIR, "temp_scale_speech.wav")
    print("[1] Synthesizing scale comparison speech...")
    comm = edge_tts.Communicate(SCRIPT, VOICE, rate="+16%", pitch="+2Hz")
    await comm.save(mp3_temp)
    
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_temp,
        "-ar", "44100", "-ac", "2",
        wav_temp
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wav_temp

def build_sound_track(speech_wav):
    print("[2] Building master audio with progressive bass drops...")
    with wave.open(speech_wav, 'rb') as w:
        sr = w.getframerate()
        n_frames = w.getnframes()
        channels = w.getnchannels()
        speech_bytes = w.readframes(n_frames)
    
    total_duration = 24.0
    total_samples = int(sr * total_duration)
    
    left = [0.0] * total_samples
    right = [0.0] * total_samples
    
    speech_ints = struct.unpack(f"<{n_frames * channels}h", speech_bytes)
    start_sample = int(0.4 * sr)
    for i in range(n_frames):
        if start_sample + i < total_samples:
            val_l = speech_ints[i * channels] / 32768.0
            val_r = speech_ints[i * channels + (1 if channels > 1 else 0)] / 32768.0
            left[start_sample + i] += val_l * 0.95
            right[start_sample + i] += val_r * 0.95

    # Progressive rising bass hits at each scale reveal:
    # 1: Frog (t=3.0s), 2: Eli (t=6.0s), 3: Carrot (t=9.5s), 4: Dragon (t=13.0s), 5: Colossus (t=16.5s), 6: Sector 9 (t=19.5s)
    reveals = [3.0, 6.0, 9.5, 13.0, 16.5, 19.5]
    for idx, r_time in enumerate(reveals):
        start_i = int(r_time * sr)
        hit_len = int(1.2 * sr)
        base_freq = 120 - idx * 12  # Gets deeper and more massive
        impact_vol = 0.25 + idx * 0.05
        for i in range(hit_len):
            s_idx = start_i + i
            if s_idx < total_samples:
                p = i / hit_len
                s = math.sin(2 * math.pi * base_freq * (i / sr)) * math.exp(-p * 3.5) * impact_vol
                left[s_idx] += s
                right[s_idx] += s

    # Background energetic cyber riser
    for i in range(total_samples):
        t = i / sr
        vol = min(1.0, t / 3.0) * 0.08
        if t > 21.0:
            vol *= max(0.0, 1.0 - (t - 21.0) / 3.0)
        synth = math.sin(2 * math.pi * (140 + t * 8) * t)
        left[i] += synth * vol
        right[i] += synth * vol

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
    
    print(f"[OK] Master Scale audio ready: {AUDIO_OUT} ({total_duration}s)")

if __name__ == "__main__":
    sp = asyncio.run(generate_speech())
    build_sound_track(sp)
