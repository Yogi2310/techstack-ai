import os, sys, math, json, textwrap, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJ_DIR = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems"
AUDIO_DIR = os.path.join(PROJ_DIR, "audio")
SNAPSHOT_DIR = os.path.join(PROJ_DIR, "snapshots")
TIMELINE_FILE = os.path.join(PROJ_DIR, "lego_action_timeline.json")
MASTER_AUDIO = os.path.join(AUDIO_DIR, "lego_master_audio.wav")
OUTPUT_VIDEO = os.path.join(PROJ_DIR, "LEGO_AGENT_FIXING_SYSTEMS_16x9.mp4")
LOGO_PATH = r"D:\Antigravity\Pro\channel_profile_pic.png"

with open(TIMELINE_FILE, 'r', encoding='utf-8') as f:
    timeline_data = json.load(f)

TOTAL_DURATION = timeline_data["total_duration"]
FPS = 24
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)
WIDTH, HEIGHT = 1280, 720

print(f"[+] Re-rendering Branded LEGO Movie: {TOTAL_DURATION}s | {TOTAL_FRAMES} frames @ {FPS}fps")

def get_font(name, size):
    try:
        path = os.path.join("C:/Windows/Fonts", name)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_brand = get_font("arialbd.ttf", 26)
font_sub_speaker = get_font("arialbd.ttf", 24)
font_sub_body = get_font("arial.ttf", 24)
font_hud_title = get_font("arialbd.ttf", 18)
font_hud_code = get_font("consola.ttf", 17)
font_hud_code_bold = get_font("consolab.ttf", 17)
font_server_status = get_font("arialbd.ttf", 16)
font_lever_gauge = get_font("arialbd.ttf", 18)
font_banner_main = get_font("arialbd.ttf", 34)
font_banner_sub = get_font("arialbd.ttf", 21)

# -----------------------------------------------------------------------------
# Channel Logo Generator
# -----------------------------------------------------------------------------
def make_circular_logo(img, size, border_color=(0, 220, 255), border_width=3):
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([0, 0, size - 1, size - 1], fill=255)
    
    circ = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circ.paste(img, (0, 0), mask=mask)
    
    draw_circ = ImageDraw.Draw(circ)
    draw_circ.ellipse([border_width//2, border_width//2, size - 1 - border_width//2, size - 1 - border_width//2], outline=border_color, width=border_width)
    return circ

logo_raw = Image.open(LOGO_PATH).convert("RGBA")
logo_header = make_circular_logo(logo_raw, 54, border_color=(0, 240, 255), border_width=2)
logo_watermark = make_circular_logo(logo_raw, 56, border_color=(0, 240, 255), border_width=2)
logo_victory = make_circular_logo(logo_raw, 84, border_color=(0, 255, 220), border_width=3)

# -----------------------------------------------------------------------------
# 3D LEGO Primitives
# -----------------------------------------------------------------------------
def draw_lego_stud(draw, cx, cy, r=10, h=6, base_col=(175, 180, 190), top_col=(235, 240, 250), outline_col=(185, 190, 200)):
    draw.ellipse([cx - r, cy - h, cx + r, cy + h], fill=base_col)
    draw.ellipse([cx - r + 1, cy - h - 3, cx + r - 1, cy + h - 3], fill=top_col, outline=outline_col, width=2)
    ir = r * 0.52
    draw.ellipse([cx - ir, cy - h*0.5 - 3, cx + ir, cy + h*0.5 - 3], outline=outline_col, width=1)

def draw_lego_brick(draw, x0, y0, w, h, base_col, light_col, shadow_col, studs=4, outline=(20, 25, 30)):
    top_h = 12
    top_poly = [(x0, y0), (x0 + 12, y0 - top_h), (x0 + w + 12, y0 - top_h), (x0 + w, y0)]
    draw.polygon(top_poly, fill=light_col, outline=outline, width=2)
    
    front_poly = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    draw.polygon(front_poly, fill=base_col, outline=outline, width=2)
    
    right_poly = [(x0 + w, y0), (x0 + w + 12, y0 - top_h), (x0 + w + 12, y0 + h - top_h), (x0 + w, y0 + h)]
    draw.polygon(right_poly, fill=shadow_col, outline=outline, width=2)
    
    if studs > 0:
        step = w / studs
        for i in range(studs):
            scx = x0 + (i + 0.5) * step + 6
            scy = y0 - top_h * 0.5
            draw_lego_stud(draw, scx, scy, r=max(5, int(step*0.24)), h=4, base_col=shadow_col, top_col=light_col, outline_col=outline)

def draw_large_lego_minifigure(draw, x, y, scale=1.45, leg_angle=0.0, arm_l=0.0, arm_r=0.0, body_tilt=0.0, facing=1, action="idle", scan_t=0.0, t_sec=0.0):
    H_HEAD = 42 * scale
    W_HEAD = 38 * scale
    H_STUD = 9 * scale
    W_STUD = 20 * scale
    H_TORSO = 68 * scale
    W_SHOULDER = 52 * scale
    W_WAIST = 64 * scale
    H_HIPS = 18 * scale
    W_HIPS = 62 * scale
    H_LEGS = 68 * scale
    W_LEG = 29 * scale
    
    YELLOW_BASE = (255, 212, 0)
    YELLOW_LIGHT = (255, 245, 130)
    YELLOW_SHADOW = (210, 155, 0)
    CYAN_BASE = (0, 175, 220)
    CYAN_LIGHT = (60, 225, 255)
    CYAN_SHADOW = (0, 115, 150)
    NAVY_BASE = (24, 70, 125)
    NAVY_LIGHT = (45, 110, 185)
    NAVY_SHADOW = (12, 38, 72)
    BLACK_PLASTIC = (30, 32, 38)
    RED_BEANIE = (225, 32, 32)
    RED_BEANIE_LIGHT = (255, 95, 95)
    RED_BEANIE_SHADOW = (155, 18, 18)

    draw.ellipse([x - 48*scale, y - 12*scale, x + 48*scale, y + 12*scale], fill=(35, 45, 60, 100))

    hip_y = y - H_LEGS
    torso_bottom_y = hip_y - H_HIPS
    torso_top_y = torso_bottom_y - H_TORSO
    neck_y = torso_top_y - 4 * scale
    head_bottom_y = neck_y
    head_top_y = head_bottom_y - H_HEAD
    stud_top_y = head_top_y - H_STUD

    waddle_dx = math.sin(math.radians(body_tilt)) * 16 * scale

    def render_leg(lx, ly, angle, is_front=True):
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        w2 = W_LEG / 2.0
        local_pts = [(-w2, 0), (w2, 0), (w2, H_LEGS), (-w2, H_LEGS)]
        world_pts = [(px * cos_a - py * sin_a + lx, px * sin_a + py * cos_a + ly) for px, py in local_pts]
        col = NAVY_BASE if is_front else NAVY_SHADOW
        draw.polygon(world_pts, fill=col, outline=(15, 20, 28), width=3)
        hl_pts = [(-w2 + 3*scale, 4*scale), (-w2 + 8*scale, 4*scale), (-w2 + 8*scale, H_LEGS - 4*scale), (-w2 + 3*scale, H_LEGS - 4*scale)]
        world_hl = [(px * cos_a - py * sin_a + lx, px * sin_a + py * cos_a + ly) for px, py in hl_pts]
        draw.polygon(world_hl, fill=NAVY_LIGHT)

    back_leg_ang = -leg_angle if facing >= 0 else leg_angle
    front_leg_ang = leg_angle if facing >= 0 else -leg_angle

    if facing == 0:
        render_leg(x - W_LEG*0.55, hip_y, leg_angle, True)
        render_leg(x + W_LEG*0.55, hip_y, -leg_angle, True)
    else:
        render_leg(x - (W_LEG*0.25*facing), hip_y, back_leg_ang, False)
        render_leg(x + (W_LEG*0.25*facing), hip_y, front_leg_ang, True)

    draw.rounded_rectangle([x - W_HIPS//2, hip_y - H_HIPS, x + W_HIPS//2, hip_y], radius=int(5*scale), fill=BLACK_PLASTIC, outline=(15, 18, 22), width=3)
    draw.ellipse([x - 8*scale, hip_y - H_HIPS + 3*scale, x + 8*scale, hip_y - 3*scale], fill=(70, 75, 88))

    tx = x + waddle_dx
    torso_pts = [
        (tx - W_SHOULDER//2, torso_top_y),
        (tx + W_SHOULDER//2, torso_top_y),
        (tx + W_WAIST//2, torso_bottom_y),
        (tx - W_WAIST//2, torso_bottom_y)
    ]
    draw.polygon(torso_pts, fill=CYAN_BASE, outline=(10, 20, 30), width=3)
    draw.polygon([
        (tx - W_SHOULDER//2 + 3*scale, torso_top_y + 2*scale),
        (tx - W_SHOULDER//2 + 9*scale, torso_top_y + 2*scale),
        (tx - W_WAIST//2 + 9*scale, torso_bottom_y - 2*scale),
        (tx - W_WAIST//2 + 3*scale, torso_bottom_y - 2*scale)
    ], fill=CYAN_LIGHT)
    draw.polygon([
        (tx + W_SHOULDER//2 - 8*scale, torso_top_y + 2*scale),
        (tx + W_SHOULDER//2 - 2*scale, torso_top_y + 2*scale),
        (tx + W_WAIST//2 - 2*scale, torso_bottom_y - 2*scale),
        (tx + W_WAIST//2 - 8*scale, torso_bottom_y - 2*scale)
    ], fill=CYAN_SHADOW)

    mid_ty = (torso_top_y + torso_bottom_y) / 2.0
    draw.line([(tx - 15*scale, torso_top_y + 16*scale), (tx + 15*scale, torso_top_y + 16*scale)], fill=(240, 255, 255), width=3)
    core_r = 12 * scale
    draw.ellipse([tx - core_r, mid_ty - core_r, tx + core_r, mid_ty + core_r], fill=(225, 255, 255), outline=(0, 240, 255), width=3)
    draw.ellipse([tx - core_r*0.5, mid_ty - core_r*0.5, tx + core_r*0.5, mid_ty + core_r*0.5], fill=(0, 215, 255))
    draw.rectangle([tx - 9*scale, neck_y, tx + 9*scale, torso_top_y], fill=BLACK_PLASTIC)

    hx = tx
    draw.rounded_rectangle([hx - W_HEAD//2, head_top_y, hx + W_HEAD//2, head_bottom_y], radius=int(7*scale), fill=YELLOW_BASE, outline=(30, 25, 10), width=3)
    draw.rounded_rectangle([hx - W_HEAD//2 + 3*scale, head_top_y + 4*scale, hx - W_HEAD//2 + 9*scale, head_bottom_y - 4*scale], radius=int(3*scale), fill=YELLOW_LIGHT)
    draw.rounded_rectangle([hx + W_HEAD//2 - 7*scale, head_top_y + 4*scale, hx + W_HEAD//2 - 2*scale, head_bottom_y - 4*scale], radius=int(2*scale), fill=YELLOW_SHADOW)
    draw.rounded_rectangle([hx - W_STUD//2, stud_top_y, hx + W_STUD//2, head_top_y], radius=int(2*scale), fill=YELLOW_BASE, outline=(30, 25, 10), width=2)

    beanie_w = W_HEAD + 10 * scale
    beanie_h = 26 * scale
    beanie_y = head_top_y - 7 * scale
    draw.ellipse([hx - beanie_w//2, beanie_y - beanie_h//2, hx + beanie_w//2, beanie_y + beanie_h//2 + 6*scale], fill=RED_BEANIE, outline=(30, 10, 10), width=3)
    draw.rounded_rectangle([hx - beanie_w//2 - 2*scale, beanie_y + 2*scale, hx + beanie_w//2 + 2*scale, beanie_y + 13*scale], radius=int(3*scale), fill=RED_BEANIE_LIGHT, outline=(30, 10, 10), width=2)
    draw.ellipse([hx - 7*scale, beanie_y - beanie_h//2 - 4*scale, hx + 7*scale, beanie_y - beanie_h//2 + 4*scale], fill=RED_BEANIE_LIGHT)

    face_y = head_top_y + 18 * scale
    eye_offset = 8 * scale
    eye_look_x = 2 * scale * facing
    draw.line([(hx - eye_offset - 5*scale, face_y - 8*scale), (hx - eye_offset + 3*scale, face_y - 7*scale)], fill=(30, 20, 10), width=3)
    draw.line([(hx + eye_offset - 3*scale, face_y - 7*scale), (hx + eye_offset + 5*scale, face_y - 9*scale)], fill=(30, 20, 10), width=3)
    for side in [-1, 1]:
        ex = hx + (eye_offset * side) + eye_look_x
        draw.ellipse([ex - 4*scale, face_y - 5*scale, ex + 4*scale, face_y + 5*scale], fill=(15, 15, 20))
        draw.ellipse([ex - 2*scale, face_y - 4*scale, ex + 1.5*scale, face_y - 0.5*scale], fill=(255, 255, 255))
    draw.arc([hx - 8*scale + eye_look_x, face_y + 4*scale, hx + 8*scale + eye_look_x, face_y + 15*scale], start=10, end=170, fill=(25, 15, 10), width=3)

    def render_arm(is_right=True, arm_ang=0.0):
        side = 1 if is_right else -1
        sx = tx + (W_SHOULDER * 0.46 * side)
        sy = torso_top_y + 9 * scale
        rad = math.radians(arm_ang)
        arm_len = 42 * scale
        wx = sx + math.sin(rad) * arm_len + (9 * scale * side if facing == 0 else 0)
        wy = sy + math.cos(rad) * arm_len
        col = CYAN_BASE if (side * facing >= 0 or facing == 0) else CYAN_SHADOW
        draw.line([(sx, sy), (wx, wy)], fill=col, width=int(16 * scale))
        draw.ellipse([sx - 8*scale, sy - 8*scale, sx + 8*scale, sy + 8*scale], fill=col)
        draw.ellipse([wx - 7*scale, wy - 7*scale, wx + 7*scale, wy + 7*scale], fill=YELLOW_SHADOW)
        hr = 10 * scale
        hx_c = wx + math.sin(rad) * (hr + 2*scale)
        hy_c = wy + math.cos(rad) * (hr + 2*scale)
        open_deg = math.degrees(rad) - 90
        draw.arc([hx_c - hr, hy_c - hr, hx_c + hr, hy_c + hr], start=open_deg + 45, end=open_deg + 315, fill=YELLOW_BASE, width=int(6*scale))
        return hx_c, hy_c

    lhx, lhy = render_arm(False, arm_l)
    rhx, rhy = render_arm(True, arm_r)

    if action == "scan":
        draw.rectangle([rhx, rhy - 4*scale, rhx + 18*scale, rhy + 10*scale], fill=(0, 230, 255), outline=(255, 255, 255), width=2)
        for b in range(30, 300, 22):
            by = rhy + math.sin(scan_t * 6.0 + b * 0.08) * 55
            draw.line([(rhx + 18*scale, rhy + 2*scale), (rhx + 18*scale + b, by)], fill=(0, 240, 255), width=3)

    elif action == "victory":
        bx = tx
        by = head_top_y - 50 * scale
        draw.rectangle([bx - 14*scale, by - 12*scale, bx + 14*scale, by + 12*scale], fill=(0, 245, 255), outline=(255, 255, 255), width=3)
        draw.rectangle([bx - 5*scale, by - 19*scale, bx + 5*scale, by - 12*scale], fill=(180, 255, 255), outline=(255, 255, 255), width=2)
        for r_deg in range(0, 360, 45):
            rr = math.radians(r_deg + t_sec * 60.0)
            draw.line([(bx, by), (bx + math.cos(rr)*38*scale, by + math.sin(rr)*38*scale)], fill=(225, 255, 255), width=3)

# -----------------------------------------------------------------------------
# Master Frame Rendering Function
# -----------------------------------------------------------------------------
def render_frame(t):
    im = Image.new('RGB', (WIDTH, HEIGHT), (242, 246, 252))
    draw = ImageDraw.Draw(im)

    # Floor (y=480 to 720)
    floor_y = 480
    draw.rectangle([0, floor_y, WIDTH, HEIGHT], fill=(215, 222, 232))
    for row in range(floor_y + 15, HEIGHT, 30):
        depth_fac = (row - floor_y) / (HEIGHT - floor_y)
        stud_r = 8 + int(depth_fac * 8)
        spacing = 48 + int(depth_fac * 30)
        stud_h = 5 + int(depth_fac * 4)
        for col in range(25, WIDTH, spacing):
            draw_lego_stud(draw, col, row, r=stud_r, h=stud_h)

    # 1. Server Rack (Right side, x=920)
    rack_x, rack_y = 920, 180
    server_fixed = t > 15.0
    brick_colors = [
        ((40, 45, 52), (65, 72, 82), (25, 28, 34)),
        ((35, 40, 48), (60, 68, 78), (22, 25, 30)),
    ]
    for b_idx in range(7):
        by = rack_y + b_idx * 42
        b_col, l_col, s_col = brick_colors[b_idx % 2]
        draw_lego_brick(draw, rack_x, by, 200, 38, b_col, l_col, s_col, studs=6)
        for g in range(rack_x + 15, rack_x + 145, 12):
            draw.line([(g, by + 10), (g, by + 28)], fill=(15, 18, 22), width=3)
        
        if not server_fixed:
            flash_on = (int(t * 5.0) % 2 == 0)
            led_col = (255, 40, 40) if flash_on else (140, 20, 20)
            draw.ellipse([rack_x + 160, by + 12, rack_x + 185, by + 26], fill=led_col, outline=(255, 180, 180), width=2)
        else:
            draw.ellipse([rack_x + 160, by + 12, rack_x + 185, by + 26], fill=(0, 230, 255), outline=(180, 255, 255), width=2)

    # Server Status Header (Ultra Clear Digital Badge)
    if not server_fixed:
        draw.rounded_rectangle([rack_x, rack_y - 48, rack_x + 200, rack_y - 12], radius=8, fill=(35, 15, 20), outline=(255, 60, 60), width=2)
        draw.text((rack_x + 16, rack_y - 40), "BLADE 01: CRITICAL FAULT", font=font_server_status, fill=(255, 80, 80))
        
        # Smoke puffs
        smoke_offset = (t * 25.0) % 30
        smoke_pts = [
            (rack_x + 70, rack_y - 65 - smoke_offset, 22),
            (rack_x + 100, rack_y - 90 - smoke_offset * 1.2, 30),
            (rack_x + 130, rack_y - 75 - smoke_offset * 0.9, 26)
        ]
        for sx, sy, sr in smoke_pts:
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(230, 235, 240), outline=(190, 195, 205), width=2)
    else:
        draw.rounded_rectangle([rack_x, rack_y - 48, rack_x + 200, rack_y - 12], radius=8, fill=(10, 30, 40), outline=(0, 220, 255), width=2)
        draw.text((rack_x + 20, rack_y - 40), "BLADE 01: ONLINE [HOTFIX]", font=font_server_status, fill=(0, 240, 255))
        if t < 18.0:
            for sp_i in range(8):
                sp_x = rack_x + 30 + (sp_i * 20)
                sp_y = rack_y - 65 - math.sin(t * 8.0 + sp_i) * 20
                draw.ellipse([sp_x - 4, sp_y - 4, sp_x + 4, sp_y + 4], fill=(0, 255, 220))

    # Hotfix Brick Animation
    if 13.5 <= t <= 15.2:
        hf_progress = min(1.0, (t - 13.5) / 1.5)
        hf_x = 740 + hf_progress * (rack_x - 740 + 20)
        hf_y = 360 - math.sin(hf_progress * math.pi) * 85
        draw_lego_brick(draw, int(hf_x), int(hf_y), 70, 30, (0, 210, 255), (100, 240, 255), (0, 140, 180), studs=2)

    # 2. Cyber Terminal Desk (x=140)
    term_x, term_y = 140, 380
    draw_lego_brick(draw, term_x, term_y, 200, 100, (160, 168, 178), (200, 208, 218), (120, 128, 138), studs=6)
    slope_poly = [(term_x + 50, term_y - 5), (term_x + 150, term_y - 5), (term_x + 165, term_y - 35), (term_x + 35, term_y - 35)]
    draw.polygon(slope_poly, fill=(45, 50, 60), outline=(15, 20, 25), width=2)
    for kx in range(term_x + 55, term_x + 145, 16):
        draw.line([(kx, term_y - 10), (kx, term_y - 30)], fill=(0, 240, 255), width=3)

    # EXPANDED HOLOGRAPHIC HUD (360px wide, high contrast)
    hud_x, hud_y = term_x - 30, term_y - 230
    draw.rounded_rectangle([hud_x, hud_y, hud_x + 360, hud_y + 175], radius=14, fill=(10, 18, 32), outline=(0, 220, 255), width=3)
    draw.text((hud_x + 16, hud_y + 14), "CYBER TERMINAL v4.2", font=font_hud_title, fill=(0, 240, 255))
    draw.text((hud_x + 245, hud_y + 16), "[TEST SUITE]", font=font_hud_code_bold, fill=(0, 180, 220))
    draw.line([(hud_x + 14, hud_y + 38), (hud_x + 346, hud_y + 38)], fill=(0, 140, 180), width=2)

    tests_passed = t > 28.5
    draw.text((hud_x + 16, hud_y + 48), "const hotfix = await Hotfix.apply();", font=font_hud_code, fill=(220, 240, 255))
    draw.text((hud_x + 16, hud_y + 72), "RUNNING: 42 integration tests...", font=font_hud_code, fill=(0, 220, 255))
    
    db_pass = t > 24.0
    agent_pass = t > 26.5
    draw.text((hud_x + 16, hud_y + 96), "> db_connection_pool: " + ("OK [PASS]" if db_pass else "RUNNING..."), font=font_hud_code_bold, fill=((0, 255, 120) if db_pass else (200, 220, 240)))
    draw.text((hud_x + 16, hud_y + 120), "> autonomous_worker: " + ("OK [PASS]" if agent_pass else "WAITING..."), font=font_hud_code_bold, fill=((0, 255, 120) if agent_pass else (160, 180, 200)))

    draw.rounded_rectangle([hud_x + 16, hud_y + 145, hud_x + 344, hud_y + 167], radius=6, fill=(20, 35, 55))
    if tests_passed:
        draw.rounded_rectangle([hud_x + 16, hud_y + 145, hud_x + 344, hud_y + 167], radius=6, fill=(0, 255, 140))
        draw.text((hud_x + 75, hud_y + 148), "ALL 42 TESTS PASS [100%]", font=font_hud_code_bold, fill=(10, 25, 40))
    else:
        prog = min(1.0, max(0.1, (t - 21.67) / (28.5 - 21.67))) if t >= 21.67 else 0.1
        pw = int(prog * 328)
        draw.rounded_rectangle([hud_x + 16, hud_y + 145, hud_x + 16 + pw, hud_y + 167], radius=6, fill=(0, 220, 255))
        draw.text((hud_x + 85, hud_y + 148), f"RUNNING SUITE: {int(prog*100)}%", font=font_hud_code_bold, fill=(255, 255, 255))

    # 3. Technic Lever Station (x=620)
    lever_x, lever_y = 620, 330
    draw_lego_brick(draw, lever_x, lever_y, 55, 150, (55, 60, 70), (85, 90, 102), (35, 40, 48), studs=1)
    for py in range(lever_y + 25, lever_y + 135, 30):
        draw.ellipse([lever_x + 18, py, lever_x + 38, py + 18], fill=(25, 30, 38), outline=(90, 95, 108), width=2)

    draw.rounded_rectangle([lever_x - 35, lever_y - 48, lever_x + 95, lever_y - 12], radius=8, fill=(12, 22, 36), outline=(0, 240, 255), width=2)
    lever_pulled = t >= 35.0
    gauge_txt = "DEPLOY: 100% [LOCKED]" if lever_pulled else "DEPLOY: STANDBY"
    gauge_col = (0, 255, 140) if lever_pulled else (0, 220, 255)
    draw.text((lever_x - 26, lever_y - 40), gauge_txt, font=font_lever_gauge, fill=gauge_col)

    if t < 34.0:
        lever_ang_deg = 30.0
    elif t < 35.0:
        lever_ang_deg = 30.0 - ((t - 34.0) / 1.0) * 65.0
    else:
        lever_ang_deg = -35.0
        
    pivot_x, pivot_y = lever_x + 28, lever_y + 40
    lever_rad = math.radians(lever_ang_deg)
    arm_len = 60
    ball_x = pivot_x + math.sin(lever_rad) * arm_len
    ball_y = pivot_y - math.cos(lever_rad) * arm_len
    draw.line([(pivot_x, pivot_y), (ball_x, ball_y)], fill=(225, 35, 35), width=8)
    draw.ellipse([pivot_x - 9, pivot_y - 9, pivot_x + 9, pivot_y + 9], fill=(20, 25, 30))
    draw.ellipse([ball_x - 12, ball_y - 12, ball_x + 12, ball_y + 12], fill=(255, 212, 0), outline=(210, 155, 0), width=3)

    if t >= 35.0:
        for _ in range(5):
            import random
            random.seed(int(t * 100) + _)
            sx = lever_x + random.randint(5, 55)
            sy = lever_y + random.randint(15, 100)
            draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 200))

    # Rocket Launch
    if 36.5 <= t <= 42.0:
        rocket_y = 480 - ((t - 36.5) / 5.5) * 550
        rocket_x = 730
        draw.polygon([(rocket_x, rocket_y - 35), (rocket_x + 16, rocket_y), (rocket_x - 16, rocket_y)], fill=(245, 245, 250), outline=(30, 35, 45), width=3)
        draw.ellipse([rocket_x - 10, rocket_y, rocket_x + 10, rocket_y + 28], fill=(255, 120, 0))
        draw.ellipse([rocket_x - 5, rocket_y + 8, rocket_x + 5, rocket_y + 36], fill=(255, 220, 0))

    # -------------------------------------------------------------------------
    # Character Animation (scale = 1.45)
    # -------------------------------------------------------------------------
    char_y = 590
    scale = 1.45

    if t < 0.3:
        char_x = 100
        facing = 1
        action = "walk"
        leg_ang, arm_l, arm_r, body_tilt = 0.0, 0.0, 0.0, 0.0

    elif t < 9.95:
        progress = (t - 0.3) / (9.95 - 0.3)
        char_x = 100 + progress * (760 - 100)
        facing = 1
        action = "walk"
        cycle = t * 3.5 * math.pi
        leg_ang = math.sin(cycle) * 26.0
        arm_l = -math.sin(cycle) * 32.0
        arm_r = math.sin(cycle) * 32.0
        body_tilt = math.sin(cycle) * 3.5

    elif t < 21.17:
        char_x = 760
        facing = 1
        action = "scan"
        leg_ang = 0.0
        body_tilt = 0.0
        arm_l = 15.0
        arm_r = -45.0 + math.sin(t * 3.0) * 12.0

    elif t < 26.0:
        progress = (t - 21.17) / (26.0 - 21.17)
        char_x = 760 - progress * (760 - 330)
        facing = -1
        action = "walk"
        cycle = t * 3.5 * math.pi
        leg_ang = math.sin(cycle) * 26.0
        arm_l = -math.sin(cycle) * 32.0
        arm_r = math.sin(cycle) * 32.0
        body_tilt = -math.sin(cycle) * 3.5

    elif t < 31.37:
        char_x = 330
        facing = -1
        action = "type"
        leg_ang = 0.0
        body_tilt = 0.0
        type_cycle = t * 14.0
        arm_l = -55.0 + math.sin(type_cycle) * 18.0
        arm_r = -55.0 - math.sin(type_cycle) * 18.0

    elif t < 34.0:
        progress = (t - 31.37) / (34.0 - 31.37)
        char_x = 330 + progress * (570 - 330)
        facing = 1
        action = "walk"
        cycle = t * 3.5 * math.pi
        leg_ang = math.sin(cycle) * 26.0
        arm_l = -math.sin(cycle) * 32.0
        arm_r = math.sin(cycle) * 32.0
        body_tilt = math.sin(cycle) * 3.5

    elif t < 41.69:
        char_x = 570
        facing = 1
        action = "pull_lever"
        leg_ang = 10.0
        body_tilt = 4.0
        arm_l = 20.0
        arm_r = -40.0 if t < 35.0 else -15.0

    elif t < 45.0:
        progress = (t - 41.69) / (45.0 - 41.69)
        char_x = 570 + progress * (640 - 570)
        facing = 1
        action = "walk"
        cycle = t * 3.0 * math.pi
        leg_ang = math.sin(cycle) * 22.0
        arm_l = -math.sin(cycle) * 28.0
        arm_r = math.sin(cycle) * 28.0
        body_tilt = math.sin(cycle) * 3.0

    else:
        char_x = 640
        facing = 0
        action = "victory"
        leg_ang = 0.0
        body_tilt = 0.0
        arm_l = -140.0
        arm_r = -140.0

    draw_large_lego_minifigure(
        draw, 
        x=char_x, y=char_y, 
        scale=scale, 
        leg_angle=leg_ang, 
        arm_l=arm_l, 
        arm_r=arm_r, 
        body_tilt=body_tilt, 
        facing=facing, 
        action=action, 
        scan_t=t, 
        t_sec=t
    )

    # Confetti studs in Act 5
    if t > 44.0:
        confetti_cols = [(255, 212, 0), (0, 215, 255), (255, 45, 45), (40, 255, 120), (255, 140, 0)]
        import random
        random.seed(42)
        for c_idx in range(55):
            cx = random.randint(40, WIDTH - 40)
            cy_init = random.randint(-150, 420)
            cy = (cy_init + int((t - 44.0) * 115)) % 670
            col = confetti_cols[c_idx % len(confetti_cols)]
            draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=col)

    # -------------------------------------------------------------------------
    # Subtitle Card with Word Wrapping
    # -------------------------------------------------------------------------
    current_text = ""
    for sc in timeline_data["scenes"]:
        if sc["start"] <= t <= sc["end"] + 0.3:
            current_text = sc["text"]
            break

    if current_text:
        wrapped_lines = textwrap.wrap(current_text, width=72)
        card_h = 36 + len(wrapped_lines) * 30
        card_w = 1180
        card_x = (WIDTH - card_w) // 2
        card_y = HEIGHT - card_h - 18

        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(10, 16, 26), outline=(0, 220, 255), width=3)
        draw.text((card_x + 28, card_y + 14), "LEGO AGENT:", font=font_sub_speaker, fill=(255, 212, 0))
        for li, line in enumerate(wrapped_lines):
            lx = card_x + 200 if li == 0 else card_x + 28
            draw.text((lx, card_y + 14 + li * 30), line, font=font_sub_body, fill=(245, 250, 255))

    # -------------------------------------------------------------------------
    # Channel Logo Branding Integrations
    # -------------------------------------------------------------------------
    # 1. Top-Left Brand Pill with Embedded Channel Avatar
    draw.rounded_rectangle([35, 20, 420, 85], radius=16, fill=(12, 18, 30), outline=(0, 220, 255), width=3)
    im.paste(logo_header, (48, 25), mask=logo_header)
    draw.text((116, 38), "LEGO AI AGENT", font=font_brand, fill=(255, 255, 255))

    # 2. Top-Right Watermark Card
    wm_x, wm_y = 1180, 22
    draw.rounded_rectangle([wm_x - 10, wm_y - 2, wm_x + 66, wm_y + 60], radius=16, fill=(10, 16, 26), outline=(0, 220, 255), width=2)
    im.paste(logo_watermark, (wm_x, wm_y), mask=logo_watermark)

    # 3. Victory End Card with Large Channel Avatar (t > 46.0s)
    if t > 46.0:
        v_w = 920
        v_h = 115
        v_x = (WIDTH - v_w) // 2
        v_y = 95
        draw.rounded_rectangle([v_x, v_y, v_x + v_w, v_y + v_h], radius=20, fill=(10, 18, 32), outline=(0, 240, 255), width=3)
        # Paste Large Victory Logo on left side of banner
        im.paste(logo_victory, (v_x + 22, v_y + 15), mask=logo_victory)
        draw.text((v_x + 125, v_y + 22), "AUTONOMOUS LEGO AGENT: SHIPPED!", font=font_banner_main, fill=(0, 240, 255))
        draw.text((v_x + 128, v_y + 68), "Zero Human Handoffs • 100% Automated Infrastructure", font=font_banner_sub, fill=(230, 242, 255))

    return im

# -----------------------------------------------------------------------------
# Encoding Execution
# -----------------------------------------------------------------------------
def render_full_movie():
    print(f"[+] Starting FFmpeg pipe encoding for {TOTAL_FRAMES} frames...")
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", MASTER_AUDIO,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / float(FPS)
        im = render_frame(t)
        raw_bytes = im.tobytes()
        proc.stdin.write(raw_bytes)
        
        if frame_idx % 150 == 0 or frame_idx == TOTAL_FRAMES - 1:
            pct = (frame_idx / float(TOTAL_FRAMES)) * 100.0
            print(f"    Frame {frame_idx}/{TOTAL_FRAMES} ({pct:.1f}%) | Time: {t:.2f}s")
            
    proc.stdin.close()
    proc.wait()
    print(f"[+] Branded LEGO Movie rendered successfully: {OUTPUT_VIDEO}")
    
    if os.path.exists(OUTPUT_VIDEO):
        size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f"[+] Output size: {size_mb:.2f} MB")

if __name__ == '__main__':
    render_full_movie()
