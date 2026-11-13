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

    if action == "wrench":
        wx, wy = rhx, rhy - 15
        draw.rectangle([wx - 6, wy - 25, wx + 6, wy + 25], fill=(0, 240, 255), outline=(255, 255, 255), width=2)
        draw.ellipse([wx - 14, wy - 35, wx + 14, wy - 15], outline=(0, 240, 255), width=4)
        draw.text((wx - 25, wy - 55), "ORCHESTRATOR FIX", font=font_hud_code_bold, fill=(0, 255, 200))
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
    draw.text((150, 128), "Real Systems Engineering • Breaking Tech", font=font_brand_sub, fill=(160, 210, 245))

    card_y = 200

    # 5 Scenes based on 53.09s timeline
    # Scene 1: 0.0 - 11.65s (Hook: Global Outage Today)
    if t < 11.65:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(255, 50, 50, 35), outline=(255, 60, 60), width=2)
        draw.text((775, 96), "🚨 BREAKING TODAY", font=font_category, fill=(255, 80, 80))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 16, 20), outline=(255, 60, 60), width=3)
        draw.text((80, card_y + 20), "MICROSOFT DOWN TODAY", font=font_tool_badge, fill=(255, 80, 80))
        draw.text((80, card_y + 85), "Teams, Outlook & Copilot Worldwide Crash", font=font_card_sub, fill=(255, 210, 210))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(32, 20, 25), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(32, 20, 25), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(225, 215, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6, base_col=(180, 170, 170), top_col=(240, 230, 230), outline_col=(190, 180, 180))

        # Downdetector & Service Outage HUD
        pulse = (math.sin(t * 8.0) + 1.0) * 0.5
        draw.rounded_rectangle([80, 540, 1000, 890], radius=20, fill=(30, 14, 18), outline=(int(200 + 55*pulse), 60, 60), width=3)
        draw.text((110, 565), "🚨 DOWNDETECTOR SPIKE: 130,000+ REPORTS TODAY", font=font_hud_title, fill=(255, 80, 80))
        draw.line([(100, 605), (980, 605)], fill=(180, 40, 40), width=2)
        
        # Outage Status Grid
        draw.rounded_rectangle([110, 625, 520, 705], radius=10, fill=(45, 18, 22), outline=(255, 80, 80), width=2)
        draw.text((130, 640), "MICROSOFT TEAMS", font=font_hud_code_bold, fill=(255, 220, 220))
        draw.text((130, 670), "STATUS: OFFLINE [503 GATEWAY]", font=font_hud_code, fill=(255, 80, 80))

        draw.rounded_rectangle([560, 625, 970, 705], radius=10, fill=(45, 18, 22), outline=(255, 80, 80), width=2)
        draw.text((580, 640), "OUTLOOK / EXCHANGE", font=font_hud_code_bold, fill=(255, 220, 220))
        draw.text((580, 670), "STATUS: DISCONNECTED", font=font_hud_code, fill=(255, 80, 80))

        draw.rounded_rectangle([110, 725, 520, 805], radius=10, fill=(45, 18, 22), outline=(255, 80, 80), width=2)
        draw.text((130, 740), "COPILOT 365 AI", font=font_hud_code_bold, fill=(255, 220, 220))
        draw.text((130, 770), "STATUS: TIMEOUT / UNRESPONSIVE", font=font_hud_code, fill=(255, 80, 80))

        draw.rounded_rectangle([560, 725, 970, 805], radius=10, fill=(45, 18, 22), outline=(255, 80, 80), width=2)
        draw.text((580, 740), "SHUTDOWN CAUSE", font=font_hud_code_bold, fill=(255, 220, 220))
        draw.text((580, 770), "NOT A HACKER • INTERNAL CASCADE", font=font_hud_code, fill=(255, 220, 50))

        draw.rounded_rectangle([110, 825, 970, 870], radius=10, fill=(220, 40, 40))
        draw.text((230, 835), "ENTERPRISE IMPACT: 130,000+ ACTIVE TENANTS LOCKED OUT", font=font_hud_code_bold, fill=(255, 255, 255))

        waddle = math.sin(t * 8.0) * 12
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.85, leg_angle=waddle, arm_l=-35.0 + math.sin(t*8)*15, arm_r=35.0 - math.sin(t*8)*15, body_tilt=math.sin(t*4)*2.0, facing=0, action="shocked", anim_t=t)

        if t < 6.0:
            sub_text = "Microsoft just went down worldwide again today!"
            hl_word = "down worldwide"
        else:
            sub_text = "Over one hundred and thirty thousand enterprise users were kicked out of Teams, Outlook, and Copilot."
            hl_word = "one hundred and thirty thousand"

    # Scene 2: 11.65 - 21.82s (The Incident MO1550821 & Health Check)
    elif t < 21.82:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(255, 160, 0, 30), outline=(255, 180, 0), width=2)
        draw.text((775, 96), "🔍 MO1550821", font=font_category, fill=(255, 180, 0))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 22, 14), outline=(255, 180, 0), width=3)
        draw.text((80, card_y + 20), "THE FAILED HEALTH-CHECK", font=font_tool_badge, fill=(255, 200, 50))
        draw.text((80, card_y + 85), "Watchdog Monitors Failed Under Backend Latency", font=font_card_sub, fill=(255, 235, 200))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(34, 28, 20), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(34, 28, 20), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(230, 225, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Health Check Failure HUD
        draw.rounded_rectangle([80, 540, 1000, 900], radius=20, fill=(18, 16, 24), outline=(255, 160, 0), width=3)
        draw.text((110, 565), "⚙️ INCIDENT ARCHITECTURE: WATCHDOG HEALTH-CHECK", font=font_hud_title, fill=(255, 180, 0))
        draw.line([(100, 605), (980, 605)], fill=(160, 110, 0), width=2)
        
        draw.rounded_rectangle([110, 625, 970, 715], radius=12, fill=(14, 20, 32), outline=(0, 220, 255), width=2)
        draw.text((130, 640), "STEP 1: BACKEND ELEVATED PROCESSING LOAD", font=font_hud_code_bold, fill=(0, 240, 255))
        draw.text((130, 675), "• Subset of backend worker nodes experienced elevated latency (>3500ms)", font=font_hud_code, fill=(220, 240, 255))

        draw.rounded_rectangle([110, 735, 970, 825], radius=12, fill=(35, 15, 18), outline=(255, 60, 60), width=2)
        draw.text((130, 750), "STEP 2: WATCHDOG PROBE DETECTS TIMEOUT", font=font_hud_code_bold, fill=(255, 80, 80))
        draw.text((130, 785), "• GET /healthz -> FAILED (Node marked UNHEALTHY by orchestrator)", font=font_hud_code, fill=(255, 200, 200))

        draw.rounded_rectangle([110, 845, 970, 885], radius=8, fill=(10, 12, 20), outline=(255, 200, 0), width=1)
        draw.text((130, 855), "ORCHESTRATOR DECISION: REMOVE NODES FROM ACTIVE POOL INSTANTLY", font=font_hud_code_bold, fill=(255, 220, 100))

        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.8, leg_angle=-10.0, arm_l=-40.0, arm_r=-50.0, body_tilt=0.0, facing=1, action="idle", anim_t=t)

        if t < 16.5:
            sub_text = "Microsoft tracked the chaos under incident M-O 1550821."
            hl_word = "MO1550821."
        else:
            sub_text = "It started when a backend cluster experienced sudden latency, causing automated health checks to fail."
            hl_word = "health checks to fail."

    # Scene 3: 21.82 - 32.58s (The Cascading Failure / Thundering Herd)
    elif t < 32.58:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(255, 50, 50, 35), outline=(255, 60, 60), width=2)
        draw.text((775, 96), "⚠️ CASCADING BUG", font=font_category, fill=(255, 80, 80))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(32, 12, 18), outline=(255, 60, 60), width=3)
        draw.text((80, card_y + 20), "THE THUNDERING HERD", font=font_tool_badge, fill=(255, 80, 80))
        draw.text((80, card_y + 85), "Dead Nodes Dumped 100% Load on Surviving Servers", font=font_card_sub, fill=(255, 220, 220))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(36, 18, 22), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(36, 18, 22), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(225, 215, 220))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Cascading Failure Spiral HUD
        draw.rounded_rectangle([80, 540, 1000, 910], radius=20, fill=(26, 12, 16), outline=(255, 60, 60), width=3)
        draw.text((110, 565), "💀 DISTRIBUTED SYSTEMS DEATH SPIRAL", font=font_hud_title, fill=(255, 80, 80))
        draw.line([(100, 605), (980, 605)], fill=(180, 40, 40), width=2)
        
        # Server Node Status Simulation
        nodes = [
            ("CLUSTER A", "DEAD", (255, 60, 60)),
            ("CLUSTER B", "DEAD", (255, 60, 60)),
            ("CLUSTER C", "DEAD", (255, 60, 60)),
            ("CLUSTER D", "100% CPU OVERLOAD", (255, 180, 0))
        ]
        for idx, (cname, cstat, ccol) in enumerate(nodes):
            ny = 625 + idx * 55
            draw.rounded_rectangle([110, ny, 970, ny + 46], radius=8, fill=(40, 15, 20), outline=ccol, width=2)
            draw.text((130, ny + 12), cname, font=font_hud_code_bold, fill=(255, 255, 255))
            draw.text((450, ny + 12), f"STATUS: {cstat}", font=font_hud_code_bold, fill=ccol)

        draw.rounded_rectangle([110, 855, 970, 895], radius=8, fill=(220, 40, 40))
        draw.text((250, 865), "RESULT: TOTAL COLLAPSE OF TLS HANDSHAKE PROXIES", font=font_hud_code_bold, fill=(255, 255, 255))

        waddle = math.sin(t * 8.0) * 8
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.85, leg_angle=waddle, arm_l=-35.0, arm_r=35.0, body_tilt=0.0, facing=0, action="shocked", anim_t=t)

        if t < 27.0:
            sub_text = "Instead of throttling traffic, the orchestrator automatically pulled those servers offline!"
            hl_word = "pulled those servers offline!"
        else:
            sub_text = "That dumped one hundred percent of global traffic onto surviving nodes, creating an instant cascading collapse!"
            hl_word = "cascading collapse!"

    # Scene 4: 32.58 - 41.39s (Global Traffic Rerouting & Emergency Bypass)
    elif t < 41.39:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(0, 240, 180, 30), outline=(0, 240, 180), width=2)
        draw.text((775, 96), "🌐 REROUTING", font=font_category, fill=(0, 240, 180))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(12, 28, 25), outline=(0, 240, 180), width=3)
        draw.text((80, card_y + 20), "EMERGENCY NODE BYPASS", font=font_tool_badge, fill=(0, 240, 180))
        draw.text((80, card_y + 85), "Manual Capacity Re-injection & Traffic Diversion", font=font_card_sub, fill=(200, 255, 235))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(18, 36, 32), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(18, 36, 32), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(215, 235, 225))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Recovery Operations Terminal HUD
        draw.rounded_rectangle([80, 540, 1000, 900], radius=20, fill=(10, 22, 20), outline=(0, 255, 160), width=3)
        draw.text((110, 565), "🛠️ MICROSOFT SRE INCIDENT MITIGATION", font=font_hud_title, fill=(0, 255, 160))
        draw.line([(100, 605), (980, 605)], fill=(0, 160, 100), width=2)
        draw.text((110, 630), "> isolate_degraded_nodes --region ALL", font=font_hud_code, fill=(220, 255, 240))
        draw.text((110, 670), "> shift_traffic --target ALT_NETWORK_PATHWAYS", font=font_hud_code, fill=(220, 255, 240))
        draw.text((110, 710), "> override_health_checks --force-rejoin", font=font_hud_code_bold, fill=(255, 220, 50))
        draw.text((110, 750), "> RE-INJECTING 85% RESTART CAPACITY...", font=font_hud_code_bold, fill=(0, 240, 255))
        draw.text((110, 790), "> RESTORING TEAMS & OUTLOOK CONNECTION PIPES...", font=font_hud_code_bold, fill=(0, 255, 140))
        
        draw.rounded_rectangle([110, 830, 970, 880], radius=10, fill=(0, 200, 120))
        draw.text((260, 842), "MITIGATION IN PROGRESS: TRAFFIC STABILIZING", font=font_hud_code_bold, fill=(10, 25, 20))

        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.8, leg_angle=-8.0, arm_l=-30.0, arm_r=-55.0, body_tilt=0.0, facing=1, action="wrench", anim_t=t)

        if t < 37.0:
            sub_text = "The secure handshake proxies choked. Microsoft engineers had to manually bypass broken routing."
            hl_word = "manually bypass broken routing."
        else:
            sub_text = "And force healthy capacity back into the cluster to halt the spiral."
            hl_word = "halt the spiral."

    # Scene 5: 41.39 - 53.09s (Systems Engineering Lesson & Subscribe CTA)
    else:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(255, 200, 0, 30), outline=(255, 215, 0), width=2)
        draw.text((775, 96), "💡 SYSTEMS LESSON", font=font_category, fill=(255, 215, 0))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 24, 14), outline=(255, 215, 0), width=3)
        draw.text((80, card_y + 20), "CIRCUIT BREAKER RULE", font=font_tool_badge, fill=(255, 225, 50))
        draw.text((80, card_y + 85), "Never Let Health Checks Kill Clusters", font=font_card_sub, fill=(255, 240, 200))

        for gy in range(380, 1420, 60):
            draw.line([(50, gy), (1030, gy)], fill=(36, 30, 20), width=1)
        for gx in range(50, 1030, 60):
            draw.line([(gx, 380), (gx, 1420)], fill=(36, 30, 20), width=1)

        draw.rectangle([50, 1180, 1030, 1420], fill=(235, 230, 215))
        for row in range(1200, 1420, 36):
            for col in range(90, 1010, 60):
                draw_lego_stud(draw, col, row, r=10, h=6)

        # Floating Subscribe Card
        sub_box_y = 540
        draw.rounded_rectangle([140, sub_box_y, 940, sub_box_y + 260], radius=24, fill=(16, 22, 34), outline=(255, 215, 0), width=4)
        
        btn_pulse = (math.sin(t * 8.0) + 1.0) * 4
        draw.rounded_rectangle([int(200 - btn_pulse), int(sub_box_y + 40 - btn_pulse), int(880 + btn_pulse), int(sub_box_y + 130 + btn_pulse)], radius=18, fill=(255, 0, 0), outline=(255, 255, 255), width=3)
        draw.polygon([(260, sub_box_y + 60), (260, sub_box_y + 110), (305, sub_box_y + 85)], fill=(255, 255, 255))
        draw.text((330, sub_box_y + 58), "SUBSCRIBE FOR POST-MORTEMS", font=font_giant_btn, fill=(255, 255, 255))
        
        draw.text((210, sub_box_y + 160), "🔔 Real Engineering Disasters & Distributed Systems", font=font_category, fill=(255, 225, 120))
        draw.text((310, sub_box_y + 205), "@TechStacAI on YouTube & Shorts", font=font_brand_sub, fill=(180, 215, 245))

        for c in range(16):
            cy_c = int((t * 120 + c * 85) % 1000) + 400
            cx_c = 80 + (c * 62) % 920
            c_col = [(255, 215, 0), (0, 240, 255), (255, 70, 70), (0, 255, 120)][c % 4]
            draw_lego_stud(draw, cx_c, cy_c, r=8, h=5, base_col=c_col, top_col=(255, 255, 255), outline_col=(30, 30, 30))

        arm_wave = math.sin(t * 10.0) * 10.0
        draw_large_lego_minifigure(draw, x=540, y=1340, scale=1.9, leg_angle=0.0, arm_l=-75.0 + arm_wave, arm_r=-80.0 - arm_wave, body_tilt=0.0, facing=0, action="victory", anim_t=t)

        if t < 47.0:
            sub_text = "The golden rule of distributed systems: Never let your health checks kill more than twenty percent of your fleet at once."
            hl_word = "twenty percent"
        else:
            sub_text = "Subscribe to TechStack AI for real engineering post-mortems!"
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
    proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_today_outage_short"
    audio_path = os.path.join(proj_dir, "audio", "short_master_audio.wav")
    output_video = os.path.join(proj_dir, "MICROSOFT_TODAY_OUTAGE_SHORT_9x16.mp4")
    logo_path = r"D:\Antigravity\Pro\channel_profile_pic.png"

    logo_raw = Image.open(logo_path).convert("RGBA")
    logo_header = make_circular_logo(logo_raw, 84, border_color=(0, 240, 255), border_width=3)

    total_duration = 53.09
    fps = 24
    total_frames = int(round(total_duration * fps))

    print(f"--- RENDERING MICROSOFT TODAY OUTAGE VERTICAL SHORT (1080x1920) ---", flush=True)
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

            if frame_idx % 120 == 0 or frame_idx == total_frames - 1:
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
