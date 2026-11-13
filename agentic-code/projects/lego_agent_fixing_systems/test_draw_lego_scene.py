import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_lego_stud(draw, cx, cy, r=8, h=5, base_col=(180, 185, 195), top_col=(230, 235, 245), outline_col=(195, 200, 210)):
    """Draws a clean 3D perspective LEGO stud with highlight and embossed logo ring."""
    # Stud bottom shadow/cylinder side
    draw.ellipse([cx - r, cy - h, cx + r, cy + h], fill=base_col)
    # Stud top cap
    draw.ellipse([cx - r + 1, cy - h - 3, cx + r - 1, cy + h - 3], fill=top_col, outline=outline_col)
    # Inner embossed circle ring
    ir = r * 0.52
    draw.ellipse([cx - ir, cy - h*0.5 - 3, cx + ir, cy + h*0.5 - 3], outline=outline_col)

def draw_lego_brick(draw, x0, y0, w, h, base_col, light_col, shadow_col, studs=4, outline=(20, 25, 30)):
    """Draws a standard 3D shaded LEGO brick with top studs."""
    # Top face
    top_h = 10
    top_poly = [
        (x0, y0),
        (x0 + 12, y0 - top_h),
        (x0 + w + 12, y0 - top_h),
        (x0 + w, y0)
    ]
    draw.polygon(top_poly, fill=light_col, outline=outline)
    
    # Front face
    front_poly = [
        (x0, y0),
        (x0 + w, y0),
        (x0 + w, y0 + h),
        (x0, y0 + h)
    ]
    draw.polygon(front_poly, fill=base_col, outline=outline)
    
    # Right side face
    right_poly = [
        (x0 + w, y0),
        (x0 + w + 12, y0 - top_h),
        (x0 + w + 12, y0 + h - top_h),
        (x0 + w, y0 + h)
    ]
    draw.polygon(right_poly, fill=shadow_col, outline=outline)
    
    # Studs on top face
    if studs > 0:
        step = w / studs
        for i in range(studs):
            scx = x0 + (i + 0.5) * step + 6
            scy = y0 - top_h * 0.5
            draw_lego_stud(draw, scx, scy, r=max(4, int(step*0.25)), h=3, base_col=shadow_col, top_col=light_col, outline_col=outline)

def draw_lego_character(draw, x, y, scale=1.0, leg_angle=0.0, arm_l=0.0, arm_r=0.0, body_tilt=0.0, facing=1, action="idle"):
    """
    Renders an authentic, 3D-shaded LEGO Minifigure with plastic highlights,
    studs, C-clamp hands, face decal, and articulated limbs.
    Coordinates (x, y) represent center bottom of feet.
    """
    H_HEAD = 38 * scale
    W_HEAD = 34 * scale
    H_STUD = 8 * scale
    W_STUD = 18 * scale
    H_TORSO = 62 * scale
    W_SHOULDER = 46 * scale
    W_WAIST = 58 * scale
    H_HIPS = 16 * scale
    W_HIPS = 56 * scale
    H_LEGS = 62 * scale
    W_LEG = 26 * scale
    
    YELLOW_BASE = (255, 209, 0)
    YELLOW_LIGHT = (255, 238, 100)
    YELLOW_SHADOW = (210, 155, 0)
    
    CYAN_BASE = (0, 165, 205)
    CYAN_LIGHT = (45, 215, 255)
    CYAN_SHADOW = (0, 115, 145)
    
    NAVY_BASE = (26, 68, 120)
    NAVY_LIGHT = (45, 105, 175)
    NAVY_SHADOW = (14, 40, 75)
    
    BLACK_PLASTIC = (35, 38, 44)
    RED_BEANIE = (220, 38, 38)
    RED_BEANIE_LIGHT = (255, 85, 85)
    RED_BEANIE_SHADOW = (160, 20, 20)

    # Soft contact shadow
    draw.ellipse([x - 38*scale, y - 10*scale, x + 38*scale, y + 10*scale], fill=(30, 40, 55, 90))

    hip_y = y - H_LEGS
    torso_bottom_y = hip_y - H_HIPS
    torso_top_y = torso_bottom_y - H_TORSO
    neck_y = torso_top_y - 4 * scale
    head_bottom_y = neck_y
    head_top_y = head_bottom_y - H_HEAD
    stud_top_y = head_top_y - H_STUD

    waddle_dx = math.sin(math.radians(body_tilt)) * 14 * scale

    # Legs
    def render_leg(lx, ly, angle, is_front=True):
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        w2 = W_LEG / 2.0
        local_pts = [(-w2, 0), (w2, 0), (w2, H_LEGS), (-w2, H_LEGS)]
        world_pts = [(px * cos_a - py * sin_a + lx, px * sin_a + py * cos_a + ly) for px, py in local_pts]
        col = NAVY_BASE if is_front else NAVY_SHADOW
        draw.polygon(world_pts, fill=col, outline=NAVY_SHADOW, width=max(1, int(2*scale)))
        # Highlight
        hl_pts = [(-w2 + 3*scale, 4*scale), (-w2 + 7*scale, 4*scale), (-w2 + 7*scale, H_LEGS - 4*scale), (-w2 + 3*scale, H_LEGS - 4*scale)]
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
    draw.rounded_rectangle([x - W_HIPS//2, hip_y - H_HIPS, x + W_HIPS//2, hip_y], radius=int(4*scale), fill=BLACK_PLASTIC, outline=(15, 18, 22), width=max(1, int(2*scale)))
    draw.ellipse([x - 7*scale, hip_y - H_HIPS + 3*scale, x + 7*scale, hip_y - 3*scale], fill=(60, 65, 75))

    # Torso
    tx = x + waddle_dx
    torso_pts = [
        (tx - W_SHOULDER//2, torso_top_y),
        (tx + W_SHOULDER//2, torso_top_y),
        (tx + W_WAIST//2, torso_bottom_y),
        (tx - W_WAIST//2, torso_bottom_y)
    ]
    draw.polygon(torso_pts, fill=CYAN_BASE, outline=CYAN_SHADOW, width=max(1, int(2*scale)))
    # Bevel highlights
    draw.polygon([
        (tx - W_SHOULDER//2 + 3*scale, torso_top_y + 2*scale),
        (tx - W_SHOULDER//2 + 8*scale, torso_top_y + 2*scale),
        (tx - W_WAIST//2 + 8*scale, torso_bottom_y - 2*scale),
        (tx - W_WAIST//2 + 3*scale, torso_bottom_y - 2*scale)
    ], fill=CYAN_LIGHT)
    draw.polygon([
        (tx + W_SHOULDER//2 - 7*scale, torso_top_y + 2*scale),
        (tx + W_SHOULDER//2 - 2*scale, torso_top_y + 2*scale),
        (tx + W_WAIST//2 - 2*scale, torso_bottom_y - 2*scale),
        (tx + W_WAIST//2 - 7*scale, torso_bottom_y - 2*scale)
    ], fill=CYAN_SHADOW)

    # Torso Print Decal
    mid_ty = (torso_top_y + torso_bottom_y) / 2.0
    draw.line([(tx - 12*scale, torso_top_y + 14*scale), (tx + 12*scale, torso_top_y + 14*scale)], fill=(240, 255, 255), width=max(1, int(2*scale)))
    core_r = 10 * scale
    draw.ellipse([tx - core_r, mid_ty - core_r, tx + core_r, mid_ty + core_r], fill=(220, 255, 255), outline=(0, 240, 255), width=max(1, int(2*scale)))
    draw.ellipse([tx - core_r*0.5, mid_ty - core_r*0.5, tx + core_r*0.5, mid_ty + core_r*0.5], fill=(0, 220, 255))
    draw.rectangle([tx - 8*scale, neck_y, tx + 8*scale, torso_top_y], fill=BLACK_PLASTIC)

    # Head
    hx = tx
    draw.rounded_rectangle([hx - W_HEAD//2, head_top_y, hx + W_HEAD//2, head_bottom_y], radius=int(6*scale), fill=YELLOW_BASE, outline=YELLOW_SHADOW, width=max(1, int(2*scale)))
    draw.rounded_rectangle([hx - W_HEAD//2 + 3*scale, head_top_y + 4*scale, hx - W_HEAD//2 + 8*scale, head_bottom_y - 4*scale], radius=int(3*scale), fill=YELLOW_LIGHT)
    draw.rounded_rectangle([hx + W_HEAD//2 - 6*scale, head_top_y + 4*scale, hx + W_HEAD//2 - 2*scale, head_bottom_y - 4*scale], radius=int(2*scale), fill=YELLOW_SHADOW)
    draw.rounded_rectangle([hx - W_STUD//2, stud_top_y, hx + W_STUD//2, head_top_y], radius=int(2*scale), fill=YELLOW_BASE, outline=YELLOW_SHADOW, width=max(1, int(1.5*scale)))

    # Beanie
    beanie_w = W_HEAD + 8 * scale
    beanie_h = 24 * scale
    beanie_y = head_top_y - 6 * scale
    draw.ellipse([hx - beanie_w//2, beanie_y - beanie_h//2, hx + beanie_w//2, beanie_y + beanie_h//2 + 6*scale], fill=RED_BEANIE, outline=RED_BEANIE_SHADOW, width=max(1, int(2*scale)))
    draw.rounded_rectangle([hx - beanie_w//2 - 2*scale, beanie_y + 2*scale, hx + beanie_w//2 + 2*scale, beanie_y + 12*scale], radius=int(3*scale), fill=RED_BEANIE_LIGHT, outline=RED_BEANIE_SHADOW, width=max(1, int(1.5*scale)))
    draw.ellipse([hx - 6*scale, beanie_y - beanie_h//2 - 4*scale, hx + 6*scale, beanie_y - beanie_h//2 + 4*scale], fill=RED_BEANIE_LIGHT)

    # Face Decal
    face_y = head_top_y + 16 * scale
    eye_offset = 7 * scale
    eye_look_x = 2 * scale * facing
    draw.line([(hx - eye_offset - 4*scale, face_y - 7*scale), (hx - eye_offset + 3*scale, face_y - 6*scale)], fill=(40, 30, 10), width=max(1, int(2*scale)))
    draw.line([(hx + eye_offset - 3*scale, face_y - 6*scale), (hx + eye_offset + 4*scale, face_y - 8*scale)], fill=(40, 30, 10), width=max(1, int(2*scale)))
    for side in [-1, 1]:
        ex = hx + (eye_offset * side) + eye_look_x
        draw.ellipse([ex - 3*scale, face_y - 4*scale, ex + 3*scale, face_y + 4*scale], fill=(20, 20, 25))
        draw.ellipse([ex - 1.5*scale, face_y - 3*scale, ex + 1*scale, face_y - 0.5*scale], fill=(255, 255, 255))
    draw.arc([hx - 7*scale + eye_look_x, face_y + 4*scale, hx + 7*scale + eye_look_x, face_y + 13*scale], start=10, end=170, fill=(30, 20, 10), width=max(1, int(2.5*scale)))

    # Arms and Clean C-Clamp Hands (using draw.arc!)
    def render_arm(is_right=True, arm_ang=0.0):
        side = 1 if is_right else -1
        sx = tx + (W_SHOULDER * 0.46 * side)
        sy = torso_top_y + 8 * scale
        rad = math.radians(arm_ang)
        
        # Arm vector
        arm_len = 38 * scale
        wx = sx + math.sin(rad) * arm_len + (8 * scale * side if facing == 0 else 0)
        wy = sy + math.cos(rad) * arm_len
        
        col = CYAN_BASE if (side * facing >= 0 or facing == 0) else CYAN_SHADOW
        draw.line([(sx, sy), (wx, wy)], fill=col, width=int(14 * scale))
        draw.ellipse([sx - 7*scale, sy - 7*scale, sx + 7*scale, sy + 7*scale], fill=col)
        draw.ellipse([wx - 6*scale, wy - 6*scale, wx + 6*scale, wy + 6*scale], fill=YELLOW_SHADOW)
        
        # LEGO C-Clamp Hand using clean arc
        hr = 9 * scale
        hx_c = wx + math.sin(rad) * (hr + 2*scale)
        hy_c = wy + math.cos(rad) * (hr + 2*scale)
        
        # Base angle of C opening
        open_deg = math.degrees(rad) - 90
        draw.arc([hx_c - hr, hy_c - hr, hx_c + hr, hy_c + hr], start=open_deg + 45, end=open_deg + 315, fill=YELLOW_BASE, width=int(5*scale))
        return hx_c, hy_c

    render_arm(False, arm_l)
    rhx, rhy = render_arm(True, arm_r)

    # Props
    if action == "scan":
        # Handheld scanner with cyan beam
        draw.rectangle([rhx, rhy - 4*scale, rhx + 16*scale, rhy + 8*scale], fill=(0, 230, 255), outline=(255, 255, 255))
        for b in range(30, 240, 20):
            by = rhy + math.sin(b * 0.12) * 35
            draw.line([(rhx + 16*scale, rhy + 2*scale), (rhx + 16*scale + b, by)], fill=(0, 240, 255), width=max(1, int(1.5*scale)))

    elif action == "victory":
        # Holding glowing 1x1 LEGO brick
        bx = tx
        by = head_top_y - 45 * scale
        draw.rectangle([bx - 12*scale, by - 10*scale, bx + 12*scale, by + 10*scale], fill=(0, 245, 255), outline=(255, 255, 255), width=max(1, int(2*scale)))
        draw.rectangle([bx - 4*scale, by - 16*scale, bx + 4*scale, by - 10*scale], fill=(180, 255, 255), outline=(255, 255, 255))
        for r_deg in range(0, 360, 45):
            rr = math.radians(r_deg)
            draw.line([(bx, by), (bx + math.cos(rr)*32*scale, by + math.sin(rr)*32*scale)], fill=(220, 255, 255), width=max(1, int(2*scale)))

def generate_scene_preview():
    w, h = 1280, 720
    im = Image.new('RGB', (w, h), (242, 246, 252))
    draw = ImageDraw.Draw(im)

    # 1. Floor
    floor_y = 480
    draw.rectangle([0, floor_y, w, h], fill=(215, 222, 232))
    # Perspective grid & studs
    for row in range(floor_y + 15, h, 30):
        depth_fac = (row - floor_y) / (h - floor_y)
        stud_r = 7 + int(depth_fac * 7)
        spacing = 45 + int(depth_fac * 30)
        stud_h = 4 + int(depth_fac * 4)
        for col in range(25, w, spacing):
            draw_lego_stud(draw, col, row, r=stud_r, h=stud_h)

    # 2. Station 1: LEGO Brick Server Rack (Right side, x=920)
    rack_x, rack_y = 920, 200
    # Stack 6 layers of bricks
    brick_colors = [
        ((40, 45, 52), (65, 72, 82), (25, 28, 34)),
        ((35, 40, 48), (60, 68, 78), (22, 25, 30)),
    ]
    for b_idx in range(7):
        by = rack_y + b_idx * 40
        b_col, l_col, s_col = brick_colors[b_idx % 2]
        draw_lego_brick(draw, rack_x, by, 180, 36, b_col, l_col, s_col, studs=6)
        # Server grill vents
        for g in range(rack_x + 15, rack_x + 130, 10):
            draw.line([(g, by + 10), (g, by + 26)], fill=(15, 18, 22), width=3)
        # LED round studs (flashing alarm red)
        draw.ellipse([rack_x + 145, by + 12, rack_x + 165, by + 24], fill=(255, 50, 50), outline=(255, 180, 180))

    # Server smoke puffs (made of puffy white/grey round bricks)
    smoke_pts = [(rack_x + 60, rack_y - 20, 22), (rack_x + 85, rack_y - 45, 30), (rack_x + 115, rack_y - 30, 26)]
    for sx, sy, sr in smoke_pts:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(230, 235, 240, 180), outline=(190, 195, 205), width=2)

    # 3. Station 2: Cyber Terminal (Left side, x=180)
    term_x, term_y = 180, 380
    # Desk base
    draw_lego_brick(draw, term_x, term_y, 160, 100, (160, 168, 178), (200, 208, 218), (120, 128, 138), studs=5)
    # Angled 45 degree slope brick for keyboard
    slope_poly = [
        (term_x + 40, term_y - 5),
        (term_x + 120, term_y - 5),
        (term_x + 130, term_y - 30),
        (term_x + 30, term_y - 30)
    ]
    draw.polygon(slope_poly, fill=(50, 55, 65), outline=(20, 25, 30), width=2)
    # Printed keyboard keys
    for kx in range(term_x + 45, term_x + 115, 14):
        draw.line([(kx, term_y - 10), (kx, term_y - 25)], fill=(0, 240, 255), width=2)

    # Floating Holographic Screen HUD
    hud_x, hud_y = term_x - 10, term_y - 180
    draw.rounded_rectangle([hud_x, hud_y, hud_x + 180, hud_y + 130], radius=10, fill=(10, 25, 45), outline=(0, 210, 255), width=2)
    draw.text((hud_x + 12, hud_y + 10), "CYBER TERMINAL v4.2", fill=(0, 240, 255))
    draw.line([(hud_x + 12, hud_y + 28), (hud_x + 168, hud_y + 28)], fill=(0, 140, 180), width=1)
    # Matrix code lines
    code_lines = [
        "const patch = await Hotfix.apply();",
        "RUNNING: 42 integration tests...",
        "> test_db_pool: OK",
        "> test_agent_loop: OK",
        "STATUS: ALL 42 TESTS PASS [100%]"
    ]
    for i, line in enumerate(code_lines):
        col = (40, 255, 120) if "PASS" in line or "OK" in line else (160, 210, 240)
        draw.text((hud_x + 12, hud_y + 36 + i * 18), line, fill=col)

    # 4. Station 3: Technic Master Lever (Center-Right, x=640)
    lever_x, lever_y = 620, 360
    # Technic upright pillar
    draw_lego_brick(draw, lever_x, lever_y, 45, 120, (55, 60, 70), (85, 90, 102), (35, 40, 48), studs=1)
    # Technic peg holes
    for py in range(lever_y + 20, lever_y + 110, 25):
        draw.ellipse([lever_x + 15, py, lever_x + 30, py + 15], fill=(25, 30, 38), outline=(90, 95, 108))

    # Lever Arm with bright red shaft and yellow ball
    pivot_x, pivot_y = lever_x + 22, lever_y + 35
    lever_ang = math.radians(-35) # Pulled down!
    arm_len = 55
    ball_x = pivot_x + math.sin(lever_ang) * arm_len
    ball_y = pivot_y - math.cos(lever_ang) * arm_len
    draw.line([(pivot_x, pivot_y), (ball_x, ball_y)], fill=(220, 40, 40), width=6)
    draw.ellipse([pivot_x - 7, pivot_y - 7, pivot_x + 7, pivot_y + 7], fill=(20, 25, 30))
    # Yellow ball handle
    draw.ellipse([ball_x - 9, ball_y - 9, ball_x + 9, ball_y + 9], fill=(255, 209, 0), outline=(210, 155, 0), width=2)

    # 5. Minifigure Walking toward the station!
    draw_lego_character(
        draw, 
        x=450, y=590, 
        scale=1.15, 
        leg_angle=26.0, 
        arm_l=-30.0, 
        arm_r=32.0, 
        body_tilt=3.5, 
        facing=1, 
        action="walk"
    )

    out_path = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\snapshots\test_scene_preview.png"
    im.save(out_path)
    print("Full scene preview rendered to:", out_path)

if __name__ == '__main__':
    generate_scene_preview()
