import os
import sys
import math

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter

out_dir = r"D:\Antigravity\Pro"
profile_path = os.path.join(out_dir, "channel_profile_pic.png")
banner_path = os.path.join(out_dir, "channel_banner.png")

# Fonts
font_huge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 96)
font_large = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 68)
font_med = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 44)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 34)
font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
font_tiny = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)

# ==============================================================================
# 1. GENERATE PROFILE PICTURE (800 x 800)
# ==============================================================================
print("[+] Generating 800x800 Profile Picture...")
p_size = 800
p_img = Image.new("RGBA", (p_size, p_size), color=(10, 14, 26, 255))
p_draw = ImageDraw.Draw(p_img)

cx, cy = p_size // 2, p_size // 2

# Radial background gradient simulation
for r in range(400, 0, -8):
    factor = r / 400.0
    # Blend from dark violet-indigo to deep slate
    cr = int(12 + (1.0 - factor) * 45)
    cg = int(16 + (1.0 - factor) * 35)
    cb = int(32 + (1.0 - factor) * 85)
    p_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(cr, cg, cb, 255))

# Outer glowing rings (safe inside circular 800x800 crop)
p_draw.ellipse([cx - 350, cy - 350, cx + 350, cy + 350], outline=(40, 50, 80, 180), width=4)
p_draw.ellipse([cx - 330, cy - 330, cx + 330, cy + 330], outline=(34, 211, 238, 240), width=6)

# Modern Tech Nodes on the circle
for angle in [30, 90, 150, 210, 270, 330]:
    rad = math.radians(angle)
    nx = cx + int(330 * math.cos(rad))
    ny = cy + int(330 * math.sin(rad))
    p_draw.ellipse([nx - 14, ny - 14, nx + 14, ny + 14], fill=(168, 85, 247, 255), outline=(34, 211, 238, 255), width=3)

# Hexagon / Shield Center Element
hex_r = 210
hex_points = []
for i in range(6):
    angle = math.radians(60 * i - 30)
    hex_points.append((cx + int(hex_r * math.cos(angle)), cy + int(hex_r * math.sin(angle))))

p_draw.polygon(hex_points, fill=(18, 24, 46, 255), outline=(34, 211, 238, 255))

# Circuit tracks into center
for pt in hex_points:
    p_draw.line([pt[0], pt[1], cx, cy], fill=(45, 60, 100, 150), width=3)

# Central Emblem: Stylized "TS" with AI Sparkle
# Glow shadow for text
p_draw.text((cx - 105, cy - 115), "TS", font=font_huge, fill=(34, 211, 238, 80))
p_draw.text((cx - 100, cy - 110), "TS", font=font_huge, fill=(255, 255, 255, 255))

# AI Sparkle Icon top-right of TS
sx, sy = cx + 80, cy - 100
p_draw.line([sx - 24, sy, sx + 24, sy], fill=(34, 211, 238, 255), width=5)
p_draw.line([sx, sy - 24, sx, sy + 24], fill=(34, 211, 238, 255), width=5)
p_draw.line([sx - 12, sy - 12, sx + 12, sy + 12], fill=(168, 85, 247, 255), width=3)
p_draw.line([sx - 12, sy + 12, sx + 12, sy - 12], fill=(168, 85, 247, 255), width=3)

# Subtitle badge inside hexagon
p_draw.rounded_rectangle([cx - 130, cy + 50, cx + 130, cy + 96], radius=12, fill=(34, 211, 238, 230))
p_draw.text((cx - 108, cy + 56), "TECHSTACK", font=font_small, fill=(10, 14, 26, 255))

# Save Profile Picture
p_img.convert("RGB").save(profile_path, "PNG", quality=95)
print(f"[✓] Saved Profile Picture: {profile_path}")


# ==============================================================================
# 2. GENERATE CHANNEL BANNER (2560 x 1440)
# ==============================================================================
print("[+] Generating 2560x1440 YouTube Banner...")
b_w, b_h = 2560, 1440
b_img = Image.new("RGBA", (b_w, b_h), color=(8, 11, 20, 255))
b_draw = ImageDraw.Draw(b_img)

# Background Cyber Grid (visible across TV & Desktop)
for x in range(0, b_w, 80):
    b_draw.line([x, 0, x, b_h], fill=(18, 24, 40, 255), width=1)
for y in range(0, b_h, 80):
    b_draw.line([0, y, b_w, y], fill=(18, 24, 40, 255), width=1)

# Ambient Glows (TV & Large Screens)
b_draw.ellipse([b_w//2 - 900, b_h//2 - 400, b_w//2 + 900, b_h//2 + 400], fill=(20, 25, 55, 120))
b_draw.ellipse([b_w//2 - 600, b_h//2 - 250, b_w//2 + 600, b_h//2 + 250], fill=(30, 45, 90, 140))

# Safe Area definition (1235x338 in center)
# Center is x=1280, y=720
# Safe rect: x1 = 1280 - 618 = 662, x2 = 1280 + 618 = 1898
#            y1 = 720 - 169 = 551,  y2 = 720 + 169 = 889
safe_x1, safe_y1 = 662, 551
safe_x2, safe_y2 = 1898, 889

# Center Content Base Card (Safe for mobile, tablet, desktop)
b_draw.rounded_rectangle(
    [safe_x1 + 30, safe_y1 + 15, safe_x2 - 30, safe_y2 - 15],
    radius=24,
    fill=(15, 20, 36, 230),
    outline=(34, 211, 238, 160),
    width=3
)

# Subtle decorative circuit lines inside banner safe area
b_draw.line([safe_x1 + 70, safe_y1 + 170, safe_x1 + 220, safe_y1 + 170], fill=(34, 211, 238, 200), width=3)
b_draw.line([safe_x2 - 220, safe_y1 + 170, safe_x2 - 70, safe_y1 + 170], fill=(168, 85, 247, 200), width=3)

# Center Icon Badge
ic_cx = safe_x1 + 170
ic_cy = 720
b_draw.ellipse([ic_cx - 75, ic_cy - 75, ic_cx + 75, ic_cy + 75], fill=(24, 32, 60, 255), outline=(34, 211, 238, 255), width=4)
b_draw.text((ic_cx - 40, ic_cy - 38), "TS", font=font_large, fill=(255, 255, 255, 255))
b_draw.ellipse([ic_cx + 42, ic_cy - 48, ic_cx + 56, ic_cy - 34], fill=(168, 85, 247, 255))

# Text Content Coordinates (Left aligned next to icon)
tx = safe_x1 + 285

# Title
b_draw.text((tx, safe_y1 + 45), "TECHSTACK", font=font_large, fill=(255, 255, 255, 255))
b_draw.text((tx + 400, safe_y1 + 45), "AI", font=font_large, fill=(34, 211, 238, 255))

# Subtitle
b_draw.text((tx, safe_y1 + 125), "AI Tools · Smart Workflows · Developer Shortcuts", font=font_sub, fill=(203, 213, 225, 255))

# Badges (Value proposition & Upload cadence)
# Badge 1: Save 10+ Hours
b_draw.rounded_rectangle([tx, safe_y1 + 195, tx + 310, safe_y1 + 250], radius=14, fill=(6, 78, 59, 230), outline=(16, 185, 129, 255), width=2)
b_draw.text((tx + 22, safe_y1 + 207), "⚡ SAVE 10+ HRS / WEEK", font=font_tiny, fill=(52, 211, 153, 255))

# Badge 2: New Shorts Daily
b_draw.rounded_rectangle([tx + 330, safe_y1 + 195, tx + 620, safe_y1 + 250], radius=14, fill=(30, 25, 60, 230), outline=(168, 85, 247, 255), width=2)
b_draw.text((tx + 352, safe_y1 + 207), "🔥 DAILY 45s BREAKDOWNS", font=font_tiny, fill=(216, 180, 254, 255))

# Badge 3: Subscribe
b_draw.rounded_rectangle([tx + 640, safe_y1 + 195, tx + 880, safe_y1 + 250], radius=14, fill=(60, 15, 20, 230), outline=(239, 68, 68, 255), width=2)
b_draw.text((tx + 665, safe_y1 + 207), "▶ SUBSCRIBE NOW", font=font_tiny, fill=(252, 165, 165, 255))

# Save Banner
b_img.convert("RGB").save(banner_path, "PNG", quality=95)
print(f"[✓] Saved Channel Banner: {banner_path}")
