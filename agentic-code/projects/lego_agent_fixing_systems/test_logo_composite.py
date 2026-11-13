import os
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size):
    try:
        path = os.path.join("C:/Windows/Fonts", name)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_brand = get_font("arialbd.ttf", 26)

def make_circular_logo(img, size, border_color=(0, 220, 255), border_width=3):
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([0, 0, size - 1, size - 1], fill=255)
    
    circ = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circ.paste(img, (0, 0), mask=mask)
    
    draw_circ = ImageDraw.Draw(circ)
    draw_circ.ellipse([border_width//2, border_width//2, size - 1 - border_width//2, size - 1 - border_width//2], outline=border_color, width=border_width)
    return circ

logo_path = r"D:\Antigravity\Pro\channel_profile_pic.png"
logo_raw = Image.open(logo_path).convert("RGBA")

# Load our preview frame
frame_path = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\snapshots\test_clear_preview.png"
im = Image.open(frame_path).convert("RGBA")

# 1. Place small logo inside top-left brand card
logo_header = make_circular_logo(logo_raw, 54, border_color=(0, 240, 255), border_width=2)
# Draw updated top-left card
draw = ImageDraw.Draw(im)
draw.rounded_rectangle([35, 20, 420, 85], radius=16, fill=(12, 18, 30, 245), outline=(0, 220, 255), width=3)
im.paste(logo_header, (48, 25), mask=logo_header)
draw.text((116, 38), "LEGO AI AGENT", font=font_brand, fill=(255, 255, 255))

# 2. Top-Right Watermark Card
logo_wm = make_circular_logo(logo_raw, 56, border_color=(0, 240, 255), border_width=2)
wm_x, wm_y = 1180, 22
draw.rounded_rectangle([wm_x - 10, wm_y - 2, wm_x + 66, wm_y + 60], radius=16, fill=(10, 16, 26, 220), outline=(0, 220, 255, 180), width=2)
im.paste(logo_wm, (wm_x, wm_y), mask=logo_wm)

out_test = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\snapshots\test_logo_preview.png"
im.convert('RGB').save(out_test)
print("Saved test logo composite to:", out_test)
