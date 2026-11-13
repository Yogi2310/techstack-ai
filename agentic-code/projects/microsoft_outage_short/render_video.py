import os, sys, math, subprocess, json, textwrap
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

# --- FONTS ---
def get_font(name, size):
    try:
        path = os.path.join("C:/Windows/Fonts", name)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_brand = get_font("arialbd.ttf", 36)
font_brand_sub = get_font("arial.ttf", 22)
font_category = get_font("arialbd.ttf", 30)
font_tool_badge = get_font("arialbd.ttf", 52)
font_card_sub = get_font("arialbd.ttf", 28)
font_hud_title = get_font("arialbd.ttf", 26)
font_hud_code = get_font("consola.ttf", 22)
font_hud_code_bold = get_font("consolab.ttf", 24)
font_bsod_sad = get_font("arial.ttf", 72)
font_sub_bold = get_font("arialbd.ttf", 44)
font_giant_btn = get_font("arialbd.ttf", 44)

# --- LOGO HELPER ---
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

# --- LEGO GEOMETRY HELPERS ---
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

# --- 3D LEGO MINIFIGURE MASCOT ---
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

    draw.ellipse([x - 56*scale, y - 14*scale, x + 56*scale, y + 14*scale], fill=(20, 28, 42, 120))

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
    
    if action == "shocked":
        draw.ellipse([hx - 7*scale, face_y + 5*scale, hx + 7*scale, face_y + 16*scale], fill=(25, 15, 10))
    elif action == "victory":
        draw.arc([hx - 10*scale, face_y + 3*scale, hx + 10*scale, face_y + 16*scale], start=10, end=170, fill=(25, 15, 10), width=4)
        draw.chord([hx - 9*scale, face_y + 5*scale, hx + 9*scale, face_y + 15*scale], start=10, end=170, fill=(240, 60, 60))
    else:
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

    if action == "usb":
        ux, uy = rhx, rhy - 15
        draw.rectangle([ux - 8, uy - 18, ux + 8, uy + 18], fill=(0, 240, 255), outline=(255, 255, 255), width=2)
        draw.rectangle([ux - 5, uy - 28, ux + 5, uy - 18], fill=(220, 220, 230), outline=(100, 100, 100), width=1)
        draw.text((ux - 20, uy - 50), "RESCUE USB", font=font_hud_code_bold, fill=(0, 255, 200))
    elif action == "victory":
        gx, gy = rhx - 15, rhy - 70
        draw_lego_brick(draw, gx, gy, 60, 38, (255, 205, 0), (255, 245, 120), (195, 145, 0), studs=2, outline=(50, 40, 10))
        for deg in range(0, 360, 45):
            rad = math.radians(deg + anim_t * 60)
            bx1 = gx + 30 + math.cos(rad) * 45
            by1 = gy + 20 + math.sin(rad) * 45
            bx2 = gx + 30 + math.cos(rad) * (75 + math.sin(anim_t*10)*15)
            by2 = gy + 20 + math.sin(rad) * (75 + math.sin(anim_t*10)*15)
            draw.line([(bx1, by1), (bx2, by2)], fill=(255, 235, 100), width=3)

    return (tx, torso_top_y, rhx, rhy)


def render_vertical_frame(t, total_d, logo_header):
    w, h = 1080, 1920
    im = Image.new('RGB', (w, h), (10, 16, 28))
    draw = ImageDraw.Draw(im)

    # 1. Top Progress Bar
    prog_pct = min(1.0, max(0.0, t / total_d))
    draw.rectangle([40, 45, 1040, 55], fill=(25, 35, 55))
    draw.rounded_rectangle([40, 45, int(40 + 1000 * prog_pct), 55], radius=4, fill=(0, 240, 255))

    # 2. Header Bar
    im.paste(logo_header, (50, 75), mask=logo_header)
    draw.text((150, 85), "TECHSTACK AI", font=font_brand, fill=(255, 255, 255))
    draw.text((150, 128), "Engineering Post-Mortems • AI Workflows", font=font_brand_sub, fill=(160, 210, 245))

    card_y = 200

    # Scene Logic based on 53.93s timeline
    if t < 10.8:
        # Beat 1: Hook (The Global Crash)
        draw.rounded_rectangle([780, 85, 1030, 135], radius=12, fill=(255, 50, 50, 35), outline=(255, 60, 60), width=2)
        draw.text((805, 96), "🚨 GLOBAL CRASH", font=font_category, fill=(255, 80, 80))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 16, 20), outline=(255, 60, 60), width=3)
        draw.text((80, card_y + 20), "8.5M COMPUTERS DOWN", font=font_tool_badge, fill=(255, 80, 80))
        draw.text((80, card_y + 85), "How a 78-Byte File Broke the World", font=font_card_sub, fill=(255, 210, 210))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(32, 20, 25), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(32, 20, 25), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(225, 215, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6, base_col=(180, 170, 170), top_col=(240, 230, 230), outline_col=(190, 180, 180))

        # Huge Disaster HUD with pulsing red alarm
        pulse = (math.sin(t * 8.0) + 1.0) * 0.5
        draw.rounded_rectangle([80, 540, 1000, 880], radius=20, fill=(30, 14, 18), outline=(int(200 + 55*pulse), 60, 60), width=3)
        draw.text((110, 565), "🚨 CRITICAL OUTAGE: JULY 19, 2024", font=font_hud_title, fill=(255, 80, 80))
        draw.line([(100, 605), (980, 605)], fill=(180, 40, 40), width=2)
        draw.text((110, 625), "• 8,500,000 Windows PCs Blue-Screened Instantly", font=font_hud_code_bold, fill=(255, 220, 220))
        draw.text((110, 665), "• 5,000+ Airline Flights Cancelled Worldwide", font=font_hud_code_bold, fill=(255, 220, 220))
        draw.text((110, 705), "• 911 Dispatch Centers & Hospitals Locked Out", font=font_hud_code_bold, fill=(255, 220, 220))
        draw.text((110, 745), "• Root Cause: 1 Single Configuration Update", font=font_hud_code_bold, fill=(255, 220, 220))
        
        draw.rounded_rectangle([110, 800, 970, 850], radius=10, fill=(220, 40, 40))
        draw.text((260, 812), "GLOBAL IMPACT: $10,000,000,000+ DAMAGE", font=font_hud_code_bold, fill=(255, 255, 255))

        waddle = math.sin(t * 8.0) * 12
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.85, leg_angle=waddle, arm_l=-35.0 + math.sin(t*8)*15, arm_r=35.0 - math.sin(t*8)*15, body_tilt=math.sin(t*4)*2.0, facing=0, action="shocked", anim_t=t)

        if t < 5.5:
            sub_text = "How did a tiny 78-byte file cause the largest IT crash in human history?"
            hl_word = "78-byte file"
        else:
            sub_text = "On July 19th, 8.5 million Windows computers died in a single second."
            hl_word = "single second."

    elif t < 21.42:
        # Beat 2: Ring 0 Kernel Bug
        draw.rounded_rectangle([780, 85, 1030, 135], radius=12, fill=(255, 160, 0, 30), outline=(255, 180, 0), width=2)
        draw.text((805, 96), "⚠️ RING 0 BUG", font=font_category, fill=(255, 180, 0))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 22, 14), outline=(255, 180, 0), width=3)
        draw.text((80, card_y + 20), "OUT-OF-BOUNDS READ", font=font_tool_badge, fill=(255, 200, 50))
        draw.text((80, card_y + 85), "Channel File 291 Pointer Exception in Kernel Space", font=font_card_sub, fill=(255, 235, 200))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(34, 28, 20), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(34, 28, 20), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(230, 225, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Kernel Rings Architecture HUD
        draw.rounded_rectangle([80, 540, 1000, 900], radius=20, fill=(18, 16, 24), outline=(255, 160, 0), width=3)
        draw.text((110, 565), "⚙️ WINDOWS PRIVILEGE RINGS (SECURITY ARCHITECTURE)", font=font_hud_title, fill=(255, 180, 0))
        draw.line([(100, 605), (980, 605)], fill=(160, 110, 0), width=2)
        
        draw.rounded_rectangle([110, 630, 520, 780], radius=12, fill=(12, 28, 20), outline=(0, 220, 140), width=2)
        draw.text((130, 645), "RING 3: USER MODE (APPs)", font=font_hud_code_bold, fill=(0, 255, 160))
        draw.text((130, 680), "• Chrome, Slack, VS Code", font=font_hud_code, fill=(200, 240, 220))
        draw.text((130, 715), "• If an app crashes -> OS lives", font=font_hud_code, fill=(200, 240, 220))
        draw.text((130, 745), "✔ Full Sandboxed Safety Net", font=font_hud_code_bold, fill=(0, 255, 160))

        draw.rounded_rectangle([560, 630, 970, 780], radius=12, fill=(35, 15, 18), outline=(255, 60, 60), width=2)
        draw.text((580, 645), "RING 0: KERNEL MODE (DRIVERS)", font=font_hud_code_bold, fill=(255, 80, 80))
        draw.text((580, 680), "• csagent.sys (Falcon Sensor)", font=font_hud_code, fill=(255, 200, 200))
        draw.text((580, 715), "• Read address 0x0000009c", font=font_hud_code, fill=(255, 200, 200))
        draw.text((580, 745), "❌ NO SAFETY NET -> INSTANT CRASH", font=font_hud_code_bold, fill=(255, 80, 80))

        draw.rounded_rectangle([110, 810, 970, 870], radius=10, fill=(10, 12, 20), outline=(255, 200, 0), width=1)
        draw.text((130, 825), "INSTRUCTION: mov r8, [r9+0x9c] -> EXCEPTION: PAGE_FAULT_IN_NONPAGED_AREA", font=font_hud_code, fill=(255, 220, 100))

        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.8, leg_angle=-10.0, arm_l=-40.0, arm_r=-50.0, body_tilt=0.0, facing=1, action="idle", anim_t=t)

        if t < 16.0:
            sub_text = "CrowdStrike pushed Channel File 291. It told their kernel driver to read memory that did not exist."
            hl_word = "read memory"
        else:
            sub_text = "In Ring Zero kernel space, there is zero safety net."
            hl_word = "Ring Zero"

    elif t < 31.81:
        # Beat 3: Blue Screen Boot Loop
        draw.rounded_rectangle([780, 85, 1030, 135], radius=12, fill=(0, 120, 255, 30), outline=(0, 140, 255), width=2)
        draw.text((805, 96), "💀 BSOD LOOP", font=font_category, fill=(0, 180, 255))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(10, 22, 45), outline=(0, 140, 255), width=3)
        draw.text((80, card_y + 20), "INFINITE BSOD CRASH", font=font_tool_badge, fill=(0, 220, 255))
        draw.text((80, card_y + 85), "Crashed During Boot • Zero Wi-Fi to Download Fix", font=font_card_sub, fill=(200, 235, 255))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(0, 70, 160), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(0, 70, 160), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(210, 225, 245))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Huge Authentic BSOD Window
        draw.rounded_rectangle([80, 520, 1000, 920], radius=20, fill=(0, 120, 215), outline=(255, 255, 255), width=3)
        draw.text((120, 545), ":(", font=font_bsod_sad, fill=(255, 255, 255))
        draw.text((120, 640), "Your PC ran into a problem and needs to restart.", font=font_hud_title, fill=(255, 255, 255))
        draw.text((120, 680), "We're just collecting some error info, and then we'll restart for you.", font=font_card_sub, fill=(230, 240, 255))
        
        # Rotating percentage
        bsod_pct = int((t * 25.0) % 100)
        draw.text((120, 730), f"{bsod_pct}% complete [REBOOTING...]", font=font_hud_title, fill=(255, 255, 255))
        
        draw.line([(120, 780), (960, 780)], fill=(255, 255, 255), width=2)
        draw.text((120, 800), "Stop code: PAGE_FAULT_IN_NONPAGED_AREA", font=font_hud_code_bold, fill=(255, 255, 255))
        draw.text((120, 835), "What failed: csagent.sys (CrowdStrike Falcon)", font=font_hud_code_bold, fill=(255, 255, 255))
        draw.text((120, 870), "Status: INFINITE BOOT LOOP [CANNOT CONNECT TO WI-FI]", font=font_hud_code_bold, fill=(255, 240, 50))

        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.85, leg_angle=0.0, arm_l=-35.0, arm_r=35.0, body_tilt=0.0, facing=0, action="shocked", anim_t=t)

        if t < 26.5:
            sub_text = "Windows threw a page fault and crashed into the blue screen of death."
            hl_word = "blue screen of death."
        else:
            sub_text = "Worse, because it crashed during boot, machines could not connect to Wi-Fi to receive a patch!"
            hl_word = "connect to Wi-Fi"

    elif t < 42.18:
        # Beat 4: The USB Recovery
        draw.rounded_rectangle([780, 85, 1030, 135], radius=12, fill=(0, 240, 180, 30), outline=(0, 240, 180), width=2)
        draw.text((805, 96), "🛠️ USB RESCUE", font=font_category, fill=(0, 240, 180))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(12, 28, 25), outline=(0, 240, 180), width=3)
        draw.text((80, card_y + 20), "MANUAL BOOT RESCUE", font=font_tool_badge, fill=(0, 240, 180))
        draw.text((80, card_y + 85), "Safe Mode Deletion of C-00000291*.sys", font=font_card_sub, fill=(200, 255, 235))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(18, 36, 32), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(18, 36, 32), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(215, 235, 225))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Rescue Terminal HUD
        draw.rounded_rectangle([80, 540, 1000, 900], radius=20, fill=(10, 22, 20), outline=(0, 255, 160), width=3)
        draw.text((110, 565), "🛠️ MANUAL SAFE MODE REMEDIATION", font=font_hud_title, fill=(0, 255, 160))
        draw.line([(100, 605), (980, 605)], fill=(0, 160, 100), width=2)
        draw.text((110, 630), "C:\\> bcdedit /set {default} safeboot minimal", font=font_hud_code, fill=(220, 255, 240))
        draw.text((110, 670), "C:\\> cd C:\\Windows\\System32\\drivers\\CrowdStrike", font=font_hud_code, fill=(220, 255, 240))
        draw.text((110, 710), "C:\\> del C-00000291*.sys", font=font_hud_code_bold, fill=(255, 80, 80))
        draw.text((110, 750), "> DELETING MALFORMED CHANNEL FILE 291...", font=font_hud_code_bold, fill=(255, 220, 50))
        draw.text((110, 790), "> REBOOTING TO NORMAL WINDOWS...", font=font_hud_code_bold, fill=(0, 255, 140))
        
        draw.rounded_rectangle([110, 830, 970, 880], radius=10, fill=(0, 200, 120))
        draw.text((280, 842), "SYSTEM REBOOT SUCCESSFUL [200 OK]", font=font_hud_code_bold, fill=(10, 25, 20))

        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.8, leg_angle=-8.0, arm_l=-30.0, arm_r=-55.0, body_tilt=0.0, facing=1, action="usb", anim_t=t)

        if t < 37.0:
            sub_text = "IT admins had to physically run to millions of laptops with USB thumb drives."
            hl_word = "USB thumb drives."
        else:
            sub_text = "Boot into Safe Mode, and manually delete Channel File 291."
            hl_word = "Safe Mode,"

    else:
        # Beat 5: Outro & The Golden Rule CTA
        draw.rounded_rectangle([780, 85, 1030, 135], radius=12, fill=(255, 200, 0, 30), outline=(255, 215, 0), width=2)
        draw.text((805, 96), "💡 GOLDEN RULE", font=font_category, fill=(255, 215, 0))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 24, 14), outline=(255, 215, 0), width=3)
        draw.text((80, card_y + 20), "ALWAYS USE CANARY DEPLOYS", font=font_tool_badge, fill=(255, 225, 50))
        draw.text((80, card_y + 85), "Staged Rollouts • Ring 0 Sandboxing", font=font_card_sub, fill=(255, 240, 200))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(36, 30, 20), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(36, 30, 20), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(235, 230, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Floating Subscribe Box
        sub_box_y = 540
        draw.rounded_rectangle([140, sub_box_y, 940, sub_box_y + 260], radius=24, fill=(16, 22, 34), outline=(255, 215, 0), width=4)
        
        btn_pulse = (math.sin(t * 8.0) + 1.0) * 4
        draw.rounded_rectangle([int(200 - btn_pulse), int(sub_box_y + 40 - btn_pulse), int(880 + btn_pulse), int(sub_box_y + 130 + btn_pulse)], radius=18, fill=(255, 0, 0), outline=(255, 255, 255), width=3)
        draw.polygon([(260, sub_box_y + 60), (260, sub_box_y + 110), (305, sub_box_y + 85)], fill=(255, 255, 255))
        draw.text((330, sub_box_y + 58), "SUBSCRIBE FOR POST-MORTEMS", font=font_giant_btn, fill=(255, 255, 255))
        
        draw.text((210, sub_box_y + 160), "🔔 Real Engineering Disasters & AI Dev Breakthroughs", font=font_category, fill=(255, 225, 120))
        draw.text((310, sub_box_y + 205), "@TechStacAI on YouTube & Shorts", font=font_brand_sub, fill=(180, 215, 245))

        for c in range(16):
            cy_c = int((t * 120 + c * 85) % 1000) + 400
            cx_c = 80 + (c * 62) % 920
            c_col = [(255, 215, 0), (0, 240, 255), (255, 70, 70), (0, 255, 120)][c % 4]
            draw_lego_stud(draw, cx_c, cy_c, r=8, h=5, base_col=c_col, top_col=(255, 255, 255), outline_col=(30, 30, 30))

        arm_wave = math.sin(t * 10.0) * 10.0
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.9, leg_angle=0.0, arm_l=-75.0 + arm_wave, arm_r=-80.0 - arm_wave, body_tilt=0.0, facing=0, action="victory", anim_t=t)

        if t < 47.5:
            sub_text = "The golden rule? Never push updates to everyone at once without canary rollouts."
            hl_word = "canary rollouts."
        else:
            sub_text = "Subscribe to TechStack AI for daily engineering post-mortems!"
            hl_word = "Subscribe"

    # Subtitles container
    wrapped = textwrap.wrap(sub_text, width=38)
    sub_h = 40 + len(wrapped) * 54
    sub_y = h - sub_h - 70
    draw.rounded_rectangle([40, sub_y, 1040, sub_y + sub_h], radius=24, fill=(10, 16, 26, 245), outline=(0, 240, 255), width=4)
    
    for i, line in enumerate(wrapped):
        words = line.split(" ")
        curr_x = 70
        for word in words:
            w_col = (255, 235, 50) if hl_word.lower() in word.lower() else (255, 255, 255)
            draw.text((curr_x, sub_y + 22 + i * 54), word + " ", font=font_sub_bold, fill=w_col)
            curr_x += int(draw.textlength(word + " ", font=font_sub_bold))

    return im


def main():
    proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_outage_short"
    audio_path = os.path.join(proj_dir, "audio", "short_master_audio.wav")
    output_video = os.path.join(proj_dir, "MICROSOFT_OUTAGE_SHORT_9x16.mp4")
    logo_path = r"D:\Antigravity\Pro\channel_profile_pic.png"

    logo_raw = Image.open(logo_path).convert("RGBA")
    logo_header = make_circular_logo(logo_raw, 84, border_color=(0, 240, 255), border_width=3)

    total_duration = 53.93
    fps = 24
    total_frames = int(round(total_duration * fps))

    print(f"--- RENDERING MICROSOFT OUTAGE VERTICAL SHORT (1080x1920) ---", flush=True)
    print(f"Total Duration: {total_duration:.2f}s | FPS: {fps} | Frames: {total_frames}", flush=True)
    print(f"Audio Source: {audio_path}", flush=True)
    print(f"Output Video: {output_video}", flush=True)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video
    ]

    ffmpeg_log = os.path.join(proj_dir, "ffmpeg_render.log")
    with open(ffmpeg_log, "wb") as err_log:
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=err_log)

        for frame_idx in range(total_frames):
            t = frame_idx / fps
            im = render_vertical_frame(t, total_duration, logo_header)
            proc.stdin.write(im.tobytes())

            if frame_idx % 100 == 0 or frame_idx == total_frames - 1:
                pct = (frame_idx + 1) / total_frames * 100.0
                print(f"Rendered frame {frame_idx + 1}/{total_frames} ({pct:.1f}%) [t={t:.2f}s]", flush=True)

        proc.stdin.close()
        proc.wait()

    if proc.returncode == 0:
        file_size_mb = os.path.getsize(output_video) / (1024 * 1024)
        print(f"\n[SUCCESS] Render complete! Video saved to:", flush=True)
        print(f"Path: {output_video}", flush=True)
        print(f"Size: {file_size_mb:.2f} MB", flush=True)
    else:
        with open(ffmpeg_log, "r", encoding="utf-8", errors="ignore") as f:
            err_text = f.read()
        print(f"\n[ERROR] FFmpeg failed with code {proc.returncode}:", flush=True)
        print(err_text[-1000:], flush=True)

if __name__ == '__main__':
    main()
