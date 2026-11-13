import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

def create_lego_minifigure(
    draw, 
    x, y, 
    scale=1.0, 
    leg_angle=0.0,       # Degrees (+ forward, - backward for left leg; right leg opposite)
    arm_left_angle=0.0,  # Degrees
    arm_right_angle=0.0, # Degrees
    body_tilt=0.0,       # Degrees tilt for walking waddle
    facing=1,            # 1 = face right, -1 = face left, 0 = face camera
    action="idle"        # idle, walk, scan, type, pull_lever, victory
):
    """
    Renders an authentic, 3D-shaded LEGO Minifigure with plastic highlights,
    studs, C-clamp hands, face decal, and articulated limbs.
    Coordinates (x, y) represent the center bottom of the feet on the ground.
    """
    # Minifigure dimensions at scale 1.0 (total height ~ 180px)
    H_HEAD = 38 * scale
    W_HEAD = 34 * scale
    H_STUD = 8 * scale
    W_STUD = 18 * scale
    H_TORSO = 64 * scale
    W_SHOULDER = 46 * scale
    W_WAIST = 58 * scale
    H_HIPS = 16 * scale
    W_HIPS = 56 * scale
    H_LEGS = 62 * scale
    W_LEG = 26 * scale
    
    # Base colors with 3D plastic highlights & shadows
    YELLOW_BASE = (255, 209, 0)
    YELLOW_LIGHT = (255, 240, 110)
    YELLOW_SHADOW = (215, 160, 0)
    
    CYAN_BASE = (0, 165, 205)
    CYAN_LIGHT = (40, 215, 255)
    CYAN_SHADOW = (0, 115, 145)
    
    NAVY_BASE = (26, 68, 120)
    NAVY_LIGHT = (45, 105, 175)
    NAVY_SHADOW = (14, 40, 75)
    
    BLACK_PLASTIC = (35, 38, 44)
    RED_BEANIE = (220, 38, 38)
    RED_BEANIE_LIGHT = (255, 85, 85)
    RED_BEANIE_SHADOW = (160, 20, 20)

    # 1. Drop shadow on floor beneath minifigure
    shadow_w = int(70 * scale)
    shadow_h = int(18 * scale)
    draw.ellipse([x - shadow_w//2, y - shadow_h//2, x + shadow_w//2, y + shadow_h//2], fill=(20, 30, 45, 110))

    # Calculate vertical stack positions from ground up:
    # y is ground level (bottom of feet)
    hip_y = y - H_LEGS
    torso_bottom_y = hip_y - H_HIPS
    torso_top_y = torso_bottom_y - H_TORSO
    neck_y = torso_top_y - 4 * scale
    head_bottom_y = neck_y
    head_top_y = head_bottom_y - H_HEAD
    stud_top_y = head_top_y - H_STUD

    # Body waddle offset
    waddle_dx = math.sin(math.radians(body_tilt)) * (H_LEGS + H_TORSO) * 0.25

    # -------------------------------------------------------------------------
    # 2. LEGS & HIPS
    # -------------------------------------------------------------------------
    # In LEGO minifigures, legs swing from the hip hinge
    # Left leg angle = leg_angle, Right leg angle = -leg_angle
    # When facing sideways or 3/4, one leg is front, one back
    
    def draw_lego_leg(lx, ly, angle, is_front=True):
        # Draw a boxy rectangular leg rotating around (lx, ly)
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Leg polygon corners in local coords (top-left, top-right, bottom-right, bottom-left)
        w2 = W_LEG / 2.0
        local_pts = [
            (-w2, 0),
            (w2, 0),
            (w2, H_LEGS),
            (-w2, H_LEGS)
        ]
        
        # Rotate and translate
        world_pts = []
        for px, py in local_pts:
            rx = px * cos_a - py * sin_a + lx
            ry = px * sin_a + py * cos_a + ly
            world_pts.append((rx, ry))
            
        color = NAVY_BASE if is_front else NAVY_SHADOW
        draw.polygon(world_pts, fill=color, outline=NAVY_SHADOW, width=max(1, int(2 * scale)))
        
        # 3D Highlight strip on front edge
        hl_pts = [
            (-w2 + 3 * scale, 3 * scale),
            (-w2 + 7 * scale, 3 * scale),
            (-w2 + 7 * scale, H_LEGS - 3 * scale),
            (-w2 + 3 * scale, H_LEGS - 3 * scale)
        ]
        world_hl = []
        for px, py in hl_pts:
            rx = px * cos_a - py * sin_a + lx
            ry = px * sin_a + py * cos_a + ly
            world_hl.append((rx, ry))
        draw.polygon(world_hl, fill=NAVY_LIGHT)
        
        # Foot shelf stud holes (LEGO detail at base of foot)
        foot_bottom_x = (-w2 * sin_a) + lx
        foot_bottom_y = (H_LEGS * cos_a) + ly
        # Small dark indent
        draw.line([world_pts[3], world_pts[2]], fill=NAVY_SHADOW, width=max(1, int(3*scale)))

    # Draw Back Leg first
    back_angle = -leg_angle if facing >= 0 else leg_angle
    front_angle = leg_angle if facing >= 0 else -leg_angle
    
    if facing == 0:
        # Facing camera: both legs side by side
        draw_lego_leg(x - W_LEG * 0.55, hip_y, leg_angle, is_front=True)
        draw_lego_leg(x + W_LEG * 0.55, hip_y, -leg_angle, is_front=True)
    else:
        draw_lego_leg(x - (W_LEG * 0.25 * facing), hip_y, back_angle, is_front=False)
        draw_lego_leg(x + (W_LEG * 0.25 * facing), hip_y, front_angle, is_front=True)

    # Hip assembly (black pivot block)
    draw.rounded_rectangle([
        x - W_HIPS//2, hip_y - H_HIPS,
        x + W_HIPS//2, hip_y
    ], radius=int(4 * scale), fill=BLACK_PLASTIC, outline=(15, 18, 22), width=max(1, int(2*scale)))
    # Hip round center joint button
    draw.ellipse([x - 7 * scale, hip_y - H_HIPS + 3 * scale, x + 7 * scale, hip_y - 3 * scale], fill=(60, 65, 75))

    # -------------------------------------------------------------------------
    # 3. TORSO (Classic Trapezoid with high-tech AI decal)
    # -------------------------------------------------------------------------
    tx = x + waddle_dx
    torso_pts = [
        (tx - W_SHOULDER//2, torso_top_y),   # Top left
        (tx + W_SHOULDER//2, torso_top_y),   # Top right
        (tx + W_WAIST//2, torso_bottom_y),    # Bottom right
        (tx - W_WAIST//2, torso_bottom_y)     # Bottom left
    ]
    draw.polygon(torso_pts, fill=CYAN_BASE, outline=CYAN_SHADOW, width=max(1, int(2*scale)))

    # Plastic lighting gradient / bevel on torso
    # Left highlight band
    draw.polygon([
        (tx - W_SHOULDER//2 + 3*scale, torso_top_y + 2*scale),
        (tx - W_SHOULDER//2 + 9*scale, torso_top_y + 2*scale),
        (tx - W_WAIST//2 + 9*scale, torso_bottom_y - 2*scale),
        (tx - W_WAIST//2 + 3*scale, torso_bottom_y - 2*scale)
    ], fill=CYAN_LIGHT)
    
    # Right shadow band
    draw.polygon([
        (tx + W_SHOULDER//2 - 7*scale, torso_top_y + 2*scale),
        (tx + W_SHOULDER//2 - 2*scale, torso_top_y + 2*scale),
        (tx + W_WAIST//2 - 2*scale, torso_bottom_y - 2*scale),
        (tx + W_WAIST//2 - 7*scale, torso_bottom_y - 2*scale)
    ], fill=CYAN_SHADOW)

    # Torso High-Tech Decal (Printed LEGO Graphic)
    # Circuit traces
    mid_ty = (torso_top_y + torso_bottom_y) / 2.0
    draw.line([(tx - 12*scale, torso_top_y + 14*scale), (tx + 12*scale, torso_top_y + 14*scale)], fill=(240, 255, 255), width=max(1, int(2*scale)))
    draw.line([(tx - 8*scale, torso_top_y + 14*scale), (tx - 8*scale, mid_ty + 6*scale)], fill=(255, 230, 80), width=max(1, int(1.5*scale)))
    draw.line([(tx + 8*scale, torso_top_y + 14*scale), (tx + 8*scale, mid_ty + 6*scale)], fill=(255, 230, 80), width=max(1, int(1.5*scale)))

    # Glowing AI Core Hexagon/Circle on chest
    core_r = 10 * scale
    draw.ellipse([tx - core_r, mid_ty - core_r, tx + core_r, mid_ty + core_r], fill=(220, 255, 255), outline=(0, 240, 255), width=max(1, int(2*scale)))
    draw.ellipse([tx - core_r*0.5, mid_ty - core_r*0.5, tx + core_r*0.5, mid_ty + core_r*0.5], fill=(0, 220, 255))
    
    # Collar ring
    draw.rectangle([tx - 8*scale, neck_y, tx + 8*scale, torso_top_y], fill=BLACK_PLASTIC)

    # -------------------------------------------------------------------------
    # 4. HEAD & FACE DECAL & BEANIE
    # -------------------------------------------------------------------------
    hx = tx
    # Head cylinder base
    draw.rounded_rectangle([
        hx - W_HEAD//2, head_top_y,
        hx + W_HEAD//2, head_bottom_y
    ], radius=int(6*scale), fill=YELLOW_BASE, outline=YELLOW_SHADOW, width=max(1, int(2*scale)))

    # Head 3D Specular Highlight on left side
    draw.rounded_rectangle([
        hx - W_HEAD//2 + 3*scale, head_top_y + 4*scale,
        hx - W_HEAD//2 + 8*scale, head_bottom_y - 4*scale
    ], radius=int(3*scale), fill=YELLOW_LIGHT)
    
    # Head Shadow on right side
    draw.rounded_rectangle([
        hx + W_HEAD//2 - 6*scale, head_top_y + 4*scale,
        hx + W_HEAD//2 - 2*scale, head_bottom_y - 4*scale
    ], radius=int(2*scale), fill=YELLOW_SHADOW)

    # Top Stud (embossed LEGO stud)
    draw.rounded_rectangle([
        hx - W_STUD//2, stud_top_y,
        hx + W_STUD//2, head_top_y
    ], radius=int(2*scale), fill=YELLOW_BASE, outline=YELLOW_SHADOW, width=max(1, int(1.5*scale)))
    draw.ellipse([hx - W_STUD//2 + 3*scale, stud_top_y + 1*scale, hx + W_STUD//2 - 3*scale, stud_top_y + 4*scale], fill=YELLOW_LIGHT)

    # Red Beanie Hat (sitting tilted over the head stud)
    beanie_w = W_HEAD + 8 * scale
    beanie_h = 24 * scale
    beanie_y = head_top_y - 6 * scale
    # Beanie dome
    draw.ellipse([hx - beanie_w//2, beanie_y - beanie_h//2, hx + beanie_w//2, beanie_y + beanie_h//2 + 6*scale], fill=RED_BEANIE, outline=RED_BEANIE_SHADOW, width=max(1, int(2*scale)))
    # Beanie cuff rim
    draw.rounded_rectangle([hx - beanie_w//2 - 2*scale, beanie_y + 2*scale, hx + beanie_w//2 + 2*scale, beanie_y + 12*scale], radius=int(3*scale), fill=RED_BEANIE_LIGHT, outline=RED_BEANIE_SHADOW, width=max(1, int(1.5*scale)))
    # Beanie top pom-pom / fold
    draw.ellipse([hx - 6*scale, beanie_y - beanie_h//2 - 4*scale, hx + 6*scale, beanie_y - beanie_h//2 + 4*scale], fill=RED_BEANIE_LIGHT)

    # Face Decal (Eyes, Eyebrows, Smirk)
    face_y = head_top_y + 16 * scale
    eye_offset = 7 * scale
    eye_look_x = 2 * scale * facing
    
    # Eyebrows (confident slight angle)
    draw.line([(hx - eye_offset - 4*scale, face_y - 7*scale), (hx - eye_offset + 3*scale, face_y - 6*scale)], fill=(40, 30, 10), width=max(1, int(2*scale)))
    draw.line([(hx + eye_offset - 3*scale, face_y - 6*scale), (hx + eye_offset + 4*scale, face_y - 8*scale)], fill=(40, 30, 10), width=max(1, int(2*scale)))

    # Eyes (classic black pill with white specular highlight)
    for side in [-1, 1]:
        ex = hx + (eye_offset * side) + eye_look_x
        draw.ellipse([ex - 3*scale, face_y - 4*scale, ex + 3*scale, face_y + 4*scale], fill=(20, 20, 25))
        # White twinkle dot
        draw.ellipse([ex - 1.5*scale, face_y - 3*scale, ex + 1*scale, face_y - 0.5*scale], fill=(255, 255, 255))

    # Smirk mouth
    draw.arc([hx - 7*scale + eye_look_x, face_y + 4*scale, hx + 7*scale + eye_look_x, face_y + 13*scale], start=10, end=170, fill=(30, 20, 10), width=max(1, int(2.5*scale)))

    # -------------------------------------------------------------------------
    # 5. ARMS & YELLOW C-CLAMP HANDS
    # -------------------------------------------------------------------------
    def draw_lego_arm_and_hand(is_right=True, arm_angle=0.0):
        # Shoulder anchor
        shoulder_side = 1 if is_right else -1
        sx = tx + (W_SHOULDER * 0.48 * shoulder_side)
        sy = torso_top_y + 8 * scale
        
        # Arm length: upper arm (28px), forearm (26px)
        rad = math.radians(arm_angle)
        # If facing right, right arm is forward/back
        elbow_dx = math.sin(rad) * 26 * scale + (12 * scale * shoulder_side)
        elbow_dy = math.cos(rad) * 26 * scale
        
        wrist_dx = elbow_dx + math.sin(rad + 0.3 * shoulder_side) * 24 * scale
        wrist_dy = elbow_dy + math.cos(rad + 0.3 * shoulder_side) * 24 * scale
        
        ex = sx + elbow_dx
        ey = sy + elbow_dy
        wx = sx + wrist_dx
        wy = sy + wrist_dy
        
        # Draw curved plastic sleeve
        arm_color = CYAN_BASE if (shoulder_side * facing >= 0 or facing == 0) else CYAN_SHADOW
        draw.line([(sx, sy), (ex, ey)], fill=arm_color, width=int(14 * scale))
        draw.line([(ex, ey), (wx, wy)], fill=arm_color, width=int(12 * scale))
        # Joint cap
        draw.ellipse([sx - 7*scale, sy - 7*scale, sx + 7*scale, sy + 7*scale], fill=arm_color)
        draw.ellipse([ex - 6*scale, ey - 6*scale, ex + 6*scale, ey + 6*scale], fill=arm_color)
        
        # Yellow wrist cuff
        draw.ellipse([wx - 5*scale, wy - 5*scale, wx + 5*scale, wy + 5*scale], fill=YELLOW_SHADOW)
        
        # Iconic Yellow C-Clamp Hand
        # Hand radius ~ 9px, thickness ~ 5px, with an open gap (C-shape)
        hand_r = 9 * scale
        hand_dir = rad + (0.5 if is_right else -0.5)
        # Center of C-hand
        hx_c = wx + math.sin(hand_dir) * (hand_r + 2*scale)
        hy_c = wy + math.cos(hand_dir) * (hand_r + 2*scale)
        
        # Draw outer claw ring
        draw.ellipse([hx_c - hand_r, hy_c - hand_r, hx_c + hand_r, hy_c + hand_r], fill=YELLOW_BASE, outline=YELLOW_SHADOW, width=max(1, int(2*scale)))
        # Inner cutout
        inner_r = hand_r * 0.48
        draw.ellipse([hx_c - inner_r, hy_c - inner_r, hx_c + inner_r, hy_c + inner_r], fill=(30, 35, 45))
        # Clip open gap for the C-shape
        gap_angle = hand_dir + math.pi/2
        gx = hx_c + math.cos(gap_angle) * (hand_r * 0.7)
        gy = hx_c + math.sin(gap_angle) * (hand_r * 0.7)
        draw.line([(hx_c, hy_c), (gx, gy)], fill=(30, 35, 45), width=int(inner_r * 1.6))

        return hx_c, hy_c

    # Back arm
    draw_lego_arm_and_hand(is_right=False, arm_angle=arm_left_angle)
    # Front arm
    hx_r, hy_r = draw_lego_arm_and_hand(is_right=True, arm_angle=arm_right_angle)

    # -------------------------------------------------------------------------
    # 6. ACTION PROPS HELD BY MINIFIGURE
    # -------------------------------------------------------------------------
    if action == "scan":
        # Draw high-tech LEGO scanner tool in front hand
        tool_x = hx_r + 14 * scale
        tool_y = hy_r - 6 * scale
        # Translucent cyan scanner body
        draw.rectangle([hx_r, hy_r - 4*scale, tool_x, tool_y + 8*scale], fill=(0, 230, 255), outline=(255, 255, 255))
        draw.ellipse([tool_x - 3*scale, tool_y - 6*scale, tool_x + 9*scale, tool_y + 10*scale], fill=(180, 255, 255))
        # Sweeping cyan laser fan emitting forward
        for r_beam in range(20, 220, 15):
            beam_y = tool_y + math.sin(r_beam * 0.1) * 35
            draw.line([(tool_x + 6*scale, tool_y + 2*scale), (tool_x + 6*scale + r_beam * scale, beam_y)], fill=(0, 240, 255, 120), width=max(1, int(2*scale)))

    elif action == "victory":
        # Minifigure holding glowing 1x1 LEGO energy cube brick above head
        cube_x = tx
        cube_y = head_top_y - 48 * scale
        cw = 24 * scale
        ch = 20 * scale
        # Glowing cube body
        draw.rectangle([cube_x - cw//2, cube_y - ch//2, cube_x + cw//2, cube_y + ch//2], fill=(0, 245, 255), outline=(255, 255, 255), width=max(1, int(2*scale)))
        # Top stud on brick
        draw.rectangle([cube_x - 7*scale, cube_y - ch//2 - 6*scale, cube_x + 7*scale, cube_y - ch//2], fill=(180, 255, 255), outline=(255, 255, 255))
        # Sparkle rays
        for ray_deg in range(0, 360, 45):
            rr = math.radians(ray_deg)
            draw.line([(cube_x, cube_y), (cube_x + math.cos(rr) * 35*scale, cube_y + math.sin(rr) * 35*scale)], fill=(220, 255, 255), width=max(1, int(2*scale)))


def test_render():
    w, h = 1280, 720
    im = Image.new('RGB', (w, h), (240, 245, 250))
    draw = ImageDraw.Draw(im)

    # 1. Perspective studded LEGO baseplate floor
    floor_y = 480
    draw.rectangle([0, floor_y, w, h], fill=(215, 220, 228))
    
    # Draw studs in perspective
    for row in range(floor_y + 15, h, 28):
        depth_fac = (row - floor_y) / (h - floor_y)
        stud_r = 7 + int(depth_fac * 8)
        spacing = 40 + int(depth_fac * 35)
        stud_h = 4 + int(depth_fac * 5)
        for col in range(20, w, spacing):
            # Stud base shadow
            draw.ellipse([col - stud_r, row - stud_h, col + stud_r, row + stud_h], fill=(180, 185, 195))
            # Stud top face
            draw.ellipse([col - stud_r + 1, row - stud_h - 3, col + stud_r - 1, row + stud_h - 3], fill=(235, 240, 248), outline=(195, 200, 210))
            # Embossed center circle
            draw.ellipse([col - stud_r*0.5, row - stud_h*0.5 - 3, col + stud_r*0.5, row + stud_h*0.5 - 3], outline=(205, 210, 220))

    # 2. Draw 3 Minifigures in different actions to verify:
    # A) Walking Minifigure
    create_lego_minifigure(draw, x=260, y=620, scale=1.1, leg_angle=28.0, arm_left_angle=-35.0, arm_right_angle=30.0, body_tilt=4.0, facing=1, action="walk")
    
    # B) Scanning Minifigure
    create_lego_minifigure(draw, x=640, y=620, scale=1.1, leg_angle=0.0, arm_left_angle=10.0, arm_right_angle=-45.0, body_tilt=0.0, facing=1, action="scan")
    
    # C) Victory Minifigure
    create_lego_minifigure(draw, x=1020, y=620, scale=1.1, leg_angle=0.0, arm_left_angle=-140.0, arm_right_angle=-140.0, body_tilt=0.0, facing=0, action="victory")

    out_test = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\snapshots\test_lego_preview.png"
    im.save(out_test)
    print("Test preview saved to:", out_test)

if __name__ == '__main__':
    test_render()
