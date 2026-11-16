import wave
import numpy as np

wav_path = r"D:\Antigravity\Pro\instagram_downloads\ig_reel_audio.wav"
with wave.open(wav_path, 'r') as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()
    duration = n_frames / float(framerate)
    data = wf.readframes(n_frames)

print(f"Channels: {n_channels}, Sample Rate: {framerate}, Duration: {duration:.2f}s")
audio_data = np.frombuffer(data, dtype=np.int16)
max_amp = np.max(np.abs(audio_data))
rms = np.sqrt(np.mean(audio_data.astype(np.float64)**2))
print(f"Max Amplitude: {max_amp}, RMS: {rms:.2f}")

# Check if speech_recognition or whisper is available
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        print("Recognized speech (Google):", text)
    except Exception as e:
        print("Google speech recognition note:", e)
except Exception as e:
    print("Speech recognition module not available:", e)
