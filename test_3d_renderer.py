import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

out_path = r"D:\Antigravity\Pro\shorts_studio\temp\preview_3d_character.png"

WIDTH = 720
HEIGHT = 1280
img = Image.new("RGBA", (WIDTH, HEIGHT), color=(10, 12, 22, 255))
draw = ImageDraw.Draw(img)

# 1. Background Cyber Matrix Grid & Glows
for x in range(0, WIDTH, 60):
    draw.line([x, 0, x, HEIGHT], fill=(18, 24, 42, 255), width=1)
for y in range(0, HEIGHT, 60):
    draw.line([0, y, WIDTH, y], fill=(18, 24, 42, 255), width=1)

# Ambient Radial Glow in center
draw.ellipse([WIDTH//2 - 350, 400, WIDTH//2 + 350, 1100], fill=(25, 35, 75, 120))
draw.ellipse([WIDTH//2 - 200, 500, WIDTH//2 + 200, 900], fill=(34, 211, 238, 40))

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 38)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
font_big = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)

# 2. Draw 3D Shaded Sphere (Head)
def draw_3d_sphere(draw, cx, cy, radius, base_col=(25, 30, 45), highlight_col=(180, 210, 240)):
    # Layered concentric spheres with offset highlight towards light source (top-left)
    for r in range(radius, 0, -2):
        t = (radius - r) / float(radius)
        # offset towards (-0.35, -0.35)
        ox = int((radius - r) * -0.35)
        oy = int((radius - r) * -0.35)
        cr = int(base_col[0] + t * (highlight_col[0] - base_col[0]))
        cg = int(base_col[1] + t * (highlight_col[1] - base_col[1]))
        cb = int(base_col[2] + t * (highlight_col[2] - base_col[2]))
        draw.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=(cr, cg, cb, 255))

# 3. Draw 3D Shaded Cylinder (Limb)
def draw_3d_limb(draw, x1, y1, x2, y2, thickness=16, base_col=(25, 30, 45), highlight_col=(160, 190, 220), glow_col=None):
    # Main limb
    draw.line([x1, y1, x2, y2], fill=base_col, width=thickness)
    # Specular shine core
    draw.line([x1 - 2, y1 - 2, x2 - 2, y2 - 2], fill=highlight_col, width=thickness // 3)
    if glow_col:
        # Glowing joint node at ends
        draw.ellipse([x1 - 8, y1 - 8, x1 + 8, y1 + 8], fill=glow_col)
        draw.ellipse([x2 - 8, y2 - 8, x2 + 8, y2 + 8], fill=glow_col)

# Render 3D Stickman Character in "Point" Action
cx = 360
cy = 820
head_r = 46

# Head Y center
head_cy = cy - 130

# Torso (3D shaded pill)
draw_3d_limb(draw, cx, cy - 75, cx, cy + 35, thickness=24, base_col=(20, 25, 38), highlight_col=(140, 170, 210))

# Left Arm (Holding Hologram)
draw_3d_limb(draw, cx - 10, cy - 50, cx - 75, cy - 20, thickness=16, glow_col="#22D3EE")
draw_3d_limb(draw, cx - 75, cy - 20, cx - 110, cy - 80, thickness=14, glow_col="#A855F7")

# Right Arm (Pointing at 3D Floating UI)
draw_3d_limb(draw, cx + 10, cy - 50, cx + 80, cy - 30, thickness=16, glow_col="#22D3EE")
draw_3d_limb(draw, cx + 80, cy - 30, cx + 180, cy - 30, thickness=14, glow_col="#22D3EE")

# Floating Energy Particle Beam from pointing finger
draw.ellipse([cx + 175, cy - 35, cx + 195, cy - 15], fill="#22D3EE")
draw.line([cx + 190, cy - 30, cx + 240, cy - 30], fill="#34D399", width=4)

# Legs (3D Shaded)
draw_3d_limb(draw, cx - 10, cy + 35, cx - 45, cy + 140, thickness=18, glow_col="#22D3EE")
draw_3d_limb(draw, cx + 10, cy + 35, cx + 45, cy + 140, thickness=18, glow_col="#22D3EE")

# 3D Head
draw_3d_sphere(draw, cx, head_cy, head_r, base_col=(20, 25, 40), highlight_col=(180, 215, 250))

# 3D Glowing Cyber Visor (Curved glass)
vx1, vy1, vx2, vy2 = cx - 36, head_cy - 10, cx + 36, head_cy + 14
draw.rounded_rectangle([vx1, vy1, vx2, vy2], radius=10, fill=(34, 211, 238, 255), outline=(168, 85, 247, 255), width=2)
# Visor Specular Glare
draw.line([vx1 + 8, vy1 + 4, vx1 + 35, vy1 + 4], fill="white", width=3)

# 3D Cyber Headphones (Over head)
draw.arc([cx - 52, head_cy - 48, cx + 52, head_cy + 30], 190, 350, fill=(45, 55, 80), width=6)
# Earcups (Glowing pill badges)
draw.rounded_rectangle([cx - 54, head_cy - 12, cx - 42, head_cy + 18], radius=6, fill=(168, 85, 247, 255), outline="#22D3EE", width=2)
draw.rounded_rectangle([cx + 42, head_cy - 12, cx + 54, head_cy + 18], radius=6, fill=(168, 85, 247, 255), outline="#22D3EE", width=2)

# 4. Floating 3D Holographic Card in Foreground
card_x1, card_y1 = 80, 220
card_x2, card_y2 = 640, 520

# Drop shadow / neon back-glow for card
draw.rounded_rectangle([card_x1 - 4, card_y1 - 4, card_x2 + 4, card_y2 + 4], radius=24, fill=(15, 23, 42, 240), outline="#22D3EE", width=3)

# Tech Grid inside card
for gx in range(card_x1 + 40, card_x2, 60):
    draw.line([gx, card_y1 + 10, gx, card_y2 - 10], fill=(25, 35, 60, 100), width=1)

# Card Content
draw.text((card_x1 + 35, card_y1 + 30), "3D HOLOGRAPHIC AI HUD", font=font_tag, fill="#22D3EE")
draw.text((card_x1 + 35, card_y1 + 65), "THE 10X UPGRADE", font=font_big, fill="white")

# 3D Glowing Value Meter
draw.text((card_x1 + 35, card_y1 + 145), "Viewer Retention:", font=font_sub, fill="#9CA3AF")
draw.rounded_rectangle([card_x1 + 35, card_y1 + 190, card_x2 - 35, card_y1 + 225], radius=10, fill=(20, 25, 40, 255), outline="#374151", width=2)
draw.rounded_rectangle([card_x1 + 35, card_y1 + 190, card_x1 + 420, card_y1 + 225], radius=10, fill=(16, 185, 129, 255))
draw.text((card_x1 + 435, card_y1 + 193), "+85%", font=font_tag, fill="#34D399")

draw.text((card_x1 + 35, card_y1 + 245), "Visual Production Quality: Hollywood Tier", font=font_sub, fill="#38BDF8")

# Top HUD
draw.rounded_rectangle([30, 40, 390, 82], radius=15, fill=(28, 30, 46, 255), outline=(65, 70, 98, 255), width=2)
draw.text((48, 50), "3D ENGINE · NEXT GEN", font=font_tag, fill="#22D3EE")

# Bottom Subtitle Ribbon (Kinetic Highlight Style)
draw.rounded_rectangle([30, 1120, WIDTH - 30, 1220], radius=18, fill=(15, 20, 35, 255), outline=(34, 211, 238, 200), width=2)
draw.text((50, 1135), "Full 3D Character with Specular Lighting", font=font_sub, fill="white")
draw.text((50, 1170), "Visor Glare, Cyber Headphones & 3D HUD", font=font_sub, fill="#22D3EE")

img.save(out_path)
print(f"[✓] Generated 3D Preview Frame: {out_path}")
