import os, sys, math, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\realistic_character_fixing_systems"
audio_path = os.path.join(proj_dir, "audio", "master_action_audio.wav")
output_mp4 = os.path.join(proj_dir, "AGENT_FIXING_SYSTEMS_16x9.mp4")
timeline_path = os.path.join(proj_dir, "action_timeline.json")

with open(timeline_path, 'r', encoding='utf-8') as f:
    t_data = json.load(f)

TOTAL_DURATION = t_data["total_duration"]
timeline = t_data["timeline"]

WIDTH = 1280
HEIGHT = 720
FPS = 24
TOTAL_FRAMES = int(math.ceil(TOTAL_DURATION * FPS))

print(f"[+] Initializing Action Animation Render ({TOTAL_DURATION:.2f}s, {TOTAL_FRAMES} frames)...")

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)
font_caption_bold = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 34)
font_caption_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)
font_hud = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 44)

# Colors
BG_WHITE = (248, 250, 252)
GRID_LINE = (226, 232, 240)
CYAN = (6, 182, 212)
CYAN_GLOW = (165, 243, 252)
GREEN = (34, 197, 94)
AMBER = (245, 158, 11)
RED_ALERT = (239, 68, 68)
YELLOW_SHIRT = (250, 204, 21)
RED_BEANIE = (225, 29, 72)
INDIGO_SHORTS = (49, 46, 129)
BLACK = (15, 23, 42)
WHITE = (255, 255, 255)
SERVER_DARK = (30, 41, 59)

# Ground line
GROUND_Y = 530

# -----------------------------------------------------------------------------
# Kinematic Character Drawing Function
# -----------------------------------------------------------------------------
def draw_character(draw, cx, cy, state="stand", facing="right", walk_phase=0.0, action_t=0.0):
    """
    Renders realistic articulated 3D stickman mascot with 2-segment limbs:
    - State: 'stand', 'walk', 'scan', 'type', 'pull_lever', 'victory'
    - Facing: 'right' or 'left'
    """
    s = 1.25
    dir_m = 1 if facing == "right" else -1
    
    # Vertical body bob during walk
    bob = -abs(math.sin(walk_phase * 2.0)) * 5.0 if state == "walk" else 0.0
    
    # Head & Beanie
    head_r = int(22 * s)
    head_cy = int(cy - 92 * s + bob)
    head_cx = int(cx)
    
    # Shadow beneath character on floor
    draw.ellipse([cx - int(32 * s), GROUND_Y - 4, cx + int(32 * s), GROUND_Y + 6], fill=(210, 218, 226))
    
    # 1. Head (Hollow sphere with smooth specular shading)
    draw.ellipse([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
                 fill=WHITE, outline=BLACK, width=int(3 * s))
    
    # Eye direction gaze
    eye_ox = int(7 * s * dir_m)
    eye_oy = -2
    if state == "type":
        eye_oy = 5  # looking down at keyboard
    elif state == "scan":
        eye_ox = int(9 * s * dir_m)
    draw.ellipse([head_cx + eye_ox - 2, head_cy + eye_oy - 3,
                  head_cx + eye_ox + 2, head_cy + eye_oy + 1], fill=BLACK)
    
    # Red Beanie (Smooth rounded knit, no pom-pom)
    draw.pieslice([head_cx - head_r - int(2*s), head_cy - head_r - int(12*s),
                   head_cx + head_r + int(2*s), head_cy], 180, 360, fill=RED_BEANIE, outline=BLACK, width=2)
    draw.rounded_rectangle([head_cx - head_r - int(3*s), head_cy - int(14*s),
                            head_cx + head_r + int(3*s), head_cy - int(4*s)],
                           radius=int(4*s), fill=RED_BEANIE, outline=BLACK, width=2)
    
    # 2. Torso / Yellow Shirt
    torso_top = head_cy + head_r
    torso_bot = int(cy - 34 * s + bob)
    shirt_w = int(18 * s)
    draw.rounded_rectangle([head_cx - shirt_w, torso_top, head_cx + shirt_w, torso_bot],
                           radius=int(6*s), fill=YELLOW_SHIRT, outline=BLACK, width=int(2.5*s))
    
    # Dark Shorts
    shorts_bot = int(cy - 20 * s + bob)
    draw.rectangle([head_cx - shirt_w + int(2*s), torso_bot, head_cx + shirt_w - int(2*s), shorts_bot],
                   fill=INDIGO_SHORTS, outline=BLACK, width=2)
    
    # 3. Articulated Legs (Hip -> Knee -> Foot)
    hip_y = shorts_bot
    hip_l = head_cx - int(6 * s)
    hip_r = head_cx + int(6 * s)
    limb_w = int(3.5 * s)
    
    if state == "walk":
        # Stride phase: Left and Right legs 180 deg apart
        str_l = math.sin(walk_phase)
        str_r = math.sin(walk_phase + math.pi)
        
        # Left Leg
        foot_l_x = hip_l + int(str_l * 28 * s * dir_m)
        foot_l_y = GROUND_Y - max(0, int(-math.cos(walk_phase) * 12 * s))
        knee_l_x = (hip_l + foot_l_x) // 2 + int(4 * s * dir_m)
        knee_l_y = (hip_y + foot_l_y) // 2
        draw.line([(hip_l, hip_y), (knee_l_x, knee_l_y)], fill=BLACK, width=limb_w)
        draw.line([(knee_l_x, knee_l_y), (foot_l_x, foot_l_y)], fill=BLACK, width=limb_w)
        draw.line([(foot_l_x, foot_l_y), (foot_l_x + int(8*s*dir_m), foot_l_y)], fill=BLACK, width=limb_w)
        
        # Right Leg
        foot_r_x = hip_r + int(str_r * 28 * s * dir_m)
        foot_r_y = GROUND_Y - max(0, int(-math.cos(walk_phase + math.pi) * 12 * s))
        knee_r_x = (hip_r + foot_r_x) // 2 + int(4 * s * dir_m)
        knee_r_y = (hip_y + foot_r_y) // 2
        draw.line([(hip_r, hip_y), (knee_r_x, knee_r_y)], fill=BLACK, width=limb_w)
        draw.line([(knee_r_x, knee_r_y), (foot_r_x, foot_r_y)], fill=BLACK, width=limb_w)
        draw.line([(foot_r_x, foot_r_y), (foot_r_x + int(8*s*dir_m), foot_r_y)], fill=BLACK, width=limb_w)
        
    else:
        # Standing straight
        draw.line([(hip_l, hip_y), (hip_l, GROUND_Y)], fill=BLACK, width=limb_w)
        draw.line([(hip_l, GROUND_Y), (hip_l + int(8*s*dir_m), GROUND_Y)], fill=BLACK, width=limb_w)
        draw.line([(hip_r, hip_y), (hip_r, GROUND_Y)], fill=BLACK, width=limb_w)
        draw.line([(hip_r, GROUND_Y), (hip_r + int(8*s*dir_m), GROUND_Y)], fill=BLACK, width=limb_w)

    # 4. Articulated Arms (Shoulder -> Elbow -> Hand)
    sh_y = torso_top + int(8 * s)
    sh_l = head_cx - shirt_w
    sh_r = head_cx + shirt_w
    
    if state == "walk":
        # Arms swing in counter-rhythm
        sw_l = math.sin(walk_phase + math.pi) * 22 * s
        sw_r = math.sin(walk_phase) * 22 * s
        draw.line([(sh_l, sh_y), (sh_l - int(sw_l * 0.4), sh_y + int(24*s)), (sh_l - int(sw_l), sh_y + int(42*s))], fill=BLACK, width=limb_w)
        draw.line([(sh_r, sh_y), (sh_r + int(sw_r * 0.4), sh_y + int(24*s)), (sh_r + int(sw_r), sh_y + int(42*s))], fill=BLACK, width=limb_w)
        
    elif state == "scan":
        # Left arm on hip
        draw.line([(sh_l, sh_y), (sh_l - int(12*s), sh_y + int(20*s)), (head_cx - shirt_w, torso_bot)], fill=BLACK, width=limb_w)
        # Right arm pointing diagnostic scanner at server
        scanner_x = head_cx + int(55 * s * dir_m)
        scanner_y = sh_y - int(5 * s)
        draw.line([(sh_r, sh_y), (head_cx + int(30*s*dir_m), sh_y - int(10*s)), (scanner_x, scanner_y)], fill=BLACK, width=limb_w)
        # Handheld scanner tool
        draw.rounded_rectangle([scanner_x - 6, scanner_y - 12, scanner_x + 14, scanner_y + 12], radius=3, fill=BLACK, outline=CYAN, width=2)
        # Emitter tip
        draw.ellipse([scanner_x + 12*dir_m - 4, scanner_y - 4, scanner_x + 12*dir_m + 4, scanner_y + 4], fill=CYAN)
        
    elif state == "type":
        # Rapid typing on holographic keyboard
        tap_l = math.sin(action_t * 32.0) * 8.0
        tap_r = math.cos(action_t * 32.0) * 8.0
        # Left arm
        draw.line([(sh_l, sh_y), (head_cx - int(10*s), sh_y + int(22*s)), (head_cx - int(2*s), sh_y + int(36*s + tap_l))], fill=BLACK, width=limb_w)
        # Right arm
        draw.line([(sh_r, sh_y), (head_cx + int(14*s), sh_y + int(22*s)), (head_cx + int(20*s), sh_y + int(36*s + tap_r))], fill=BLACK, width=limb_w)
        
    elif state == "pull_lever":
        # Left arm relaxed
        draw.line([(sh_l, sh_y), (sh_l - int(8*s), sh_y + int(35*s))], fill=BLACK, width=limb_w)
        # Right arm raised reaching for lever knob
        lever_grip_x = cx + int(45 * s)
        lever_grip_y = cy - int(50 * s)
        draw.line([(sh_r, sh_y), (sh_r + int(20*s), sh_y - int(25*s)), (lever_grip_x, lever_grip_y)], fill=BLACK, width=limb_w)
        
    elif state == "victory":
        # Both arms raised in high "V" triumph holding floating cyan cube
        draw.line([(sh_l, sh_y), (sh_l - int(32*s), sh_y - int(38*s))], fill=BLACK, width=limb_w)
        draw.line([(sh_r, sh_y), (sh_r + int(32*s), sh_y - int(38*s))], fill=BLACK, width=limb_w)
        # Floating glowing cyan cube overhead
        cube_cx = cx
        cube_cy = head_cy - int(45 * s) + int(math.sin(action_t * 5.0) * 6)
        cr = int(18 * s)
        draw.rounded_rectangle([cube_cx - cr, cube_cy - cr, cube_cx + cr, cube_cy + cr], radius=4, fill=CYAN, outline=WHITE, width=2)
        draw.ellipse([cube_cx - cr - 8, cube_cy - cr - 8, cube_cx + cr + 8, cube_cy + cr + 8], outline=CYAN_GLOW, width=2)

    else: # stand
        draw.line([(sh_l, sh_y), (sh_l - int(10*s), sh_y + int(36*s))], fill=BLACK, width=limb_w)
        draw.line([(sh_r, sh_y), (sh_r + int(10*s), sh_y + int(36*s))], fill=BLACK, width=limb_w)

# -----------------------------------------------------------------------------
# Environment & Systems Drawing
# -----------------------------------------------------------------------------
def draw_studio_backdrop(draw):
    # Floor perspective grid
    draw.line([(0, 390), (WIDTH, 390)], fill=GRID_LINE, width=1)
    for x in range(-200, WIDTH + 400, 75):
        draw.line([(WIDTH // 2, 390), (x, HEIGHT)], fill=GRID_LINE, width=1)
    for i in range(1, 12):
        y = int(390 + ((i / 11.0) ** 1.7) * (HEIGHT - 390))
        draw.line([(0, y), (WIDTH, y)], fill=GRID_LINE, width=1)

def draw_server_rack(draw, t, server_fixed=False, is_scanning=False):
    """Station 1 at X=160: Dual Server Tower"""
    sx, sy = 90, 200
    sw, sh = 150, 330
    
    # Server cabinet
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=SERVER_DARK, outline=BLACK, width=3)
    
    # Server bays
    for bay in range(7):
        by = sy + 25 + bay * 40
        draw.rectangle([sx + 10, by, sx + sw - 10, by + 30], fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        # Drive bays
        draw.rectangle([sx + 15, by + 6, sx + 50, by + 24], fill=(71, 85, 105))
        # Status LEDs
        led_col = GREEN if server_fixed else (RED_ALERT if bay % 2 == 0 else AMBER)
        if not server_fixed and (int(t * 8) % 2 == 0):
            led_col = (100, 20, 20)  # blinking alarm
        for l in range(3):
            draw.ellipse([sx + 60 + l * 14, by + 12, sx + 68 + l * 14, by + 20], fill=led_col)
            
    # Top Alarm Beacon
    beacon_col = GREEN if server_fixed else ((255, 50, 50) if (int(t * 6) % 2 == 0) else (120, 0, 0))
    draw.rounded_rectangle([sx + 50, sy - 22, sx + 100, sy], radius=6, fill=beacon_col, outline=BLACK, width=2)
    
    # LCD Banner on rack
    lcd_text = "STATUS: 100% HEALTHY" if server_fixed else "ERR: POOL CRASHED"
    lcd_col = GREEN if server_fixed else RED_ALERT
    draw.rectangle([sx + 10, sy + 6, sx + sw - 10, sy + 22], fill=BLACK)
    draw.text((sx + 14, sy + 7), lcd_text, font=font_code, fill=lcd_col)
    
    # Scanning laser fan effect
    if is_scanning:
        laser_y = int(sy + 30 + (math.sin(t * 8.0) * 0.5 + 0.5) * 260)
        draw.line([(sx, laser_y), (sx + sw, laser_y)], fill=CYAN, width=3)
        draw.polygon([(280, 420), (sx, laser_y - 12), (sx, laser_y + 12)], fill=(6, 182, 212, 60))

def draw_cyber_console(draw, t, is_typing=False, tests_passed=0):
    """Station 2 at X=640: Central Cyber Console with Curved Holographic Glass"""
    cx, cy = 640, 390
    
    # Console pedestal base
    draw.polygon([(cx - 120, GROUND_Y), (cx + 120, GROUND_Y),
                  (cx + 80, cy + 50), (cx - 80, cy + 50)], fill=(51, 65, 85), outline=BLACK)
    
    # Floating curved glass terminal
    draw.ellipse([cx - 150, cy + 30, cx + 150, cy + 70], fill=(15, 23, 42), outline=CYAN, width=2)
    
    # Virtual glowing keyboard on desk
    for kx in range(-90, 100, 24):
        for ky in [42, 54]:
            k_glow = YELLOW_SHIRT if (is_typing and (int(t * 20 + kx) % 3 == 0)) else CYAN
            draw.rectangle([cx + kx - 8, cy + ky - 4, cx + kx + 8, cy + ky + 4], fill=k_glow)
            
    # Floating Curved Holographic Monitors above desk
    # Center Monitor
    draw.rounded_rectangle([cx - 140, cy - 140, cx + 140, cy + 10], radius=10, fill=(10, 18, 35), outline=CYAN, width=2)
    draw.text((cx - 125, cy - 130), "> AGENT EXECUTION TERMINAL", font=font_code, fill=CYAN)
    draw.line([(cx - 130, cy - 110), (cx + 130, cy - 110)], fill=CYAN, width=1)
    
    # Dynamic code feed lines
    code_lines = [
        ("git checkout -b hotfix/conn-pool", WHITE),
        ("patch --apply connection_manager.ts", YELLOW_SHIRT),
        ("Running 48 unit tests...", CYAN)
    ]
    for i, (cline, ccol) in enumerate(code_lines):
        draw.text((cx - 125, cy - 95 + i * 20), cline, font=font_code, fill=ccol)
        
    # Test pass indicators
    if tests_passed >= 1:
        draw.text((cx - 125, cy - 35), "✔ [PASS] tests/auth.spec.ts", font=font_code, fill=GREEN)
    if tests_passed >= 2:
        draw.text((cx - 125, cy - 18), "✔ [PASS] tests/db_pool.spec.ts", font=font_code, fill=GREEN)
    if tests_passed >= 3:
        draw.text((cx - 125, cy - 1), "✔ [PASS] tests/api_gateway.spec.ts", font=font_code, fill=GREEN)

def draw_deploy_pillar(draw, t, is_lever_down=False, is_launching=False):
    """Station 3 at X=1080: Deployment Core Pillar & Satellite Uplink"""
    px, py = 1040, 220
    pw, ph = 120, 310
    
    # Cylindrical power tower
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill=SERVER_DARK, outline=BLACK, width=3)
    
    # Vertical glowing energy gauge (fills up)
    fill_pct = 1.0 if is_lever_down else min(1.0, max(0.0, (t - 26.5) / 6.0))
    gauge_h = int(220 * fill_pct)
    gauge_col = GREEN if is_lever_down else CYAN
    
    draw.rounded_rectangle([px + 20, py + 30, px + 50, py + 250], radius=8, fill=BLACK, outline=CYAN, width=2)
    if gauge_h > 2:
        draw.rounded_rectangle([px + 22, py + 250 - gauge_h, px + 48, py + 248], radius=min(6, gauge_h // 2), fill=gauge_col)
    draw.text((px + 12, py + 260), f"{int(fill_pct*100)}%", font=font_code, fill=WHITE)
    
    # Master Deployment Switch / Lever
    lever_box_x = px + 65
    lever_box_y = py + 120
    draw.rounded_rectangle([lever_box_x, lever_box_y, lever_box_x + 35, lever_box_y + 80], radius=6, fill=BLACK, outline=AMBER, width=2)
    
    lever_pivot_x = lever_box_x + 17
    lever_pivot_y = lever_box_y + 40
    
    lever_end_y = lever_pivot_y + 25 if is_lever_down else lever_pivot_y - 25
    lever_end_x = lever_pivot_x + 8
    draw.line([(lever_pivot_x, lever_pivot_y), (lever_end_x, lever_end_y)], fill=AMBER, width=6)
    draw.ellipse([lever_end_x - 8, lever_end_y - 8, lever_end_x + 8, lever_end_y + 8], fill=RED_ALERT, outline=WHITE, width=2)
    
    # Top Rocket / Satellite Uplink Beam
    if is_launching:
        beam_x = px + pw // 2
        draw.line([(beam_x, py), (beam_x, 0)], fill=CYAN, width=12)
        draw.line([(beam_x, py), (beam_x, 0)], fill=WHITE, width=4)
        for spark_i in range(8):
            sy = int((t * 600 + spark_i * 80) % py)
            draw.ellipse([beam_x - 8, sy - 8, beam_x + 8, sy + 8], fill=CYAN_GLOW)
            
        draw.rounded_rectangle([px - 40, py - 45, px + pw + 40, py - 5], radius=8, fill=BLACK, outline=GREEN, width=2)
        draw.text((px - 25, py - 35), "🚀 DEPLOYED TO EDGE", font=font_title, fill=GREEN)

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

# Scene Script Metadata
scene_captions = {
    1: {
        "title": "ACT 1: ALARM & DISPATCH",
        "main": "SERVER CRASH AT 2:00 AM — AGENT DEPLOYED 🚨",
        "sub": "Autonomous agent immediately approaches Server Rack 04.",
        "badge": "🚨 EMERGENCY INTERVENTION"
    },
    2: {
        "title": "ACT 2: SCAN & INJECT HOTFIX",
        "main": "SCANNING HARDWARE & INJECTING PATCH ⚡",
        "sub": "Memory leak detected at line 142. Bypassed in under 6 seconds.",
        "badge": "🔧 IN-PLACE HARDWARE FIX"
    },
    3: {
        "title": "ACT 3: CONSOLE INTEGRATION TESTS",
        "main": "TYPING TESTS ON CYBER CONSOLE 💻",
        "sub": "Running 48 unit tests in real time — all regression suites green.",
        "badge": "💻 ZERO-HUMAN TESTING"
    },
    4: {
        "title": "ACT 4: GLOBAL PRODUCTION DEPLOY",
        "main": "PULLING MASTER DEPLOYMENT LEVER 🚀",
        "sub": "Patch routed through edge pipeline. Global production online.",
        "badge": "🚀 INSTANT PRODUCTION RELEASE"
    },
    5: {
        "title": "ACT 5: RESTORATION & VERDICT",
        "main": "FIXED IN 45s WITHOUT WAKING HUMANS 🏆",
        "sub": "Are you still fixing bugs manually? Drop your thoughts below!",
        "badge": "🏆 AUTONOMOUS VICTORY"
    }
}

for f in range(TOTAL_FRAMES):
    t = f / float(FPS)
    
    # Identify active scene
    cur_sc = timeline[-1]
    for sc in timeline:
        if sc["start"] <= t < sc["end"]:
            cur_sc = sc
            break
            
    sc_id = cur_sc["id"]
    sc_t = max(0.0, t - cur_sc["start"])
    sc_dur = max(0.1, cur_sc["duration"])
    
    # -------------------------------------------------------------------------
    # Character State & Waypoint Locomotion
    # -------------------------------------------------------------------------
    # Waypoints:
    # Station 1 (Server): X = 280
    # Station 2 (Console): X = 640
    # Station 3 (Pillar): X = 1010
    
    walk_cycle_speed = 14.0
    
    if sc_id == 1:
        # Act 1: Walks from center (640) to server (280)
        # Move between 1.0s and 5.2s
        walk_p = min(1.0, max(0.0, (sc_t - 1.0) / 4.2))
        char_x = int(640 - walk_p * (640 - 280))
        char_facing = "left"
        if 1.0 <= sc_t < 5.2:
            char_state = "walk"
            char_walk_phase = sc_t * walk_cycle_speed
        else:
            char_state = "stand"
            char_walk_phase = 0.0

    elif sc_id == 2:
        # Act 2: Stands at server (280) and scans hardware
        char_x = 280
        char_facing = "left"
        char_walk_phase = 0.0
        if sc_t < 6.5:
            char_state = "scan"
        else:
            char_state = "stand"

    elif sc_id == 3:
        # Act 3: Walks from server (280) to console (640), then types
        # Walk between 0.0s and 3.5s
        walk_p = min(1.0, max(0.0, sc_t / 3.5))
        char_x = int(280 + walk_p * (640 - 280))
        char_facing = "right"
        if sc_t < 3.5:
            char_state = "walk"
            char_walk_phase = sc_t * walk_cycle_speed
        else:
            char_state = "type"
            char_walk_phase = 0.0

    elif sc_id == 4:
        # Act 4: Walks from console (640) to deploy pillar (1010), then pulls lever
        # Walk between 0.0s and 3.4s
        walk_p = min(1.0, max(0.0, sc_t / 3.4))
        char_x = int(640 + walk_p * (1010 - 640))
        char_facing = "right"
        if sc_t < 3.4:
            char_state = "walk"
            char_walk_phase = sc_t * walk_cycle_speed
        elif sc_t < 6.8:
            char_state = "pull_lever"
            char_walk_phase = 0.0
        else:
            char_state = "stand"
            char_walk_phase = 0.0

    else:
        # Act 5: Walks back from pillar (1010) to center (640) and victory pose
        # Walk between 0.0s and 3.2s
        walk_p = min(1.0, max(0.0, sc_t / 3.2))
        char_x = int(1010 - walk_p * (1010 - 640))
        char_facing = "left" if sc_t < 3.2 else "right"
        if sc_t < 3.2:
            char_state = "walk"
            char_walk_phase = sc_t * walk_cycle_speed
        else:
            char_state = "victory"
            char_walk_phase = 0.0

    # -------------------------------------------------------------------------
    # Render Studio Canvas
    # -------------------------------------------------------------------------
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_WHITE)
    draw = ImageDraw.Draw(img)
    
    # 1. Background studio grid
    draw_studio_backdrop(draw)
    
    # 2. Draw Interactive Systems
    # Server fixed after Act 2 (t >= 14.6s)
    server_is_fixed = (t >= 14.6)
    server_is_scanning = (sc_id == 2 and sc_t < 6.5)
    draw_server_rack(draw, t, server_fixed=server_is_fixed, is_scanning=server_is_scanning)
    
    # Cyber console typing & unit tests
    console_is_typing = (sc_id == 3 and sc_t >= 3.5)
    tests_count = 0
    if sc_id == 3:
        if sc_t >= 4.5: tests_count = 1
        if sc_t >= 5.8: tests_count = 2
        if sc_t >= 7.0: tests_count = 3
    elif sc_id >= 4:
        tests_count = 3
    draw_cyber_console(draw, t, is_typing=console_is_typing, tests_passed=tests_count)
    
    # Deploy pillar & master lever
    lever_is_pulled = (t >= 33.2)
    launch_is_active = (t >= 34.5)
    draw_deploy_pillar(draw, t, is_lever_down=lever_is_pulled, is_launching=launch_is_active)
    
    # 3. Draw Character with Articulated Limbs
    draw_character(draw, char_x, GROUND_Y, state=char_state, facing=char_facing,
                   walk_phase=char_walk_phase, action_t=sc_t)
                   
    # -------------------------------------------------------------------------
    # GLOBAL HUD: HEADER BADGE, SUBTITLES, PROGRESS BAR
    # -------------------------------------------------------------------------
    cap_info = scene_captions.get(sc_id, scene_captions[1])
    
    # Top Header
    draw.rounded_rectangle([40, 25, 430, 75], radius=10, fill=BLACK, outline=CYAN, width=2)
    draw.text((55, 37), "AUTONOMOUS SYSTEM REPAIR", font=font_title, fill=WHITE)
    
    draw.rounded_rectangle([WIDTH - 360, 25, WIDTH - 40, 75], radius=10, fill=WHITE, outline=BLACK, width=2)
    draw.text((WIDTH - 340, 39), cap_info["badge"], font=font_badge, fill=BLACK)
    
    # Lower-Third Dynamic Subtitles
    sub_y = 575
    draw.rounded_rectangle([40, sub_y, WIDTH - 40, sub_y + 115], radius=16, fill=BLACK, outline=CYAN, width=3)
    draw.text((65, sub_y + 16), cap_info["main"], font=font_caption_bold, fill=YELLOW_SHIRT)
    draw.text((65, sub_y + 70), cap_info["sub"], font=font_caption_sub, fill=WHITE)
    
    # Bottom Progress Bar
    prog = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 10, int(WIDTH * prog), HEIGHT], fill=CYAN)
    
    # Write RGB frame to FFmpeg
    proc.stdin.write(img.tobytes())
    
    if f % 120 == 0:
        pct = (f / float(TOTAL_FRAMES)) * 100.0
        print(f"  Rendering frame {f}/{TOTAL_FRAMES} ({pct:.1f}% | {t:.1f}s)...")

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print("REALISTIC CHARACTER ACTION VIDEO RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames @ 24fps)")
if os.path.exists(output_mp4):
    size_mb = os.path.getsize(output_mp4) / 1_000_000.0
    print(f"File Size: {size_mb:.2f} MB")
print("="*60)
