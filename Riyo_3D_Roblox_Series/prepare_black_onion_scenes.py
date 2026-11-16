import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BRAIN_DIR = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"
SERIES_DIR = r"D:\Antigravity\Pro\Riyo_3D_Roblox_Series"
KEYFRAMES_DIR = os.path.join(SERIES_DIR, "scene_keyframes")
os.makedirs(KEYFRAMES_DIR, exist_ok=True)

# 1. Scene 1: Recap & Golden Dragon
s1_src = os.path.join(BRAIN_DIR, "eli_golden_dragon_storm_1794849299159.jpg")
s1_dst = os.path.join(KEYFRAMES_DIR, "scene1_golden_dragon_recap.jpg")
shutil.copyfile(s1_src, s1_dst)
print("[OK] Scene 1 ready:", s1_dst)

# 2. Scene 2: Colossal Carrot & Grandma Tank
s2_src = os.path.join(BRAIN_DIR, "colossal_carrot_town_square_1794849297128.jpg")
s2_dst = os.path.join(KEYFRAMES_DIR, "scene2_colossal_carrot_grandma.jpg")
shutil.copyfile(s2_src, s2_dst)
print("[OK] Scene 2 ready:", s2_dst)

# 3. Scene 3: Forbidden Black Onion Vault
s3_src = os.path.join(BRAIN_DIR, "forbidden_black_onion_vault_1794849349702.jpg")
s3_dst = os.path.join(KEYFRAMES_DIR, "scene3_black_onion_vault.jpg")
shutil.copyfile(s3_src, s3_dst)
print("[OK] Scene 3 ready:", s3_dst)

# 4. Scene 4: Launching Black Onion at Shadow Colossus
s4_src = os.path.join(BRAIN_DIR, "shadow_colossus_emerges_1794660974169.jpg")
s4_img = Image.open(s4_src).convert("RGBA")

# Draw glowing purple projectile trail towards the Colossus chest
overlay = Image.new("RGBA", s4_img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Target chest area around (384, 550), launch from bottom right (650, 1150)
start_pt = (620, 1150)
end_pt = (384, 580)

# Draw purple hypersonic trail
for w, alpha in [(30, 40), (20, 80), (12, 140), (6, 220), (2, 255)]:
    draw.line([start_pt, end_pt], fill=(168, 85, 247, alpha), width=w)

# Core glowing projectile at end_pt
for r, alpha in [(50, 30), (35, 70), (20, 150), (10, 240)]:
    draw.ellipse([end_pt[0]-r, end_pt[1]-r, end_pt[0]+r, end_pt[1]+r], fill=(216, 180, 254, alpha))

s4_final = Image.alpha_composite(s4_img, overlay).convert("RGB")
s4_dst = os.path.join(KEYFRAMES_DIR, "scene4_water_tower_hypersonic_throw.jpg")
s4_final.save(s4_dst, quality=95)
print("[OK] Scene 4 ready:", s4_dst)

# 5. Scene 5: Tamed Colossus with Sector 9 Plaque
# Base from scene 1 or scene 4 with warm sunset tone and Sector 9 HUD
s5_img = Image.open(s1_src).convert("RGBA")
overlay5 = Image.new("RGBA", s5_img.size, (0, 0, 0, 0))
draw5 = ImageDraw.Draw(overlay5)

# Cinematic lower third plaque box
w, h = s5_img.size
box_top = int(h * 0.72)
box_bottom = int(h * 0.88)
box_left = int(w * 0.08)
box_right = int(w * 0.92)

# Titanium border & dark tinted glass
draw5.rounded_rectangle([box_left, box_top, box_right, box_bottom], radius=16, fill=(10, 15, 25, 220), outline=(0, 242, 254, 240), width=3)

# Glowing cyan accent dots
draw5.ellipse([box_left + 15, box_top + 15, box_left + 25, box_top + 25], fill=(0, 242, 254, 255))
draw5.ellipse([box_right - 25, box_top + 15, box_right - 15, box_top + 25], fill=(239, 68, 68, 255))

# Text
try:
    font_lg = ImageFont.truetype("arialbd.ttf", 34)
    font_sm = ImageFont.truetype("arialbd.ttf", 24)
except:
    font_lg = ImageFont.load_default()
    font_sm = ImageFont.load_default()

draw5.text((w/2, box_top + 35), "PROPERTY OF SECTOR 9", fill=(0, 242, 254, 255), font=font_lg, anchor="mm")
draw5.text((w/2, box_top + 80), "⚠️ CLASSIFIED TITAN: DO NOT RELEASE ⚠️", fill=(255, 214, 10, 255), font=font_sm, anchor="mm")
draw5.text((w/2, box_top + 120), "STATUS: TAMED BY ELI (LEVEL 999)", fill=(52, 211, 153, 255), font=font_sm, anchor="mm")

s5_final = Image.alpha_composite(s5_img, overlay5).convert("RGB")
s5_dst = os.path.join(KEYFRAMES_DIR, "scene5_tamed_titan_sector9.jpg")
s5_final.save(s5_dst, quality=95)
print("[OK] Scene 5 ready:", s5_dst)

print("\n✨ ALL 5 SCENE KEYFRAMES ASSEMBLED IN:", KEYFRAMES_DIR)
