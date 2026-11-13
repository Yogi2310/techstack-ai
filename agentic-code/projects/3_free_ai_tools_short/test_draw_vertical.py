import os, sys, math, textwrap
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size):
    try:
        path = os.path.join("C:/Windows/Fonts", name)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_brand = get_font("arialbd.ttf", 36)
font_brand_sub = get_font("arial.ttf", 22)
font_category = get_font("arialbd.ttf", 32)
font_tool_badge = get_font("arialbd.ttf", 52)
font_hud_title = get_font("arialbd.ttf", 24)
font_hud_code = get_font("consola.ttf", 22)
font_hud_code_bold = get_font("consolab.ttf", 24)
font_sub_bold = get_font("arialbd.ttf", 44)

def make_circular_logo(img, size, border_color=(0, 220, 255), border_width=4):
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([0, 0, size - 1, size - 1], fill=255)
    
    circ = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circ.paste(img, (0, 0), mask=mask)
    
    draw_circ = ImageDraw.Draw(circ)
    draw_circ.ellipse([border_width//2, border_width//2, size - 1 - border_width//2, size - 1 - border_width//2], outline=border_color, width=border_width)
    return circ

def draw_lego_stud(draw, cx, cy, r=12, h=7, base_col=(175, 180, 190), top_col=(235, 240, 250), outline_col=(185, 190, 200)):
    draw.ellipse([cx - r, cy - h, cx + r, cy + h], fill=base_col)
    draw.ellipse([cx - r + 1, cy - h - 3, cx + r - 1, cy + h - 3], fill=top_col, outline=outline_col, width=2)
    ir = r * 0.52
    draw.ellipse([cx - ir, cy - h*0.5 - 3, cx + ir, cy + h*0.5 - 3], outline=outline_col, width=1)

def draw_lego_brick(draw, x0, y0, w, h, base_col, light_col, shadow_col, studs=4, outline=(20, 25, 30)):
    top_h = 14
    top_poly = [(x0, y0), (x0 + 14, y0 - top_h), (x0 + w + 14, y0 - top_h), (x0 + w, y0)]
    draw.polygon(top_poly, fill=light_col, outline=outline, width=3)
    front_poly = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    draw.polygon(front_poly, fill=base_col, outline=outline, width=3)
    right_poly = [(x0 + w, y0), (x0 + w + 14, y0 - top_h), (x0 + w + 14, y0 + h - top_h), (x0 + w, y0 + h)]
    draw.polygon(right_poly, fill=shadow_col, outline=outline, width=3)
    if studs > 0:
        step = w / studs
        for i in range(studs):
            scx = x0 + (i + 0.5) * step + 7
            scy = y0 - top_h * 0.5
            draw_lego_stud(draw, scx, scy, r=max(6, int(step*0.24)), h=5, base_col=shadow_col, top_col=light_col, outline_col=outline)

def draw_large_lego_minifigure(draw, x, y, scale=1.8, leg_angle=0.0, arm_l=0.0, arm_r=0.0, body_tilt=0.0, facing=1, action="idle", scan_t=0.0, t_sec=0.0):
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

    draw.ellipse([x - 52*scale, y - 14*scale, x + 52*scale, y + 14*scale], fill=(35, 45, 60, 110))

    hip_y = y - H_LEGS
    torso_bottom_y = hip_y - H_HIPS
    torso_top_y = torso_bottom_y - H_TORSO
    neck_y = torso_top_y - 5 * scale
    head_bottom_y = neck_y
    head_top_y = head_bottom_y - H_HEAD
    stud_top_y = head_top_y - H_STUD

    waddle_dx = math.sin(math.radians(body_tilt)) * 18 * scale

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
        draw.rectangle([rhx, rhy - 4*scale, rhx + 22*scale, rhy + 12*scale], fill=(0, 230, 255), outline=(255, 255, 255), width=2)
        for b in range(30, 360, 25):
            by = rhy + math.sin(scan_t * 6.0 + b * 0.08) * 65
            draw.line([(rhx + 22*scale, rhy + 2*scale), (rhx + 22*scale + b, by)], fill=(0, 240, 255), width=3)


def test_vertical_render():
    w, h = 1080, 1920
    im = Image.new('RGB', (w, h), (12, 18, 30))
    draw = ImageDraw.Draw(im)

    # 1. Top Progress Bar
    draw.rectangle([40, 45, 1040, 55], fill=(25, 35, 55))
    draw.rounded_rectangle([40, 45, 380, 55], radius=4, fill=(0, 240, 255))

    # 2. Top Header Bar (Avatar + Channel Name + Badge)
    logo_path = r"D:\Antigravity\Pro\channel_profile_pic.png"
    logo_raw = Image.open(logo_path).convert("RGBA")
    logo_header = make_circular_logo(logo_raw, 84, border_color=(0, 240, 255), border_width=3)
    im.paste(logo_header, (50, 75), mask=logo_header)

    draw.text((150, 85), "TECHSTACK AI", font=font_brand, fill=(255, 255, 255))
    draw.text((150, 128), "Daily Developer Hacks • AI Tools", font=font_brand_sub, fill=(160, 210, 245))

    draw.rounded_rectangle([820, 85, 1030, 135], radius=12, fill=(0, 240, 255, 25), outline=(0, 240, 255), width=2)
    draw.text((845, 96), "TOOL #1", font=font_category, fill=(0, 240, 255))

    # 3. Giant Tool Title Card (Center Top)
    card_y = 200
    draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(18, 26, 42), outline=(0, 240, 255), width=3)
    draw.text((80, card_y + 20), "ANTIGRAVITY AGENT", font=font_tool_badge, fill=(255, 215, 0))
    draw.text((80, card_y + 85), "Autonomous Bug Fixer & Microservice Deployer", font=font_category, fill=(230, 240, 255))

    # 4. Animated Stage (y=380 to 1420)
    # Background Grid
    for gy in range(380, 1420, 60):
        draw.line([(50, gy), (1030, gy)], fill=(22, 32, 50), width=1)
    for gx in range(50, 1030, 60):
        draw.line([(gx, 380), (gx, 1420)], fill=(22, 32, 50), width=1)

    # Perspective Studded Baseplate Platform
    draw.rectangle([50, 1180, 1030, 1420], fill=(215, 222, 232))
    for row in range(1200, 1420, 36):
        for col in range(90, 1010, 60):
            draw_lego_stud(draw, col, row, r=10, h=6)

    # Server Rack (Right side)
    rack_x, rack_y = 660, 620
    for b_idx in range(11):
        by = rack_y + b_idx * 48
        draw_lego_brick(draw, rack_x, by, 320, 42, (38, 44, 52), (65, 72, 82), (22, 26, 32), studs=6)
        for g in range(rack_x + 20, rack_x + 240, 16):
            draw.line([(g, by + 12), (g, by + 32)], fill=(15, 18, 22), width=4)
        draw.ellipse([rack_x + 265, by + 14, rack_x + 295, by + 30], fill=(0, 240, 255), outline=(180, 255, 255), width=2)

    # Large Cyber HUD (Left side)
    hud_x, hud_y = 80, 620
    draw.rounded_rectangle([hud_x, hud_y, hud_x + 520, hud_y + 320], radius=18, fill=(10, 18, 32), outline=(0, 240, 255), width=3)
    draw.text((hud_x + 24, hud_y + 20), "AGENT REPO RUNNER", font=font_hud_title, fill=(0, 240, 255))
    draw.line([(hud_x + 20, hud_y + 55), (hud_x + 500, hud_y + 55)], fill=(0, 140, 180), width=2)
    draw.text((hud_x + 24, hud_y + 70), "git checkout -b bugfix/agent", font=font_hud_code, fill=(220, 240, 255))
    draw.text((hud_x + 24, hud_y + 105), "Running test suite...", font=font_hud_code, fill=(0, 220, 255))
    draw.text((hud_x + 24, hud_y + 140), "> test_auth_token: PASS", font=font_hud_code_bold, fill=(0, 255, 120))
    draw.text((hud_x + 24, hud_y + 175), "> test_api_gateway: PASS", font=font_hud_code_bold, fill=(0, 255, 120))
    draw.text((hud_x + 24, hud_y + 210), "> test_database_pool: PASS", font=font_hud_code_bold, fill=(0, 255, 120))
    # Full progress bar
    draw.rounded_rectangle([hud_x + 24, hud_y + 255, hud_x + 496, hud_y + 285], radius=8, fill=(0, 255, 140))
    draw.text((hud_x + 130, hud_y + 258), "42/42 TESTS PASSED [100%]", font=font_hud_code_bold, fill=(10, 25, 40))

    # Minifigure center stage
    draw_large_lego_minifigure(
        draw,
        x=450, y=1340,
        scale=1.8,
        leg_angle=18.0,
        arm_l=15.0,
        arm_r=-45.0,
        body_tilt=2.5,
        facing=1,
        action="scan"
    )

    # 5. Massive High-Contrast Kinetic Subtitles (Bottom)
    sub_text = "It doesn't just suggest lines. It clones your repository, debugs failing unit tests, and patches microservices autonomously!"
    wrapped = textwrap.wrap(sub_text, width=38)
    
    sub_h = 40 + len(wrapped) * 54
    sub_y = h - sub_h - 60
    draw.rounded_rectangle([40, sub_y, 1040, sub_y + sub_h], radius=24, fill=(10, 16, 26, 245), outline=(0, 240, 255), width=4)
    
    for i, line in enumerate(wrapped):
        draw.text((70, sub_y + 22 + i * 54), line, font=font_sub_bold, fill=(255, 255, 255))

    out_p = r"D:\Antigravity\Pro\agentic-code\projects\3_free_ai_tools_short\snapshots\test_vertical_preview.png"
    im.save(out_p)
    print("Vertical preview frame saved to:", out_p)

if __name__ == '__main__':
    test_vertical_render()
