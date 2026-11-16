import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

def create_metallic_gold_logo():
    # 4x supersampling: 1200 x 400 -> 300 x 100
    W, H = 1200, 400
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    
    font_path = 'C:/Windows/Fonts/impact.ttf'
    font_main = ImageFont.truetype(font_path, 200)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 48)
    
    # 1. Drop shadow layer
    shadow_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.text((280, 100), "RIYO", font=font_main, fill=(0, 0, 0, 180))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(15))
    base = Image.alpha_composite(base, shadow_img)
    
    # 2. 3D Extrusion / Bevel depth (Draw dark gold offset copies)
    draw = ImageDraw.Draw(base)
    for offset in range(16, 0, -2):
        shade = int(120 + offset * 4)
        draw.text((270 + offset//2, 80 + offset), "RIYO", font=font_main, fill=(shade, int(shade*0.7), 20, 255))
        
    # 3. Gold Gradient Text
    mask = Image.new('L', (W, H), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.text((270, 80), "RIYO", font=font_main, fill=255)
    
    # Create rich gold vertical gradient
    gold_grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(80, 280):
        t = (y - 80) / 200.0
        # Gold palette: Pale cream -> Bright gold -> Deep amber
        if t < 0.35:
            r = int(255 - t * 40)
            g = int(245 - t * 60)
            b = int(200 - t * 180)
        elif t < 0.7:
            r = 255
            g = int(215 - (t - 0.35) * 80)
            b = 10
        else:
            r = int(255 - (t - 0.7) * 70)
            g = int(170 - (t - 0.7) * 90)
            b = 0
        gold_grad.paste((r, g, b, 255), [0, y, W, y+1])
        
    base.paste(gold_grad, (0, 0), mask)
    
    # 4. Metallic stroke / highlight outline
    draw = ImageDraw.Draw(base)
    draw.text((270, 80), "RIYO", font=font_main, fill=None, stroke_width=3, stroke_fill=(255, 255, 255, 220))
    
    # 5. Icon: 3D Faceted Golden Star / Crown on left
    cx, cy = 150, 175
    # Outer diamond
    draw.polygon([(cx, cy - 90), (cx + 70, cy), (cx, cy + 90), (cx - 70, cy)], fill=(218, 165, 32, 255), outline=(255, 255, 255, 240), width=4)
    # Facets for 3D look
    draw.polygon([(cx, cy - 90), (cx, cy), (cx - 70, cy)], fill=(255, 235, 120, 255))
    draw.polygon([(cx, cy - 90), (cx + 70, cy), (cx, cy)], fill=(240, 190, 40, 255))
    draw.polygon([(cx - 70, cy), (cx, cy), (cx, cy + 90)], fill=(180, 120, 10, 255))
    draw.polygon([(cx, cy), (cx + 70, cy), (cx, cy + 90)], fill=(210, 150, 20, 255))
    # Core sparkling star
    draw.polygon([(cx, cy - 40), (cx + 25, cy), (cx, cy + 40), (cx - 25, cy)], fill=(255, 255, 255, 250))
    
    # 6. Subtitle 'STUDIOS' with letter spacing
    sub_text = "A N I M A T I O N"
    draw.text((280, 275), sub_text, font=font_sub, fill=(255, 214, 10, 240))
    
    # Downscale for crispness
    final = base.resize((360, 120), Image.Resampling.LANCZOS)
    final.save(r'D:\Antigravity\Pro\logo_style_1_gold.png')
    print("Logo 1 (Gold Metallic) created!")

def create_neon_cyber_logo():
    W, H = 1200, 400
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    font_main = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 190)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 44)
    
    # Glow layer (Neon Cyan / Electric Blue)
    glow_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_img)
    gdraw.text((270, 75), "RIYO", font=font_main, fill=(0, 240, 255, 255))
    # Icon glow
    cx, cy = 140, 170
    gdraw.polygon([(cx, cy - 80), (cx + 65, cy), (cx, cy + 80), (cx - 65, cy)], fill=(0, 240, 255, 255))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(25))
    base = Image.alpha_composite(base, glow_img)
    
    # Second tighter magenta glow
    glow_img2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw2 = ImageDraw.Draw(glow_img2)
    gdraw2.text((270, 75), "RIYO", font=font_main, fill=(255, 0, 128, 200))
    glow_img2 = glow_img2.filter(ImageFilter.GaussianBlur(10))
    base = Image.alpha_composite(base, glow_img2)
    
    # Core sharp text in crisp white with cyan outline
    draw = ImageDraw.Draw(base)
    # Extrusion
    for d in range(8, 0, -2):
        draw.text((270 + d, 75 + d), "RIYO", font=font_main, fill=(10, 30, 60, 255))
        
    draw.text((270, 75), "RIYO", font=font_main, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 240, 255, 255))
    
    # Cyber Crest Icon
    draw.polygon([(cx, cy - 75), (cx + 60, cy), (cx, cy + 75), (cx - 60, cy)], fill=(15, 23, 42, 240), outline=(0, 240, 255, 255), width=6)
    draw.polygon([(cx, cy - 45), (cx + 35, cy), (cx, cy + 45), (cx - 35, cy)], fill=(255, 0, 128, 255))
    draw.polygon([(cx, cy - 20), (cx + 15, cy), (cx, cy + 20), (cx - 15, cy)], fill=(255, 255, 255, 255))
    
    # Subtitle
    draw.text((275, 270), "P R O D U C T I O N S", font=font_sub, fill=(0, 240, 255, 240))
    
    final = base.resize((360, 120), Image.Resampling.LANCZOS)
    final.save(r'D:\Antigravity\Pro\logo_style_2_cyber.png')
    print("Logo 2 (Cyber Neon) created!")

def create_roblox_cartoon_logo():
    # Style 3: 3D Glossy Cartoon / Roblox Style (Bright Orange/Yellow bubble with thick white rim)
    W, H = 1200, 400
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    font_main = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 210)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 52)
    
    draw = ImageDraw.Draw(base)
    
    # Drop shadow
    s_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_img)
    s_draw.text((270, 85), "RIYO", font=font_main, fill=(0, 0, 0, 160), stroke_width=20, stroke_fill=(0, 0, 0, 160))
    s_img = s_img.filter(ImageFilter.GaussianBlur(16))
    base = Image.alpha_composite(base, s_img)
    
    draw = ImageDraw.Draw(base)
    # Thick heavy black border for cartoon pop
    draw.text((260, 70), "RIYO", font=font_main, fill=(20, 20, 20, 255), stroke_width=24, stroke_fill=(10, 10, 10, 255))
    
    # Thick white outline
    draw.text((260, 70), "RIYO", font=font_main, fill=(255, 255, 255, 255), stroke_width=12, stroke_fill=(255, 255, 255, 255))
    
    # Rich Orange-to-Yellow Gradient fill
    mask = Image.new('L', (W, H), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.text((260, 70), "RIYO", font=font_main, fill=255)
    
    grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(70, 290):
        t = (y - 70) / 220.0
        # Warm sunset orange to bright sun yellow
        r = 255
        g = int(120 + t * 135)
        b = int(20 + t * 30)
        grad.paste((r, g, b, 255), [0, y, W, y+1])
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    # Specular gloss highlight on upper half
    gloss_mask = Image.new('L', (W, H), 0)
    gmdraw = ImageDraw.Draw(gloss_mask)
    gmdraw.text((260, 70), "RIYO", font=font_main, fill=140)
    # cut bottom half of gloss
    gmdraw.rectangle([0, 170, W, H], fill=0)
    gloss = Image.new('RGBA', (W, H), (255, 255, 255, 200))
    base.paste(gloss, (0, 0), gloss_mask)
    
    # Cartoon Mascot Icon: 3D Blocky Crown / Star
    cx, cy = 140, 175
    # Thick cartoon outline
    draw.ellipse([cx-75, cy-75, cx+75, cy+75], fill=(10, 10, 10, 255))
    draw.ellipse([cx-65, cy-65, cx+65, cy+65], fill=(255, 255, 255, 255))
    draw.ellipse([cx-55, cy-55, cx+55, cy+55], fill=(255, 180, 0, 255))
    # Star inside
    star = [
        (cx, cy - 40), (cx + 12, cy - 12), (cx + 40, cy - 12),
        (cx + 18, cy + 6), (cx + 26, cy + 35), (cx, cy + 18),
        (cx - 26, cy + 35), (cx - 18, cy + 6), (cx - 40, cy - 12),
        (cx - 12, cy - 12)
    ]
    draw.polygon(star, fill=(255, 255, 255, 255))
    
    # Subtext '3D' in cute pill badge
    draw.rounded_rectangle([720, 180, 840, 250], radius=20, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=6)
    draw.text((745, 185), "3D", font=font_sub, fill=(255, 80, 0, 255))
    
    final = base.resize((360, 120), Image.Resampling.LANCZOS)
    final.save(r'D:\Antigravity\Pro\logo_style_3_cartoon.png')
    print("Logo 3 (Roblox Cartoon) created!")

if __name__ == '__main__':
    create_metallic_gold_logo()
    create_neon_cyber_logo()
    create_roblox_cartoon_logo()
