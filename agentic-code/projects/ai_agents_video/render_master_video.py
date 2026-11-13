import os, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\ai_agents_video"
audio_path = os.path.join(proj_dir, "audio", "master_audio.wav")
output_mp4 = os.path.join(proj_dir, "ai_agents_replacing_teams.mp4")

WIDTH = 1280
HEIGHT = 720
FPS = 24
TOTAL_DURATION = 65.37
TOTAL_FRAMES = int(math.ceil(TOTAL_DURATION * FPS))

# Colors
BG_COLOR = (248, 250, 252)          # Modern bright white high-key studio
GRID_COLOR = (226, 232, 240)        # Subtle light-gray perspective grid
CYAN = (6, 182, 212)                # Glowing electric cyan (AI / velocity)
CYAN_GLOW = (165, 243, 252)
AMBER = (245, 158, 11)              # Alert amber (friction / bottlenecks)
INDIGO = (67, 56, 202)              # Deep indigo (legacy model / org chart)
BLACK = (15, 23, 42)                # Sharp stick figure strokes
RED_BEANIE = (225, 29, 72)          # Vibrant smooth red beanie
YELLOW_SHIRT = (250, 204, 21)       # Vibrant yellow t-shirt
WHITE = (255, 255, 255)

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
font_caption = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
font_caption_bold = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 32)
font_node = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 16)
font_big_badge = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 42)

# Scenes & Captions definition matching master audio
scenes = [
    {
        "id": 1,
        "start": 0.0,
        "end": 7.66,
        "caption_main": "THE BIGGEST ENGINEERING BOTTLENECK ISN'T HEADCOUNT",
        "caption_sub": "It's the simple fact that humans sleep.",
        "badge": "🚨 STAGE 1: THE GOLDEN HOOK"
    },
    {
        "id": 2,
        "start": 7.66,
        "end": 18.95,
        "caption_main": "MORE DEVELOPERS = SLOWER SHIPPING",
        "caption_sub": "Adding engineers multiplies meetings, reviews, and context-switching.",
        "badge": "💥 STAGE 2: DISRUPTING ASSUMPTIONS"
    },
    {
        "id": 3,
        "start": 18.95,
        "end": 31.36,
        "caption_main": "THE SECRET REAL COST: COORDINATION",
        "caption_sub": "Software costs aren't salaries — every human handoff is a failure point.",
        "badge": "🔓 STAGE 3: UNVEILING INSIDER SECRETS"
    },
    {
        "id": 4,
        "start": 31.36,
        "end": 43.16,
        "caption_main": "AI AGENTS DON'T HAND OFF. THEY CLOSE THE LOOP.",
        "caption_sub": "Write → Test → Verify → Deploy — in one uninterrupted loop.",
        "badge": "🤖 STAGE 4: AUTONOMOUS MECHANISM"
    },
    {
        "id": 5,
        "start": 43.16,
        "end": 53.21,
        "caption_main": "10X SHIPPING VELOCITY WITHOUT 10X HEADCOUNT",
        "caption_sub": "They aren't hiring more people — they removed the waiting entirely.",
        "badge": "⚡ STAGE 5: SCALE & MULTIPLIER"
    },
    {
        "id": 6,
        "start": 53.21,
        "end": 65.37,
        "caption_main": "ARE YOU BUILDING WITH AGENTS... OR COMPETING WITH THEM?",
        "caption_sub": "The choice will define every engineering team by 2026.",
        "badge": "🏆 STAGE 6: THE ULTIMATE CHOICE"
    }
]

def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)

def draw_outlined_text(draw, pos, text, font, fill_color, stroke_color=BLACK, stroke_width=3):
    draw.text(pos, text, font=font, fill=fill_color, stroke_fill=stroke_color, stroke_width=stroke_width)

def draw_stickman(draw, x, y, scale=1.0, pose="stand", facing="right"):
    """
    Renders Style 2A Stickman (Anti-Deformation Lock):
    - Red beanie (smooth rounded knit, NO pom-pom)
    - Yellow t-shirt
    - Simple black stick limbs and dark shorts
    - Hollow circular head, no facial deformation
    """
    s = scale
    dir_mult = 1 if facing == "right" else -1
    
    # Coordinates
    head_r = int(22 * s)
    head_cy = y - int(95 * s)
    head_cx = x
    
    # 1. Head (Hollow circle, clean white fill with crisp black outline)
    draw.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
                 fill=WHITE, outline=BLACK, width=int(3 * s))
    
    # Simple clean dot eyes
    eye_offset = int(7 * s * dir_mult)
    draw.ellipse([head_cx + eye_offset - 2, head_cy - 4, head_cx + eye_offset + 2, head_cy], fill=BLACK)
    
    # 2. Red Beanie (Smooth rounded dome on top, no pom-pom)
    beanie_top = head_cy - int(30 * s)
    draw.pieslice([head_cx - head_r - int(2*s), head_cy - head_r - int(12*s),
                   head_cx + head_r + int(2*s), head_cy],
                  180, 360, fill=RED_BEANIE, outline=BLACK, width=2)
    # Beanie rim
    draw.rounded_rectangle([head_cx - head_r - int(3*s), head_cy - int(14*s),
                            head_cx + head_r + int(3*s), head_cy - int(4*s)],
                           radius=int(4*s), fill=RED_BEANIE, outline=BLACK, width=2)
    
    # 3. Torso / Yellow T-Shirt
    torso_top = head_cy + head_r
    torso_bot = y - int(35 * s)
    shirt_w = int(18 * s)
    draw.rounded_rectangle([head_cx - shirt_w, torso_top, head_cx + shirt_w, torso_bot],
                           radius=int(6*s), fill=YELLOW_SHIRT, outline=BLACK, width=int(2.5*s))
    
    # Shorts
    shorts_bot = y - int(20 * s)
    draw.rectangle([head_cx - shirt_w + int(2*s), torso_bot, head_cx + shirt_w - int(2*s), shorts_bot],
                   fill=INDIGO, outline=BLACK, width=2)
    
    # 4. Limbs based on pose
    lw = int(3.5 * s)
    
    if pose == "stand":
        # Legs straight down with small feet
        draw.line([(head_cx - int(7*s), shorts_bot), (head_cx - int(8*s), y)], fill=BLACK, width=lw)
        draw.line([(head_cx + int(7*s), shorts_bot), (head_cx + int(8*s), y)], fill=BLACK, width=lw)
        draw.line([(head_cx - int(8*s), y), (head_cx - int(8*s) + int(9*s*dir_mult), y)], fill=BLACK, width=lw)
        draw.line([(head_cx + int(8*s), y), (head_cx + int(8*s) + int(9*s*dir_mult), y)], fill=BLACK, width=lw)
        # Arms relaxed
        draw.line([(head_cx - shirt_w, torso_top + int(10*s)), (head_cx - shirt_w - int(12*s), torso_bot)], fill=BLACK, width=lw)
        draw.line([(head_cx + shirt_w, torso_top + int(10*s)), (head_cx + shirt_w + int(12*s), torso_bot)], fill=BLACK, width=lw)
        
    elif pose == "arms_wide":
        # Shock / Eureka: both arms spread wide
        draw.line([(head_cx - int(9*s), shorts_bot), (head_cx - int(14*s), y)], fill=BLACK, width=lw)
        draw.line([(head_cx + int(9*s), shorts_bot), (head_cx + int(14*s), y)], fill=BLACK, width=lw)
        # Arms angled up
        draw.line([(head_cx - shirt_w, torso_top + int(10*s)), (head_cx - shirt_w - int(32*s), torso_top - int(15*s))], fill=BLACK, width=lw)
        draw.line([(head_cx + shirt_w, torso_top + int(10*s)), (head_cx + shirt_w + int(32*s), torso_top - int(15*s))], fill=BLACK, width=lw)
        
    elif pose == "point":
        # Pointing arm forward
        draw.line([(head_cx - int(7*s), shorts_bot), (head_cx - int(8*s), y)], fill=BLACK, width=lw)
        draw.line([(head_cx + int(7*s), shorts_bot), (head_cx + int(8*s), y)], fill=BLACK, width=lw)
        # Left arm on hip
        draw.line([(head_cx - shirt_w * dir_mult, torso_top + int(10*s)), (head_cx - int(24*s)*dir_mult, torso_bot - int(5*s))], fill=BLACK, width=lw)
        draw.line([(head_cx - int(24*s)*dir_mult, torso_bot - int(5*s)), (head_cx - shirt_w * dir_mult, torso_bot)], fill=BLACK, width=lw)
        # Right arm pointing forward
        draw.line([(head_cx + shirt_w * dir_mult, torso_top + int(10*s)), (head_cx + int(45*s)*dir_mult, torso_top + int(2*s))], fill=BLACK, width=lw)
        draw.line([(head_cx + int(45*s)*dir_mult, torso_top + int(2*s)), (head_cx + int(58*s)*dir_mult, torso_top - int(2*s))], fill=BLACK, width=lw)
        
    elif pose == "surf":
        # Surfing dynamic leaning pose
        draw.line([(head_cx - int(5*s), shorts_bot), (head_cx - int(25*s), y - int(5*s))], fill=BLACK, width=lw)
        draw.line([(head_cx + int(5*s), shorts_bot), (head_cx + int(20*s), y)], fill=BLACK, width=lw)
        # Arms spread forward/back for balance
        draw.line([(head_cx - shirt_w, torso_top + int(10*s)), (head_cx - int(35*s), torso_top - int(8*s))], fill=BLACK, width=lw)
        draw.line([(head_cx + shirt_w, torso_top + int(10*s)), (head_cx + int(35*s), torso_top - int(12*s))], fill=BLACK, width=lw)

    elif pose == "stumble":
        # Stumbling right
        draw.line([(head_cx - int(7*s), shorts_bot), (head_cx - int(20*s), y)], fill=BLACK, width=lw)
        draw.line([(head_cx + int(7*s), shorts_bot), (head_cx + int(2*s), y - int(12*s))], fill=BLACK, width=lw)
        draw.line([(head_cx - shirt_w, torso_top + int(10*s)), (head_cx - int(30*s), torso_top + int(30*s))], fill=BLACK, width=lw)
        draw.line([(head_cx + shirt_w, torso_top + int(10*s)), (head_cx + int(35*s), torso_top - int(20*s))], fill=BLACK, width=lw)

def draw_studio_grid(draw, vanishing_y=380):
    """Style 2A floor perspective grid and high-key white studio space."""
    # Horizon line
    draw.line([(0, vanishing_y), (WIDTH, vanishing_y)], fill=GRID_COLOR, width=1)
    
    # Radiating perspective lines
    cx = WIDTH // 2
    for x in range(-WIDTH, 2 * WIDTH, 80):
        draw.line([(cx, vanishing_y), (x, HEIGHT)], fill=GRID_COLOR, width=1)
        
    # Horizontal grid lines with perspective spacing
    for i in range(1, 14):
        dist = (i / 13.0) ** 1.8
        y = int(vanishing_y + dist * (HEIGHT - vanishing_y))
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

print(f"[+] Initializing FFmpeg render pipeline for Style 2A ({TOTAL_DURATION}s, {TOTAL_FRAMES} frames)...")

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
    
    # Identify active scene
    cur_scene = scenes[-1]
    for sc in scenes:
        if sc["start"] <= t < sc["end"]:
            cur_scene = sc
            break
            
    sc_t = t - cur_scene["start"]
    sc_dur = cur_scene["end"] - cur_scene["start"]
    sc_pct = min(1.0, max(0.0, sc_t / sc_dur))
    
    # Create frame
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Studio perspective grid
    draw_studio_grid(draw, vanishing_y=400)
    
    # -------------------------------------------------------------------------
    # SCENE 1: The Golden Hook (Clock + TEAM panels dissolving + Node Web)
    # -------------------------------------------------------------------------
    if cur_scene["id"] == 1:
        # Stickman glides in from left to center
        stick_x = int(120 + ease_in_out(min(1.0, sc_t / 2.0)) * 260)
        pose = "stand" if sc_t < 4.0 else "arms_wide"
        draw_stickman(draw, stick_x, 500, scale=1.3, pose=pose, facing="right")
        
        # Spinning cyan clock above
        clock_x, clock_y = stick_x, 230
        clock_r = 44
        draw.ellipse([clock_x - clock_r, clock_y - clock_r, clock_x + clock_r, clock_y + clock_r],
                     fill=WHITE, outline=CYAN, width=4)
        # Holographic glow ring
        draw.ellipse([clock_x - clock_r - 6, clock_y - clock_r - 6, clock_x + clock_r + 6, clock_y + clock_r + 6],
                     outline=CYAN_GLOW, width=2)
        # Clock hands spinning fast
        hand_angle = t * 12.0
        draw.line([(clock_x, clock_y),
                   (clock_x + int(math.sin(hand_angle) * 26), clock_y - int(math.cos(hand_angle) * 26))],
                  fill=BLACK, width=3)
        draw.line([(clock_x, clock_y),
                   (clock_x + int(math.sin(hand_angle * 3.5) * 34), clock_y - int(math.cos(hand_angle * 3.5) * 34))],
                  fill=CYAN, width=2)
        
        # Two indigo TEAM panels (fading out around t=3.5s)
        fade = max(0.0, 1.0 - max(0.0, (sc_t - 2.8) / 1.5))
        if fade > 0.05:
            # Team A panel
            draw.rounded_rectangle([720, 200, 940, 310], radius=14,
                                   fill=(int(INDIGO[0]*fade + BG_COLOR[0]*(1-fade)),
                                         int(INDIGO[1]*fade + BG_COLOR[1]*(1-fade)),
                                         int(INDIGO[2]*fade + BG_COLOR[2]*(1-fade))),
                                   outline=CYAN if fade > 0.6 else None, width=2)
            draw.text((750, 235), "TEAM A (OFFLINE)", font=font_title, fill=WHITE)
            draw.text((750, 270), "8 hrs / day active", font=font_node, fill=CYAN_GLOW)
            
            # Team B panel
            draw.rounded_rectangle([990, 200, 1210, 310], radius=14,
                                   fill=(int(INDIGO[0]*fade + BG_COLOR[0]*(1-fade)),
                                         int(INDIGO[1]*fade + BG_COLOR[1]*(1-fade)),
                                         int(INDIGO[2]*fade + BG_COLOR[2]*(1-fade))),
                                   outline=CYAN if fade > 0.6 else None, width=2)
            draw.text((1020, 235), "TEAM B (SLEEPING)", font=font_title, fill=WHITE)
            draw.text((1020, 270), "Awaiting morning sync", font=font_node, fill=CYAN_GLOW)
            
        # At t > 4s, expanding glowing cyan node web blooms
        if sc_t > 3.8:
            web_grow = min(1.0, (sc_t - 3.8) / 2.0)
            center_x, center_y = 960, 260
            draw.ellipse([center_x - 14, center_y - 14, center_x + 14, center_y + 14], fill=CYAN, outline=WHITE, width=2)
            
            node_positions = [
                (center_x - 160 * web_grow, center_y - 90 * web_grow),
                (center_x + 150 * web_grow, center_y - 80 * web_grow),
                (center_x - 120 * web_grow, center_y + 90 * web_grow),
                (center_x + 140 * web_grow, center_y + 100 * web_grow),
                (center_x - 220 * web_grow, center_y + 10 * web_grow),
                (center_x + 220 * web_grow, center_y + 20 * web_grow),
            ]
            for nx, ny in node_positions:
                draw.line([(center_x, center_y), (nx, ny)], fill=CYAN, width=2)
                draw.ellipse([nx - 10, ny - 10, nx + 10, ny + 10], fill=WHITE, outline=CYAN, width=3)
                
            draw_outlined_text(draw, (830, 390), "24/7 AUTONOMOUS CONTINUITY", font=font_title, fill_color=CYAN, stroke_color=WHITE, stroke_width=2)

    # -------------------------------------------------------------------------
    # SCENE 2: Disrupting Assumptions (Org-chart grows, cracks, tilts)
    # -------------------------------------------------------------------------
    elif cur_scene["id"] == 2:
        # Tilt angle after fracture
        tilt_factor = min(1.0, max(0.0, (sc_t - 5.5) / 2.0))
        tilt_y = int(tilt_factor * 45)
        
        # Stickman stumbles when chart tilts
        stick_pose = "point" if sc_t < 5.5 else "stumble"
        draw_stickman(draw, 340, 500, scale=1.3, pose=stick_pose, facing="right")
        
        # Org chart root
        root_x, root_y = 820, 150 + tilt_y
        draw.rounded_rectangle([root_x - 70, root_y - 25, root_x + 70, root_y + 25], radius=10, fill=INDIGO, outline=BLACK, width=2)
        draw.text((root_x - 55, root_y - 12), "ENGINEERING", font=font_node, fill=WHITE)
        
        # Level 1 Managers
        m1_x, m1_y = root_x - 180, root_y + 90
        m2_x, m2_y = root_x + 180, root_y + 90 + int(tilt_factor * 25)
        
        draw.line([(root_x, root_y + 25), (m1_x, m1_y - 20)], fill=BLACK, width=2)
        draw.line([(root_x, root_y + 25), (m2_x, m2_y - 20)], fill=BLACK, width=2)
        
        draw.rounded_rectangle([m1_x - 65, m1_y - 20, m1_x + 65, m1_y + 20], radius=8, fill=INDIGO, outline=BLACK, width=2)
        draw.text((m1_x - 50, m1_y - 10), "TEAM ALPHA", font=font_node, fill=WHITE)
        
        draw.rounded_rectangle([m2_x - 65, m2_y - 20, m2_x + 65, m2_y + 20], radius=8, fill=INDIGO, outline=BLACK, width=2)
        draw.text((m2_x - 50, m2_y - 10), "TEAM BETA", font=font_node, fill=WHITE)
        
        # Level 2 developers & amber bottleneck badges (meetings, review blockers)
        num_devs = min(6, int(2 + sc_t * 0.5))
        for d in range(num_devs):
            dx = 550 + d * 80
            dy = 320 + tilt_y + (d % 2) * 20
            draw.line([(m1_x if d < 3 else m2_x, m1_y + 20 if d < 3 else m2_y + 20), (dx, dy - 18)], fill=BLACK, width=1)
            draw.ellipse([dx - 18, dy - 18, dx + 18, dy + 18], fill=YELLOW_SHIRT, outline=BLACK, width=2)
            
        # Amber friction icons floating around
        if sc_t > 3.0:
            draw.rounded_rectangle([680, 230, 840, 275], radius=8, fill=AMBER, outline=BLACK, width=2)
            draw.text((695, 242), "📅 5 HRS MEETINGS", font=font_node, fill=BLACK)
            
            draw.rounded_rectangle([860, 210, 1020, 255], radius=8, fill=AMBER, outline=BLACK, width=2)
            draw.text((875, 222), "💬 PR BLOCKED (3d)", font=font_node, fill=BLACK)
            
        # Crack fracture lines radiating
        if sc_t > 5.0:
            crack_prog = min(1.0, (sc_t - 5.0) / 1.5)
            draw.line([(root_x, root_y), (root_x - int(120*crack_prog), root_y + int(140*crack_prog))], fill=AMBER, width=4)
            draw.line([(root_x, root_y), (root_x + int(140*crack_prog), root_y + int(110*crack_prog))], fill=AMBER, width=4)
            draw.line([(m1_x, m1_y), (m1_x + int(80*crack_prog), m1_y + int(90*crack_prog))], fill=AMBER, width=3)
            
            draw_outlined_text(draw, (710, 70), "COORDINATION OVERHEAD!", font=font_big_badge, fill_color=AMBER, stroke_color=BLACK, stroke_width=4)

    # -------------------------------------------------------------------------
    # SCENE 3: Insider Secrets (Two platforms drifting, file dropped)
    # -------------------------------------------------------------------------
    elif cur_scene["id"] == 3:
        # Platforms drifting apart
        drift = min(160, int(ease_in_out(min(1.0, sc_t / 5.0)) * 160))
        p1_x = 360 - drift
        p2_x = 760 + drift
        
        # Platform 1 (Left - Dev)
        draw.rounded_rectangle([p1_x - 180, 480, p1_x + 180, 520], radius=10, fill=INDIGO, outline=BLACK, width=3)
        draw.text((p1_x - 70, 490), "DEVELOPER POD", font=font_title, fill=WHITE)
        
        # Platform 2 (Right - QA / Deployment)
        draw.rounded_rectangle([p2_x - 180, 480, p2_x + 180, 520], radius=10, fill=INDIGO, outline=BLACK, width=3)
        draw.text((p2_x - 70, 490), "DEPLOYMENT POD", font=font_title, fill=WHITE)
        
        # Stickman on left platform edge
        stickman_pose = "stand" if sc_t < 4.0 else "stumble"
        draw_stickman(draw, p1_x + 110, 480, scale=1.3, pose=stickman_pose, facing="right")
        
        # Cyan file / artifact icon tossed into the gap
        file_start_x = p1_x + 130
        file_target_x = 560
        if sc_t < 4.0:
            # File moves forward in air
            prog = sc_t / 4.0
            fx = int(file_start_x + prog * (file_target_x - file_start_x))
            fy = int(360 - math.sin(prog * math.pi) * 80)
            draw.rounded_rectangle([fx - 24, fy - 30, fx + 24, fy + 30], radius=6, fill=CYAN, outline=BLACK, width=2)
            draw.text((fx - 14, fy - 16), "CODE", font=font_node, fill=WHITE)
        else:
            # File stalls and plummets downward into the abyss
            fall_prog = min(1.0, (sc_t - 4.0) / 4.0)
            fx = file_target_x
            fy = int(360 + fall_prog * fall_prog * 400)
            # Fading file
            if fy < HEIGHT + 50:
                draw.rounded_rectangle([fx - 24, fy - 30, fx + 24, fy + 30], radius=6, fill=AMBER, outline=BLACK, width=2)
                draw.text((fx - 16, fy - 14), "DROP", font=font_node, fill=WHITE)
                
            # Danger alert banner
            draw.rounded_rectangle([440, 220, 780, 280], radius=12, fill=AMBER, outline=BLACK, width=3)
            draw.text((465, 235), "⚠️ 72-HOUR HANDOFF GAP", font=font_title, fill=BLACK)

    # -------------------------------------------------------------------------
    # SCENE 4: Autonomous Mechanism (Robotic Arm + Continuous Loop)
    # -------------------------------------------------------------------------
    elif cur_scene["id"] == 4:
        stick_x = 280
        draw_stickman(draw, stick_x, 500, scale=1.3, pose="stand", facing="right")
        
        # Continuous circular loop (Write -> Test -> Deploy)
        loop_cx, loop_cy = 820, 310
        loop_r = 160
        
        # Rotating loop angle
        loop_ang = t * 1.8
        
        # Draw glowing circular track
        draw.ellipse([loop_cx - loop_r, loop_cy - loop_r, loop_cx + loop_r, loop_cy + loop_r],
                     outline=CYAN_GLOW, width=8)
        draw.ellipse([loop_cx - loop_r, loop_cy - loop_r, loop_cx + loop_r, loop_cy + loop_r],
                     outline=CYAN, width=3)
        
        # 3 Stages on the loop
        stages = [
            ("1. WRITE CODE", 0.0),
            ("2. RUN TESTS", 2.094),     # 2*pi/3
            ("3. DEPLOY & LOG", 4.188)   # 4*pi/3
        ]
        
        for name, base_a in stages:
            a = base_a + loop_ang
            nx = int(loop_cx + math.cos(a) * loop_r)
            ny = int(loop_cy + math.sin(a) * loop_r)
            draw.ellipse([nx - 36, ny - 36, nx + 36, ny + 36], fill=WHITE, outline=CYAN, width=4)
            draw.ellipse([nx - 28, ny - 28, nx + 28, ny + 28], fill=CYAN)
            draw_outlined_text(draw, (nx - 50, ny + 42), name, font=font_node, fill_color=BLACK, stroke_color=WHITE, stroke_width=2)
            
        # Center core: "AGENT LOOP"
        draw.ellipse([loop_cx - 50, loop_cy - 50, loop_cx + 50, loop_cy + 50], fill=INDIGO, outline=WHITE, width=3)
        draw.text((loop_cx - 36, loop_cy - 12), "ZERO WAIT", font=font_node, fill=WHITE)
        
        # If stickman steps in, loop gracefully arcs around
        if sc_t > 5.0:
            draw.line([(stick_x + 30, 420), (loop_cx - loop_r - 20, 310)], fill=CYAN, width=2)
            draw_outlined_text(draw, (560, 100), "NO WAITING FOR SLACK REPLIES ⚡", font=font_big_badge, fill_color=CYAN, stroke_color=BLACK, stroke_width=4)

    # -------------------------------------------------------------------------
    # SCENE 5: Scale & Multiplier (10 Orbiting Nodes + 10X Stack + Wave)
    # -------------------------------------------------------------------------
    elif cur_scene["id"] == 5:
        stick_x = int(320 + sc_pct * 160)
        draw_stickman(draw, stick_x, 500, scale=1.3, pose="surf", facing="right")
        
        # Surfing energy wave on floor
        wave_front = int(stick_x + 80)
        draw.arc([wave_front - 200, 480, wave_front + 200, 560], 180, 360, fill=CYAN, width=6)
        draw.arc([wave_front - 240, 490, wave_front + 240, 570], 180, 360, fill=CYAN_GLOW, width=3)
        
        # 10 Orbiting agent nodes
        orbit_r = 180
        for i in range(10):
            node_ang = (i / 10.0) * 2 * math.pi + t * 3.0
            nx = int(stick_x + math.cos(node_ang) * orbit_r)
            ny = int(350 + math.sin(node_ang) * (orbit_r * 0.45))
            draw.ellipse([nx - 12, ny - 12, nx + 12, ny + 12], fill=CYAN, outline=WHITE, width=2)
            # Motion particle trail
            trail_ang = node_ang - 0.25
            tx = int(stick_x + math.cos(trail_ang) * orbit_r)
            ty = int(350 + math.sin(trail_ang) * (orbit_r * 0.45))
            draw.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=CYAN_GLOW)
            
        # 10X Multiplier Badge
        draw.rounded_rectangle([880, 160, 1180, 270], radius=16, fill=BLACK, outline=CYAN, width=4)
        draw.text((910, 185), "10X VELOCITY", font=font_big_badge, fill=YELLOW_SHIRT)
        draw.text((915, 235), "Same headcount. No idle time.", font=font_node, fill=WHITE)

    # -------------------------------------------------------------------------
    # SCENE 6: Elevation & CTA (Fork in the Road + Point to Viewer)
    # -------------------------------------------------------------------------
    elif cur_scene["id"] == 6:
        # Stickman stands center, pointing forward
        stick_x, stick_y = 640, 490
        draw_stickman(draw, stick_x, stick_y, scale=1.4, pose="point", facing="right")
        
        # Floor grid splits into two diverging colored tracks
        # Left path (Amber): "COMPETING AGAINST AGENTS"
        draw.line([(stick_x, 490), (220, 280)], fill=AMBER, width=6)
        draw.rounded_rectangle([100, 210, 340, 280], radius=12, fill=WHITE, outline=AMBER, width=3)
        draw.text((120, 225), "LEGACY TEAMS", font=font_title, fill=BLACK)
        draw.text((120, 255), "Friction & Burnout", font=font_node, fill=AMBER)
        
        # Right path (Electric Cyan): "BUILDING WITH AGENTS"
        draw.line([(stick_x, 490), (1060, 280)], fill=CYAN, width=6)
        draw.rounded_rectangle([860, 210, 1180, 280], radius=12, fill=WHITE, outline=CYAN, width=3)
        draw.text((885, 225), "AGENTIC TEAMS", font=font_title, fill=BLACK)
        draw.text((885, 255), "10x Output & Velocity", font=font_node, fill=CYAN)
        
        # Central Question Callout
        draw_outlined_text(draw, (380, 90), "WHAT DO YOU THINK? 👇", font=font_big_badge, fill_color=YELLOW_SHIRT, stroke_color=BLACK, stroke_width=4)

    # -------------------------------------------------------------------------
    # GLOBAL HUD: TOP TITLE BADGE, LOWER-THIRD SUBTITLES, PROGRESS BAR
    # -------------------------------------------------------------------------
    # 1. Top Title Badge (Clean modern tech sticker)
    draw.rounded_rectangle([35, 25, 430, 75], radius=10, fill=BLACK, outline=CYAN, width=2)
    draw.text((50, 37), "AI AGENTS VS DEV TEAMS", font=font_title, fill=WHITE)
    
    # Stage Tag on Right
    draw.rounded_rectangle([WIDTH - 360, 25, WIDTH - 35, 75], radius=10, fill=WHITE, outline=BLACK, width=2)
    draw.text((WIDTH - 340, 38), cur_scene["badge"], font=font_node, fill=INDIGO)
    
    # 2. Lower-Third High-Engagement Subtitles
    sub_bg_y = 575
    draw.rounded_rectangle([35, sub_bg_y, WIDTH - 35, sub_bg_y + 115], radius=14, fill=BLACK, outline=CYAN, width=2)
    
    # Headline in bold yellow/cyan
    draw.text((55, sub_bg_y + 18), cur_scene["caption_main"], font=font_caption_bold, fill=YELLOW_SHIRT)
    # Secondary explanation in clean white
    draw.text((55, sub_bg_y + 68), cur_scene["caption_sub"], font=font_caption, fill=WHITE)
    
    # 3. Bottom Progress Bar in Cyan
    prog_pct = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 8, int(WIDTH * prog_pct), HEIGHT], fill=CYAN)

    # Write raw RGB bytes directly to FFmpeg stdin
    rgb_bytes = img.tobytes()
    proc.stdin.write(rgb_bytes)
    
    if f % 120 == 0:
        pct = (f / float(TOTAL_FRAMES)) * 100.0
        print(f"  Rendering frame {f}/{TOTAL_FRAMES} ({pct:.1f}% | {t:.1f}s)...")

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"🎉 MASTER 60S STICKMAN VIDEO RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames @ 24fps)")
if os.path.exists(output_mp4):
    size_mb = os.path.getsize(output_mp4) / 1_000_000.0
    print(f"File Size: {size_mb:.2f} MB")
print("="*60)
