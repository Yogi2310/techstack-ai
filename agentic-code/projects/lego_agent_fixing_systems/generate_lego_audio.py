import os
import wave
import struct
import math
import pythoncom
import win32com.client

AUDIO_DIR = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 1. Generate Voiceover using SAPI
pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
stream = win32com.client.Dispatch("SAPI.SpFileStream")

# Pick Microsoft David or available male voice
for voice in speaker.GetVoices():
    if "David" in voice.GetDescription():
        speaker.Voice = voice
        break

speaker.Rate = 0  # Natural conversational tempo

VO_SCRIPT = (
    "Meet the Autonomous Brick Agent! When production crashes at two AM and the server rack is smoking red, "
    "this little yellow engineer springs into action. First station: Server Blade zero-one. "
    "Activating laser diagnostic... memory leak isolated, daemon restarted! All systems back to solid cyan. "
    "Next station: the Cyber Terminal. Generating automated regression tests, refactoring endpoints... "
    "all forty-two unit tests pass! "
    "Final stop: the Technic master deployment lever. Locking C-clamps into position, pulling down... "
    "One hundred percent pipeline charged! Cloud payload successfully launched into production! "
    "Ship autonomous code twenty-four seven. Subscribe for more agentic workflows!"
)

vo_path = os.path.join(AUDIO_DIR, "lego_narration.wav")
stream.Open(vo_path, 3, False)  # 3 = SSFMCreateForWrite
speaker.AudioOutputStream = stream
speaker.Speak(VO_SCRIPT)
stream.Close()
pythoncom.CoUninitialize()

# Check duration of voiceover
with wave.open(vo_path, 'rb') as wf:
    vo_frames = wf.getnframes()
    vo_rate = wf.getframerate()
    vo_channels = wf.getnchannels()
    vo_width = wf.getsampwidth()
    vo_duration = vo_frames / float(vo_rate)
    vo_raw = wf.readframes(vo_frames)

print(f"Voiceover generated: {vo_duration:.2f}s at {vo_rate}Hz, channels={vo_channels}")

# We will create an audio mix with 44100Hz mono
TARGET_RATE = 44100
total_duration = max(vo_duration + 3.0, 44.0)
total_samples = int(total_duration * TARGET_RATE)

# Unpack voiceover and resample to TARGET_RATE if needed
# SAPI typically outputs 22050Hz 16-bit mono
if vo_width == 2:
    raw_samples = struct.unpack(f"<{vo_frames * vo_channels}h", vo_raw)
    if vo_channels == 2:
        raw_samples = raw_samples[::2]
else:
    raw_samples = [0] * vo_frames

# Linear resample VO
resampled_vo = [0.0] * total_samples
step = vo_rate / TARGET_RATE
for i in range(total_samples):
    src_idx = i * step
    idx0 = int(src_idx)
    idx1 = min(idx0 + 1, len(raw_samples) - 1)
    frac = src_idx - idx0
    if idx0 < len(raw_samples):
        resampled_vo[i] = (raw_samples[idx0] * (1.0 - frac) + raw_samples[idx1] * frac) / 32768.0

# 2. Synthesize Sound Effects & Music
# Master buffer
mix = [0.0] * total_samples

# Add VO to mix (voice level ~ 0.75)
for i in range(total_samples):
    mix[i] += resampled_vo[i] * 0.85

def add_tone(buf, start_s, dur_s, freq, vol=0.2, wave_type='sine', decay=0.0):
    start_i = int(start_s * TARGET_RATE)
    dur_i = int(dur_s * TARGET_RATE)
    for j in range(dur_i):
        idx = start_i + j
        if idx >= len(buf):
            break
        t = j / TARGET_RATE
        env = math.exp(-decay * t) if decay > 0 else (1.0 - j / dur_i)
        if wave_type == 'sine':
            val = math.sin(2 * math.pi * freq * t)
        elif wave_type == 'square':
            val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        elif wave_type == 'triangle':
            val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0
        elif wave_type == 'noise':
            import random
            val = random.uniform(-1.0, 1.0)
        else:
            val = math.sin(2 * math.pi * freq * t)
        buf[idx] += val * vol * env

def add_lego_brick_click(buf, start_s, vol=0.25):
    # Distinct plastic high-Q resonant click (1200Hz + 2400Hz snap + short noise burst)
    add_tone(buf, start_s, 0.04, 1800, vol=vol, wave_type='triangle', decay=90.0)
    add_tone(buf, start_s, 0.02, 3200, vol=vol*0.6, wave_type='sine', decay=120.0)
    add_tone(buf, start_s, 0.015, 0, vol=vol*0.3, wave_type='noise', decay=150.0)

def add_laser_scan(buf, start_s, dur_s, vol=0.18):
    start_i = int(start_s * TARGET_RATE)
    dur_i = int(dur_s * TARGET_RATE)
    for j in range(dur_i):
        idx = start_i + j
        if idx >= len(buf):
            break
        t = j / TARGET_RATE
        # Sweeping FM laser pitch
        f = 500 + 350 * math.sin(2 * math.pi * 4.0 * t)
        val = math.sin(2 * math.pi * f * t) + 0.25 * math.sin(2 * math.pi * f * 2 * t)
        buf[idx] += val * vol * min(1.0, t * 5.0, (dur_s - t) * 5.0)

def add_test_pass_chord(buf, start_s, vol=0.25):
    # Bright arpeggio chime (C6, E6, G6, C7)
    notes = [1046.50, 1318.51, 1567.98, 2093.00]
    for k, n in enumerate(notes):
        add_tone(buf, start_s + k * 0.07, 0.8, n, vol=vol, wave_type='sine', decay=4.5)

def add_lever_clack(buf, start_s, vol=0.4):
    # Heavy plastic ratchet snap + mechanical thud
    add_tone(buf, start_s, 0.08, 140, vol=vol*0.8, wave_type='triangle', decay=30.0)
    add_lego_brick_click(buf, start_s, vol=vol)
    add_lego_brick_click(buf, start_s + 0.03, vol=vol*0.8)

# Schedule Action SFX:
# Act 1: Walking footsteps (0.5s to 6.5s)
for step_t in [0.5, 0.9, 1.3, 1.7, 2.1, 2.5, 2.9, 3.3, 3.7, 4.1, 4.5, 4.9, 5.3, 5.7]:
    add_lego_brick_click(mix, step_t, vol=0.18)

# Act 2: Laser scanner on broken server (9.0s to 15.0s)
add_laser_scan(mix, 9.2, 5.5, vol=0.12)
# Server reboot / fix chime at 15.2s
add_test_pass_chord(mix, 15.2, vol=0.22)

# Walking from server to cyber terminal (16.5s to 19.5s)
for step_t in [16.8, 17.2, 17.6, 18.0, 18.4, 18.8, 19.2]:
    add_lego_brick_click(mix, step_t, vol=0.16)

# Act 3: Rapid keyboard typing on cyber slope brick (20.5s to 25.5s)
import random
random.seed(42)
t_type = 20.2
while t_type < 25.5:
    add_lego_brick_click(mix, t_type, vol=0.12)
    t_type += random.uniform(0.08, 0.16)

# Test pass fanfare chime at 25.8s
add_test_pass_chord(mix, 25.8, vol=0.3)

# Walking to deployment lever (27.0s to 30.0s)
for step_t in [27.2, 27.6, 28.0, 28.4, 28.8, 29.2]:
    add_lego_brick_click(mix, step_t, vol=0.16)

# Act 4: Lever pull (31.0s)
add_lever_clack(mix, 31.0, vol=0.45)
# Power charging drone (31.2s to 34.5s)
add_tone(mix, 31.2, 3.5, 88.0, vol=0.18, wave_type='triangle', decay=0.3)
add_tone(mix, 31.2, 3.5, 176.0, vol=0.12, wave_type='sine', decay=0.3)

# Rocket uplink launch whoosh at 35.0s
start_i = int(35.0 * TARGET_RATE)
dur_i = int(2.5 * TARGET_RATE)
for j in range(dur_i):
    idx = start_i + j
    if idx >= len(mix):
        break
    t = j / TARGET_RATE
    env = math.sin(math.pi * (t / 2.5))
    mix[idx] += random.uniform(-1.0, 1.0) * 0.18 * env

# Act 5: Victory chime at 39.0s
add_test_pass_chord(mix, 39.0, vol=0.32)

# 3. Add Background Rhodes Synthesizer Chord Progression
chords = [
    (0.0, 8.0, [261.63, 329.63, 392.00, 523.25]),     # C major 7
    (8.0, 17.0, [220.00, 261.63, 329.63, 392.00]),    # A minor 7
    (17.0, 27.0, [174.61, 220.00, 261.63, 329.63]),   # F major 7
    (27.0, 37.0, [196.00, 246.94, 293.66, 392.00]),   # G dominant 7
    (37.0, total_duration, [261.63, 329.63, 392.00, 523.25]), # C major
]

for c_start, c_end, freqs in chords:
    c_dur = c_end - c_start
    c_start_i = int(c_start * TARGET_RATE)
    c_dur_i = int(c_dur * TARGET_RATE)
    for f in freqs:
        for j in range(c_dur_i):
            idx = c_start_i + j
            if idx >= len(mix):
                break
            t = j / TARGET_RATE
            env = 0.5 + 0.5 * math.sin(2 * math.pi * 0.3 * t)
            val = math.sin(2 * math.pi * f * t) + 0.3 * math.sin(2 * math.pi * 2 * f * t)
            mix[idx] += val * 0.025 * env

# Normalize and write output wav
max_val = max(abs(x) for x in mix)
gain = 0.92 / max_val if max_val > 0.92 else 1.0

out_wav = os.path.join(AUDIO_DIR, "lego_master_audio.wav")
with wave.open(out_wav, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(TARGET_RATE)
    out_bytes = bytearray()
    for s in mix:
        val = int(max(-32767, min(32767, s * gain * 32767.0)))
        out_bytes.extend(struct.pack('<h', val))
    wf.writeframes(out_bytes)

print(f"Master audio saved: {out_wav} ({total_duration:.2f}s, {total_samples} samples)")
