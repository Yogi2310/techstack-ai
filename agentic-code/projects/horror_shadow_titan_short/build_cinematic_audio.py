"""
Ultra-Realistic Cinematic Horror Audio Production Pipeline
Produces a 55.60s Hollywood-grade sound design for 'The Midnight Colossus':
1. Distinct character voices (Narrator, Shouting Old Man Miller, Screaming Boy).
2. Thunderous seismic footsteps, guttural monster roar, 13 midnight bell tolls,
   racing panic heartbeats, howling wind, wet running footsteps, and heavy panting.
3. Mastered in 44.1kHz 16-bit Stereo WAV with sub-bass impact and dynamic EQ.
"""
import os
import subprocess
import numpy as np
from gtts import gTTS

AUDIO_DIR = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short\audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

SR = 44100
TOTAL_DUR = 55.60
TOTAL_SAMPLES = int(TOTAL_DUR * SR)

print("[1] Synthesizing Character Dialogue Tracks...")

# Dialogue scripts per act
dialogues = [
    {
        "id": "act1_narrator",
        "text": "Rule number one of Blackwood Creek. When the midnight bells strike thirteen... you do not stay out in the mist.",
        "lang": "en",
        "tld": "co.uk",
        # Deep cinematic horror narrator filter
        "filter": "rubberband=pitch=0.82,atempo=1.02,equalizer=f=110:width_type=h:width=90:g=8,equalizer=f=3200:width_type=h:width=1200:g=3,aecho=0.8:0.85:35:0.22,volume=1.5",
        "time_start": 0.8
    },
    {
        "id": "act2_miller",
        "text": "Turn back boy! Get off the road! It awakens!",
        "lang": "en",
        "tld": "com",
        # Frantic, cracked elderly shout from attic window
        "filter": "atempo=1.15,rubberband=pitch=1.12,highpass=f=260,lowpass=f=4500,aecho=0.8:0.88:45:0.35,volume=2.2",
        "time_start": 12.0
    },
    {
        "id": "act3_narrator",
        "text": "Then the wind died. And the ground began to tremble.",
        "lang": "en",
        "tld": "co.uk",
        "filter": "rubberband=pitch=0.80,atempo=0.96,equalizer=f=100:width_type=h:width=80:g=9,aecho=0.8:0.85:40:0.28,volume=1.6",
        "time_start": 22.8
    },
    {
        "id": "act4_narrator",
        "text": "A forty-foot titan emerged from the mist, towering over the pine trees.",
        "lang": "en",
        "tld": "co.uk",
        "filter": "rubberband=pitch=0.82,atempo=1.04,equalizer=f=120:width_type=h:width=90:g=7,aecho=0.8:0.85:35:0.25,volume=1.5",
        "time_start": 33.5
    },
    {
        "id": "act5_scream",
        "text": "Run! Don't look back! Run!",
        "lang": "en",
        "tld": "com",
        # Desperate vocal scream
        "filter": "atempo=1.20,rubberband=pitch=1.15,equalizer=f=2800:width_type=h:width=1000:g=6,aecho=0.8:0.88:30:0.32,volume=2.4",
        "time_start": 44.5
    }
]

dialogue_track = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)

for d in dialogues:
    raw_mp3 = os.path.join(AUDIO_DIR, f"{d['id']}_raw.mp3")
    proc_wav = os.path.join(AUDIO_DIR, f"{d['id']}_proc.wav")
    
    tts = gTTS(text=d["text"], lang=d["lang"], tld=d["tld"], slow=False)
    tts.save(raw_mp3)
    
    cmd = [
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", d["filter"],
        "-ar", str(SR), "-ac", "2", proc_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Load into dialogue track
    import wave
    with wave.open(proc_wav, 'rb') as wf:
        n_frames = wf.getnframes()
        data = np.frombuffer(wf.readframes(n_frames), dtype=np.int16).astype(np.float32) / 32768.0
        data = data.reshape(-1, 2)
        
        start_idx = int(d["time_start"] * SR)
        end_idx = min(TOTAL_SAMPLES, start_idx + len(data))
        dialogue_track[start_idx:end_idx] += data[:end_idx - start_idx]
    
    print(f"Processed dialogue: {d['id']} at {d['time_start']}s")

print("\n[2] Synthesizing Procedural Sound Effects & Horror Ambience...")

sfx_track = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
t = np.linspace(0, TOTAL_DUR, TOTAL_SAMPLES, endpoint=False)

# A. Deep Sub-Bass Tension Drone & Night Wind
wind_rumble = np.sin(2 * np.pi * 38 * t) * 0.12 + np.sin(2 * np.pi * 54 * t) * 0.08
wind_noise = np.random.normal(0, 0.04, TOTAL_SAMPLES).astype(np.float32)
wind_filter = np.convolve(wind_noise, np.ones(600) / 600, mode='same')
sfx_track[:, 0] += wind_rumble + wind_filter * 1.8
sfx_track[:, 1] += wind_rumble + wind_filter * 1.8

# B. 13 Midnight Church Bell Tolls in Act 1
print("Synthesizing 13 ominous church bell tolls...")
bell_times = [0.2, 1.0, 1.8, 2.6, 3.4, 4.2, 5.0, 5.8, 6.6, 7.4, 8.2, 9.0, 9.8]
for bt in bell_times:
    idx = int(bt * SR)
    dur = 2.8
    n_bell = int(dur * SR)
    if idx + n_bell < TOTAL_SAMPLES:
        tb = np.linspace(0, dur, n_bell, endpoint=False)
        decay = np.exp(-2.2 * tb)
        # Deep hollow bronze bell resonance
        bell = (
            np.sin(2 * np.pi * 146.8 * tb) * 1.0 +     # D3 fundamental
            np.sin(2 * np.pi * 293.6 * tb) * 0.55 +    # Octave
            np.sin(2 * np.pi * 440.0 * tb) * 0.35 +    # Fifth
            np.sin(2 * np.pi * 698.4 * tb) * 0.18      # Minor third
        ) * decay * 0.28
        sfx_track[idx:idx+n_bell, 0] += bell * 0.9
        sfx_track[idx:idx+n_bell, 1] += bell * 1.1

# C. Wooden Window Shutter SLAM & Creak at 11.2s (Old Man Miller)
shutter_idx = int(11.2 * SR)
shutter_len = int(1.2 * SR)
ts = np.linspace(0, 1.2, shutter_len, endpoint=False)
slam = np.random.normal(0, 0.6, shutter_len) * np.exp(-12 * ts)
creak = np.sin(2 * np.pi * (240 + 80 * np.sin(ts * 18)) * ts) * np.exp(-3.5 * ts) * 0.35
sfx_track[shutter_idx:shutter_idx+shutter_len, 0] += (slam + creak) * 0.8
sfx_track[shutter_idx:shutter_idx+shutter_len, 1] += (slam + creak) * 0.8

# D. Seismic Footstep Impacts (Acts 4 & 5)
print("Synthesizing seismic colossal footstep thuds...")
stomp_times = [
    # Act 4 Colossus Stomps (t=33s to 44s, stompCycle freq 2.4 rad/s => step every ~1.3s)
    33.6, 34.9, 36.2, 37.5, 38.8, 40.1, 41.4, 42.7,
    # Act 5 Chasing Stomps (t=44s to 55.6s, faster cadence every ~0.95s)
    44.4, 45.35, 46.3, 47.25, 48.2, 49.15, 50.1, 51.05, 52.0, 52.95, 53.9, 54.85
]

for st in stomp_times:
    s_idx = int(st * SR)
    dur = 0.95
    n_st = int(dur * SR)
    if s_idx + n_st < TOTAL_SAMPLES:
        t_st = np.linspace(0, dur, n_st, endpoint=False)
        decay = np.exp(-7.5 * t_st)
        # 60Hz to 28Hz sub-bass earthquake sweep
        freq = 60.0 * np.exp(-5.0 * t_st) + 26.0
        phase = 2 * np.pi * np.cumsum(freq) / SR
        sub_thud = np.sin(phase) * decay * 1.6
        # Ground gravel crunch
        crunch = np.random.normal(0, 0.35, n_st) * np.exp(-18 * t_st)
        sfx_track[s_idx:s_idx+n_st, 0] += sub_thud + crunch
        sfx_track[s_idx:s_idx+n_st, 1] += sub_thud + crunch

# E. Blood-Curdling Demonic Colossus Roars (t=27.5s reveal and t=44.0s sprint charge)
print("Synthesizing monstrous demonic Colossus roars...")
roar_moments = [(27.2, 4.2, 1.4), (43.8, 5.0, 2.0)]
for (r_start, r_dur, r_vol) in roar_moments:
    r_idx = int(r_start * SR)
    n_r = int(r_dur * SR)
    if r_idx + n_r < TOTAL_SAMPLES:
        tr = np.linspace(0, r_dur, n_r, endpoint=False)
        # Dual-frequency guttural frequency modulation (monster growl)
        mod = np.sin(2 * np.pi * 32 * tr) * 45.0
        carrier_freq = 135.0 * np.exp(-0.4 * tr) + mod
        phase = 2 * np.pi * np.cumsum(carrier_freq) / SR
        growl = np.sin(phase)
        # Add harmonic distortion and rasp
        growl = np.clip(growl * 2.5, -1.0, 1.0)
        # Stereo screech overlay
        screech = np.sin(2 * np.pi * (380 + 120 * np.sin(tr * 15)) * tr) * 0.35
        # Envelope: swell then sustain then fade
        env = np.minimum(tr / 0.4, 1.0) * np.exp(-0.55 * tr)
        roar_sound = (growl + screech) * env * r_vol * 0.45
        sfx_track[r_idx:r_idx+n_r, 0] += roar_sound * 0.95
        sfx_track[r_idx:r_idx+n_r, 1] += roar_sound * 1.05

# F. Panicked Racing Heartbeat (accelerates across the short)
print("Synthesizing accelerating panic heartbeat...")
hb_times = []
# Act 1: Calm 70 bpm (every 0.85s)
cur = 0.5
while cur < 22.0:
    hb_times.append((cur, 0.35))
    hb_times.append((cur + 0.18, 0.22))
    cur += 0.90

# Act 3: Rising dread 95 bpm (every 0.63s)
cur = 22.0
while cur < 33.0:
    hb_times.append((cur, 0.65))
    hb_times.append((cur + 0.15, 0.45))
    cur += 0.63

# Act 4: Heavy pounding 120 bpm (every 0.50s)
cur = 33.0
while cur < 44.0:
    hb_times.append((cur, 0.90))
    hb_times.append((cur + 0.13, 0.70))
    cur += 0.50

# Act 5: Maximum terror 160 bpm (every 0.375s)
cur = 44.0
while cur < 55.6:
    hb_times.append((cur, 1.25))
    hb_times.append((cur + 0.11, 0.95))
    cur += 0.375

for (hbt, vol) in hb_times:
    idx = int(hbt * SR)
    dur = 0.18
    n_hb = int(dur * SR)
    if idx + n_hb < TOTAL_SAMPLES:
        thb = np.linspace(0, dur, n_hb, endpoint=False)
        hb_wave = np.sin(2 * np.pi * 58 * thb) * np.exp(-18 * thb) * vol * 0.35
        sfx_track[idx:idx+n_hb, 0] += hb_wave
        sfx_track[idx:idx+n_hb, 1] += hb_wave

# G. Rapid Running Cobblestone Footsteps & Heavy Panting in Act 5
print("Synthesizing Act 5 rapid running footsteps and panicked panting...")
step_times = np.linspace(44.0, 55.5, int((55.5 - 44.0) * 5.5)) # ~5.5 steps per sec
for st in step_times:
    idx = int(st * SR)
    dur = 0.08
    n_step = int(dur * SR)
    if idx + n_step < TOTAL_SAMPLES:
        t_step = np.linspace(0, dur, n_step, endpoint=False)
        # Crisp wet shoe slap
        slap = (np.sin(2 * np.pi * 850 * t_step) + np.random.normal(0, 0.4, n_step)) * np.exp(-35 * t_step) * 0.35
        sfx_track[idx:idx+n_step, 0] += slap
        sfx_track[idx:idx+n_step, 1] += slap

# Panting breath sounds
for pt in np.linspace(44.2, 55.0, 14):
    idx = int(pt * SR)
    dur = 0.45
    n_p = int(dur * SR)
    if idx + n_p < TOTAL_SAMPLES:
        tp = np.linspace(0, dur, n_p, endpoint=False)
        pant = np.random.normal(0, 0.18, n_p) * np.sin(np.pi * tp / dur) * 0.28
        sfx_track[idx:idx+n_p, 0] += pant
        sfx_track[idx:idx+n_p, 1] += pant

print("\n[3] Final Master Mixing & Limiting...")
# Combine dialogue and SFX with dynamic balance
master = dialogue_track * 1.1 + sfx_track * 0.85

# Soft brickwall limiting to prevent clipping
peak = np.max(np.abs(master))
if peak > 0.95:
    print(f"Limiting peak: {peak:.2f} -> 0.95")
    master = master * (0.95 / peak)

# Convert to 16-bit PCM
pcm_data = (master * 32767.0).astype(np.int16)

OUTPUT_MASTER = os.path.join(AUDIO_DIR, "horror_master_audio.wav")
import wave
with wave.open(OUTPUT_MASTER, 'wb') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(pcm_data.tobytes())

size_mb = os.path.getsize(OUTPUT_MASTER) / (1024 * 1024)
print(f"Master Horror Audio successfully rendered: {OUTPUT_MASTER}")
print(f"Duration: {TOTAL_DUR:.2f}s | Channels: 2 | Sample Rate: {SR}Hz | Size: {size_mb:.2f} MB")
