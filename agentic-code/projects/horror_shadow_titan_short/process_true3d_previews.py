import os
import subprocess
import shutil

proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short"
video_path = os.path.join(proj_dir, "THE_MIDNIGHT_COLOSSUS_TRUE_3D_9x16.mp4")
brain_dir = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"
brain_video = os.path.join(brain_dir, "THE_MIDNIGHT_COLOSSUS_TRUE_3D_9x16.mp4")

shutil.copyfile(video_path, brain_video)
print("Copied video to brain!")

# Extract snapshots
shots = [
    ("true3d_scene_1_walking.png", "00:00:05.000"),
    ("true3d_scene_2_hermit_window.png", "00:00:16.000"),
    ("true3d_scene_3_boy_turnaround.png", "00:00:27.000"),
    ("true3d_scene_4_colossus_stomp.png", "00:00:38.000"),
    ("true3d_scene_5_sprint_chase.png", "00:00:49.000")
]

for name, ts in shots:
    out_proj = os.path.join(proj_dir, "snapshots", name)
    out_brain = os.path.join(brain_dir, name)
    os.makedirs(os.path.dirname(out_proj), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", video_path, "-vframes", "1", "-q:v", "2", out_proj], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(out_proj):
        shutil.copyfile(out_proj, out_brain)
        print(f"Captured snapshot: {name}")

# Animated GIF
gif_proj = os.path.join(proj_dir, "preview_true_3d.gif")
gif_brain = os.path.join(brain_dir, "preview_true_3d.gif")
print("Generating animated preview GIF...")
subprocess.run(["ffmpeg", "-y", "-ss", "00:00:02", "-t", "12", "-i", video_path, "-vf", "fps=10,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-loop", "0", gif_proj], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if os.path.exists(gif_proj):
    shutil.copyfile(gif_proj, gif_brain)
    print("Created preview GIF!")

# Create HTML player
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Midnight Colossus - True 3D Animated Video</title>
  <style>
    body {
      background: #06080e;
      color: #f1f2f6;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      margin: 0;
      padding: 30px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }
    .badge {
      display: inline-block;
      padding: 6px 16px;
      background: rgba(46, 213, 115, 0.2);
      border: 1px solid #2ed573;
      border-radius: 30px;
      color: #2ed573;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 10px;
    }
    h1 {
      margin: 6px 0 12px 0;
      font-size: 28px;
      background: linear-gradient(135deg, #fff 0%, #2ed573 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-align: center;
    }
    .meta {
      color: #a4b0be;
      font-size: 14px;
      margin-bottom: 25px;
      text-align: center;
    }
    .video-card {
      background: rgba(18, 24, 38, 0.9);
      border: 1px solid #2f3542;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.7);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    video {
      width: 340px;
      height: 604px;
      border-radius: 14px;
      background: #000;
      box-shadow: 0 8px 30px rgba(46, 213, 115, 0.25);
      outline: none;
    }
    .footer {
      margin-top: 15px;
      color: #747d8c;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="badge">TRUE 3D CHARACTER MOTION COMPLETED</div>
  <h1>The Midnight Colossus of Blackwood Creek</h1>
  <div class="meta">Full Rigged 3D Character Animation &bull; 9:16 Vertical (720&times;1280 @ 24fps) &bull; Duration: 55.60s</div>

  <div class="video-card">
    <video controls autoplay loop playsinline src="THE_MIDNIGHT_COLOSSUS_TRUE_3D_9x16.mp4"></video>
    <div class="footer">File: <code>THE_MIDNIGHT_COLOSSUS_TRUE_3D_9x16.mp4</code> (10.84 MB)</div>
  </div>
</body>
</html>"""

with open(os.path.join(proj_dir, "preview_true_3d.html"), "w", encoding="utf-8") as f:
    f.write(html_content)
with open(os.path.join(brain_dir, "preview_true_3d.html"), "w", encoding="utf-8") as f:
    f.write(html_content)
print("HTML preview players created!")
