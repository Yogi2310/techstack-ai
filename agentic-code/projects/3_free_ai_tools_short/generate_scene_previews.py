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
font_category = get_font("arialbd.ttf", 30)
font_tool_badge = get_font("arialbd.ttf", 54)
font_card_sub = get_font("arialbd.ttf", 30)
font_hud_title = get_font("arialbd.ttf", 26)
font_hud_code = get_font("consola.ttf", 22)
font_hud_code_bold = get_font("consolab.ttf", 24)
font_sub_bold = get_font("arialbd.ttf", 44)
font_giant_btn = get_font("arialbd.ttf", 46)

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

def draw_large_lego_minifigure(draw, x, y, scale=1.8, leg_angle=0.0, arm_l=0.0, arm_r=0.0, body_tilt=0.0, facing=1, action="idle", anim_t=0.0):
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

    # Shadow
    draw.ellipse([x - 56*scale, y - 14*scale, x + 56*scale, y + 14*scale], fill=(20, 28, 42, 120))

    hip_y = y - H_LEGS
    torso_bottom_y = hip_y - H_HIPS
    torso_top_y = torso_bottom_y - H_TORSO
    neck_y = torso_top_y - 5 * scale
    head_bottom_y = neck_y
    head_top_y = head_bottom_y - H_HEAD
    stud_top_y = head_top_y - H_STUD

    waddle_dx = math.sin(math.radians(body_tilt)) * 18 * scale

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

    # Hip piece
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

    # Cyber Chest Core
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

    # Red Beanie
    beanie_w = W_HEAD + 10 * scale
    beanie_h = 26 * scale
    beanie_y = head_top_y - 7 * scale
    draw.ellipse([hx - beanie_w//2, beanie_y - beanie_h//2, hx + beanie_w//2, beanie_y + beanie_h//2 + 6*scale], fill=RED_BEANIE, outline=(30, 10, 10), width=3)
    draw.rounded_rectangle([hx - beanie_w//2 - 2*scale, beanie_y + 2*scale, hx + beanie_w//2 + 2*scale, beanie_y + 13*scale], radius=int(3*scale), fill=RED_BEANIE_LIGHT, outline=(30, 10, 10), width=2)
    draw.ellipse([hx - 7*scale, beanie_y - beanie_h//2 - 4*scale, hx + 7*scale, beanie_y - beanie_h//2 + 4*scale], fill=RED_BEANIE_LIGHT)

    # Face
    face_y = head_top_y + 18 * scale
    eye_offset = 8 * scale
    eye_look_x = 2 * scale * facing
    draw.line([(hx - eye_offset - 5*scale, face_y - 8*scale), (hx - eye_offset + 3*scale, face_y - 7*scale)], fill=(30, 20, 10), width=3)
    draw.line([(hx + eye_offset - 3*scale, face_y - 7*scale), (hx + eye_offset + 5*scale, face_y - 9*scale)], fill=(30, 20, 10), width=3)
    for side in [-1, 1]:
        ex = hx + (eye_offset * side) + eye_look_x
        draw.ellipse([ex - 4*scale, face_y - 5*scale, ex + 4*scale, face_y + 5*scale], fill=(15, 15, 20))
        draw.ellipse([ex - 2*scale, face_y - 4*scale, ex + 1.5*scale, face_y - 0.5*scale], fill=(255, 255, 255))
    
    if action == "shocked":
        draw.ellipse([hx - 7*scale, face_y + 5*scale, hx + 7*scale, face_y + 16*scale], fill=(25, 15, 10))
    elif action == "victory":
        draw.arc([hx - 10*scale, face_y + 3*scale, hx + 10*scale, face_y + 16*scale], start=10, end=170, fill=(25, 15, 10), width=4)
        draw.chord([hx - 9*scale, face_y + 5*scale, hx + 9*scale, face_y + 15*scale], start=10, end=170, fill=(240, 60, 60))
    else:
        draw.arc([hx - 8*scale + eye_look_x, face_y + 4*scale, hx + 8*scale + eye_look_x, face_y + 15*scale], start=10, end=170, fill=(25, 15, 10), width=3)

    # Arms & Hands
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
            by = rhy + math.sin(anim_t * 8.0 + b * 0.08) * 65
            draw.line([(rhx + 22*scale, rhy + 2*scale), (rhx + 22*scale + b, by)], fill=(0, 240, 255), width=3)
    elif action == "victory":
        # Glowing Golden AI Brick in right hand
        gx, gy = rhx - 15, rhy - 70
        draw_lego_brick(draw, gx, gy, 60, 38, (255, 205, 0), (255, 245, 120), (195, 145, 0), studs=2, outline=(50, 40, 10))
        # Beams
        for deg in range(0, 360, 45):
            rad = math.radians(deg + anim_t * 60)
            bx1 = gx + 30 + math.cos(rad) * 45
            by1 = gy + 20 + math.sin(rad) * 45
            bx2 = gx + 30 + math.cos(rad) * (75 + math.sin(anim_t*10)*15)
            by2 = gy + 20 + math.sin(rad) * (75 + math.sin(anim_t*10)*15)
            draw.line([(bx1, by1), (bx2, by2)], fill=(255, 235, 100), width=3)

    return (tx, torso_top_y, rhx, rhy)


def render_scene_frame(scene_idx, t_sec=0.0):
    w, h = 1080, 1920
    im = Image.new('RGB', (w, h), (10, 16, 28))
    draw = ImageDraw.Draw(im)

    # 1. Top Global Progress Bar (0 to 50.79s)
    total_d = 50.79
    prog_pct = min(1.0, max(0.0, t_sec / total_d))
    draw.rectangle([40, 45, 1040, 55], fill=(25, 35, 55))
    draw.rounded_rectangle([40, 45, int(40 + 1000 * prog_pct), 55], radius=4, fill=(0, 240, 255))

    # 2. Header Bar (Avatar + Channel Name + Badge)
    logo_path = r"D:\Antigravity\Pro\channel_profile_pic.png"
    logo_raw = Image.open(logo_path).convert("RGBA")
    logo_header = make_circular_logo(logo_raw, 84, border_color=(0, 240, 255), border_width=3)
    im.paste(logo_header, (50, 75), mask=logo_header)

    draw.text((150, 85), "TECHSTACK AI", font=font_brand, fill=(255, 255, 255))
    draw.text((150, 128), "Daily Developer Hacks • AI Tools", font=font_brand_sub, fill=(160, 210, 245))

    # Scene specific badge & title card & stage
    card_y = 200
    if scene_idx == 1:
        # Hook Scene (Warning / Stop hand coding)
        draw.rounded_rectangle([800, 85, 1030, 135], radius=12, fill=(255, 50, 50, 35), outline=(255, 60, 60), width=2)
        draw.text((822, 96), "🚨 ALERT", font=font_category, fill=(255, 80, 80))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 16, 20), outline=(255, 60, 60), width=3)
        draw.text((80, card_y + 20), "STOP CODING BY HAND", font=font_tool_badge, fill=(255, 80, 80))
        draw.text((80, card_y + 85), "3 Free AI Tools That Feel Illegal in 2026", font=font_card_sub, fill=(255, 210, 210))

        # Stage: Overwhelmed developer desk, manual error logs, warning signs
        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(32, 20, 25), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(32, 20, 25), width=1)

        # Studded Baseplate
        draw.rectangle([50, 1180, 1030, 1420], fill=(225, 215, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6, base_col=(180, 170, 170), top_col=(240, 230, 230), outline_col=(190, 180, 180))

        # Floating Alert HUDs
        draw.rounded_rectangle([80, 520, 480, 780], radius=18, fill=(35, 18, 22), outline=(255, 60, 60), width=3)
        draw.text((110, 545), "⚠️ MANUAL BURNOUT", font=font_hud_title, fill=(255, 80, 80))
        draw.line([(100, 585), (460, 585)], fill=(180, 40, 40), width=2)
        draw.text((110, 605), "• 4 Hours Writing CRUD Boilerplate", font=font_hud_code, fill=(255, 200, 200))
        draw.text((110, 645), "• 3 Hours Debugging Edge Cases", font=font_hud_code, fill=(255, 200, 200))
        draw.text((110, 685), "• 2 Hours Fixing Broken CI/CD", font=font_hud_code, fill=(255, 200, 200))
        draw.rounded_rectangle([110, 725, 450, 760], radius=8, fill=(220, 40, 40))
        draw.text((135, 730), "STATUS: EXHAUSTION [0% SPEED]", font=font_hud_code_bold, fill=(255, 255, 255))

        # Right HUD: Crossed out manual stack
        draw.rounded_rectangle([580, 520, 980, 780], radius=18, fill=(25, 22, 35), outline=(255, 180, 0), width=3)
        draw.text((610, 545), "❌ LEGACY CODING 2020", font=font_hud_title, fill=(255, 180, 0))
        draw.line([(600, 585), (960, 585)], fill=(180, 120, 0), width=2)
        draw.text((610, 605), "• Typing line by line", font=font_hud_code, fill=(240, 230, 200))
        draw.text((610, 645), "• Googling StackOverflow for hours", font=font_hud_code, fill=(240, 230, 200))
        draw.text((610, 685), "• Manual regex & SQL schemas", font=font_hud_code, fill=(240, 230, 200))
        draw.rounded_rectangle([610, 725, 950, 760], radius=8, fill=(200, 140, 0))
        draw.text((645, 730), "TIME WASTED: 25 HRS / WK", font=font_hud_code_bold, fill=(15, 20, 30))

        # Shocked Minifigure center
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.85, leg_angle=12.0, arm_l=-35.0, arm_r=35.0, body_tilt=0.0, facing=0, action="shocked", anim_t=t_sec)

        sub_text = "If you are still writing boilerplate code by hand in 2026, stop. These three free AI tools feel illegal for developers."

    elif scene_idx == 2:
        # Tool 1: Antigravity Agent
        draw.rounded_rectangle([820, 85, 1030, 135], radius=12, fill=(0, 240, 255, 25), outline=(0, 240, 255), width=2)
        draw.text((845, 96), "TOOL #1", font=font_category, fill=(0, 240, 255))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(14, 24, 40), outline=(0, 240, 255), width=3)
        draw.text((80, card_y + 20), "ANTIGRAVITY AGENT", font=font_tool_badge, fill=(255, 215, 0))
        draw.text((80, card_y + 85), "Autonomous Bug Fixer & Microservice Deployer", font=font_card_sub, fill=(220, 240, 255))

        # Stage Grid
        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(20, 32, 52), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(20, 32, 52), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(215, 222, 232))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Server Rack Right
        rack_x, rack_y = 660, 560
        for b_idx in range(12):
            by = rack_y + b_idx * 48
            draw_lego_brick(draw, rack_x, by, 320, 42, (38, 44, 52), (65, 72, 82), (22, 26, 32), studs=6)
            for g in range(rack_x + 20, rack_x + 240, 16):
                draw.line([(g, by + 12), (g, by + 32)], fill=(15, 18, 22), width=4)
            draw.ellipse([rack_x + 265, by + 14, rack_x + 295, by + 30], fill=(0, 240, 255), outline=(180, 255, 255), width=2)

        # Left HUD: Test runner passing
        hud_x, hud_y = 80, 560
        draw.rounded_rectangle([hud_x, hud_y, hud_x + 520, hud_y + 360], radius=18, fill=(10, 18, 32), outline=(0, 240, 255), width=3)
        draw.text((hud_x + 24, hud_y + 20), "AGENT REPO RUNNER", font=font_hud_title, fill=(0, 240, 255))
        draw.line([(hud_x + 20, hud_y + 55), (hud_x + 500, hud_y + 55)], fill=(0, 140, 180), width=2)
        draw.text((hud_x + 24, hud_y + 70), "$ git clone internal-api.git", font=font_hud_code, fill=(220, 240, 255))
        draw.text((hud_x + 24, hud_y + 105), "$ pytest --fix-agent auto", font=font_hud_code, fill=(0, 220, 255))
        draw.text((hud_x + 24, hud_y + 145), "> test_auth_token: PASS", font=font_hud_code_bold, fill=(0, 255, 120))
        draw.text((hud_x + 24, hud_y + 180), "> test_api_gateway: PASS", font=font_hud_code_bold, fill=(0, 255, 120))
        draw.text((hud_x + 24, hud_y + 215), "> test_database_pool: PASS", font=font_hud_code_bold, fill=(0, 255, 120))
        draw.text((hud_x + 24, hud_y + 250), "> auto_pr_merged: #1409", font=font_hud_code_bold, fill=(0, 255, 120))
        draw.rounded_rectangle([hud_x + 24, hud_y + 295, hud_x + 496, hud_y + 335], radius=8, fill=(0, 255, 140))
        draw.text((hud_x + 90, hud_y + 302), "42/42 ALL TESTS PASSED [100%]", font=font_hud_code_bold, fill=(10, 25, 40))

        # Scanning Minifigure
        draw_large_lego_minifigure(draw, x=450, y=1340, scale=1.8, leg_angle=18.0, arm_l=15.0, arm_r=-45.0, body_tilt=2.5, facing=1, action="scan", anim_t=t_sec)

        sub_text = "Number one: Antigravity Code Agent. It does not just suggest lines. It clones your repo, debugs failing unit tests, and patches microservices autonomously."

    elif scene_idx == 3:
        # Tool 2: Bolt & Cursor
        draw.rounded_rectangle([820, 85, 1030, 135], radius=12, fill=(180, 50, 255, 25), outline=(180, 50, 255), width=2)
        draw.text((845, 96), "TOOL #2", font=font_category, fill=(200, 80, 255))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(22, 14, 35), outline=(180, 50, 255), width=3)
        draw.text((80, card_y + 20), "BOLT.NEW & CURSOR", font=font_tool_badge, fill=(255, 220, 50))
        draw.text((80, card_y + 85), "Instant Full-Stack Cloud Sandboxing in 60s", font=font_card_sub, fill=(235, 215, 255))

        # Stage Grid (Purple tint)
        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(32, 20, 48), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(32, 20, 48), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(220, 215, 228))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6, base_col=(180, 170, 190), top_col=(235, 230, 245), outline_col=(190, 180, 200))

        # Left HUD: Cursor AI Editor
        c_x, c_y = 80, 560
        draw.rounded_rectangle([c_x, c_y, c_x + 440, c_y + 360], radius=18, fill=(18, 12, 30), outline=(180, 60, 255), width=3)
        draw.text((c_x + 24, c_y + 20), "CURSOR AI EDITOR", font=font_hud_title, fill=(200, 80, 255))
        draw.line([(c_x + 20, c_y + 55), (c_x + 420, c_y + 55)], fill=(120, 40, 180), width=2)
        draw.text((c_x + 24, c_y + 70), "const app = createServer();", font=font_hud_code, fill=(230, 215, 255))
        draw.text((c_x + 24, c_y + 105), "// Cmd+K: Auto generate auth", font=font_hud_code, fill=(150, 130, 200))
        draw.text((c_x + 24, c_y + 145), "+ app.use(supabaseAuth());", font=font_hud_code_bold, fill=(0, 255, 160))
        draw.text((c_x + 24, c_y + 180), "+ app.post('/api/billing');", font=font_hud_code_bold, fill=(0, 255, 160))
        draw.text((c_x + 24, c_y + 215), "+ await db.syncSchemas();", font=font_hud_code_bold, fill=(0, 255, 160))
        draw.rounded_rectangle([c_x + 24, c_y + 285, c_x + 416, c_y + 325], radius=8, fill=(180, 50, 255))
        draw.text((c_x + 75, c_y + 292), "STACK COMPLETE: NEXT.JS 15", font=font_hud_code_bold, fill=(255, 255, 255))

        # Right HUD: Bolt.new Live Browser
        b_x, b_y = 560, 560
        draw.rounded_rectangle([b_x, b_y, b_x + 440, b_y + 360], radius=18, fill=(12, 22, 28), outline=(0, 240, 180), width=3)
        draw.text((b_x + 24, b_y + 20), "BOLT.NEW WEBCONTAINER", font=font_hud_title, fill=(0, 240, 180))
        draw.line([(b_x + 20, b_y + 55), (b_x + 420, b_y + 55)], fill=(0, 150, 120), width=2)
        draw.text((b_x + 24, b_y + 70), "npm run dev [Vite 6.0]", font=font_hud_code, fill=(200, 255, 240))
        draw.text((b_x + 24, b_y + 105), "Ready in 142ms", font=font_hud_code, fill=(0, 240, 180))
        draw.rounded_rectangle([b_x + 24, b_y + 145, b_x + 416, b_y + 260], radius=12, fill=(18, 32, 40), outline=(0, 220, 160), width=2)
        draw.text((b_x + 45, b_y + 165), "LIVE APP AT :3000", font=font_hud_title, fill=(255, 255, 255))
        draw.text((b_x + 45, b_y + 205), "Zero Local Config Needed", font=font_hud_code, fill=(180, 230, 220))
        draw.rounded_rectangle([b_x + 24, b_y + 285, b_x + 416, b_y + 325], radius=8, fill=(0, 220, 160))
        draw.text((b_x + 75, b_y + 292), "DEPLOYED TO PRODUCTION", font=font_hud_code_bold, fill=(10, 25, 25))

        # Minifigure typing happily
        draw_large_lego_minifigure(draw, x=510, y=1340, scale=1.8, leg_angle=-10.0, arm_l=-45.0, arm_r=-45.0, body_tilt=-2.0, facing=1, action="idle", anim_t=t_sec)

        sub_text = "Number two: Bolt dot new and Cursor. Full stack cloud prototyping directly inside your browser with instant zero config deployments in sixty seconds."

    elif scene_idx == 4:
        # Tool 3: Gemini 3.1 Flash
        draw.rounded_rectangle([820, 85, 1030, 135], radius=12, fill=(50, 120, 255, 25), outline=(50, 140, 255), width=2)
        draw.text((845, 96), "TOOL #3", font=font_category, fill=(70, 160, 255))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(14, 20, 42), outline=(50, 140, 255), width=3)
        draw.text((80, card_y + 20), "GEMINI 3.1 FLASH", font=font_tool_badge, fill=(0, 235, 255))
        draw.text((80, card_y + 85), "1,000,000 Token Context • Entire Codebase Ingestion", font=font_card_sub, fill=(215, 235, 255))

        # Stage Grid (Electric Blue)
        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(18, 30, 58), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(18, 30, 58), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(215, 222, 236))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Center Giant Glowing AI Brain Core
        cx, cy = 540, 660
        draw.ellipse([cx - 240, cy - 140, cx + 240, cy + 140], fill=(12, 25, 52), outline=(50, 150, 255), width=4)
        draw.ellipse([cx - 200, cy - 110, cx + 200, cy + 110], fill=(20, 40, 80), outline=(0, 235, 255), width=2)
        draw.text((cx - 180, cy - 65), "1,000,000 TOKENS", font=font_giant_btn, fill=(255, 255, 255))
        draw.text((cx - 140, cy), "FULL REPOSITORY INGESTION", font=font_category, fill=(0, 230, 255))
        # Giant Capacity Bar
        draw.rounded_rectangle([cx - 200, cy + 50, cx + 200, cy + 85], radius=10, fill=(10, 18, 35), outline=(0, 240, 255), width=2)
        draw.rounded_rectangle([cx - 195, cy + 55, cx + 195, cy + 80], radius=8, fill=(0, 240, 255))

        # Surrounding File Nodes
        files = ["src/auth.ts", "lib/database.go", "api/routes.py", "docker-compose.yml", "schema.sql"]
        f_coords = [(160, 540), (840, 540), (140, 820), (860, 820), (540, 890)]
        for fn, (fx, fy) in zip(files, f_coords):
            draw.rounded_rectangle([fx - 110, fy - 30, fx + 110, fy + 30], radius=10, fill=(16, 28, 50), outline=(0, 200, 255), width=2)
            draw.text((fx - 90, fy - 12), fn, font=font_hud_code, fill=(220, 245, 255))
            draw.line([(fx, fy), (cx, cy)], fill=(0, 180, 255, 120), width=2)

        # Minifigure pointing up at the giant core
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.8, leg_angle=0.0, arm_l=-30.0, arm_r=-85.0, body_tilt=0.0, facing=1, action="idle", anim_t=t_sec)

        sub_text = "Number three: Gemini Three Flash. A one million token context window that ingests entire multi gigabyte codebases in two seconds flat."

    elif scene_idx == 5:
        # Outro / CTA: TechStack AI
        draw.rounded_rectangle([780, 85, 1030, 135], radius=12, fill=(255, 200, 0, 30), outline=(255, 215, 0), width=2)
        draw.text((802, 96), "🔥 10X SPEED", font=font_category, fill=(255, 215, 0))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 24, 14), outline=(255, 215, 0), width=3)
        draw.text((80, card_y + 20), "SAVE 10 HOURS / WEEK", font=font_tool_badge, fill=(255, 225, 50))
        draw.text((80, card_y + 85), "Which One Are You Testing First? Comment Below!", font=font_card_sub, fill=(255, 240, 200))

        # Stage Grid (Golden festive)
        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(36, 30, 20), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(36, 30, 20), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(235, 230, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6, base_col=(195, 185, 165), top_col=(250, 245, 230), outline_col=(205, 195, 175))

        # Giant Floating Subscribe Box
        sub_box_y = 540
        draw.rounded_rectangle([140, sub_box_y, 940, sub_box_y + 260], radius=24, fill=(16, 22, 34), outline=(255, 215, 0), width=4)
        
        # Giant Red YouTube Subscribe Button
        draw.rounded_rectangle([200, sub_box_y + 40, 880, sub_box_y + 130], radius=18, fill=(255, 0, 0), outline=(255, 255, 255), width=3)
        draw.polygon([(260, sub_box_y + 60), (260, sub_box_y + 110), (305, sub_box_y + 85)], fill=(255, 255, 255))
        draw.text((330, sub_box_y + 58), "SUBSCRIBE FOR DAILY HACKS", font=font_giant_btn, fill=(255, 255, 255))
        
        # Under text
        draw.text((220, sub_box_y + 160), "🔔 Turn On All Notifications • Never Miss An AI Tool", font=font_category, fill=(255, 225, 120))
        draw.text((310, sub_box_y + 205), "@TechStacAI on YouTube & Shorts", font=font_brand_sub, fill=(180, 215, 245))

        # Victory Minifigure with glowing golden AI brick!
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.9, leg_angle=0.0, arm_l=-75.0, arm_r=-80.0, body_tilt=0.0, facing=0, action="victory", anim_t=t_sec)

        sub_text = "Save ten hours every single week. Which one are you testing first? Subscribe to TechStack AI for daily developer hacks!"

    # 4. Massive Kinetic Subtitles (Bottom)
    wrapped = textwrap.wrap(sub_text, width=38)
    sub_h = 40 + len(wrapped) * 54
    sub_y = h - sub_h - 60
    draw.rounded_rectangle([40, sub_y, 1040, sub_y + sub_h], radius=24, fill=(10, 16, 26, 245), outline=(0, 240, 255), width=4)
    
    for i, line in enumerate(wrapped):
        draw.text((70, sub_y + 22 + i * 54), line, font=font_sub_bold, fill=(255, 255, 255))

    return im

def main():
    os.makedirs(r"D:\Antigravity\Pro\agentic-code\projects\3_free_ai_tools_short\snapshots", exist_ok=True)
    for s_idx in range(1, 6):
        im = render_scene_frame(s_idx, t_sec=float(s_idx * 8.0))
        out_p = fr"D:\Antigravity\Pro\agentic-code\projects\3_free_ai_tools_short\snapshots\preview_scene_{s_idx}.png"
        im.save(out_p)
        print(f"Saved snapshot: preview_scene_{s_idx}.png")

if __name__ == '__main__':
    main()
