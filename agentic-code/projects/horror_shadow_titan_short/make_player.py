"""
Interactive Web Preview Player for 'The Midnight Colossus of Blackwood Creek' 60s Horror Short
"""
import os
import base64

PROJECT_DIR = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short"
VIDEO_PATH = os.path.join(PROJECT_DIR, "THE_MIDNIGHT_COLOSSUS_9x16.mp4")
BRAIN_DIR = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"

if not os.path.exists(VIDEO_PATH):
    print("Video file does not exist yet.")
    exit(0)

print("Reading video for data URI embedding...")
with open(VIDEO_PATH, "rb") as f:
    v_b64 = base64.b64encode(f.read()).decode('utf-8')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Midnight Colossus of Blackwood Creek - 60s Horror Short</title>
  <style>
    :root {{
      --bg: #07090e;
      --card-bg: rgba(18, 22, 32, 0.88);
      --border: #2d3748;
      --accent: #ff3838;
      --accent-glow: rgba(255, 56, 56, 0.4);
      --text: #f1f2f6;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      background: var(--bg);
      background-image: radial-gradient(circle at 50% 20%, #1a0808 0%, #07090e 70%);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 30px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }}
    .header {{
      text-align: center;
      max-width: 800px;
      margin-bottom: 25px;
    }}
    .badge {{
      display: inline-block;
      padding: 6px 16px;
      background: rgba(255, 56, 56, 0.2);
      border: 1px solid var(--accent);
      border-radius: 30px;
      color: #ff6b81;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      box-shadow: 0 0 15px var(--accent-glow);
    }}
    h1 {{
      font-size: 32px;
      margin: 12px 0 6px 0;
      background: linear-gradient(135deg, #fff 0%, #ff7675 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .meta {{
      color: #a4b0be;
      font-size: 14px;
    }}
    .container {{
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      gap: 32px;
      justify-content: center;
      max-width: 1100px;
      width: 100%;
    }}
    .player-wrap {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 18px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.6);
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    video {{
      width: 320px;
      height: 568px;
      border-radius: 14px;
      background: #000;
      box-shadow: 0 6px 30px rgba(255, 56, 56, 0.25);
      outline: none;
    }}
    .details-wrap {{
      flex: 1;
      min-width: 340px;
      max-width: 620px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 24px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    }}
    h2 {{
      font-size: 20px;
      margin-top: 0;
      color: #ff6b81;
      border-bottom: 1px solid #2f3542;
      padding-bottom: 10px;
    }}
    .beat-card {{
      margin-bottom: 14px;
      padding: 12px 16px;
      background: rgba(255,255,255,0.03);
      border-left: 3px solid var(--accent);
      border-radius: 0 10px 10px 0;
    }}
    .beat-time {{
      font-weight: 700;
      font-size: 13px;
      color: #ff7675;
      margin-bottom: 3px;
    }}
    .beat-desc {{
      font-size: 14px;
      color: #ced6e0;
      line-height: 1.45;
    }}
    .action-box {{
      margin-top: 24px;
      padding: 16px;
      background: rgba(255, 56, 56, 0.08);
      border: 1px solid rgba(255, 56, 56, 0.3);
      border-radius: 12px;
      font-size: 14px;
    }}
    .btn {{
      display: inline-block;
      margin-top: 10px;
      padding: 10px 20px;
      background: #ff4757;
      color: #fff;
      text-decoration: none;
      border-radius: 8px;
      font-weight: 700;
      box-shadow: 0 4px 15px rgba(255,71,87,0.4);
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="badge">Original 60s 3D Horror Animation</div>
    <h1>The Midnight Colossus of Blackwood Creek</h1>
    <div class="meta">
      Format: <b>9:16 Vertical (1080&times;1920)</b> &bull; Duration: <b>55.60s</b> &bull; Style: <b>Stylized 3D Unreal Horror</b>
    </div>
  </div>

  <div class="container">
    <div class="player-wrap">
      <video controls autoplay loop playsinline src="data:video/mp4;base64,{v_b64}"></video>
      <div style="margin-top: 12px; font-size: 12px; color: #747d8c;">
        Target Channel: <b>@TechStacAI</b> &bull; YouTube Shorts & Instagram Reels
      </div>
    </div>

    <div class="details-wrap">
      <h2>🎬 Story & Scene Progression (55.60s)</h2>

      <div class="beat-card">
        <div class="beat-time">0:00 – 0:11 | Beat 1: The Midnight Curfew</div>
        <div class="beat-desc">
          <i>"Rule #1 of Blackwood Creek: When the village bells strike thirteen at midnight... you do not stay out in the mist."</i><br>
          Dense volumetric fog, damp gravel reflections, warm hanging lanterns, and an ominous blood-orange moon.
        </div>
      </div>

      <div class="beat-card">
        <div class="beat-time">0:11 – 0:22 | Beat 2: The Hermit's Iron Key</div>
        <div class="beat-desc">
          <i>"Old Man Miller slammed open his shutter, tossing down a rusted iron key! 'KID! Get inside... he's off the chain!'"</i><br>
          A terrified old hermit frantically shouts from the second-story attic window as yellow warning lanterns flicker.
        </div>
      </div>

      <div class="beat-card">
        <div class="beat-time">0:22 – 0:33 | Beat 3: Dead Silence & The Tremor</div>
        <div class="beat-desc">
          <i>"Then... the street went dead silent. The puddles began to ripple. An immense shadow stretched forty feet across the road."</i><br>
          Heartbeat pulse audio effect; water ripples; camera zooms with each accelerating heartbeat.
        </div>
      </div>

      <div class="beat-card">
        <div class="beat-time">0:33 – 0:44 | Beat 4: The Colossus Rises</div>
        <div class="beat-desc">
          <i>"Rising out of the black pines was the Colossus of Hollow Creek! Two burning red eyes... and a jaw of razor fangs!"</i><br>
          Massive 40-foot monolithic shadow beast towers above the pines with glowing neon red eyes and razor teeth.
        </div>
      </div>

      <div class="beat-card">
        <div class="beat-time">0:44 – 0:55 | Beat 5: The Screaming Sprint</div>
        <div class="beat-desc">
          <i>"With a bone-shattering roar, it charged! I lunged for the cabin door as its claws slammed into the dirt behind me! Did I make it in time? Comment for Part 2!"</i><br>
          Extreme camera shake, red alert flashing, claw slamming into gravel, boy screaming in terror before sudden cut to black!
        </div>
      </div>

      <div class="action-box">
        <b>💡 Audience Retention Formula:</b>
        <p style="margin: 6px 0 0 0; color: #a4b0be; font-size: 13.5px;">
          Engineered with an immediate 3-second hook ("Thirteenth bell"), accelerating heartbeat pacing, visceral scale reveal, and a heart-stopping cliffhanger that drives thousands of comments demanding "Part 2".
        </p>
      </div>
    </div>
  </div>
</body>
</html>
"""

html_proj = os.path.join(PROJECT_DIR, "preview_colossus.html")
html_brain = os.path.join(BRAIN_DIR, "preview_colossus.html")

with open(html_proj, "w", encoding="utf-8") as f:
    f.write(html_content)
with open(html_brain, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Embedded player created successfully! Brain: {os.path.getsize(html_brain)} bytes, Proj: {os.path.getsize(html_proj)} bytes")
