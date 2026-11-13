import os, sys, math, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\proper_3d_tech_explainer"
assets_dir = os.path.join(proj_dir, "assets")
audio_path = os.path.join(proj_dir, "audio", "master_audio_with_sfx.wav")
output_mp4 = os.path.join(proj_dir, "AI_AGENTS_VS_DEV_TEAMS_16x9.mp4")
timeline_path = os.path.join(proj_dir, "timeline.json")

with open(timeline_path, 'r', encoding='utf-8') as f:
    t_data = json.load(f)

TOTAL_DURATION = t_data["total_duration"]
timeline = t_data["timeline"]

WIDTH = 1280
HEIGHT = 720
FPS = 24
TOTAL_FRAMES = int(math.ceil(TOTAL_DURATION * FPS))

print(f"[+] Initializing 16:9 Video Render ({TOTAL_DURATION:.2f}s, {TOTAL_FRAMES} frames)...")

# Load 3D base plates
img_burnout = Image.open(os.path.join(assets_dir, "scene1_burnout.jpg")).convert("RGB")
img_cyber = Image.open(os.path.join(assets_dir, "scene4_cyber_deck.jpg")).convert("RGB")
img_mascot = Image.open(os.path.join(assets_dir, "mascot_cube.jpg")).convert("RGB")

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)
font_caption_bold = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 36)
font_caption_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
font_hud = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 46)

# Colors
CYAN = (6, 182, 212)
CYAN_GLOW = (165, 243, 252)
AMBER = (245, 158, 11)
RED_ALERT = (239, 68, 68)
YELLOW_ACCENT = (250, 204, 21)
WHITE = (255, 255, 255)
BLACK = (15, 23, 42)
DARK_CARD = (15, 23, 42)

# Scene Script Metadata
scene_meta = {
    1: {
        "title": "SCENE 1: THE 2:00 AM CATASTROPHE",
        "cap_main": "IT'S 2:00 AM... AND PRODUCTION CRASHED 🚨",
        "cap_sub": "The server throws 500 errors. Your lead developer is dead asleep.",
        "badge": "🚨 EMERGENCY BREAKDOWN"
    },
    2: {
        "title": "SCENE 2: THE 10-DEVELOPER MYTH",
        "cap_main": "MORE DEVS = MORE MEETINGS & MERGE CONFLICTS 💀",
        "cap_sub": "Adding headcount doesn't speed up delivery — it multiplies coordination chaos.",
        "badge": "💥 THE BOTTLENECK"
    },
    3: {
        "title": "SCENE 3: ENTER THE AUTONOMOUS AGENT",
        "cap_main": "WHILE HUMANS SLEEP... THE AI AGENT WAKES UP ⚡",
        "cap_sub": "Detects the exception, spins up a sandbox, isolates tests, and writes the patch.",
        "badge": "🤖 AUTONOMOUS DISPATCH"
    },
    4: {
        "title": "SCENE 4: THE ZERO-HANDOFF LOOP",
        "cap_main": "NO WAITING. NO PR ARGUMENTS. INSTANT DEPLOY. 🚀",
        "cap_sub": "Tests regression safety and deploys directly to production in minutes.",
        "badge": "🔄 CLOSED-LOOP VELOCITY"
    },
    5: {
        "title": "SCENE 5: THE 10X SOLO FOUNDER REALITY",
        "cap_main": "SOLO FOUNDER + 5 AGENTS = 10X SHIPPING SPEED 🔥",
        "cap_sub": "The most dangerous startups aren't 50-person teams — they are agentic fleets.",
        "badge": "⚡ 10X FORCE MULTIPLIER"
    },
    6: {
        "title": "SCENE 6: THE FINAL VERDICT",
        "cap_main": "ARE YOU BUILDING WITH AGENTS... OR COMPETING? 👇",
        "cap_sub": "Which side of history are you on? Drop your opinion in the comments!",
        "badge": "🏆 THE 2026 CHOICE"
    }
}

def get_ken_burns(img, t_pct, zoom_start=1.0, zoom_end=1.12, pan_dir=(0, 0)):
    """Extract a smooth zooming/panning sub-window from base 3D plate."""
    orig_w, orig_h = img.size
    cur_zoom = zoom_start + (zoom_end - zoom_start) * t_pct
    
    view_w = int(orig_w / cur_zoom)
    view_h = int(orig_h / cur_zoom)
    
    # Calculate pan offset
    max_pan_x = orig_w - view_w
    max_pan_y = orig_h - view_h
    
    offset_x = int(max_pan_x * 0.5 + pan_dir[0] * (max_pan_x * 0.5) * t_pct)
    offset_y = int(max_pan_y * 0.5 + pan_dir[1] * (max_pan_y * 0.5) * t_pct)
    
    offset_x = max(0, min(offset_x, max_pan_x))
    offset_y = max(0, min(offset_y, max_pan_y))
    
    crop = img.crop((offset_x, offset_y, offset_x + view_w, offset_y + view_h))
    return crop.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

def draw_outlined(draw, pos, text, font, fill, stroke=BLACK, stroke_w=3):
    draw.text(pos, text, font=font, fill=fill, stroke_fill=stroke, stroke_width=stroke_w)

# Start FFmpeg subprocess
ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", audio_path,
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_mp4
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

for f in range(TOTAL_FRAMES):
    t = f / float(FPS)
    
    # Identify active scene from timeline
    cur_sc = timeline[-1]
    for sc in timeline:
        if sc["start"] <= t < sc["end"]:
            cur_sc = sc
            break
            
    sc_id = cur_sc["id"]
    sc_t = max(0.0, t - cur_sc["start"])
    sc_dur = max(0.1, cur_sc["duration"])
    sc_pct = min(1.0, sc_t / sc_dur)
    
    # -------------------------------------------------------------------------
    # Render Scene 3D Background with Ken Burns Motion
    # -------------------------------------------------------------------------
    shake_x = 0
    shake_y = 0
    
    if sc_id == 1:
        # Scene 1: Burnout (Camera push-in from wide to sleeping dev)
        base_frame = get_ken_burns(img_burnout, sc_pct, zoom_start=1.0, zoom_end=1.14, pan_dir=(0.2, 0.1))
        draw = ImageDraw.Draw(base_frame)
        
        # Red emergency light pulsing
        pulse = 0.5 + 0.5 * math.sin(t * 5.0)
        red_overlay = int(pulse * 35)
        # Vignette tint
        draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(red_overlay, 0, 0, 0), outline=None)
        
        # Flashing clock badge
        draw.rounded_rectangle([WIDTH - 250, 110, WIDTH - 50, 175], radius=10, fill=BLACK, outline=RED_ALERT, width=3)
        draw.text((WIDTH - 230, 122), "⏱️ 02:00:14 AM", font=font_title, fill=RED_ALERT)
        
        # Stack trace snippet on side
        draw.rounded_rectangle([50, 120, 420, 260], radius=10, fill=(10, 15, 30, 200), outline=RED_ALERT, width=2)
        draw.text((70, 135), "FATAL: Connection pool exhausted", font=font_code, fill=RED_ALERT)
        draw.text((70, 165), "Error 500: Database unreachable", font=font_code, fill=AMBER)
        draw.text((70, 195), "dev_lead: OFFLINE (Away 4h)", font=font_code, fill=WHITE)
        draw.text((70, 225), ">>> SYSTEM BLOCKED", font=font_code, fill=RED_ALERT)

    elif sc_id == 2:
        # Scene 2: 10-Dev Chaos (Shake on vine boom around t=20.4s)
        if 20.2 <= t <= 21.0:
            shake_amp = (1.0 - (t - 20.2) / 0.8) * 14
            shake_x = int(math.sin(t * 60.0) * shake_amp)
            shake_y = int(math.cos(t * 60.0) * shake_amp)
            
        base_frame = get_ken_burns(img_burnout, sc_pct, zoom_start=1.15, zoom_end=1.0, pan_dir=(-0.2, -0.1))
        draw = ImageDraw.Draw(base_frame)
        
        # Dim background to highlight chaotic UI cards
        draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(0, 0, 0, 80))
        
        # Chaotic floating Jira/Slack badges
        badges = [
            (220, 160, "📅 STANDUP (45m)", AMBER),
            (560, 140, "💬 48 SLACK THREADS", RED_ALERT),
            (880, 180, "⚠️ MERGE CONFLICT (6 files)", RED_ALERT),
            (320, 260, "🔄 SPRINT RETROSPECTIVE", AMBER),
            (760, 280, "⛔ BLOCKED ON BACKEND PR", RED_ALERT)
        ]
        
        for bx, by, btext, bcol in badges:
            bob = int(math.sin(t * 4.0 + bx) * 8)
            draw.rounded_rectangle([bx - 120, by + bob - 25, bx + 120, by + bob + 25], radius=12, fill=BLACK, outline=bcol, width=3)
            draw.text((bx - 105, by + bob - 12), btext, font=font_code, fill=WHITE)
            
        draw_outlined(draw, (360 + shake_x, 370 + shake_y), "COORDINATION OVERLOAD!", font=font_hud, fill=YELLOW_ACCENT, stroke=BLACK, stroke_w=4)

    elif sc_id == 3:
        # Scene 3: Enter the AI Agent (Cyber Deck, slow pan right)
        base_frame = get_ken_burns(img_cyber, sc_pct, zoom_start=1.0, zoom_end=1.10, pan_dir=(0.25, 0.0))
        draw = ImageDraw.Draw(base_frame)
        
        # Rotating holographic HUD circle
        cx, cy = 960, 320
        r = 130
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=CYAN_GLOW, width=4)
        draw.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], outline=CYAN, width=2)
        
        # Rotating nodes on HUD
        for a_deg in [0, 60, 120, 180, 240, 300]:
            rad = math.radians(a_deg + t * 45.0)
            nx = cx + int(r * math.cos(rad))
            ny = cy + int(r * math.sin(rad))
            draw.ellipse([nx - 8, ny - 8, nx + 8, ny + 8], fill=CYAN, outline=WHITE, width=2)
            
        # Agent status card on left
        draw.rounded_rectangle([60, 140, 440, 320], radius=14, fill=BLACK, outline=CYAN, width=3)
        draw.text((85, 160), "🤖 AGENT: ACTIVE (0.02s response)", font=font_title, fill=CYAN)
        draw.text((85, 200), "✔ Sandboxed Environment: Ready", font=font_code, fill=WHITE)
        draw.text((85, 230), "✔ Stack Trace Analyzed: Line 142", font=font_code, fill=WHITE)
        draw.text((85, 260), "✔ Unit Test Isolated: TestAuth()", font=font_code, fill=WHITE)
        draw.text((85, 290), "✔ Automated Patch: GENERATED", font=font_code, fill=YELLOW_ACCENT)

    elif sc_id == 4:
        # Scene 4: The Zero-Handoff Loop (Cyber deck closer angle + verified deployment)
        base_frame = get_ken_burns(img_cyber, sc_pct, zoom_start=1.10, zoom_end=1.18, pan_dir=(-0.15, -0.1))
        draw = ImageDraw.Draw(base_frame)
        
        # Golden checkmark banner
        draw.rounded_rectangle([720, 140, 1200, 290], radius=16, fill=BLACK, outline=YELLOW_ACCENT, width=4)
        draw.text((750, 165), "🚀 ZERO-HANDOFF PIPELINE", font=font_title, fill=YELLOW_ACCENT)
        draw.text((750, 205), "• Write Code: 12 seconds", font=font_caption_sub, fill=WHITE)
        draw.text((750, 235), "• Regression Tests: PASSED (100%)", font=font_caption_sub, fill=CYAN)
        draw.text((750, 265), "• Production Deploy: COMPLETE", font=font_caption_sub, fill=WHITE)
        
        draw_outlined(draw, (70, 360), "HUMAN WAIT TIME: 0 SECONDS", font=font_hud, fill=CYAN, stroke=BLACK, stroke_w=4)

    elif sc_id == 5:
        # Scene 5: 10X Solo Founder Reality (Mascot with glowing cube + speed lines)
        base_frame = get_ken_burns(img_mascot, sc_pct, zoom_start=1.0, zoom_end=1.12, pan_dir=(0.2, 0.05))
        draw = ImageDraw.Draw(base_frame)
        
        # 10X Multiplier Badge
        draw.rounded_rectangle([740, 130, 1210, 290], radius=18, fill=BLACK, outline=CYAN, width=4)
        draw.text((770, 155), "10X MULTIPLIER 🔥", font=font_hud, fill=YELLOW_ACCENT)
        draw.text((775, 220), "1 Founder + 5 Autonomous Agents", font=font_title, fill=WHITE)
        draw.text((775, 255), "Outshipping 50-person engineering teams.", font=font_caption_sub, fill=CYAN_GLOW)
        
        # Cyber energy particles around mascot
        for p_i in range(12):
            px = int(350 + math.cos(t * 3.0 + p_i) * (80 + p_i * 12))
            py = int(380 + math.sin(t * 2.5 + p_i) * (60 + p_i * 8))
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=CYAN, outline=WHITE, width=1)

    else:
        # Scene 6: The Verdict & Discussion CTA
        base_frame = get_ken_burns(img_mascot, sc_pct, zoom_start=1.12, zoom_end=1.20, pan_dir=(-0.1, -0.05))
        draw = ImageDraw.Draw(base_frame)
        
        # Left vs Right Choice Badges
        draw.rounded_rectangle([70, 140, 480, 240], radius=14, fill=BLACK, outline=AMBER, width=3)
        draw.text((90, 160), "❌ OLD WAY: 100% MANUAL", font=font_title, fill=AMBER)
        draw.text((90, 195), "Coordination lag, PR queues & meetings", font=font_code, fill=WHITE)
        
        draw.rounded_rectangle([790, 140, 1210, 240], radius=14, fill=BLACK, outline=CYAN, width=3)
        draw.text((810, 160), "✅ NEW WAY: AGENT-FIRST", font=font_title, fill=CYAN)
        draw.text((810, 195), "Autonomous loops, instant shipping", font=font_code, fill=WHITE)
        
        # Call to action banner
        pulse_cta = int(math.sin(t * 6.0) * 4)
        draw.rounded_rectangle([320, 290 + pulse_cta, 960, 370 + pulse_cta], radius=16, fill=YELLOW_ACCENT, outline=BLACK, width=3)
        draw.text((360, 310 + pulse_cta), "WHICH SIDE ARE YOU ON? 👇", font=font_caption_bold, fill=BLACK)

    # -------------------------------------------------------------------------
    # GLOBAL HUD: HEADER BADGE, PROGRESS BAR, LOWER-THIRD SUBTITLES
    # -------------------------------------------------------------------------
    meta = scene_meta.get(sc_id, scene_meta[1])
    
    # 1. Top Header Badges
    draw.rounded_rectangle([40, 25, 430, 75], radius=10, fill=BLACK, outline=CYAN, width=2)
    draw.text((55, 37), "AI AGENTS VS SOFTWARE TEAMS", font=font_title, fill=WHITE)
    
    draw.rounded_rectangle([WIDTH - 360, 25, WIDTH - 40, 75], radius=10, fill=WHITE, outline=BLACK, width=2)
    draw.text((WIDTH - 340, 39), meta["badge"], font=font_badge, fill=BLACK)
    
    # 2. Lower-Third Subtitle Card
    sub_y = 570
    draw.rounded_rectangle([40, sub_y, WIDTH - 40, sub_y + 120], radius=16, fill=BLACK, outline=CYAN, width=3)
    
    # Headline in bold yellow/accent
    draw.text((65, sub_y + 16), meta["cap_main"], font=font_caption_bold, fill=YELLOW_ACCENT)
    # Secondary explanation in crisp white
    draw.text((65, sub_y + 70), meta["cap_sub"], font=font_caption_sub, fill=WHITE)
    
    # 3. Bottom Progress Bar in Electric Cyan
    prog_pct = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 10, int(WIDTH * prog_pct), HEIGHT], fill=CYAN)
    
    # Apply camera shake if needed
    if shake_x != 0 or shake_y != 0:
        base_frame = ImageChops.offset(base_frame, shake_x, shake_y)
        
    # Write RGB bytes to FFmpeg stdin
    proc.stdin.write(base_frame.tobytes())
    
    if f % 120 == 0:
        pct = (f / float(TOTAL_FRAMES)) * 100.0
        print(f"  Rendering frame {f}/{TOTAL_FRAMES} ({pct:.1f}% | {t:.1f}s)...")

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"MASTER 16:9 PROPER 3D VIDEO RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames @ 24fps)")
if os.path.exists(output_mp4):
    size_mb = os.path.getsize(output_mp4) / 1_000_000.0
    print(f"File Size: {size_mb:.2f} MB")
print("="*60)
