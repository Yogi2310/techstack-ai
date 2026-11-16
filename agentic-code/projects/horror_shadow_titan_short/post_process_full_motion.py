import os
import shutil
import base64
import subprocess

PROJECT_DIR = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short"
BRAIN_DIR = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"

SRC_VIDEO = os.path.join(PROJECT_DIR, "THE_MIDNIGHT_COLOSSUS_FULL_MOTION_3D.mp4")
BRAIN_VIDEO = os.path.join(BRAIN_DIR, "THE_MIDNIGHT_COLOSSUS_FULL_MOTION_3D.mp4")

GIF_OUTPUT = os.path.join(PROJECT_DIR, "preview_full_motion_3d.gif")
BRAIN_GIF = os.path.join(BRAIN_DIR, "preview_full_motion_3d.gif")

HTML_OUTPUT = os.path.join(PROJECT_DIR, "preview_full_motion_3d.html")
BRAIN_HTML = os.path.join(BRAIN_DIR, "preview_full_motion_3d.html")

def main():
    if not os.path.exists(SRC_VIDEO):
        print(f"Error: {SRC_VIDEO} not found!")
        return

    size_mb = os.path.getsize(SRC_VIDEO) / (1024 * 1024)
    print(f"Source video ready: {size_mb:.2f} MB")

    # 1. Copy MP4 to brain
    print("Copying MP4 to brain...")
    shutil.copyfile(SRC_VIDEO, BRAIN_VIDEO)

    # 2. Generate Looping GIF (6s preview at 15fps)
    print("Generating animated looping GIF preview...")
    cmd_gif = [
        "ffmpeg", "-y",
        "-ss", "44.0", "-t", "6.0",
        "-i", SRC_VIDEO,
        "-vf", "fps=15,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        GIF_OUTPUT
    ]
    subprocess.run(cmd_gif, check=True)
    shutil.copyfile(GIF_OUTPUT, BRAIN_GIF)
    print("GIF generated and copied to brain!")

    # 3. Base64 embed into self-contained HTML player
    print("Encoding video to Base64 for 100% reliable local browser playback...")
    with open(SRC_VIDEO, "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode("ascii")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Midnight Colossus - Full-Motion 3D Animation (Character Moving)</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: #050811;
      color: #fff;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px 20px;
    }}
    .header {{
      text-align: center;
      margin-bottom: 24px;
      max-width: 650px;
    }}
    .badge {{
      display: inline-block;
      background: #ff4757;
      color: #fff;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 12px;
      box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
    }}
    h1 {{
      font-size: 26px;
      margin-bottom: 8px;
      color: #ffffff;
    }}
    p {{
      color: #a4b0be;
      font-size: 15px;
      line-height: 1.5;
    }}
    .player-card {{
      background: #0d1322;
      border: 1px solid #1e293b;
      border-radius: 24px;
      padding: 16px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.8);
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    video {{
      width: 360px;
      height: 640px;
      border-radius: 18px;
      background: #000;
      box-shadow: 0 8px 30px rgba(0,0,0,0.9);
      outline: none;
    }}
    .info-grid {{
      margin-top: 20px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      width: 100%;
      max-width: 420px;
    }}
    .info-box {{
      background: #151f32;
      padding: 10px;
      border-radius: 12px;
      text-align: center;
      border: 1px solid #24334d;
    }}
    .info-label {{
      font-size: 11px;
      color: #747d8c;
      text-transform: uppercase;
      font-weight: 700;
    }}
    .info-val {{
      font-size: 14px;
      font-weight: 700;
      color: #f1f2f6;
      margin-top: 4px;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="badge">Continuous Character Locomotion</div>
    <h1>The Midnight Colossus of Blackwood Creek</h1>
    <p>Full 3D Character Animation: Skeletal walking, frantic gesturing, monster stomping with impact physics, and screaming sprint chase in 100% sync with sound design.</p>
  </div>

  <div class="player-card">
    <video controls autoplay loop playsinline>
      <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
      Your browser does not support the video tag.
    </video>

    <div class="info-grid">
      <div class="info-box">
        <div class="info-label">Format</div>
        <div class="info-val">Vertical 9:16</div>
      </div>
      <div class="info-box">
        <div class="info-label">Duration</div>
        <div class="info-val">55.60s</div>
      </div>
      <div class="info-box">
        <div class="info-label">Frame Rate</div>
        <div class="info-val">24 fps</div>
      </div>
    </div>
  </div>
</body>
</html>
"""
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_content)

    shutil.copyfile(HTML_OUTPUT, BRAIN_HTML)
    print("Self-contained HTML player generated and copied to brain!")

if __name__ == "__main__":
    main()
