import subprocess
import os

files = [
    r"D:\Antigravity\Pro\instagram_downloads\reel_videogame_level1.mp4",
    r"D:\Antigravity\Pro\instagram_downloads\reel_ages_backwards.mp4"
]

out_dir = r"D:\Antigravity\Pro\instagram_downloads"

for f in files:
    print(f"[*] Transcribing {os.path.basename(f)}...")
    cmd = ["whisper", f, "--model", "base", "--output_dir", out_dir, "--output_format", "txt"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[+] Finished transcribing {os.path.basename(f)}")
    else:
        print(f"[!] Error: {res.stderr}")
