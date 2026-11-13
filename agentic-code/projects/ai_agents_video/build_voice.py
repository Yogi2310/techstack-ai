import os, sys, wave, subprocess
import win32com.client, pythoncom

audio_dir = r"D:\Antigravity\Pro\agentic-code\projects\ai_agents_video\audio"
os.makedirs(audio_dir, exist_ok=True)

lines = [
    ("clip1.wav", "What if your biggest engineering bottleneck isn't headcount? It's the fact that humans sleep."),
    ("clip2.wav", "Every team assumes more developers means faster shipping. But adding engineers also adds meetings, reviews, and miscommunications."),
    ("clip3.wav", "Here is the secret nobody talks about. The real cost of a software team isn't salaries, it's coordination. Every handoff is a failure point."),
    ("clip4.wav", "AI agents don't hand off. They write code, run tests, catch regressions, and deploy in one uninterrupted loop, never waiting for a Slack reply."),
    ("clip5.wav", "Companies using agentic workflows are shipping ten times faster, not by hiring more people, but by removing the waiting entirely."),
    ("clip6.wav", "So the real question isn't whether AI will replace developers. It's whether your team is building with agents, or competing against them. What do you think?")
]

pythoncom.CoInitialize()
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = -1  # Measured, clear delivery

total_duration = 0.0
results = []

for filename, text in lines:
    raw_path = os.path.join(audio_dir, filename)
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    stream.Open(raw_path, 3, False)
    speaker.AudioOutputStream = stream
    speaker.Speak(text)
    stream.Close()
    
    with wave.open(raw_path, 'r') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        dur = frames / float(rate)
        results.append((filename, dur, frames, rate))
        total_duration += dur

print(f"Generated {len(results)} clips, total speech duration: {total_duration:.2f}s")
for r in results:
    print(f"  {r[0]}: {r[1]:.2f}s ({r[3]}Hz)")
