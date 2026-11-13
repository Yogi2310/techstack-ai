"""
Generate TTS narration WAV files using Windows SAPI via ctypes/win32com.
"""
import subprocess, os, sys

texts = [
    "What if your biggest engineering bottleneck isn't headcount? It's the fact that humans sleep.",
    "Every team assumes more developers means faster shipping. But adding engineers also adds meetings, reviews, and miscommunications.",
    "Here is the secret nobody talks about. The real cost of a software team isn't salaries, it's coordination. Every handoff is a failure point.",
    "AI agents don't hand off. They write code, run tests, catch regressions, and deploy in one uninterrupted loop, never waiting for a Slack reply.",
    "Companies using agentic workflows are shipping ten times faster, not by hiring more people, but by removing the waiting entirely.",
    "So the real question isn't whether AI will replace developers. It's whether your team is building with agents, or competing against them. What do you think?"
]

out_dir = r"D:\Antigravity\Pro\agentic-code\projects\ai_agents_video\audio"
os.makedirs(out_dir, exist_ok=True)

for i, text in enumerate(texts, 1):
    wav_path = os.path.join(out_dir, f"clip{i}.wav").replace("\\", "/")
    # Use PowerShell one-liner with escaped text
    safe = text.replace("'", "`'").replace('"', '`"')
    ps_cmd = (
        f"Add-Type -AssemblyName System.Speech; "
        f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Rate = -2; "
        f"$s.Volume = 100; "
        f'$s.SetOutputToWaveFile("{wav_path}"); '
        f'$s.Speak("{safe}"); '
        f"$s.Dispose()"
    )
    result = subprocess.run(
        ["powershell", "-NonInteractive", "-Command", ps_cmd],
        capture_output=True, text=True
    )
    size = os.path.getsize(os.path.join(out_dir, f"clip{i}.wav")) if os.path.exists(os.path.join(out_dir, f"clip{i}.wav")) else 0
    if result.returncode == 0 and size > 1000:
        print(f"  clip{i}.wav  OK  {size//1024} KB")
    else:
        print(f"  clip{i}.wav  FAILED  rc={result.returncode}")
        if result.stderr:
            print("  STDERR:", result.stderr[:300])

print("Done.")
