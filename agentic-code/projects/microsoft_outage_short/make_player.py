import base64
import os

video_path = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_outage_short\MICROSOFT_OUTAGE_SHORT_9x16.mp4"
with open(video_path, "rb") as f:
    b64_data = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TechStack AI - Microsoft/CrowdStrike Global Outage Short Preview</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #080d1a;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 24px;
    }}
    header {{
      text-align: center;
      margin-bottom: 24px;
      max-width: 800px;
    }}
    .badge {{
      display: inline-block;
      background: rgba(239, 68, 68, 0.15);
      color: #ef4444;
      border: 1px solid #ef4444;
      border-radius: 999px;
      padding: 6px 16px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    h1 {{
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.3;
      margin-bottom: 8px;
    }}
    p.subtitle {{
      color: #94a3b8;
      font-size: 14px;
    }}
    .player-container {{
      display: flex;
      gap: 32px;
      max-width: 1100px;
      width: 100%;
      justify-content: center;
      align-items: flex-start;
      flex-wrap: wrap;
    }}
    .video-wrapper {{
      position: relative;
      width: 360px;
      height: 640px;
      background: #000;
      border-radius: 28px;
      overflow: hidden;
      box-shadow: 0 25px 60px -15px rgba(239, 68, 68, 0.35), 0 0 0 2px rgba(239, 68, 68, 0.4);
    }}
    video {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .sidebar {{
      flex: 1;
      min-width: 320px;
      max-width: 480px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .card {{
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 16px;
      padding: 20px;
    }}
    .card h2 {{
      font-size: 16px;
      color: #38bdf8;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .timeline-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 12px;
      background: #1e293b;
      border-radius: 10px;
      margin-bottom: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .timeline-item:hover {{
      background: #334155;
      transform: translateX(4px);
      border-left: 3px solid #ef4444;
    }}
    .timeline-title {{
      font-size: 13px;
      font-weight: 600;
    }}
    .timeline-time {{
      font-size: 12px;
      color: #f87171;
      font-family: monospace;
      font-weight: 700;
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 8px;
    }}
    .stat-box {{
      background: #1e293b;
      padding: 12px;
      border-radius: 10px;
      text-align: center;
    }}
    .stat-val {{
      font-size: 18px;
      font-weight: 800;
      color: #f1f5f9;
    }}
    .stat-lbl {{
      font-size: 11px;
      color: #94a3b8;
      margin-top: 2px;
      text-transform: uppercase;
    }}
    .btn-action {{
      display: block;
      width: 100%;
      background: linear-gradient(135deg, #ef4444, #b91c1c);
      color: #ffffff;
      font-weight: 800;
      text-align: center;
      padding: 14px;
      border-radius: 12px;
      text-decoration: none;
      font-size: 15px;
      cursor: pointer;
      border: none;
      margin-top: 8px;
      transition: transform 0.15s, box-shadow 0.15s;
    }}
    .btn-action:hover {{
      transform: translateY(-2px);
      box-shadow: 0 10px 25px -5px rgba(239, 68, 68, 0.4);
    }}
  </style>
</head>
<body>
  <header>
    <div class="badge">Trending Tech Disaster • Post-Mortem</div>
    <h1>How a 78-Byte File Crashed 8.5 Million Windows PCs 💥</h1>
    <p class="subtitle">Format: 9:16 Vertical (1080x1920) • 48.14s • Developer Voiceover & 3D LEGO Minifigure</p>
  </header>

  <div class="player-container">
    <div class="video-wrapper">
      <video id="shortVideo" controls autoplay loop playsinline>
        <source src="data:video/mp4;base64,{b64_data}" type="video/mp4">
        <source src="MICROSOFT_OUTAGE_SHORT_9x16.mp4" type="video/mp4">
        Your browser does not support HTML5 video.
      </video>
    </div>

    <div class="sidebar">
      <div class="card">
        <h2>⏱️ Scene Timestamps & Retention Beats</h2>
        <div class="timeline-item" onclick="seekVideo(0)">
          <span class="timeline-title">🚨 Beat 1: The Hook (8.5M PCs in 1 Second)</span>
          <span class="timeline-time">0:00</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(9.67)">
          <span class="timeline-title">⚠️ Beat 2: Ring 0 Kernel Bug (Channel File 291)</span>
          <span class="timeline-time">0:09</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(19.9)">
          <span class="timeline-title">💀 Beat 3: The Infinite BSOD Boot Loop</span>
          <span class="timeline-time">0:19</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(28.75)">
          <span class="timeline-title">🛠️ Beat 4: Safe Mode USB Key Recovery</span>
          <span class="timeline-time">0:28</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(37.57)">
          <span class="timeline-title">💡 Beat 5: Golden Rule (Canary Rollouts) & CTA</span>
          <span class="timeline-time">0:37</span>
        </div>
      </div>

      <div class="card">
        <h2>📊 Viral Video Technical Breakdown</h2>
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-val">1080x1920</div>
            <div class="stat-lbl">Vertical 9:16</div>
          </div>
          <div class="stat-box">
            <div class="stat-val">48.14s</div>
            <div class="stat-lbl">Shorts Duration</div>
          </div>
          <div class="stat-box">
            <div class="stat-val">24 FPS</div>
            <div class="stat-lbl">1,155 Frames</div>
          </div>
          <div class="stat-box">
            <div class="stat-val">Ring 0 BSOD</div>
            <div class="stat-lbl">Authentic Visuals</div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>🚀 Ready to Publish to @TechStacAI?</h2>
        <p style="font-size: 13px; line-height: 1.5; color: #cbd5e1; margin-bottom: 12px;">
          Say <b>'yes'</b> or <b>'upload'</b> to publish this immediately to your YouTube channel with full SEO packaging (tags, description, and hashtags).
        </p>
      </div>
    </div>
  </div>

  <script>
    const video = document.getElementById('shortVideo');
    function seekVideo(time) {{
      if (video) {{
        video.currentTime = time;
        video.play();
      }}
    }}
  </script>
</body>
</html>"""

out_brain = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994\preview_outage_player.html"
out_proj = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_outage_short\preview_outage_player.html"

with open(out_brain, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(out_proj, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Embedded player created successfully! Brain: {os.path.getsize(out_brain)} bytes, Proj: {os.path.getsize(out_proj)} bytes")
