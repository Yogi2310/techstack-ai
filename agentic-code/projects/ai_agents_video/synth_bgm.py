import numpy as np
import wave, math, os

def synth_piano_note(freq, duration, sr=44100, vel=0.7):
    t = np.linspace(0, duration, int(sr * duration), False)
    # Fundamental + harmonics with exponential decay
    h1 = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.5)
    h2 = 0.5 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 3.8)
    h3 = 0.25 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 5.2)
    h4 = 0.12 * np.sin(2 * np.pi * 4 * freq * t) * np.exp(-t * 7.0)
    # Soft warm strike
    attack = np.minimum(t / 0.015, 1.0)
    note = (h1 + h2 + h3 + h4) * attack * vel
    return note

def build_ambient_bgm(total_duration, out_path, sr=44100):
    # Progression: Am9 -> Fmaj7 -> Cmaj7 -> Gsus4 (warm modern tech chords)
    # Frequencies (Hz)
    chords = [
        # Am9: A2, C3, E3, G3, B3
        [110.0, 130.81, 164.81, 196.00, 246.94],
        # Fmaj7: F2, C3, E3, A3
        [87.31, 130.81, 164.81, 220.00],
        # Cmaj7: C2, G2, E3, B3
        [65.41, 98.00, 164.81, 246.94],
        # Gsus4 -> G: G2, D3, G3, C4 -> B3
        [98.00, 146.83, 196.00, 261.63]
    ]
    
    chord_len = 3.5  # seconds per chord
    total_samples = int(sr * (total_duration + 2.0))
    bgm = np.zeros(total_samples, dtype=np.float32)
    
    current_time = 0.0
    chord_idx = 0
    while current_time < total_duration:
        chord = chords[chord_idx % len(chords)]
        dur = chord_len
        # Stagger the notes slightly (gentle arpeggiation)
        for n_i, freq in enumerate(chord):
            offset = n_i * 0.08
            note_dur = dur + 1.2 - offset
            note = synth_piano_note(freq, note_dur, sr, vel=0.22)
            start_idx = int((current_time + offset) * sr)
            end_idx = min(start_idx + len(note), total_samples)
            bgm[start_idx:end_idx] += note[:end_idx - start_idx]
        
        current_time += dur
        chord_idx += 1
        
    # Gentle low rumble ambient pad
    t_full = np.linspace(0, len(bgm)/sr, len(bgm), False)
    pad = 0.06 * np.sin(2 * np.pi * 55.0 * t_full) * np.sin(2 * np.pi * 0.15 * t_full)
    bgm += pad
    
    # Normalize & soft master
    max_val = np.max(np.abs(bgm))
    if max_val > 0:
        bgm = (bgm / max_val) * 0.28  # delicate background level
        
    bgm_int = (bgm * 32767).astype(np.int16)
    with wave.open(out_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(bgm_int.tobytes())
    print(f"BGM generated: {out_path} ({len(bgm)/sr:.2f}s)")

if __name__ == '__main__':
    out_dir = r"D:\Antigravity\Pro\agentic-code\projects\ai_agents_video\audio"
    build_ambient_bgm(66.0, os.path.join(out_dir, "ambient_bgm.wav"))
