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
audio_path = os.path.join(proj_dir, "audio", "exam_panic_master_audio.wav")
output_mp4 = os.path.join(proj_dir, "videos", "rico_exam_panic_comedy_short.mp4")

WIDTH = 720
HEIGHT = 1280
FPS = 24
TOTAL_DURATION = 29.75
TOTAL_FRAMES = int(math.ceil(TOTAL_DURATION * FPS))

# Fonts
font_meme_huge = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 48)
font_meme_big = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 36)
font_text_hi = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 38)
font_text_en = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
font_comic = ImageFont.truetype(r"C:\Windows\Fonts\comicbd.ttf", 32)
font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)

captions = [
    {
        "start": 0.0,
        "end": 5.43,
        "hi": "3 घंटे का एग्जाम... 2:55 घंटे सिर्फ CALLIGRAPHY की! ✨",
        "en": "3 hr exam... spent 2h 55m writing my name in calligraphy! ✨",
        "tag": "😇 PEACEFUL VIBES"
    },
    {
        "start": 5.43,
        "end": 10.86,
        "hi": "टीचर: 'LAST 5 MINUTES!' दोस्त 12वीं EXTRA SHEET ले रहा?! 💀",
        "en": "Teacher: 'LAST 5 MINS!' Friend asking for 12th extra sheet?! 💀",
        "tag": "🚨 EXTREME PANIC"
    },
    {
        "start": 10.86,
        "end": 15.06,
        "hi": "100% दिमाग चालू... ULTRA INSTINCT MODE ON! 🔥⚡",
        "en": "100% Brain Power Activated... Ultra Instinct ON! 🔥⚡",
        "tag": "⚡ GOD MODE"
    },
    {
        "start": 15.06,
        "end": 22.09,
        "hi": "हाथ SUPERSONIC SPEED पे! कागज से धुआं निकल गया! ✍️💨",
        "en": "Mach 10 speed! Writing song lyrics! Paper caught fire! ✍️💨",
        "tag": "✍️ SUPERSONIC WRITING"
    },
    {
        "start": 22.09,
        "end": 29.75,
        "hi": "पेपर छिन गया... पर हाथ BENCH पे लिखता रहा! 🤣 Like & Sub! ❤️",
        "en": "Paper snatched... hand kept writing on the bench! 🤣",
        "tag": "💀 NO REGRETS"
    }
]

print(f"[+] Rendering Rico Style Exam Short ({TOTAL_DURATION}s, {TOTAL_FRAMES} frames)...")

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

    # 1. Base Canvas - Classroom Exam Hall Palette
    img = Image.new("RGBA", (WIDTH, HEIGHT), color=(240, 235, 225, 255))
    draw = ImageDraw.Draw(img)

    # Chalkboard Header
    draw.rectangle([40, 130, WIDTH - 40, 480], fill=(30, 65, 48, 255), outline=(139, 90, 43, 255), width=8)
    draw_outlined_text(draw, (70, 150), "FINAL BOARD EXAM: 100 MARKS", font=font_comic, fill_color="white", stroke_width=2)
    draw.text((70, 200), "TIME: 3 HOURS | NO TALKING!", font=font_small, fill=(200, 230, 210, 220))

    # Wooden Exam Desk in foreground
    desk_y = 750
    draw.polygon([(0, desk_y), (WIDTH, desk_y), (WIDTH, HEIGHT), (0, HEIGHT)], fill=(185, 125, 75, 255))
    draw.line([(0, desk_y), (WIDTH, desk_y)], fill=(110, 70, 35, 255), width=8)

    # =========================================================================
    # SCENE 1: THE PEACEFUL CALLIGRAPHY (0.0s - 5.43s)
    # =========================================================================
    if t < 5.43:
        # Clock showing 2:55 PM
        clock_x, clock_y = 570, 240
        draw.ellipse([clock_x - 60, clock_y - 60, clock_x + 60, clock_y + 60], fill="white", outline="black", width=5)
        draw.line([(clock_x, clock_y), (clock_x + 35, clock_y)], fill="black", width=5) # Hour ~3
        draw.line([(clock_x, clock_y), (clock_x - 30, clock_y - 30)], fill="black", width=4) # Minute ~55
        draw.text((clock_x - 35, clock_y + 15), "2:55 PM", font=font_small, fill="red")

        # Peaceful student with glowing golden halo
        head_x, head_y = WIDTH // 2, 600
        # Halo
        draw.ellipse([head_x - 110, head_y - 180, head_x + 110, head_y - 140], outline="#FBBF24", width=6)
        
        # White cartoon head
        draw.ellipse([head_x - 130, head_y - 130, head_x + 130, head_y + 130], fill="white", outline="black", width=6)
        
        # Blissful curved closed eyes ( ^ _ ^ )
        draw.arc([head_x - 80, head_y - 30, head_x - 20, head_y + 20], start=180, end=360, fill="black", width=4)
        draw.arc([head_x + 20, head_y - 30, head_x + 80, head_y + 20], start=180, end=360, fill="black", width=4)
        # Cute peaceful smile
        draw.arc([head_x - 35, head_y + 30, head_x + 35, head_y + 70], start=0, end=180, fill="black", width=4)
        # Rosy pink cheeks
        draw.ellipse([head_x - 90, head_y + 20, head_x - 50, head_y + 50], fill=(255, 180, 180, 200))
        draw.ellipse([head_x + 50, head_y + 20, head_x + 90, head_y + 50], fill=(255, 180, 180, 200))

        # Exam Paper on desk with fancy calligraphy
        draw.rectangle([head_x - 180, desk_y + 20, head_x + 180, desk_y + 210], fill="white", outline="black", width=3)
        draw.text((head_x - 160, desk_y + 35), "✨ NAME: Rahul Sharma ✨", font=font_small, fill="#8B5CF6")
        draw.text((head_x - 160, desk_y + 65), "🌸 ROLL NO: 42 (Section A) 🌸", font=font_small, fill="#EC4899")
        draw.text((head_x - 160, desk_y + 105), "Ans 1: ", font=font_small, fill="black")
        draw.text((head_x - 100, desk_y + 105), "[BLANK - NOTHING WRITTEN]", font=font_small, fill="gray")

        # Sparkle particles floating
        for sp_i in range(4):
            sp_t = (t * 2.0 + sp_i * 1.2) % 3.0
            sp_x = head_x - 140 + sp_i * 90 + int(math.sin(sp_t * 4.0) * 15)
            sp_y = desk_y - 40 - int(sp_t * 60)
            draw.text((sp_x, sp_y), "✨", font=font_meme_big, fill="#FBBF24")

    # =========================================================================
    # SCENE 2: THE 5-MINUTE WARNING & FRIEND'S FLEX (5.43s - 10.86s)
    # =========================================================================
    elif 5.43 <= t < 10.86:
        rel_t = t - 5.43
        # Vine Boom camera shake
        shake = int(math.sin(rel_t * 45.0) * 14 * math.exp(-rel_t * 2.5))
        
        # A. TEACHER WARNING POPUP (LEFT TOP)
        draw.rounded_rectangle([30 + shake, 150, 320 + shake, 310], radius=16, fill=(220, 38, 38, 240), outline="yellow", width=4)
        draw_outlined_text(draw, (45 + shake, 165), "TEACHER SHOUTS:", font=font_text_en, fill_color="white", stroke_width=2)
        draw_outlined_text(draw, (45 + shake, 205), "LAST 5 MINS!!", font=font_meme_huge, fill_color="yellow", stroke_width=4)
        draw_outlined_text(draw, (45 + shake, 260), "TIE YOUR PAPERS!", font=font_text_en, fill_color="white", stroke_width=2)

        # B. STUDENT TERROR FACE (CENTER)
        cx = 240 + shake
        cy = 580
        draw.ellipse([cx - 120, cy - 130, cx + 120, cy + 130], fill="white", outline="black", width=6)
        
        # Gigantic pop-out bug eyes
        eye_pop = 15 + int(math.sin(rel_t * 30.0) * 8)
        draw.ellipse([cx - 95 - eye_pop, cy - 70 - eye_pop, cx - 15 + eye_pop, cy + 10 + eye_pop], fill="white", outline="black", width=5)
        draw.ellipse([cx + 15 - eye_pop, cy - 70 - eye_pop, cx + 95 + eye_pop, cy + 10 + eye_pop], fill="white", outline="black", width=5)
        # Tiny pupils vibrating
        draw.ellipse([cx - 55, cy - 35, cx - 45, cy - 25], fill="black")
        draw.ellipse([cx + 45, cy - 35, cx + 55, cy - 25], fill="black")

        # Jaw dropping to the floor!
        draw.polygon([(cx - 50, cy + 30), (cx + 50, cy + 30), (cx + 35, cy + 150), (cx - 35, cy + 150)], fill=(40, 10, 20, 255), outline="black", width=5)
        # Sweat geyser shooting upwards
        for sw in range(3):
            sw_y = cy - 130 - int((rel_t * 240 + sw * 40) % 90)
            draw.ellipse([cx - 20 + sw * 20, sw_y, cx - 10 + sw * 20, sw_y + 15], fill="#38BDF8")

        # C. BEST FRIEND ON THE RIGHT (SMUG ANIME VILLAIN WITH 12 SHEETS)
        fx = 540 + shake
        fy = 550
        # Dark aura around friend
        draw.ellipse([fx - 110, fy - 110, fx + 110, fy + 110], fill=(147, 51, 234, 100))
        draw.ellipse([fx - 90, fy - 90, fx + 90, fy + 90], fill="white", outline="black", width=5)
        # Smug squinting anime eyes with glowing red pupils
        draw.line([(fx - 65, fy - 20), (fx - 15, fy - 10)], fill="black", width=5)
        draw.line([(fx + 15, fy - 10), (fx + 65, fy - 20)], fill="black", width=5)
        draw.ellipse([fx - 45, fy - 18, fx - 35, fy - 8], fill="red")
        draw.ellipse([fx + 35, fy - 18, fx + 45, fy - 8], fill="red")
        # Smug smirk
        draw.arc([fx - 25, fy + 15, fx + 35, fy + 45], start=0, end=180, fill="black", width=4)

        # Huge stack of 12 extra sheets in friend's hand!
        for sheet_i in range(10):
            sy_off = fy + 60 - sheet_i * 12
            draw.rectangle([fx - 70, sy_off, fx + 70, sy_off + 25], fill="white", outline="black", width=2)
        draw_outlined_text(draw, (fx - 80, fy - 120), "EXTRA SHEET #12", font=font_meme_big, fill_color="#FBBF24", stroke_width=3)

    # =========================================================================
    # SCENE 3: ULTRA INSTINCT GOD MODE (10.86s - 15.06s)
    # =========================================================================
    elif 10.86 <= t < 15.06:
        rel_t = t - 10.86
        # Anime Dark Cosmic Void background
        draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(12, 10, 28, 255))
        
        # Super Saiyan / Ultra Instinct Radiant Blue/Gold Aura
        cx, cy = WIDTH // 2, 540
        aura_r = 210 + int(math.sin(rel_t * 20.0) * 25)
        draw.ellipse([cx - aura_r, cy - aura_r, cx + aura_r, cy + aura_r], fill=(59, 130, 246, 80))
        draw.ellipse([cx - aura_r + 40, cy - aura_r + 40, cx + aura_r - 40, cy + aura_r - 40], fill=(245, 158, 11, 70))

        # Speed Lines in background
        for ang_i in range(0, 360, 18):
            rad = math.radians(ang_i + rel_t * 90.0)
            x1 = cx + math.cos(rad) * 240
            y1 = cy + math.sin(rad) * 240
            x2 = cx + math.cos(rad) * 650
            y2 = cy + math.sin(rad) * 650
            draw.line([(x1, y1), (x2, y2)], fill=(147, 197, 253, 160), width=4)

        # Character Head with Spiky Anime Hair
        # Spiky hair outlines
        draw.polygon([(cx - 140, cy - 60), (cx - 170, cy - 180), (cx - 100, cy - 140), 
                      (cx - 60, cy - 240), (cx, cy - 160), (cx + 60, cy - 240), 
                      (cx + 100, cy - 140), (cx + 170, cy - 180), (cx + 140, cy - 60)], 
                      fill="#FBBF24", outline="black", width=5)

        # Face
        draw.ellipse([cx - 130, cy - 110, cx + 130, cy + 120], fill="white", outline="black", width=6)
        
        # Sharp Ultra Instinct Eyes (Silver / White glowing)
        draw.polygon([(cx - 95, cy - 40), (cx - 20, cy - 20), (cx - 30, cy - 10), (cx - 95, cy - 25)], fill="black")
        draw.polygon([(cx + 95, cy - 40), (cx + 20, cy - 20), (cx + 30, cy - 10), (cx + 95, cy - 25)], fill="black")
        draw.ellipse([cx - 65, cy - 35, cx - 45, cy - 15], fill="#E2E8F0", outline="#38BDF8", width=3)
        draw.ellipse([cx + 45, cy - 35, cx + 65, cy - 15], fill="#E2E8F0", outline="#38BDF8", width=3)

        # Anime Vein mark (💢) on forehead
        draw.text((cx + 70, cy - 90), "💢", font=font_meme_big, fill="red")
        
        # Clenched teeth
        draw.rounded_rectangle([cx - 50, cy + 40, cx + 50, cy + 75], radius=6, fill="white", outline="black", width=4)
        for vx in range(cx - 35, cx + 45, 15):
            draw.line([(vx, cy + 40), (vx, cy + 75)], fill="black", width=2)

        # Banner
        draw_outlined_text(draw, (cx - 240, 260), "⚡ ULTRA INSTINCT: 100% ⚡", font=font_meme_huge, fill_color="#00FFFF", stroke_width=5)

    # =========================================================================
    # SCENE 4: MACH 10 WRITING SPEED & PAPER ON FIRE (15.06s - 22.09s)
    # =========================================================================
    elif 15.06 <= t < 22.09:
        rel_t = t - 15.06
        cx = WIDTH // 2
        cy = 500

        # Character Head
        draw.ellipse([cx - 130, cy - 110, cx + 130, cy + 110], fill="white", outline="black", width=6)
        # Panicked concentrated eyes
        draw.ellipse([cx - 85, cy - 50, cx - 25, cy + 10], fill="white", outline="black", width=4)
        draw.ellipse([cx + 25, cy - 50, cx + 85, cy + 10], fill="white", outline="black", width=4)
        draw.ellipse([cx - 60, cy - 30, cx - 45, cy - 15], fill="black")
        draw.ellipse([cx + 45, cy - 30, cx + 60, cy - 15], fill="black")

        # Sweat droplets flying in arcs
        for sw in range(6):
            sw_x = cx - 140 + sw * 50 + int(math.sin(rel_t * 25.0 + sw) * 20)
            sw_y = cy - 80 + int(math.cos(rel_t * 25.0 + sw) * 20)
            draw.ellipse([sw_x, sw_y, sw_x + 16, sw_y + 24], fill="#38BDF8")

        # 8 MULTIPLE BLURRED ARMS WRITING AT SOUND SPEED
        for arm_i in range(6):
            ang = math.radians(30 + arm_i * 24 + math.sin(rel_t * 40.0 + arm_i) * 20)
            ax1 = cx + 50
            ay1 = cy + 60
            ax2 = cx + 80 + math.cos(ang) * 220
            ay2 = desk_y + 40 + math.sin(ang) * 50
            draw.line([(ax1, ay1), (ax2, ay2)], fill="black", width=14)
            # Pen tip
            draw.line([(ax2, ay2), (ax2 + 20, ay2 + 25)], fill="blue", width=8)

        # FIRE & FLAMES ON EXAM PAPER!
        paper_x = cx + 110
        paper_y = desk_y + 10
        # Paper
        draw.rectangle([paper_x - 120, paper_y, paper_x + 120, paper_y + 160], fill="white", outline="black", width=3)
        draw.text((paper_x - 105, paper_y + 15), "Twinkle twinkle star...", font=font_small, fill="black")
        draw.text((paper_x - 105, paper_y + 45), "Pass kara do yaar!!", font=font_small, fill="black")
        draw.text((paper_x - 105, paper_y + 75), "Dil diya gallan...", font=font_small, fill="black")

        # Animated Cartoon Fire Flames on paper
        for flame_i in range(5):
            fx_p = paper_x - 80 + flame_i * 35
            flame_h = 45 + int(math.sin(rel_t * 30.0 + flame_i) * 25)
            draw.polygon([(fx_p - 18, paper_y + 10), (fx_p + 18, paper_y + 10), (fx_p, paper_y - flame_h)], fill="#EF4444")
            draw.polygon([(fx_p - 10, paper_y + 10), (fx_p + 10, paper_y + 10), (fx_p, paper_y - flame_h + 15)], fill="#FBBF24")

        # Smoke clouds rising
        smoke_y = paper_y - 80 - int((rel_t * 160) % 180)
        draw.ellipse([paper_x - 60, smoke_y, paper_x + 60, smoke_y + 70], fill=(120, 120, 120, 200))
        draw.ellipse([paper_x, smoke_y - 50, paper_x + 80, smoke_y + 10], fill=(160, 160, 160, 180))

        # Mach 10 label
        draw_outlined_text(draw, (cx - 210, 260), "🔥 WRITING AT MACH 10!! 🔥", font=font_meme_huge, fill_color="#FBBF24", stroke_width=5)

    # =========================================================================
    # SCENE 5: PAPER SNATCHED & DESK SCRIBBLING (22.09s - 29.75s)
    # =========================================================================
    else:
        rel_t = t - 22.09
        cx = WIDTH // 2
        cy = 540

        # Teacher's giant hand snatching paper off screen (Left to Right)
        if rel_t < 1.5:
            hand_prog = rel_t / 1.5
            hx = int(WIDTH * hand_prog)
            draw.rectangle([hx, desk_y - 40, hx + 180, desk_y + 120], fill="white", outline="black", width=4)
            draw_outlined_text(draw, (hx + 10, desk_y - 20), "*SNATCH!!*", font=font_meme_big, fill_color="yellow", stroke_width=3)

        # Desk is completely BARE WOOD now!
        # Wood scratch lines from furious writing on bare wood!
        scratch_box_x = cx + 80
        scratch_box_y = desk_y + 50
        for sc_i in range(15):
            sx1 = scratch_box_x - 70 + (sc_i * 10)
            sy1 = scratch_box_y + (sc_i % 3) * 15
            sx2 = sx1 + 35
            sy2 = sy1 + 10
            draw.line([(sx1, sy1), (sx2, sy2)], fill=(80, 45, 20, 255), width=3)
        draw_outlined_text(draw, (scratch_box_x - 60, scratch_box_y + 60), "*CARVING INTO WOOD*", font=font_small, fill_color="white", stroke_width=2)

        # Student Head (Shocked Derp / Meme Expression)
        draw.ellipse([cx - 130, cy - 120, cx + 130, cy + 120], fill="white", outline="black", width=6)
        
        # Deadpan unblinking eyes staring into distance
        draw.ellipse([cx - 85, cy - 50, cx - 25, cy + 10], fill="white", outline="black", width=4)
        draw.ellipse([cx + 25, cy - 50, cx + 85, cy + 10], fill="white", outline="black", width=4)
        draw.ellipse([cx - 58, cy - 25, cx - 50, cy - 17], fill="black")
        draw.ellipse([cx + 50, cy - 25, cx + 58, cy - 17], fill="black")

        # Hand still furiously scribbling on the wood!
        pen_shake = int(math.sin(rel_t * 35.0) * 20)
        draw.line([(cx + 40, cy + 60), (scratch_box_x + pen_shake, scratch_box_y)], fill="black", width=12)
        draw.line([(scratch_box_x + pen_shake, scratch_box_y), (scratch_box_x + pen_shake + 15, scratch_box_y + 20)], fill="blue", width=8)

        # Question mark above head
        draw_outlined_text(draw, (cx - 20, cy - 190), "???", font=font_meme_huge, fill_color="#EF4444", stroke_width=4)
        draw_outlined_text(draw, (cx - 160, 280), "WAIT... WHERE IS MY PAPER?! 💀", font=font_meme_big, fill_color="yellow", stroke_width=3)

    # =========================================================================
    # VIRAL MEME SUBTITLES & BANNER OVERLAYS (ALL SCENES)
    # =========================================================================
    # Top Meme Title Sticker
    draw.rounded_rectangle([30, 40, WIDTH - 30, 110], radius=16, fill="black", outline="#FBBF24", width=3)
    draw_outlined_text(draw, (45, 48), "LAST 5 MINS OF EXAM 😂", font=font_meme_big, fill_color="yellow", stroke_width=2)
    draw.text((WIDTH - 210, 58), cur_cap["tag"], font=font_text_en, fill="#38BDF8")

    # Lower Third Bouncy Meme Captions
    sub_y = 960
    draw.rounded_rectangle([25, sub_y, WIDTH - 25, sub_y + 175], radius=22, fill=(15, 10, 20, 245), outline="yellow", width=4)
    
    # Hindi Punchline (Large bold yellow with black outline)
    draw_outlined_text(draw, (45, sub_y + 20), cur_cap["hi"], font=font_text_hi, fill_color="#FBBF24", stroke_width=5)
    
    # English Subtitle
    draw_outlined_text(draw, (45, sub_y + 105), cur_cap["en"], font=font_text_en, fill_color="white", stroke_width=3)

    # Bottom Progress Bar
    prog_pct = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 12, int(WIDTH * prog_pct), HEIGHT], fill="#EF4444")

    rgb_frame = img.convert("RGB")
    proc.stdin.write(rgb_frame.tobytes())

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"🎉 RICO STYLE EXAM SHORT RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Total Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames)")
print("="*60)
