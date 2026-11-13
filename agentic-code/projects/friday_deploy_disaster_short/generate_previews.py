import os, sys, subprocess

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\friday_deploy_disaster_short"
video_path = os.path.join(proj_dir, "FRIDAY_DEPLOY_DISASTER_9x16.mp4")
snap_dir = os.path.join(proj_dir, "snapshots")
os.makedirs(snap_dir, exist_ok=True)

timestamps = [
    ("friday_scene_1_typing.png", "00:00:04.000"),
    ("friday_scene_2_red_alert.png", "00:00:15.000"),
    ("friday_scene_3_tracing_logs.png", "00:00:26.000"),
    ("friday_scene_4_hotfix_restart.png", "00:00:36.000"),
    ("friday_scene_5_readonly_rule.png", "00:00:48.000"),
]

print("Extracting high-resolution snapshots...")
for fname, ts in timestamps:
    out_img = os.path.join(snap_dir, fname)
    cmd = ["ffmpeg", "-y", "-ss", ts, "-i", video_path, "-vframes", "1", "-q:v", "2", out_img]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Captured: {out_img}")

gif_path = os.path.join(proj_dir, "preview_friday_deploy.gif")
print("Generating animated preview GIF...")
cmd_gif = [
    "ffmpeg", "-y", "-ss", "00:00:00", "-t", "10",
    "-i", video_path,
    "-vf", "fps=10,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    gif_path
]
subprocess.run(cmd_gif, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"GIF Preview created: {gif_path}")
