import math, textwrap
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size):
    import os
    try:
        path = os.path.join("C:/Windows/Fonts", name)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_title = get_font("arialbd.ttf", 24)
font_sub_bold = get_font("arialbd.ttf", 24)
font_sub_reg = get_font("arial.ttf", 24)
font_hud_title = get_font("arialbd.ttf", 18)
font_hud_code = get_font("consola.ttf", 17)
font_hud_code_bold = get_font("consolab.ttf", 17)
font_led = get_font("consola.ttf", 14)
font_gauge = get_font("arialbd.ttf", 20)
font_banner = get_font("arialbd.ttf", 36)

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
    """
    Renders an enhanced, ultra-clear 3D-shaded LEGO Minifigure at large scale (~260px tall).
    """
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

    # Floor shadow
    draw.ellipse([x - 48*scale, y - 12*scale, x + 48*scale, y + 12*scale], fill=(35, 45, 60, 100))

    hip_y = y - H_LEGS
    torso_bottom_y = hip_y - H_HIPS
    torso_top_y = torso_bottom_y - H_TORSO
    neck_y = torso_top_y - 4 * scale
    head_bottom_y = neck_y
    head_top_y = head_bottom_y - H_HEAD
    stud_top_y = head_top_y - H_STUD

    waddle_dx = math.sin(math.radians(body_tilt)) * 16 * scale

    # Legs
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

    # Hip block
    draw.rounded_rectangle([x - W_HIPS//2, hip_y - H_HIPS, x + W_HIPS//2, hip_y], radius=int(5*scale), fill=BLACK_PLASTIC, outline=(15, 18, 22), width=3)
    draw.ellipse([x - 8*scale, hip_y - H_HIPS + 3*scale, x + 8*scale, hip_y - 3*scale], fill=(70, 75, 88))

    # Torso
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

    # Decal: glowing AI core
    mid_ty = (torso_top_y + torso_bottom_y) / 2.0
    draw.line([(tx - 15*scale, torso_top_y + 16*scale), (tx + 15*scale, torso_top_y + 16*scale)], fill=(240, 255, 255), width=3)
    core_r = 12 * scale
    draw.ellipse([tx - core_r, mid_ty - core_r, tx + core_r, mid_ty + core_r], fill=(225, 255, 255), outline=(0, 240, 255), width=3)
    draw.ellipse([tx - core_r*0.5, mid_ty - core_r*0.5, tx + core_r*0.5, mid_ty + core_r*0.5], fill=(0, 215, 255))
    draw.rectangle([tx - 9*scale, neck_y, tx + 9*scale, torso_top_y], fill=BLACK_PLASTIC)

    # Head
    hx = tx
    draw.rounded_rectangle([hx - W_HEAD//2, head_top_y, hx + W_HEAD//2, head_bottom_y], radius=int(7*scale), fill=YELLOW_BASE, outline=(30, 25, 10), width=3)
    draw.rounded_rectangle([hx - W_HEAD//2 + 3*scale, head_top_y + 4*scale, hx - W_HEAD//2 + 9*scale, head_bottom_y - 4*scale], radius=int(3*scale), fill=YELLOW_LIGHT)
    draw.rounded_rectangle([hx + W_HEAD//2 - 7*scale, head_top_y + 4*scale, hx + W_HEAD//2 - 2*scale, head_bottom_y - 4*scale], radius=int(2*scale), fill=YELLOW_SHADOW)
    draw.rounded_rectangle([hx - W_STUD//2, stud_top_y, hx + W_STUD//2, head_top_y], radius=int(2*scale), fill=YELLOW_BASE, outline=(30, 25, 10), width=2)

    # Beanie
    beanie_w = W_HEAD + 10 * scale
    beanie_h = 26 * scale
    beanie_y = head_top_y - 7 * scale
    draw.ellipse([hx - beanie_w//2, beanie_y - beanie_h//2, hx + beanie_w//2, beanie_y + beanie_h//2 + 6*scale], fill=RED_BEANIE, outline=(30, 10, 10), width=3)
    draw.rounded_rectangle([hx - beanie_w//2 - 2*scale, beanie_y + 2*scale, hx + beanie_w//2 + 2*scale, beanie_y + 13*scale], radius=int(3*scale), fill=RED_BEANIE_LIGHT, outline=(30, 10, 10), width=2)
    draw.ellipse([hx - 7*scale, beanie_y - beanie_h//2 - 4*scale, hx + 7*scale, beanie_y - beanie_h//2 + 4*scale], fill=RED_BEANIE_LIGHT)

    # Face Decal
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

    # Arms and Yellow C-Clamp Hands
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


def test_clear_frame():
    w, h = 1280, 720
    im = Image.new('RGB', (w, h), (242, 246, 252))
    draw = ImageDraw.Draw(im)

    floor_y = 480
    draw.rectangle([0, floor_y, w, h], fill=(215, 222, 232))
    for row in range(floor_y + 15, h, 30):
        depth_fac = (row - floor_y) / (h - floor_y)
        stud_r = 8 + int(depth_fac * 8)
        spacing = 48 + int(depth_fac * 30)
        stud_h = 5 + int(depth_fac * 4)
        for col in range(25, w, spacing):
            draw_lego_stud(draw, col, row, r=stud_r, h=stud_h)

    # 1. Server Rack (Right side, x=920)
    rack_x, rack_y = 920, 180
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
        draw.ellipse([rack_x + 160, by + 12, rack_x + 185, by + 26], fill=(255, 40, 40), outline=(255, 180, 180), width=2)

    # Server Status Header Banner above rack
    draw.rounded_rectangle([rack_x, rack_y - 45, rack_x + 200, rack_y - 10], radius=8, fill=(35, 15, 20), outline=(255, 60, 60), width=2)
    draw.text((rack_x + 18, rack_y - 38), "BLADE 01: FAULT", font=font_led, fill=(255, 80, 80))

    # 2. Cyber Terminal (Left side, x=140)
    term_x, term_y = 140, 380
    draw_lego_brick(draw, term_x, term_y, 200, 100, (160, 168, 178), (200, 208, 218), (120, 128, 138), studs=6)
    slope_poly = [(term_x + 50, term_y - 5), (term_x + 150, term_y - 5), (term_x + 165, term_y - 35), (term_x + 35, term_y - 35)]
    draw.polygon(slope_poly, fill=(45, 50, 60), outline=(15, 20, 25), width=2)
    for kx in range(term_x + 55, term_x + 145, 16):
        draw.line([(kx, term_y - 10), (kx, term_y - 30)], fill=(0, 240, 255), width=3)

    # EXPANDED & ULTRA-CLEAR HOLOGRAPHIC HUD (Width 360px, Height 170px)
    hud_x, hud_y = term_x - 30, term_y - 230
    draw.rounded_rectangle([hud_x, hud_y, hud_x + 360, hud_y + 175], radius=14, fill=(10, 18, 32), outline=(0, 220, 255), width=3)
    # HUD Header
    draw.text((hud_x + 16, hud_y + 14), "CYBER TERMINAL v4.2", font=font_hud_title, fill=(0, 240, 255))
    draw.text((hud_x + 250, hud_y + 16), "[TEST SUITE]", font=font_led, fill=(0, 180, 220))
    draw.line([(hud_x + 14, hud_y + 38), (hud_x + 346, hud_y + 38)], fill=(0, 140, 180), width=2)
    
    # Ultra-clear Code Lines in 17px Consola Bold
    draw.text((hud_x + 16, hud_y + 48), "const hotfix = await Hotfix.apply();", font=font_hud_code, fill=(220, 240, 255))
    draw.text((hud_x + 16, hud_y + 72), "RUNNING: 42 integration tests...", font=font_hud_code, fill=(0, 220, 255))
    draw.text((hud_x + 16, hud_y + 96), "> db_connection_pool: OK [PASS]", font=font_hud_code_bold, fill=(0, 255, 120))
    draw.text((hud_x + 16, hud_y + 120), "> autonomous_worker: OK [PASS]", font=font_hud_code_bold, fill=(0, 255, 120))
    
    # Large Progress Bar & Status
    draw.rounded_rectangle([hud_x + 16, hud_y + 145, hud_x + 344, hud_y + 165], radius=6, fill=(20, 35, 55))
    draw.rounded_rectangle([hud_x + 16, hud_y + 145, hud_x + 344, hud_y + 165], radius=6, fill=(0, 255, 140))
    draw.text((hud_x + 85, hud_y + 147), "ALL 42 TESTS PASS [100%]", font=font_hud_code_bold, fill=(10, 25, 40))

    # 3. Technic Lever Station (Center-Right, x=640)
    lever_x, lever_y = 620, 330
    draw_lego_brick(draw, lever_x, lever_y, 55, 150, (55, 60, 70), (85, 90, 102), (35, 40, 48), studs=1)
    for py in range(lever_y + 25, lever_y + 135, 30):
        draw.ellipse([lever_x + 18, py, lever_x + 38, py + 18], fill=(25, 30, 38), outline=(90, 95, 108), width=2)

    # Power Gauge Above Lever
    draw.rounded_rectangle([lever_x - 15, lever_y - 45, lever_x + 70, lever_y - 10], radius=8, fill=(15, 25, 40), outline=(0, 240, 255), width=2)
    draw.text((lever_x - 5, lever_y - 38), "DEPLOY: 100%", font=font_gauge, fill=(0, 240, 255))

    # Lever Arm
    pivot_x, pivot_y = lever_x + 28, lever_y + 40
    ball_x, ball_y = pivot_x + 28, pivot_y - 38
    draw.line([(pivot_x, pivot_y), (ball_x, ball_y)], fill=(225, 35, 35), width=8)
    draw.ellipse([pivot_x - 9, pivot_y - 9, pivot_x + 9, pivot_y + 9], fill=(20, 25, 30))
    draw.ellipse([ball_x - 12, ball_y - 12, ball_x + 12, ball_y + 12], fill=(255, 212, 0), outline=(210, 155, 0), width=3)

    # 4. Large Enhanced Minifigure
    draw_large_lego_minifigure(
        draw, 
        x=520, y=590, 
        scale=1.45, 
        leg_angle=24.0, 
        arm_l=-30.0, 
        arm_r=32.0, 
        body_tilt=3.0, 
        facing=1, 
        action="walk"
    )

    # 5. Top Brand Banner (High-Contrast Dark Pill)
    draw.rounded_rectangle([40, 25, 380, 80], radius=14, fill=(12, 18, 30), outline=(0, 220, 255), width=3)
    draw.ellipse([58, 38, 92, 68], fill=(255, 212, 0), outline=(210, 155, 0), width=2)
    draw.text((106, 38), "LEGO AI AGENT", font=font_banner, fill=(255, 255, 255))

    # 6. High-Contrast Subtitle Card with Word Wrapping at Bottom!
    sub_text = "Scanning hardware. Memory leak detected in brick cluster. Snapping in a hotfix brick. Daemon rebooted, status solid cyan!"
    wrapped_lines = textwrap.wrap(sub_text, width=72)
    
    card_h = 42 + len(wrapped_lines) * 30
    card_w = 1180
    card_x = (w - card_w) // 2
    card_y = h - card_h - 20

    # Dark acrylic glass card with cyan glow border
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(10, 16, 26), outline=(0, 220, 255), width=3)
    # Speaker tag
    draw.text((card_x + 28, card_y + 14), "LEGO AGENT:", font=font_sub_bold, fill=(255, 212, 0))
    # Subtitle text lines
    for li, line in enumerate(wrapped_lines):
        lx = card_x + 200 if li == 0 else card_x + 28
        draw.text((lx, card_y + 14 + li * 30), line, font=font_sub_reg, fill=(245, 250, 255))

    out_path = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\snapshots\test_clear_preview.png"
    im.save(out_path)
    print("Clear preview saved to:", out_path)

if __name__ == '__main__':
    test_clear_frame()
