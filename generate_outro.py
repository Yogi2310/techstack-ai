import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import wave

OUTRO_DIR = r"D:\Antigravity\Pro\outro_frames"
os.makedirs(OUTRO_DIR, exist_ok=True)

W, H = 720, 1280
FPS = 30
DURATION = 3.5
TOTAL_FRAMES = int(FPS * DURATION)

# Load master 3D transparent logo
logo_path = r"D:\Antigravity\Pro\riyo_3d_master_transparent.png"
master_logo = Image.open(logo_path).convert('RGBA')

# Fonts
font_title = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 56)
font_btn = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 38)
font_sub = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 30)

print(f"Generating {TOTAL_FRAMES} perfected outro frames...")

# Pre-generate glowing radial backdrop
bg_glow = Image.new('RGBA', (W, H), (11, 15, 25, 255))
glow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow_layer)
# Soft golden amber center glow
g_draw.ellipse([360 - 240, 360 - 240, 360 + 240, 360 + 240], fill=(255, 190, 30, 90))
g_draw.ellipse([360 - 140, 360 - 140, 360 + 140, 360 + 140], fill=(255, 230, 120, 140))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(60))
base_bg = Image.alpha_composite(bg_glow, glow_layer)

def draw_thumb_icon(draw, cx, cy, color):
    # Stylized thumb icon
    draw.rounded_rectangle([cx-14, cy-4, cx+14, cy+14], radius=4, fill=color)
    draw.rounded_rectangle([cx-14, cy-16, cx-2, cy-4], radius=3, fill=color)

def draw_share_icon(draw, cx, cy, color):
    # Stylized curved arrow
    pts = [(cx-10, cy+10), (cx+4, cy-2), (cx+4, cy+4), (cx+14, cy-6), (cx+4, cy-16), (cx+4, cy-10), (cx-10, cy+2)]
    draw.polygon(pts, fill=color)

def draw_bell_icon(draw, cx, cy, color):
    # Stylized bell
    draw.ellipse([cx-12, cy-12, cx+12, cy+10], fill=color)
    draw.rectangle([cx-14, cy+4, cx+14, cy+10], fill=color)
    draw.ellipse([cx-4, cy+10, cx+4, cy+14], fill=color)

for i in range(TOTAL_FRAMES):
    t = i / FPS
    frame = base_bg.copy()
    draw = ImageDraw.Draw(frame)
    
    # 1. Subtle gold particles
    for p_idx in range(30):
        px = (int(p_idx * 137.5 + t * 45)) % W
        py = (int(p_idx * 219.3 - t * 65)) % H
        p_alpha = int(140 + 70 * math.sin(t * 3.5 + p_idx))
        draw.ellipse([px-3, py-3, px+3, py+3], fill=(255, 220, 80, p_alpha))
        
    # 2. 3D Logo (smooth entrance & hover)
    if t < 0.6:
        scale_t = t / 0.6
        scale = 0.8 + 0.25 * math.sin(scale_t * math.pi * 0.5)
        logo_alpha = min(1.0, t / 0.35)
    else:
        scale = 1.0 + 0.02 * math.sin((t - 0.6) * 3)
        logo_alpha = 1.0
        
    target_w = int(360 * scale)
    target_h = int(target_w * master_logo.height / master_logo.width)
    curr_logo = master_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    if logo_alpha < 1.0:
        l_arr = np.array(curr_logo)
        l_arr[:, :, 3] = (l_arr[:, :, 3] * logo_alpha).astype(np.uint8)
        curr_logo = Image.fromarray(l_arr)
        
    logo_x = (W - target_w) // 2
    logo_y = 190 - (target_h - 280) // 2
    frame.paste(curr_logo, (logo_x, logo_y), curr_logo)
    
    # 3. Middle: LIKE & SHARE Cards (Pop in at t=0.7s)
    if t >= 0.6:
        pop_t = min(1.0, (t - 0.6) / 0.4)
        pop_scale = 1.0 + 0.08 * math.sin(pop_t * math.pi) if pop_t < 1.0 else 1.0
        
        # Like Pill
        like_w, like_h = int(220 * pop_scale), int(68 * pop_scale)
        lx = 120 - (like_w - 220) // 2
        ly = 580 - (like_h - 68) // 2
        draw.rounded_rectangle([lx, ly, lx + like_w, ly + like_h], radius=34, fill=(20, 28, 48, 240), outline=(255, 214, 10, 230), width=3)
        draw_thumb_icon(draw, lx + 45, ly + 34, (255, 214, 10, 255))
        draw.text((lx + 75, ly + 14), "LIKE", font=font_btn, fill=(255, 255, 255, 255))
        
        # Share Pill
        sx = 380 - (like_w - 220) // 2
        sy = 580 - (like_h - 68) // 2
        draw.rounded_rectangle([sx, sy, sx + like_w, sy + like_h], radius=34, fill=(20, 28, 48, 240), outline=(0, 240, 255, 230), width=3)
        draw_share_icon(draw, sx + 45, sy + 34, (0, 240, 255, 255))
        draw.text((sx + 70, sy + 14), "SHARE", font=font_btn, fill=(255, 255, 255, 255))
        
    # 4. Large Glowing SUBSCRIBE Button (Pops in at t=1.1s)
    if t >= 1.0:
        pulse = 1.0 + 0.03 * math.sin((t - 1.0) * 8)
        btn_w = int(480 * pulse)
        btn_h = int(88 * pulse)
        bx = (W - btn_w) // 2
        by = 680 - (btn_h - 88) // 2
        
        # Red neon shadow
        for s_off in range(12, 0, -3):
            draw.rounded_rectangle([bx - s_off, by - s_off, bx + btn_w + s_off, by + btn_h + s_off], radius=44, fill=(255, 0, 0, int(35 * (1 - s_off/12))))
            
        draw.rounded_rectangle([bx, by, bx + btn_w, by + btn_h], radius=44, fill=(235, 30, 35, 255), outline=(255, 255, 255, 250), width=4)
        draw_bell_icon(draw, bx + 65, by + 44, (255, 255, 255, 255))
        draw.text((bx + 105, by + 18), "SUBSCRIBE", font=font_title, fill=(255, 255, 255, 255))
        
    # 5. Bottom Call to Action Text
    if t >= 1.4:
        fade_cta = min(1.0, (t - 1.4) / 0.4)
        cta_alpha = int(255 * fade_cta)
        
        # Centered "FOR MORE CONTENT!"
        title_text = "FOR MORE CONTENT!"
        bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
        tw = bbox_t[2] - bbox_t[0]
        tx = (W - tw) // 2
        draw.text((tx + 2, 832), title_text, font=font_title, fill=(0, 0, 0, cta_alpha))
        draw.text((tx, 830), title_text, font=font_title, fill=(255, 214, 10, cta_alpha))
        
        # Subtitle
        sub_text = "New 3D Stories Every Week"
        bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
        sw = bbox_s[2] - bbox_s[0]
        sx = (W - sw) // 2
        draw.text((sx, 910), sub_text, font=font_sub, fill=(148, 163, 184, cta_alpha))

    out_frame_path = os.path.join(OUTRO_DIR, f"frame_{i:04d}.png")
    frame.save(out_frame_path)

print("All perfected outro frames generated!")
