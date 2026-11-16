import os
import math
import wave
import struct
import random
import asyncio
import subprocess
import edge_tts

PROJECT_DIR = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short"
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE_BOY = "en-US-AnaNeural"
VOICE_MILLER = "en-US-ChristopherNeural"
VOICE_NARRATOR = "en-GB-RyanNeural"

# Lines and timecodes
# Total duration: 55.6s
DIALOGUE_SPECS = [
    # Act 1: Boy walking into empty street
    {"id": "boy_act1", "voice": VOICE_BOY, "text": "Why is everyone hiding? Where did everybody go?", "rate": "-4%", "pitch": "+2Hz", "start_t": 2.5},
    # Act 2: Miller screams from attic window
    {"id": "miller_act2_1", "voice": VOICE_MILLER, "text": "Turn back, boy! Get off the road! It knows when someone's outside!", "rate": "+12%", "pitch": "+6Hz", "start_t": 12.0},
    {"id": "boy_act2_2", "voice": VOICE_BOY, "text": "What are you talking about?! What knows?!", "rate": "+8%", "pitch": "+8Hz", "start_t": 17.5},
    # Act 3: Miller warning & tremor
    {"id": "miller_act3", "voice": VOICE_MILLER, "text": "The creature! Behind you!", "rate": "+18%", "pitch": "+10Hz", "start_t": 23.0},
    # Act 5: Screaming sprint
    {"id": "boy_act5_1", "voice": VOICE_BOY, "text": "No! Don't look back... RUN!", "rate": "+24%", "pitch": "+14Hz", "start_t": 44.5},
    {"id": "boy_act5_2", "voice": VOICE_BOY, "text": "Help! Somebody help me!", "rate": "+22%", "pitch": "+16Hz", "start_t": 49.0}
]

async def generate_speech_clips():
    print("Generating neural speech clips via edge-tts 7.3.1...")
    for d in DIALOGUE_SPECS:
        out_path = os.path.join(AUDIO_DIR, f"{d['id']}.mp3")
        wav_path = os.path.join(AUDIO_DIR, f"{d['id']}.wav")
        print(f"Synthesizing [{d['id']}]: '{d['text']}' with {d['voice']}...")
        comm = edge_tts.Communicate(d['text'], d['voice'], rate=d['rate'], pitch=d['pitch'])
        await comm.save(out_path)
        # Convert to 44.1kHz WAV
        subprocess.run([
            "ffmpeg", "-y", "-i", out_path,
            "-ar", "44100", "-ac", "2",
            wav_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Generated: {wav_path}")

def generate_pro_sound_effects(sample_rate=44100, duration=55.6):
    print("Synthesizing cinematic horror environment & creature foley...")
    total_samples = int(sample_rate * duration)
    mix_l = [0.0] * total_samples
    mix_r = [0.0] * total_samples

    # 1. Low Ominous Horror Drone (40Hz - 65Hz pulsating)
    for i in range(total_samples):
        t = i / sample_rate
        drone1 = math.sin(2 * math.pi * 42.0 * t) * 0.08
        drone2 = math.sin(2 * math.pi * 55.0 * t + math.sin(t * 0.3) * 2.0) * 0.06
        sub = math.sin(2 * math.pi * 28.0 * t) * 0.05
        wind = (random.random() * 2.0 - 1.0) * 0.02 * (0.8 + 0.3 * math.sin(t * 0.4))
        val = drone1 + drone2 + sub + wind
        mix_l[i] += val
        mix_r[i] += val

    # 2. Resonant Church Bell Tolls (Act 1: 0.5s, 3.5s, 6.5s, 9.5s)
    bell_times = [0.5, 3.5, 6.5, 9.5]
    for bt in bell_times:
        start_idx = int(bt * sample_rate)
        bell_len = int(3.2 * sample_rate)
        for j in range(bell_len):
            idx = start_idx + j
            if idx >= total_samples: break
            t_rel = j / sample_rate
            env = math.exp(-t_rel * 1.4)
            # Bell fundamental & eerie overtones
            b = (math.sin(2 * math.pi * 146.8 * t_rel) * 0.4 +
                 math.sin(2 * math.pi * 220.0 * t_rel) * 0.25 +
                 math.sin(2 * math.pi * 370.0 * t_rel) * 0.15 +
                 math.sin(2 * math.pi * 587.3 * t_rel) * 0.08) * env * 0.28
            mix_l[idx] += b * 0.8
            mix_r[idx] += b * 0.9

    # 3. Wooden Shutter Slam Bang (at 11.2s when Miller throws open the window)
    shutter_idx = int(11.2 * sample_rate)
    shutter_len = int(1.2 * sample_rate)
    for j in range(shutter_len):
        idx = shutter_idx + j
        if idx >= total_samples: break
        t_rel = j / sample_rate
        env = math.exp(-t_rel * 9.0)
        # Heavy wood impact crack
        crack = (random.random() * 2.0 - 1.0) * env * 0.45
        wood_res = math.sin(2 * math.pi * 110.0 * t_rel) * env * 0.35
        mix_l[idx] += (crack + wood_res) * 0.9
        mix_r[idx] += (crack + wood_res) * 0.6

    # 4. Accelerating Panic Heartbeat (Starts at 23.0s, peaks at 55s from 75bpm to 170bpm)
    cur_t = 23.0
    while cur_t < duration:
        prog = (cur_t - 23.0) / (duration - 23.0)
        bpm = 75.0 + prog * 95.0 # up to 170 bpm
        interval = 60.0 / bpm

        # Lub-Dub double thump
        for thump_offset, amp_mult in [(0.0, 1.0), (0.11, 0.7)]:
            thump_t = cur_t + thump_offset
            if thump_t >= duration: break
            s_idx = int(thump_t * sample_rate)
            t_len = int(0.22 * sample_rate)
            for j in range(t_len):
                idx = s_idx + j
                if idx >= total_samples: break
                t_rel = j / sample_rate
                env = math.exp(-t_rel * 22.0)
                freq = 52.0 - t_rel * 40.0
                h = math.sin(2 * math.pi * max(20.0, freq) * t_rel) * env * 0.32 * amp_mult * (0.6 + prog * 0.5)
                mix_l[idx] += h
                mix_r[idx] += h

        cur_t += interval

    # 5. Massive Seismic Stomps & Creature Roars (Act 4 & Act 5)
    # Stomps: 34.0, 36.5, 39.0, 41.5, 45.0, 47.2, 49.4, 51.6, 53.8
    stomp_times = [34.0, 36.5, 39.0, 41.5, 45.0, 47.2, 49.4, 51.6, 53.8]
    for st in stomp_times:
        s_idx = int(st * sample_rate)
        s_len = int(1.4 * sample_rate)
        is_chase = st >= 44.0
        amp = 0.55 if is_chase else 0.45
        for j in range(s_len):
            idx = s_idx + j
            if idx >= total_samples: break
            t_rel = j / sample_rate
            env = math.exp(-t_rel * 4.5)
            # Pitch drop sub-bass 75Hz -> 25Hz
            f = 75.0 - t_rel * 48.0
            sub_stomp = math.sin(2 * math.pi * max(22.0, f) * t_rel) * env * amp
            dirt_crunch = (random.random() * 2.0 - 1.0) * math.exp(-t_rel * 14.0) * 0.25
            mix_l[idx] += sub_stomp + dirt_crunch
            mix_r[idx] += sub_stomp + dirt_crunch

    # Creature Roars: 28.5s (distant eerie), 35.5s (full roar), 46.5s (climactic screech)
    roar_events = [
        {"t": 28.5, "dur": 3.5, "amp": 0.28, "base_f": 90.0},
        {"t": 35.5, "dur": 4.0, "amp": 0.48, "base_f": 115.0},
        {"t": 46.5, "dur": 4.5, "amp": 0.58, "base_f": 140.0}
    ]
    for r in roar_events:
        r_idx = int(r["t"] * sample_rate)
        r_len = int(r["dur"] * sample_rate)
        for j in range(r_len):
            idx = r_idx + j
            if idx >= total_samples: break
            t_rel = j / sample_rate
            env = math.sin((t_rel / r["dur"]) * math.pi) ** 1.8
            mod = math.sin(2 * math.pi * 32.0 * t_rel) * 0.4
            noise = (random.random() * 2.0 - 1.0) * 0.35
            f1 = r["base_f"] + math.sin(t_rel * 4.0) * 25.0
            f2 = r["base_f"] * 0.65
            tone = (math.sin(2 * math.pi * f1 * t_rel) + 0.6 * math.sin(2 * math.pi * f2 * t_rel) + noise) * (1.0 + mod)
            val = tone * env * r["amp"]
            mix_l[idx] += val * 0.95
            mix_r[idx] += val * 1.05

    # 6. Sprint Footsteps & Heavy Panting (Act 5: 44.0s - 55.6s)
    # Rapid gravel running footsteps (approx 3.2 per second)
    run_t = 44.2
    step_toggle = True
    while run_t < duration:
        r_idx = int(run_t * sample_rate)
        r_len = int(0.18 * sample_rate)
        for j in range(r_len):
            idx = r_idx + j
            if idx >= total_samples: break
            t_rel = j / sample_rate
            env = math.exp(-t_rel * 28.0)
            gravel = (random.random() * 2.0 - 1.0) * env * 0.22
            thud = math.sin(2 * math.pi * 120.0 * t_rel) * env * 0.18
            if step_toggle:
                mix_l[idx] += (gravel + thud) * 0.9
                mix_r[idx] += (gravel + thud) * 0.5
            else:
                mix_l[idx] += (gravel + thud) * 0.5
                mix_r[idx] += (gravel + thud) * 0.9
        step_toggle = not step_toggle
        run_t += 0.30

    # Panting breaths
    pant_t = 44.6
    while pant_t < duration:
        p_idx = int(pant_t * sample_rate)
        p_len = int(0.45 * sample_rate)
        for j in range(p_len):
            idx = p_idx + j
            if idx >= total_samples: break
            t_rel = j / sample_rate
            env = math.sin((t_rel / 0.45) * math.pi)
            breath = (random.random() * 2.0 - 1.0) * env * 0.16
            mix_l[idx] += breath
            mix_r[idx] += breath
        pant_t += 0.75

    # Save SFX track
    sfx_wav = os.path.join(AUDIO_DIR, "cinematic_sfx_track.wav")
    with wave.open(sfx_wav, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        out_bytes = bytearray()
        for i in range(total_samples):
            # Soft limiter
            sl = max(-0.95, min(0.95, mix_l[i]))
            sr = max(-0.95, min(0.95, mix_r[i]))
            out_bytes.extend(struct.pack("<hh", int(sl * 32767), int(sr * 32767)))
        f.writeframes(out_bytes)
    print(f"SFX track generated: {sfx_wav}")
    return sfx_wav

def assemble_master_audio(sfx_wav):
    print("Layering neural speech clips over cinematic SFX using FFmpeg...")
    master_wav = os.path.join(AUDIO_DIR, "horror_master_audio.wav")
    
    # Build ffmpeg filter_complex
    inputs = ["-i", sfx_wav]
    filter_parts = []
    mix_inputs = ["[0:a]"]
    
    for idx, d in enumerate(DIALOGUE_SPECS, start=1):
        wav_file = os.path.join(AUDIO_DIR, f"{d['id']}.wav")
        inputs.extend(["-i", wav_file])
        delay_ms = int(d["start_t"] * 1000)
        
        # Add slight reverb/delay to Miller for attic acoustic
        if "miller" in d["id"]:
            filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},aecho=0.8:0.7:35:0.3[a{idx}]")
        else:
            filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[a{idx}]")
        mix_inputs.append(f"[a{idx}]")
    
    filter_complex = f"{';'.join(filter_parts)};{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=2,alimiter=limit=0.92[out]"
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "44100", "-ac", "2",
        master_wav
    ]
    
    subprocess.run(cmd, check=True)
    size_mb = os.path.getsize(master_wav) / (1024 * 1024)
    print(f"Master Horror Audio Track Completed: {master_wav} ({size_mb:.2f} MB)")

async def main():
    await generate_speech_clips()
    sfx_wav = generate_pro_sound_effects()
    assemble_master_audio(sfx_wav)

if __name__ == "__main__":
    asyncio.run(main())
