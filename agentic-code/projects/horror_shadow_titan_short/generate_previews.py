"""
Preview and Snapshot Generator for 'The Midnight Colossus of Blackwood Creek' Short
"""
import os
import subprocess
import shutil

PROJECT_DIR = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short"
VIDEO_PATH = os.path.join(PROJECT_DIR, "THE_MIDNIGHT_COLOSSUS_9x16.mp4")
SNAPSHOTS_DIR = os.path.join(PROJECT_DIR, "snapshots")
BRAIN_DIR = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"

os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

# 1. High-res snapshots
shots = [
    ("colossus_scene_1_midnight_rule.png", "00:00:05.000"),
    ("colossus_scene_2_hermit_warning.png", "00:00:16.000"),
    ("colossus_scene_3_shadow_tremor.png", "00:00:27.000"),
    ("colossus_scene_4_titan_rises.png", "00:00:38.000"),
    ("colossus_scene_5_screaming_escape.png", "00:00:49.000"),
]

print("Extracting high-resolution snapshots...")
for name, ts in shots:
    out_f = os.path.join(SNAPSHOTS_DIR, name)
    brain_f = os.path.join(BRAIN_DIR, name)
    cmd = ["ffmpeg", "-y", "-ss", ts, "-i", VIDEO_PATH, "-vframes", "1", "-q:v", "2", out_f]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(out_f):
        shutil.copyfile(out_f, brain_f)
        print(f"Captured: {out_f}")

# 2. Animated Preview GIF
gif_out = os.path.join(PROJECT_DIR, "preview_colossus.gif")
brain_gif = os.path.join(BRAIN_DIR, "preview_colossus.gif")

print("Generating animated preview GIF...")
cmd_gif = [
    "ffmpeg", "-y", "-ss", "00:00:00", "-t", "14", "-i", VIDEO_PATH,
    "-vf", "fps=10,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    "-loop", "0", gif_out
]
subprocess.run(cmd_gif, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if os.path.exists(gif_out):
    shutil.copyfile(gif_out, brain_gif)
    print(f"GIF Preview created: {gif_out}")

# Copy video to brain as well
brain_video = os.path.join(BRAIN_DIR, "THE_MIDNIGHT_COLOSSUS_9x16.mp4")
if os.path.exists(VIDEO_PATH):
    shutil.copyfile(VIDEO_PATH, brain_video)
    print(f"Copied MP4 to brain: {brain_video}")

print("Previews complete!")
