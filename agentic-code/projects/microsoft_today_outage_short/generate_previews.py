import os, sys, subprocess

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_today_outage_short"
video_path = os.path.join(proj_dir, "MICROSOFT_TODAY_OUTAGE_SHORT_9x16.mp4")
snap_dir = os.path.join(proj_dir, "snapshots")
os.makedirs(snap_dir, exist_ok=True)

# Scene timestamps
timestamps = [
    ("outage_today_scene_1.png", "00:00:03.000"),
    ("outage_today_scene_2.png", "00:00:15.000"),
    ("outage_today_scene_3.png", "00:00:26.000"),
    ("outage_today_scene_4.png", "00:00:36.000"),
    ("outage_today_scene_5.png", "00:00:46.000"),
]

print("Extracting high-resolution snapshots...")
for fname, ts in timestamps:
    out_img = os.path.join(snap_dir, fname)
    cmd = ["ffmpeg", "-y", "-ss", ts, "-i", video_path, "-vframes", "1", "-q:v", "2", out_img]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Captured: {out_img}")

# Generate animated preview GIF (first 10 seconds, 360x640, 10fps)
gif_path = os.path.join(proj_dir, "preview_today_outage.gif")
print("Generating animated preview GIF...")
cmd_gif = [
    "ffmpeg", "-y", "-ss", "00:00:00", "-t", "10",
    "-i", video_path,
    "-vf", "fps=10,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    gif_path
]
subprocess.run(cmd_gif, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"GIF Preview created: {gif_path}")
