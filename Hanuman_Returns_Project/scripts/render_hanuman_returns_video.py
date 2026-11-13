import os
import sys
import math
import random
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

proj_dir = r"D:\Antigravity\Pro\Hanuman_Returns_Project"
hero_img_p = os.path.join(proj_dir, "characters", "hanuman_hero_majestic.jpg")
awaken_img_p = os.path.join(proj_dir, "characters", "hanuman_awakening_himalayas.jpg")
audio_path = os.path.join(proj_dir, "audio", "hanuman_returns_master_audio.wav")
output_mp4 = os.path.join(proj_dir, "videos", "hanuman_returns_cinematic_short.mp4")

WIDTH = 720
HEIGHT = 1280
FPS = 24
TOTAL_DURATION = 25.5
TOTAL_FRAMES = int(math.ceil(TOTAL_DURATION * FPS))

# Load high-res 9:16 character images
raw_hero = Image.open(hero_img_p).convert("RGBA")
raw_awaken = Image.open(awaken_img_p).convert("RGBA")

# Fonts
font_huge = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 48)
font_title = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 40)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 32)
font_en = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
font_shloka = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 28)

captions = [
    {
        "start": 0.0,
        "end": 5.0,
        "hi": "कलयुग में जब अधर्म और पाप बढ़ा...",
        "en": "When darkness & adharma peaked in Kalyug...",
        "badge": "⚡ कलयुग का अंधकार ⚡"
    },
    {
        "start": 5.0,
        "end": 10.5,
        "hi": "हिमालय से गूंजा महा-शंखनाद... जागे पवनपुत्र!",
        "en": "From the Himalayas, the sacred conch resonated... Hanuman Awakens!",
        "badge": "🚩 दिव्य शंखनाद 🚩"
    },
    {
        "start": 10.5,
        "end": 15.5,
        "hi": "हाथ में वज्र गदा, आंखों में सूर्य का तेज!",
        "en": "Mighty celestial mace, radiance of the sun, and Lord Ram in his heart!",
        "badge": "✨ चिरंजीवी महावीर ✨"
    },
    {
        "start": 15.5,
        "end": 20.8,
        "hi": "एक ही हुंकार से कांप उठी धरती... संकटमोचन लौटे!",
        "en": "Earth trembled at his roar... The Destroyer of Evils has returned!",
        "badge": "🔥 अधर्म का संहार 🔥"
    },
    {
        "start": 20.8,
        "end": 25.5,
        "hi": "कमेंट में 'जय श्री राम' और 'जय बजरंगबली' लिखें! 🚩",
        "en": "Comment 'Jai Shri Ram' & 'Jai Bajrangbali' below! ❤️",
        "badge": "🚩 जय श्री राम | ॐ हनुमते नमः 🚩"
    }
]

# Random golden embers
random.seed(108)
embers = []
for i in range(40):
    embers.append({
        "x": random.uniform(50, WIDTH - 50),
        "y": random.uniform(100, HEIGHT - 100),
        "vx": random.uniform(-15, 15),
        "vy": random.uniform(-60, -180),
        "size": random.randint(2, 6),
        "phase": random.uniform(0, math.pi * 2)
    })

print(f"[+] Rendering Hanuman Returns Cinematic Short ({TOTAL_DURATION}s, {TOTAL_FRAMES} frames)...")

ffmpeg_cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", audio_path,
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_mp4
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

def draw_outlined_text(draw, pos, text, font, fill_color="yellow", stroke_color="black", stroke_width=4):
    x, y = pos
    draw.text((x, y), text, font=font, fill=fill_color, stroke_fill=stroke_color, stroke_width=stroke_width)

for f in range(TOTAL_FRAMES):
    t = f / float(FPS)
    
    cur_cap = captions[-1]
    for cap in captions:
        if cap["start"] <= t < cap["end"]:
            cur_cap = cap
            break

    # =========================================================================
    # VISUAL COMPOSITING & CINEMATIC CAMERA
    # =========================================================================
    # Scene 1 & 2: Awakening in the Himalayas (0.0s - 10.5s)
    # Scene 3 & 4: Hero Majestic Warrior Avatar (10.5s - 20.8s)
    # Scene 5: Sacred Devotion Card (20.8s - 25.5s)

    if t < 10.5:
        # Camera zoom on Awakening image
        prog = t / 10.5
        zoom = 1.0 + prog * 0.12
        cur_w = int(WIDTH * zoom)
        cur_h = int(HEIGHT * zoom)
        
        # Pan subtly upward
        pan_y = int(prog * 60)
        img_scaled = raw_awaken.resize((cur_w, cur_h), Image.Resampling.LANCZOS)
        
        crop_x = (cur_w - WIDTH) // 2
        crop_y = (cur_h - HEIGHT) // 2 + pan_y
        crop_y = max(0, min(cur_h - HEIGHT, crop_y))
        
        canvas = img_scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

        # Lightning flash at t=0.2s - 0.6s and t=4.6s - 5.0s
        is_flash = (0.2 <= t <= 0.45) or (4.6 <= t <= 4.85)
        if is_flash:
            flash_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 120))
            canvas = Image.alpha_composite(canvas, flash_overlay)

    elif 10.5 <= t < 20.8:
        # Hero Majestic Hanuman Image
        prog = (t - 10.5) / 10.3
        # Majestic upward tilt / zoom
        zoom = 1.08 - prog * 0.05
        cur_w = int(WIDTH * zoom)
        cur_h = int(HEIGHT * zoom)
        
        # Tilt from torso up to face & gada
        pan_y = int((1.0 - prog) * 50)
        img_scaled = raw_hero.resize((cur_w, cur_h), Image.Resampling.LANCZOS)
        
        crop_x = (cur_w - WIDTH) // 2
        crop_y = (cur_h - HEIGHT) // 2 + pan_y
        crop_y = max(0, min(cur_h - HEIGHT, crop_y))
        
        canvas = img_scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

        # Cosmic Thunder Shock at t=15.2s - 16.0s (Screen shake)
        if 15.2 <= t <= 16.2:
            shake_prog = (t - 15.2) / 1.0
            shake_amp = math.sin(shake_prog * 40.0) * 12 * (1.0 - shake_prog)
            dx = int(shake_amp)
            dy = int(shake_amp * 0.5)
            shifted = Image.new("RGBA", (WIDTH, HEIGHT), (10, 5, 2, 255))
            shifted.paste(canvas, (dx, dy))
            canvas = shifted

    else:
        # Scene 5: Sacred Golden Temple Glow Outro
        prog = (t - 20.8) / 4.7
        # Blend Hero image with deep golden celestial glow
        canvas = raw_hero.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        golden_filter = Image.new("RGBA", (WIDTH, HEIGHT), (245, 158, 11, int(90 + math.sin(prog * 6.0) * 30)))
        canvas = Image.alpha_composite(canvas, golden_filter)

    draw = ImageDraw.Draw(canvas)

    # 2. FLOATING SACRED GOLDEN EMBERS & LIGHTNING PARTICLES
    for emb in embers:
        # Update y position with wrapping
        ey = (emb["y"] + emb["vy"] * t) % HEIGHT
        ex = emb["x"] + math.sin(t * 3.0 + emb["phase"]) * 20
        # Glistening flicker
        alpha = int(180 + math.sin(t * 12.0 + emb["phase"]) * 75)
        r = emb["size"]
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 220, 100, alpha))
        draw.ellipse([ex - r//2, ey - r//2, ex + r//2, ey + r//2], fill=(255, 255, 255, alpha))

    # 3. SACRED TOP BANNER (SANATAN / DEVOTIONAL AESTHETIC)
    draw.rounded_rectangle([25, 35, WIDTH - 25, 110], radius=18, fill=(20, 10, 5, 240), outline="#F59E0B", width=3)
    draw_outlined_text(draw, (45, 48), cur_cap["badge"], font=font_title, fill_color="#FBBF24", stroke_color="#78350F", stroke_width=4)
    draw.text((WIDTH - 190, 58), "DIVINE SHORTS", font=font_en, fill="#FCD34D")

    # 4. LOWER THIRD CINEMATIC SUBTITLES (DEVOTIONAL GOLD & SAFFRON)
    sub_y = 940
    # Rich royal dark crimson / gold bordered subtitle card
    draw.rounded_rectangle([20, sub_y, WIDTH - 20, sub_y + 200], radius=24, fill=(18, 8, 4, 250), outline="#F59E0B", width=4)
    
    # Hindi Sacred Punchline (Large bold glowing saffron with shadow)
    hi_text = cur_cap["hi"]
    draw_outlined_text(draw, (40, sub_y + 22), hi_text, font=font_huge, fill_color="#FBBF24", stroke_color="#78350F", stroke_width=5)
    
    # English Subtitle
    en_text = cur_cap["en"]
    draw_outlined_text(draw, (40, sub_y + 95), en_text, font=font_en, fill_color="#FEF08A", stroke_color="black", stroke_width=3)

    # Sacred Chanting Ribbon on lower card
    if t < 20.8:
        draw.text((40, sub_y + 145), "🚩 ॐ हं हनुमते रुद्रात्मकाय हुं फट् 🚩", font=font_shloka, fill="#F97316")
    else:
        draw.text((40, sub_y + 145), "🚩 जय बजरंगबली | संकटमोचन हनुमान 🚩", font=font_shloka, fill="#F97316")

    # 5. BOTTOM ENGAGEMENT CTA / PROGRESS BAR
    draw.rounded_rectangle([25, 1160, WIDTH - 25, 1235], radius=16, fill=(220, 38, 38, 245), outline="#FBBF24", width=3)
    draw_outlined_text(draw, (50, 1175), "🚩 COMMENT 'JAI SHRI RAM' & SUBSCRIBE! 🔔", font=font_sub, fill_color="white", stroke_color="#78350F", stroke_width=3)

    # Bottom Golden Progress Bar
    prog_pct = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 10, int(WIDTH * prog_pct), HEIGHT], fill="#F59E0B")

    # Pipe frame to FFmpeg
    rgb_frame = canvas.convert("RGB")
    proc.stdin.write(rgb_frame.tobytes())

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"🎉 HANUMAN RETURNS CINEMATIC SHORT RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Total Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames)")
print("="*60)
