import os
import sys
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

proj_dir = r"D:\Antigravity\Pro\CuteBaby_Comedy_Shorts"
baby_img_path = os.path.join(proj_dir, "characters", "cute_ai_baby_golgappa.jpg")
master_audio_wav = os.path.join(proj_dir, "audio", "demo_video_master_audio.wav")
output_mp4 = os.path.join(proj_dir, "videos", "demo_cute_baby_comedy_short.mp4")

WIDTH = 720
HEIGHT = 1280
FPS = 24
TOTAL_DURATION = 28.0
TOTAL_FRAMES = int(math.ceil(TOTAL_DURATION * FPS))

# Load character image
raw_baby = Image.open(baby_img_path).convert("RGBA")

# Fonts
font_huge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 44)
font_big = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)
font_sub_hi = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 36)
font_sub_en = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
font_comic_sfx = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)

# Scenes mapping relative to overall 28s timeline
# Voice starts at 2.5s
scenes = [
    {
        "id": "intro",
        "start": 0.0,
        "end": 2.5,
        "type": "intro_card"
    },
    {
        "id": "scene_1",
        "start": 2.5,
        "end": 7.09,
        "headline": "GOLGAPPE KA LALACH 🤤",
        "sub_hi": "भैया! एक प्लेट गोलगप्पे लगाओ... तीखा कम!",
        "sub_en": "Bhaiya! 1 Plate Golgappe... Less Spicy!",
        "effect": "zoom_in",
        "accent": "#F59E0B",
        "badge": "SCENE 1: THE ORDER"
    },
    {
        "id": "scene_2",
        "start": 7.09,
        "end": 12.00,
        "headline": "WAH! ITNA TASTY! 😋",
        "sub_hi": "वाह! इतना टेस्टी! मज़ा आ गया!",
        "sub_en": "Mmm! So Tasty! Give 3 More!",
        "effect": "bounce",
        "accent": "#10B981",
        "badge": "SCENE 2: PURE DELIGHT",
        "sfx_text": "*CRUNCH!*"
    },
    {
        "id": "scene_3",
        "start": 12.00,
        "end": 17.75,
        "headline": "BOHOT TEEKHA HAI! 🌶️🔥",
        "sub_hi": "अरे बाप रे! बहुत तीखा है! धुआं निकल गया!",
        "sub_en": "Too Spicy!! Ears On Fire! Sweet Water Fast!",
        "effect": "shake_fire",
        "accent": "#EF4444",
        "badge": "SCENE 3: SPICY SHOCK 🔥",
        "sfx_text": "*SMOKE & FIRE!*"
    },
    {
        "id": "scene_4",
        "start": 17.75,
        "end": 22.72,
        "headline": "NO COMPROMISE! 🤣😂",
        "sub_hi": "पर टेस्टी बहुत था! एक प्लेट और मेरे लिए!",
        "sub_en": "Still So Tasty! Pack 1 More For Me!",
        "effect": "triumph",
        "accent": "#8B5CF6",
        "badge": "SCENE 4: GREEDY TWIST",
        "sfx_text": "*MORE GOLGAPPE!*"
    },
    {
        "id": "scene_5",
        "start": 22.72,
        "end": 25.44,
        "headline": "LIKE & SUBSCRIBE ❤️🔔",
        "sub_hi": "लाइक और सब्सक्राइब करो!",
        "sub_en": "Like & Subscribe for Daily Shorts!",
        "effect": "pulse_cta",
        "accent": "#EC4899",
        "badge": "SCENE 5: VIRAL CTA"
    },
    {
        "id": "outro",
        "start": 25.44,
        "end": 28.0,
        "type": "outro_card"
    }
]

print(f"[+] Starting Demo Video Render ({TOTAL_DURATION}s, {TOTAL_FRAMES} frames)...")

ffmpeg_cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", master_audio_wav,
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_mp4
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / float(FPS)
    
    # Determine current scene
    cur_sc = scenes[-1]
    for sc in scenes:
        if sc["start"] <= t < sc["end"]:
            cur_sc = sc
            break
            
    sc_dur = cur_sc["end"] - cur_sc["start"]
    rel_t = t - cur_sc["start"]
    prog = rel_t / sc_dur if sc_dur > 0 else 0.0

    img = Image.new("RGBA", (WIDTH, HEIGHT), color=(15, 10, 25, 255))
    draw = ImageDraw.Draw(img)

    # A. INTRO CARD
    if cur_sc.get("type") == "intro_card":
        # Radial background gradient pulses
        pulse_r = int(math.sin(prog * math.pi) * 40)
        draw.ellipse([WIDTH//2 - 300 - pulse_r, HEIGHT//2 - 300 - pulse_r, WIDTH//2 + 300 + pulse_r, HEIGHT//2 + 300 + pulse_r], fill=(245, 158, 11, 40))
        draw.ellipse([WIDTH//2 - 180, HEIGHT//2 - 180, WIDTH//2 + 180, HEIGHT//2 + 180], fill=(236, 72, 153, 50))
        
        # Center Intro Box
        draw.rounded_rectangle([50, 360, WIDTH - 50, 920], radius=32, fill=(28, 18, 44, 250), outline="#F59E0B", width=6)
        
        # DEMO BADGE
        draw.rounded_rectangle([WIDTH//2 - 190, 410, WIDTH//2 + 190, 470], radius=16, fill=(245, 158, 11, 230))
        draw.text((WIDTH//2 - 165, 425), "🎬 3D AI COMEDY DEMO", font=font_sub_en, fill=(20, 10, 5, 255))
        
        # Title
        draw.text((WIDTH//2 - 270, 520), "GOLGAPPE KA LALACH", font=font_huge, fill="white")
        draw.text((WIDTH//2 - 240, 580), "🤣 Cute Baby Comedy 😂", font=font_big, fill="#FBBF24")
        
        # Subtitle Formula
        draw.rounded_rectangle([80, 680, WIDTH - 80, 780], radius=20, fill=(40, 25, 60, 240), outline="#EC4899", width=2)
        draw.text((105, 700), "⭐ Formula: 7M+ Views Reference", font=font_sub_en, fill="#38BDF8")
        draw.text((105, 735), "⭐ 3D Pixar + Hindi Voice + BGM & SFX", font=font_tag, fill="white")
        
        # Countdown
        countdown_num = str(max(1, int(3.5 - prog * 3.0)))
        draw.ellipse([WIDTH//2 - 45, 810, WIDTH//2 + 45, 900], fill=(220, 38, 38, 240), outline="white", width=3)
        draw.text((WIDTH//2 - 14, 830), countdown_num, font=font_huge, fill="white")

    # B. OUTRO CARD
    elif cur_sc.get("type") == "outro_card":
        draw.ellipse([WIDTH//2 - 320, HEIGHT//2 - 320, WIDTH//2 + 320, HEIGHT//2 + 320], fill=(16, 185, 129, 60))
        
        # Center Outro Box
        draw.rounded_rectangle([50, 360, WIDTH - 50, 920], radius=32, fill=(28, 18, 44, 250), outline="#10B981", width=6)
        
        # BADGE
        draw.rounded_rectangle([WIDTH//2 - 180, 420, WIDTH//2 + 180, 480], radius=16, fill=(16, 185, 129, 230))
        draw.text((WIDTH//2 - 145, 435), "🎉 DEMO COMPLETE", font=font_sub_en, fill="white")
        
        # Text
        draw.text((WIDTH//2 - 260, 530), "READY FOR YOUTUBE!", font=font_huge, fill="#FBBF24")
        draw.text((WIDTH//2 - 240, 600), "1-Click Automatic Upload", font=font_big, fill="white")
        
        draw.rounded_rectangle([80, 710, WIDTH - 80, 850], radius=20, fill=(35, 20, 50, 240), outline="#8B5CF6", width=2)
        draw.text((110, 735), "▶ Full 9:16 Shorts Resolution", font=font_sub_en, fill="#38BDF8")
        draw.text((110, 775), "▶ Pitch-Shifted Hindi Baby Voice", font=font_sub_en, fill="#EC4899")
        draw.text((110, 815), "▶ High-Retention Comedy Formula", font=font_sub_en, fill="#10B981")

    # C. STORY SCENES (1 to 5)
    else:
        effect = cur_sc["effect"]
        accent = cur_sc["accent"]

        # Camera Zoom & Shake
        if effect == "zoom_in":
            zoom = 1.0 + prog * 0.15
            shake_x, shake_y = 0, 0
        elif effect == "shake_fire":
            zoom = 1.15 + math.sin(rel_t * 18.0) * 0.04
            shake_x = int(math.sin(rel_t * 30.0) * 12)
            shake_y = int(math.cos(rel_t * 25.0) * 8)
        elif effect == "bounce":
            zoom = 1.05 + abs(math.sin(rel_t * 8.0)) * 0.06
            shake_x, shake_y = 0, int(math.sin(rel_t * 8.0) * -8)
        elif effect == "triumph":
            zoom = 1.1 + math.sin(rel_t * 5.0) * 0.05
            shake_x, shake_y = 0, 0
        else: # pulse_cta
            zoom = 1.0 + math.sin(rel_t * 4.0) * 0.04
            shake_x, shake_y = 0, 0

        # Character glow
        if effect == "shake_fire":
            draw.ellipse([WIDTH//2 - 320, 200, WIDTH//2 + 320, 800], fill=(220, 38, 38, 140))
            draw.ellipse([WIDTH//2 - 200, 300, WIDTH//2 + 200, 700], fill=(245, 158, 11, 100))
        else:
            draw.ellipse([WIDTH//2 - 320, 200, WIDTH//2 + 320, 800], fill=(245, 158, 11, 110))
            draw.ellipse([WIDTH//2 - 200, 300, WIDTH//2 + 200, 700], fill=(236, 72, 153, 50))

        # 3D Baby Image Crop & Placement
        crop_w = 640
        crop_h = 640
        curr_w = int(660 * zoom)
        curr_h = int(660 * zoom)
        scaled_baby = raw_baby.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
        cropped_baby = ImageOps.fit(scaled_baby, (crop_w, crop_h), method=Image.Resampling.LANCZOS)

        # Border & Image
        draw.rounded_rectangle([36 + shake_x, 166 + shake_y, 684 + shake_x, 814 + shake_y], radius=32, fill=(24, 18, 38, 255), outline=accent, width=6)
        mask_b = Image.new("L", (crop_w, crop_h), 0)
        ImageDraw.Draw(mask_b).rounded_rectangle([0, 0, crop_w, crop_h], radius=26, fill=255)
        img.paste(cropped_baby, (40 + shake_x, 170 + shake_y), mask_b)

        # Steam Puffs in Spicy Scene
        if effect == "shake_fire":
            steam_y = 140 + int(math.sin(rel_t * 12.0) * 10)
            draw.ellipse([110, steam_y, 170, steam_y + 40], fill=(255, 255, 255, 210))
            draw.ellipse([WIDTH - 170, steam_y, WIDTH - 110, steam_y + 40], fill=(255, 255, 255, 210))

        # Comic SFX Text Bubble if present
        if "sfx_text" in cur_sc and (rel_t < 1.4):
            bubble_scale = math.sin(min(1.0, rel_t / 1.4) * math.pi)
            if bubble_scale > 0.1:
                bx = WIDTH // 2 + 100
                by = 220
                draw.rounded_rectangle([bx - 120, by - 35, bx + 120, by + 35], radius=16, fill=(239, 68, 68, 240), outline="white", width=3)
                draw.text((bx - 105, by - 22), cur_sc["sfx_text"], font=font_sub_en, fill="white")

        # Top Scene Badge
        draw.rounded_rectangle([40, 35, 680, 95], radius=18, fill=(30, 18, 45, 240), outline=accent, width=3)
        draw.text((60, 48), cur_sc["badge"], font=font_sub_en, fill=accent)
        draw.text((450, 50), "DEMO SHOWCASE", font=font_tag, fill="white")

        # Headline
        draw.rounded_rectangle([40, 105, 680, 155], radius=14, fill=(40, 25, 55, 220))
        draw.text((60, 115), cur_sc["headline"], font=font_big, fill="white")

        # Big Subtitles Box
        sub_y = 855
        draw.rounded_rectangle([30, sub_y, WIDTH - 30, sub_y + 245], radius=28, fill=(20, 12, 32, 250), outline=accent, width=4)
        
        # Hindi Punchline
        hi_text = cur_sc["sub_hi"]
        draw.text((52, sub_y + 25), hi_text, font=font_sub_hi, fill=(20, 10, 5, 255))
        draw.text((50, sub_y + 23), hi_text, font=font_sub_hi, fill="#FBBF24")
        
        # English Subtitle
        en_text = cur_sc["sub_en"]
        draw.text((50, sub_y + 105), en_text, font=font_sub_en, fill="#38BDF8")

        # Emoji Ribbon
        emojis_str = "🤣 😂 🤤 🌶️ 🥟 👶 ❤️"
        draw.text((50, sub_y + 165), emojis_str, font=font_tag, fill="white")

        # Subscribe Banner
        draw.rounded_rectangle([40, 1135, WIDTH - 40, 1225], radius=18, fill=(220, 38, 38, 240), outline="#FBBF24", width=3)
        draw.text((70, 1155), "▶ SUBSCRIBE FOR DAILY FUNNY SHORTS!", font=font_big, fill="white")

    # Bottom Progress Bar across entire 28s video
    prog_pct = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 12, int(WIDTH * prog_pct), HEIGHT], fill="#F59E0B")

    rgb_img = img.convert("RGB")
    proc.stdin.write(rgb_img.tobytes())

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"🎉 DEMO VIDEO RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Total Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames)")
print("="*60)
