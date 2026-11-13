import base64
import os

video_path = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_today_outage_short\MICROSOFT_TODAY_OUTAGE_SHORT_9x16.mp4"
with open(video_path, "rb") as f:
    b64_data = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TechStack AI - Microsoft Global Outage Today (MO1550821) Preview</title>
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
    <div class="badge">Breaking Systems Disaster • Today</div>
    <h1>Microsoft Down Today: 130,000+ Crashes Explained 💥</h1>
    <p class="subtitle">Format: 9:16 Vertical (1080x1920) • 53.09s • Incident MO1550821 Systems Post-Mortem</p>
  </header>

  <div class="player-container">
    <div class="video-wrapper">
      <video id="shortVideo" controls autoplay loop playsinline>
        <source src="data:video/mp4;base64,{b64_data}" type="video/mp4">
        <source src="MICROSOFT_TODAY_OUTAGE_SHORT_9x16.mp4" type="video/mp4">
        Your browser does not support HTML5 video.
      </video>
    </div>

    <div class="sidebar">
      <div class="card">
        <h2>⏱️ Scene Timestamps & Retention Beats</h2>
        <div class="timeline-item" onclick="seekVideo(0)">
          <span class="timeline-title">🚨 Beat 1: The Global Outage Hook</span>
          <span class="timeline-time">0:00</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(11.93)">
          <span class="timeline-title">🔍 Beat 2: Incident MO1550821 & Health Check</span>
          <span class="timeline-time">0:11</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(22.1)">
          <span class="timeline-title">⚠️ Beat 3: Cascading Failure & Thundering Herd</span>
          <span class="timeline-time">0:22</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(32.86)">
          <span class="timeline-title">🌐 Beat 4: Emergency Traffic Bypass</span>
          <span class="timeline-time">0:32</span>
        </div>
        <div class="timeline-item" onclick="seekVideo(41.67)">
          <span class="timeline-title">💡 Beat 5: Circuit Breaker Rule & CTA</span>
          <span class="timeline-time">0:41</span>
        </div>
      </div>

      <div class="card">
        <h2>📊 Video Technical Specifications</h2>
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-val">1080x1920</div>
            <div class="stat-lbl">Vertical 9:16</div>
          </div>
          <div class="stat-box">
            <div class="stat-val">53.09s</div>
            <div class="stat-lbl">Shorts Retention</div>
          </div>
          <div class="stat-box">
            <div class="stat-val">24 FPS</div>
            <div class="stat-lbl">1,274 Frames</div>
          </div>
          <div class="stat-box">
            <div class="stat-val">MO1550821</div>
            <div class="stat-lbl">Authentic Incident</div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>🚀 Ready to Publish to @TechStacAI?</h2>
        <p style="font-size: 13px; line-height: 1.5; color: #cbd5e1; margin-bottom: 12px;">
          This breaking video covers today's global incident with maximum algorithmic timing and curiosity. Say <b>'upload'</b> or <b>'publish'</b> to release it live immediately!
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

out_brain = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994\preview_today_outage.html"
out_proj = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_today_outage_short\preview_today_outage.html"

with open(out_brain, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(out_proj, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Embedded player created successfully! Brain: {os.path.getsize(out_brain)} bytes, Proj: {os.path.getsize(out_proj)} bytes")
