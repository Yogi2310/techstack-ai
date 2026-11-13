import os
import sys
import math

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter

out_dir = r"D:\Antigravity\Pro"
avatar_path = os.path.join(out_dir, "profile_pic_stickman_3d.png")
banner_path = os.path.join(out_dir, "channel_banner.png")

# Fonts
font_huge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 96)
font_large = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 72)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 34)
font_tiny = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)

b_w, b_h = 2560, 1440
b_img = Image.new("RGBA", (b_w, b_h), color=(8, 11, 20, 255))
b_draw = ImageDraw.Draw(b_img)

# Background Cyber Grid (TV & Large Displays)
for x in range(0, b_w, 80):
    b_draw.line([x, 0, x, b_h], fill=(18, 24, 40, 255), width=1)
for y in range(0, b_h, 80):
    b_draw.line([0, y, b_w, y], fill=(18, 24, 40, 255), width=1)

# Ambient Radial Glows
b_draw.ellipse([b_w//2 - 900, b_h//2 - 400, b_w//2 + 900, b_h//2 + 400], fill=(20, 25, 55, 120))
b_draw.ellipse([b_w//2 - 600, b_h//2 - 250, b_w//2 + 600, b_h//2 + 250], fill=(30, 45, 90, 140))

# Safe Area definition (1235x338 in center)
safe_x1, safe_y1 = 662, 551
safe_x2, safe_y2 = 1898, 889

# Center Content Base Card (Safe for mobile, tablet, desktop)
b_draw.rounded_rectangle(
    [safe_x1 + 25, safe_y1 + 15, safe_x2 - 25, safe_y2 - 15],
    radius=26,
    fill=(15, 20, 36, 235),
    outline=(34, 211, 238, 180),
    width=3
)

# Insert Circular 3D Stickman Avatar on Left of Banner Safe Area
if os.path.exists(avatar_path):
    raw_av = Image.open(avatar_path).convert("RGBA")
    av_size = 250
    av_resized = raw_av.resize((av_size, av_size), Image.Resampling.LANCZOS)
    
    # Circular mask
    av_mask = Image.new("L", (av_size, av_size), 0)
    m_draw = ImageDraw.Draw(av_mask)
    m_draw.ellipse([0, 0, av_size, av_size], fill=255)
    
    av_x = safe_x1 + 65
    av_y = safe_y1 + (338 - av_size) // 2
    
    # Glowing ring behind avatar
    b_draw.ellipse([av_x - 6, av_y - 6, av_x + av_size + 6, av_y + av_size + 6], outline=(34, 211, 238, 255), width=5)
    b_draw.ellipse([av_x - 12, av_y - 12, av_x + av_size + 12, av_y + av_size + 12], outline=(168, 85, 247, 120), width=3)
    
    # Paste avatar
    b_img.paste(av_resized, (av_x, av_y), av_mask)

# Text Content Coordinates (Next to the avatar)
tx = safe_x1 + 355

# Title
b_draw.text((tx, safe_y1 + 45), "TECHSTACK", font=font_large, fill=(255, 255, 255, 255))
b_draw.text((tx + 430, safe_y1 + 45), "AI", font=font_large, fill=(34, 211, 238, 255))

# Subtitle
b_draw.text((tx, safe_y1 + 128), "AI Tools · Smart Workflows · Developer Shortcuts", font=font_sub, fill=(203, 213, 225, 255))

# Badges (Value proposition & Upload cadence)
# Badge 1: Save 10+ Hours
b_draw.rounded_rectangle([tx, safe_y1 + 195, tx + 295, safe_y1 + 250], radius=14, fill=(6, 78, 59, 230), outline=(16, 185, 129, 255), width=2)
b_draw.text((tx + 18, safe_y1 + 207), "⚡ SAVE 10+ HRS / WEEK", font=font_tiny, fill=(52, 211, 153, 255))

# Badge 2: New Shorts Daily
b_draw.rounded_rectangle([tx + 315, safe_y1 + 195, tx + 605, safe_y1 + 250], radius=14, fill=(30, 25, 60, 230), outline=(168, 85, 247, 255), width=2)
b_draw.text((tx + 338, safe_y1 + 207), "🔥 DAILY 45s BREAKDOWNS", font=font_tiny, fill=(216, 180, 254, 255))

# Badge 3: Subscribe
b_draw.rounded_rectangle([tx + 625, safe_y1 + 195, tx + 855, safe_y1 + 250], radius=14, fill=(60, 15, 20, 230), outline=(239, 68, 68, 255), width=2)
b_draw.text((tx + 648, safe_y1 + 207), "▶ SUBSCRIBE NOW", font=font_tiny, fill=(252, 165, 165, 255))

# Save Banner
b_img.convert("RGB").save(banner_path, "PNG", quality=95)
print(f"[✓] Saved Upgraded Channel Banner: {banner_path}")
