import os
import sys
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

proj_dir = r"D:\Antigravity\Pro\Rico_Style_2D_Comedy"
audio_path = os.path.join(proj_dir, "audio", "master_rico_audio.wav")
output_mp4 = os.path.join(proj_dir, "videos", "rico_style_bored_in_class.mp4")

WIDTH = 720
HEIGHT = 1280
FPS = 24
TOTAL_DURATION = 18.0
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

# Fonts
font_meme_huge = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 52)
font_meme_big = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 38)
font_text_hi = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 40)
font_text_en = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
font_comic = ImageFont.truetype(r"C:\Windows\Fonts\comicbd.ttf", 34)

# Subtitle captions for Rico style
captions = [
    {"start": 0.0, "end": 3.8, "hi": "जब क्लास में EXTREME बोरियत हो...", "en": "When you're extreme bored in class...", "tag": "😴 BOREDOM LEVEL: 100%"},
    {"start": 3.8, "end": 7.0, "hi": "लगा 2 घंटे हो गए... पर सिर्फ 2 MINUTE?! 💀", "en": "Felt like 2 hours... but only 2 minutes?!", "tag": "⏰ TIME ILLUSION"},
    {"start": 7.0, "end": 10.2, "hi": "बोरियत से बचने के लिए PEN SPINNING ✍️🔥", "en": "Pen spinning to survive boredom...", "tag": "⚡ ULTRA FOCUS ON"},
    {"start": 10.2, "end": 13.5, "hi": "अरे यार... PEN सीधा TEACHER के पास गिरा! 💀", "en": "PEN FLEW STRAIGHT TO THE TEACHER! 💀", "tag": "🚨 INSTANT DEATH"},
    {"start": 13.5, "end": 18.0, "hi": "मैडम ने घूरा तो BLANK NOTEBOOK में EINSTEIN बन गया! 🤣", "en": "Teacher stared, so I became Einstein! ✍️💨", "tag": "✍️ MACH 5 WRITING"}
]

print(f"[+] Rendering Rico Animations 2D Meme Short ({TOTAL_DURATION}s, {TOTAL_FRAMES} frames)...")

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

def draw_outlined_text(draw, pos, text, font, fill_color="yellow", stroke_color="black", stroke_width=4, fill=None):
    x, y = pos
    actual_fill = fill if fill is not None else fill_color
    draw.text((x, y), text, font=font, fill=actual_fill, stroke_fill=stroke_color, stroke_width=stroke_width)

for f in range(TOTAL_FRAMES):
    t = f / float(FPS)
    
    cur_cap = captions[-1]
    for cap in captions:
        if cap["start"] <= t < cap["end"]:
            cur_cap = cap
            break

    # 1. Base Canvas - Classroom Colors
    img = Image.new("RGBA", (WIDTH, HEIGHT), color=(245, 240, 230, 255))
    draw = ImageDraw.Draw(img)

    # Classroom Background: Green chalkboard on top half
    draw.rectangle([40, 140, WIDTH - 40, 520], fill=(35, 75, 55, 255), outline=(139, 90, 43, 255), width=8)
    
    # Chalkboard Doodles
    draw.text((70, 160), "MATH: 2 + 2 = 5?", font=font_comic, fill=(200, 230, 210, 200))
    draw.text((70, 210), "E = mc² ... Zzz", font=font_comic, fill=(200, 230, 210, 180))
    draw.text((450, 160), "HOMEWORK:", font=font_comic, fill=(240, 200, 100, 220))
    draw.text((460, 205), "PAGE 999", font=font_comic, fill=(240, 100, 100, 220))

    # School Desk in foreground (Wood color)
    desk_y = 780
    draw.polygon([(0, desk_y), (WIDTH, desk_y), (WIDTH, HEIGHT), (0, HEIGHT)], fill=(190, 130, 80, 255))
    draw.line([(0, desk_y), (WIDTH, desk_y)], fill=(120, 75, 40, 255), width=8)

    # =========================================================================
    # SCENE 1: EXTREME BOREDOM (0.0s - 3.8s)
    # =========================================================================
    if t < 3.8:
        # A. Clock on the wall (Ticking animation)
        clock_cx, clock_cy = 580, 260
        draw.ellipse([clock_cx - 65, clock_cy - 65, clock_cx + 65, clock_cy + 65], fill="white", outline="black", width=5)
        # Hour hand
        draw.line([(clock_cx, clock_cy), (clock_cx + 25, clock_cy)], fill="black", width=4)
        # Second hand (snapping on every second)
        sec_angle = (t % 1.0) * (2 * math.pi / 60.0) + (int(t) * (2 * math.pi / 60.0))
        sx = clock_cx + math.sin(sec_angle * 15.0) * 45
        sy = clock_cy - math.cos(sec_angle * 15.0) * 45
        draw.line([(clock_cx, clock_cy), (sx, sy)], fill="red", width=2)
        draw.text((clock_cx - 45, clock_cy + 15), "10:01", font=font_text_en, fill="gray")

        # B. Slumped Character (Melting onto desk)
        # Head flat on desk
        head_x, head_y = WIDTH // 2 - 20, desk_y - 40
        # White cartoon head stretched flat
        melt_w = 260 + int(math.sin(t * 3.0) * 15)
        melt_h = 130
        draw.ellipse([head_x - melt_w//2, head_y - melt_h//2, head_x + melt_w//2, head_y + melt_h//2], fill=(255, 255, 255, 255), outline="black", width=6)
        
        # Deadpan half-closed eyes
        draw.arc([head_x - 70, head_y - 25, head_x - 20, head_y + 15], start=0, end=180, fill="black", width=4)
        draw.arc([head_x + 20, head_y - 25, head_x + 70, head_y + 15], start=0, end=180, fill="black", width=4)
        
        # Drool puddle forming on desk
        drool_size = int(min(60, t * 18))
        draw.ellipse([head_x + 75, desk_y - 5, head_x + 75 + drool_size, desk_y + 15], fill=(120, 200, 255, 220))
        # Drool string from mouth
        draw.line([(head_x + 55, head_y + 20), (head_x + 75, desk_y + 5)], fill=(120, 200, 255, 220), width=4)

        # "Zzz" floating
        zzz_prog = (t * 1.5) % 3.0
        draw.text((head_x - 120, head_y - 60 - int(zzz_prog * 40)), "Z z Z ...", font=font_comic, fill="#8B5CF6")

    # =========================================================================
    # SCENE 2: THE 2-MINUTE CLOCK SHOCK (3.8s - 7.0s) (VINE BOOM IMPACT)
    # =========================================================================
    elif 3.8 <= t < 7.0:
        rel_t = t - 3.8
        # Dramatic screen shake right on Vine Boom impact (3.8s to 4.5s)
        shake = int(math.sin(rel_t * 50.0) * 18 * math.exp(-rel_t * 3.0))
        
        # A. Giant Zoomed Clock in Face
        gc_x = WIDTH // 2 + shake
        gc_y = 380
        gc_r = 170
        draw.ellipse([gc_x - gc_r, gc_y - gc_r, gc_x + gc_r, gc_y + gc_r], fill="white", outline="red", width=10)
        draw.line([(gc_x, gc_y), (gc_x + 70, gc_y)], fill="black", width=8)
        draw.line([(gc_x, gc_y), (gc_x, gc_y - 120)], fill="black", width=6)
        draw.line([(gc_x, gc_y), (gc_x + 30, gc_y + 80)], fill="red", width=4)
        draw_outlined_text(draw, (gc_x - 120, gc_y + 70), "10:02 AM", font=font_meme_big, fill="#EF4444", stroke_color="black", stroke_width=4)
        draw_outlined_text(draw, (gc_x - 110, gc_y - 60), "ONLY 2 MINS?!", font=font_meme_big, fill="black", stroke_color="yellow", stroke_width=3)

        # B. Extreme Anime Shock Face
        cx = WIDTH // 2 + shake
        cy = 720
        # White face popping up
        draw.ellipse([cx - 160, cy - 180, cx + 160, cy + 180], fill="white", outline="black", width=7)
        
        # Giant bug-eyes with tiny vibrating pupils (Rico Animations signature!)
        draw.ellipse([cx - 130, cy - 110, cx - 10, cy + 30], fill="white", outline="black", width=5)
        draw.ellipse([cx + 10, cy - 110, cx + 130, cy + 30], fill="white", outline="black", width=5)
        # Tiny pupils vibrating in disbelief
        pv = int(math.sin(rel_t * 40.0) * 8)
        draw.ellipse([cx - 75 + pv, cy - 45, cx - 65 + pv, cy - 35], fill="black")
        draw.ellipse([cx + 65 + pv, cy - 45, cx + 75 + pv, cy - 35], fill="black")

        # Jaw unhinged open to the desk!
        draw.polygon([(cx - 70, cy + 50), (cx + 70, cy + 50), (cx + 50, cy + 190), (cx - 50, cy + 190)], fill=(40, 10, 20, 255), outline="black", width=5)
        # Blue vertical panic lines on forehead
        for pl_x in [-90, -50, 0, 50, 90]:
            draw.line([(cx + pl_x, cy - 170), (cx + pl_x, cy - 120)], fill=(56, 189, 248, 255), width=4)

    # =========================================================================
    # SCENE 3: PEN SPINNING ANIME BATTLE FOCUS (7.0s - 10.2s)
    # =========================================================================
    elif 7.0 <= t < 10.2:
        rel_t = t - 7.0
        # Anime Speed Lines radiating from center
        cx, cy = WIDTH // 2, 600
        for ang_i in range(0, 360, 15):
            rad = math.radians(ang_i + rel_t * 60.0)
            r1 = 280
            r2 = 600
            x1 = cx + math.cos(rad) * r1
            y1 = cy + math.sin(rad) * r1
            x2 = cx + math.cos(rad) * r2
            y2 = cy + math.sin(rad) * r2
            draw.line([(x1, y1), (x2, y2)], fill=(200, 220, 255, 180), width=4)

        # Glowing blue aura around head
        draw.ellipse([cx - 180, cy - 190, cx + 180, cy + 190], fill=(59, 130, 246, 70))
        draw.ellipse([cx - 150, cy - 160, cx + 150, cy + 160], fill="white", outline="black", width=6)

        # Intense sharp anime eyes (Serious Mode)
        draw.polygon([(cx - 110, cy - 60), (cx - 20, cy - 30), (cx - 30, cy - 20), (cx - 110, cy - 40)], fill="black")
        draw.polygon([(cx + 110, cy - 60), (cx + 20, cy - 30), (cx + 30, cy - 20), (cx + 110, cy - 40)], fill="black")
        # Glowing cyan eyes
        draw.ellipse([cx - 65, cy - 45, cx - 45, cy - 25], fill="#00FFFF")
        draw.ellipse([cx + 45, cy - 45, cx + 65, cy - 25], fill="#00FFFF")
        
        # Sweat bead flying
        draw.ellipse([cx + 120, cy - 100, cx + 135, cy - 80], fill="#38BDF8")

        # Blurred Spinning Pen in Hand
        pen_spin_ang = rel_t * 30.0
        pen_len = 120
        px1 = cx + math.cos(pen_spin_ang) * pen_len
        py1 = 760 + math.sin(pen_spin_ang) * 40
        px2 = cx - math.cos(pen_spin_ang) * pen_len
        py2 = 760 - math.sin(pen_spin_ang) * 40
        # Draw motion blur trails
        draw.line([(px1, py1), (px2, py2)], fill=(37, 99, 235, 255), width=10)
        draw.ellipse([cx - 100, 720, cx + 100, 800], outline=(147, 197, 253, 160), width=6)

        # Comic badge
        draw_outlined_text(draw, (cx - 160, 420), "⚡ FOCUS LEVEL: OVER 9000! ⚡", font=font_meme_big, fill="#FBBF24", stroke_color="black", stroke_width=4)

    # =========================================================================
    # SCENE 4: PEN DROPS & TEACHER DEATH STARE (10.2s - 13.5s)
    # =========================================================================
    elif 10.2 <= t < 13.5:
        rel_t = t - 10.2
        # Screen turns dark dramatic red/black
        draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(20, 5, 10, 230))
        
        # A. Pen on floor with red exclamation
        draw.line([(WIDTH//2 - 60, 1000), (WIDTH//2 + 80, 1030)], fill=(37, 99, 235, 255), width=10)
        draw_outlined_text(draw, (WIDTH//2 - 40, 920), "*CLANG!!*", font=font_meme_huge, fill="yellow", stroke_color="red", stroke_width=5)

        # B. Menacing Teacher Silhouette with Glowing Red Demon Eyes
        tc_x = WIDTH // 2
        tc_y = 380
        # Dark purple shadow teacher body
        draw.ellipse([tc_x - 140, tc_y - 120, tc_x + 140, tc_y + 120], fill=(15, 8, 25, 255), outline=(220, 38, 38, 200), width=4)
        draw.polygon([(tc_x - 180, tc_y + 80), (tc_x + 180, tc_y + 80), (tc_x + 220, 720), (tc_x - 220, 720)], fill=(15, 8, 25, 255))
        
        # Piercing Glowing Red Eyes
        eye_pulse = 20 + int(math.sin(rel_t * 15.0) * 4)
        draw.ellipse([tc_x - 65 - eye_pulse//2, tc_y - 20, tc_x - 65 + eye_pulse//2, tc_y], fill="red")
        draw.ellipse([tc_x + 65 - eye_pulse//2, tc_y - 20, tc_x + 65 + eye_pulse//2, tc_y], fill="red")
        # Pupil red laser beam
        draw.ellipse([tc_x - 65, tc_y - 12, tc_x - 60, tc_y - 8], fill="white")
        draw.ellipse([tc_x + 60, tc_y - 12, tc_x + 65, tc_y - 8], fill="white")

        # Menacing Sound Effect Signs (ゴゴゴゴ)
        draw_outlined_text(draw, (100, 220), "DANGER!!", font=font_meme_huge, fill="#EF4444", stroke_color="black", stroke_width=5)
        draw_outlined_text(draw, (440, 260), "DEAD END!", font=font_meme_huge, fill="#EF4444", stroke_color="black", stroke_width=5)

    # =========================================================================
    # SCENE 5: PANIC FURIOUS WRITING MODE (13.5s - 18.0s)
    # =========================================================================
    else:
        rel_t = t - 13.5
        cx = WIDTH // 2
        cy = 580

        # Character sweating profusely, writing at supersonic speed
        draw.ellipse([cx - 150, cy - 160, cx + 150, cy + 160], fill="white", outline="black", width=6)
        
        # Nervous panicked eyes & crazy smile
        draw.ellipse([cx - 90, cy - 60, cx - 20, cy + 10], fill="white", outline="black", width=4)
        draw.ellipse([cx + 20, cy - 60, cx + 90, cy + 10], fill="white", outline="black", width=4)
        draw.ellipse([cx - 60, cy - 35, cx - 45, cy - 20], fill="black")
        draw.ellipse([cx + 45, cy - 35, cx + 60, cy - 20], fill="black")

        # Sweating water droplets flying everywhere
        for sw_i in range(5):
            sw_x = cx - 140 + sw_i * 60 + int(math.sin(t * 18.0 + sw_i) * 15)
            sw_y = cy - 120 + int(math.cos(t * 18.0 + sw_i) * 15)
            draw.ellipse([sw_x, sw_y, sw_x + 14, sw_y + 20], fill="#38BDF8")

        # Nervous teeth grin
        draw.rounded_rectangle([cx - 70, cy + 40, cx + 70, cy + 90], radius=10, fill="white", outline="black", width=4)
        for tx in range(cx - 50, cx + 60, 20):
            draw.line([(tx, cy + 40), (tx, cy + 90)], fill="black", width=2)

        # Mach 5 Blurred Multiple Arms writing furiously!
        arm_blur_phase = int(t * 30.0) % 4
        for arm_i in range(4):
            ax1 = cx + 80 + arm_i * 20
            ay1 = cy + 100 - arm_i * 10
            ax2 = cx + 160 + int(math.sin(t * 40.0 + arm_i) * 35)
            ay2 = desk_y + 20
            draw.line([(ax1, ay1), (ax2, ay2)], fill="black", width=12)

        # Smoke billowing from notebook
        smoke_offset = int((rel_t * 120) % 100)
        draw.ellipse([cx + 120, desk_y - smoke_offset, cx + 180, desk_y - smoke_offset + 50], fill=(160, 160, 160, 200))
        draw.ellipse([cx + 150, desk_y - smoke_offset - 30, cx + 200, desk_y - smoke_offset + 10], fill=(200, 200, 200, 180))

        # Mach 5 Writing label
        draw_outlined_text(draw, (cx - 180, 360), "⚡ MACH 5 WRITING SPEED! ⚡", font=font_meme_big, fill="#FBBF24", stroke_color="black", stroke_width=4)

    # =========================================================================
    # VIRAL MEME SUBTITLES & BANNER OVERLAYS (ALL SCENES)
    # =========================================================================
    # Top Meme Title Sticker
    draw.rounded_rectangle([30, 40, WIDTH - 30, 110], radius=16, fill="black", outline="#FBBF24", width=3)
    draw_outlined_text(draw, (50, 48), "WHEN BORED IN CLASS 😂", font=font_meme_big, fill="yellow", stroke_color="black", stroke_width=2)
    draw.text((WIDTH - 210, 58), cur_cap["tag"], font=font_text_en, fill="#38BDF8")

    # Lower Third Bouncy Meme Captions
    sub_y = 960
    draw.rounded_rectangle([25, sub_y, WIDTH - 25, sub_y + 170], radius=22, fill=(15, 10, 20, 245), outline="yellow", width=4)
    
    # Hindi Punchline (Large bold yellow with black outline)
    draw_outlined_text(draw, (45, sub_y + 20), cur_cap["hi"], font=font_text_hi, fill="#FBBF24", stroke_color="black", stroke_width=5)
    
    # English Subtitle
    draw_outlined_text(draw, (45, sub_y + 100), cur_cap["en"], font=font_text_en, fill="white", stroke_color="black", stroke_width=3)

    # Bottom Progress Bar
    prog_pct = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 12, int(WIDTH * prog_pct), HEIGHT], fill="#EF4444")

    rgb_frame = img.convert("RGB")
    proc.stdin.write(rgb_frame.tobytes())

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"🎉 RICO ANIMATIONS STYLE 2D MEME SHORT RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Total Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames)")
print("="*60)
