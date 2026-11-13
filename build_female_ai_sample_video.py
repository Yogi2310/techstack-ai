import os
import sys
import math
import wave
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import win32com.client
import pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

workspace_dir = r"D:\Antigravity\Pro"
temp_dir = os.path.join(workspace_dir, "shorts_studio", "temp", "female_sample")
os.makedirs(temp_dir, exist_ok=True)

output_mp4 = os.path.join(workspace_dir, "female_ai_presenter_sample.mp4")
presenter_img_path = os.path.join(workspace_dir, "female_ai_tech_creator.jpg")
logo_path = os.path.join(workspace_dir, "youtube-shorts-factory", "yts-logo.png")

scenes = [
    {
        "tag": "DAILY AI STACK",
        "script": "Here are the three AI tools I use every single day that feel like absolute superpowers.",
        "headline": "3 DAILY AI TOOLS",
        "subtext": "Supercharge Your Workflow\nSave 10+ Hours Every Week",
        "type": "spotlight",
        "color": "#22D3EE"
    },
    {
        "tag": "TOOL #1 · TERMINAL",
        "script": "First is Claude Code. It runs right inside your terminal and executes multi-file refactors autonomously.",
        "headline": "1. CLAUDE CODE",
        "subtext": "Autonomous Terminal Agent\nRefactors Entire Repositories",
        "type": "card",
        "color": "#3B82F6"
    },
    {
        "tag": "TOOL #2 · VS CODE",
        "script": "Second is Continue dot dev. It gives you free, open source local AI autocomplete inside VS Code.",
        "headline": "2. CONTINUE.DEV",
        "subtext": "100% Private Local LLMs\nZero Code Leaves Your Machine",
        "type": "card",
        "color": "#10B981"
    },
    {
        "tag": "TOOL #3 · ULTRA FAST",
        "script": "Third is Supermaven. With a massive 300,000 token context window, it predicts your next line instantly.",
        "headline": "3. SUPERMAVEN",
        "subtext": "300,000 Token Context\nZero Latency Suggestions",
        "type": "card",
        "color": "#F59E0B"
    },
    {
        "tag": "FREE SETUP GUIDE",
        "script": "Comment STACK below and I will send you my complete developer configuration guide for free!",
        "headline": "GET THE CONFIGS",
        "subtext": "COMMENT: STACK\n[✓] VS Code Settings\n[✓] Free Model Guide",
        "type": "spotlight",
        "color": "#A855F7"
    }
]

print("="*60)
print("[+] Synthesizing Female Voiceover Audio...")
print("="*60)

pythoncom.CoInitialize()
try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = 0  # Natural conversational speed
    
    for idx, sc in enumerate(scenes):
        wav_path = os.path.join(temp_dir, f"scene_{idx}.wav")
        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        stream.Open(wav_path, 3, False)
        speaker.AudioOutputStream = stream
        speaker.Speak(sc["script"])
        stream.Close()
finally:
    pythoncom.CoUninitialize()

# Combine audio
audio_data_list = []
scene_schedule = []
current_start = 0.0

for idx, sc in enumerate(scenes):
    wav_path = os.path.join(temp_dir, f"scene_{idx}.wav")
    with wave.open(wav_path, 'rb') as w:
        nframes = w.getnframes()
        rate = w.getframerate()
        nchannels = w.getnchannels()
        sampwidth = w.getsampwidth()
        data = w.readframes(nframes)
        duration = nframes / float(rate)
        audio_data_list.append((data, nchannels, sampwidth, rate))
        scene_schedule.append({
            "idx": idx,
            "tag": sc["tag"],
            "script": sc["script"],
            "headline": sc["headline"],
            "subtext": sc["subtext"],
            "type": sc["type"],
            "color": sc["color"],
            "start": current_start,
            "end": current_start + duration,
            "duration": duration
        })
        current_start += duration

total_duration = current_start
master_audio_wav = os.path.join(temp_dir, "master_audio.wav")
with wave.open(master_audio_wav, 'wb') as out_w:
    out_w.setnchannels(audio_data_list[0][1])
    out_w.setsampwidth(audio_data_list[0][2])
    out_w.setframerate(audio_data_list[0][3])
    for data, _, _, _ in audio_data_list:
        out_w.writeframes(data)

print(f"[+] Master Audio: {total_duration:.2f}s across {len(scene_schedule)} scenes.")

# Load Presenter Image
raw_presenter = Image.open(presenter_img_path).convert("RGBA")

# Pre-generate circular masks & sizes
# Size 1: Large Spotlight (340x340)
spotlight_size = 340
spotlight_img = raw_presenter.resize((spotlight_size, spotlight_size), Image.Resampling.LANCZOS)
spotlight_mask = Image.new("L", (spotlight_size, spotlight_size), 0)
ImageDraw.Draw(spotlight_mask).ellipse([0, 0, spotlight_size, spotlight_size], fill=255)

# Size 2: Corner Webcam Badge (200x200)
cam_size = 200
cam_img = raw_presenter.resize((cam_size, cam_size), Image.Resampling.LANCZOS)
cam_mask = Image.new("L", (cam_size, cam_size), 0)
ImageDraw.Draw(cam_mask).ellipse([0, 0, cam_size, cam_size], fill=255)

# Logo badge
logo_img = None
logo_mask = None
if os.path.exists(logo_path):
    raw_logo = Image.open(logo_path).convert("RGBA")
    logo_size = 64
    logo_img = raw_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    logo_mask = Image.new("L", (logo_size, logo_size), 0)
    ImageDraw.Draw(logo_mask).ellipse([0, 0, logo_size, logo_size], fill=255)

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 36)
font_subtitle = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
font_big = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 46)
font_huge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 52)
font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17)

WIDTH = 720
HEIGHT = 1280
FPS = 24
total_frames = int(math.ceil(total_duration * FPS))

print(f"[+] Rendering {total_frames} frames to {output_mp4}...")

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
    "-crf", "20",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_mp4
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

for frame_idx in range(total_frames):
    t = frame_idx / float(FPS)
    
    cur_scene = scene_schedule[-1]
    for sc in scene_schedule:
        if sc["start"] <= t < sc["end"]:
            cur_scene = sc
            break
            
    accent = cur_scene["color"]
    is_spotlight = (cur_scene["type"] == "spotlight")
    
    img = Image.new("RGBA", (WIDTH, HEIGHT), color=(10, 12, 22, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Background Cyber Matrix Grid
    for x in range(0, WIDTH, 60):
        draw.line([x, 0, x, HEIGHT], fill=(18, 24, 40, 255), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([0, y, WIDTH, y], fill=(18, 24, 40, 255), width=1)

    # Ambient Glow
    draw.ellipse([WIDTH//2 - 280, 300, WIDTH//2 + 280, 950], fill=(22, 32, 65, 120))
    draw.ellipse([WIDTH//2 - 150, 400, WIDTH//2 + 150, 750], fill=(34, 211, 238, 40))

    # 2. Top HUD Tag & Timecode
    draw.rounded_rectangle([30, 40, 390, 82], radius=15, fill=(24, 30, 50, 240), outline=(65, 75, 110, 255), width=2)
    draw.text((48, 50), cur_scene["tag"], font=font_tag, fill=accent)
    
    time_str = f"{int(t//60)}:{int(t%60):02d} / 0:{int(total_duration):02d}"
    draw.text((WIDTH - 245, 52), time_str, font=font_tag, fill=(150, 155, 175, 255))

    # 3. Logo Watermark (Top Right)
    if logo_img and logo_mask:
        lx = WIDTH - 90
        ly = 28
        img.paste(logo_img, (lx, ly), logo_mask)
        draw.ellipse([lx - 2, ly - 2, lx + 66, ly + 66], outline="#22D3EE", width=3)

    # 4. SCENE CONTENT RENDERING
    if is_spotlight:
        # Full Presenter Spotlight Mode (Intro / Outro)
        pulse = math.sin(t * 5.0) * 8
        px = (WIDTH - spotlight_size) // 2
        py = 220
        
        # Multiple glowing audio pulse rings around presenter
        draw.ellipse([px - 20 - pulse, py - 20 - pulse, px + spotlight_size + 20 + pulse, py + spotlight_size + 20 + pulse], outline=(34, 211, 238, 100), width=3)
        draw.ellipse([px - 8, py - 8, px + spotlight_size + 8, py + spotlight_size + 8], outline=(168, 85, 247, 240), width=5)
        draw.ellipse([px - 2, py - 2, px + spotlight_size + 2, py + spotlight_size + 2], outline=(34, 211, 238, 255), width=4)
        
        # Paste Large Presenter Avatar
        img.paste(spotlight_img, (px, py), spotlight_mask)
        
        # Presenter Name Badge Below Avatar
        badge_y = py + spotlight_size + 20
        draw.rounded_rectangle([WIDTH//2 - 140, badge_y, WIDTH//2 + 140, badge_y + 44], radius=12, fill=(18, 24, 42, 255), outline=accent, width=2)
        draw.text((WIDTH//2 - 110, badge_y + 8), "AI PRESENTER · TECH", font=font_tag, fill=accent)
        
        # Floating Headline Card Below
        card_y = badge_y + 70
        draw.rounded_rectangle([70, card_y, 650, card_y + 240], radius=24, fill=(16, 22, 38, 245), outline=accent, width=3)
        draw.text((105, card_y + 25), cur_scene["headline"], font=font_huge, fill="white")
        
        lines = cur_scene["subtext"].split("\n")
        for l_idx, line in enumerate(lines):
            col = accent if l_idx == 0 else (210, 225, 245, 255)
            draw.text((105, card_y + 95 + l_idx * 50), line, font=font_title, fill=col)

    else:
        # Card + Presenter Cam Mode (Tool breakdowns)
        card_pulse = math.sin(t * 4.0) * 3
        c_x1, c_y1 = int(60 - card_pulse), int(160 - card_pulse)
        c_x2, c_y2 = int(660 + card_pulse), int(640 + card_pulse)
        
        # Hologram Glass Display
        draw.rounded_rectangle([c_x1, c_y1, c_x2, c_y2], radius=26, fill=(16, 22, 38, 245), outline=accent, width=3)
        
        # Tech Lines inside Hologram
        for gx in range(c_x1 + 40, c_x2, 80):
            draw.line([gx, c_y1 + 10, gx, c_y2 - 10], fill=(25, 35, 60, 70), width=1)
            
        draw.text((c_x1 + 40, c_y1 + 35), cur_scene["headline"], font=font_huge, fill="white")
        
        lines = cur_scene["subtext"].split("\n")
        for l_idx, line in enumerate(lines):
            col = accent if l_idx == 0 else (210, 225, 245, 255)
            draw.text((c_x1 + 40, c_y1 + 115 + l_idx * 54), line, font=font_title, fill=col)
            
        # Value metric / verification badge
        draw.rounded_rectangle([c_x1 + 40, c_y1 + 250, c_x2 - 40, c_y1 + 300], radius=12, fill=(6, 78, 59, 230), outline=(16, 185, 129, 255), width=2)
        draw.text((c_x1 + 65, c_y1 + 262), "⚡ TESTED & VERIFIED BY SENIOR DEVS", font=font_tag, fill=(52, 211, 153, 255))

        # Bottom Presenter Cam Badge (Speaking to audience)
        cam_cx = WIDTH // 2
        cam_cy = 850
        cpx = cam_cx - cam_size // 2
        cpy = cam_cy - cam_size // 2
        
        pulse_c = math.sin(t * 6.0) * 5
        draw.ellipse([cpx - 10 - pulse_c, cpy - 10 - pulse_c, cpx + cam_size + 10 + pulse_c, cpy + cam_size + 10 + pulse_c], outline=(34, 211, 238, 120), width=3)
        draw.ellipse([cpx - 4, cpy - 4, cpx + cam_size + 4, cpy + cam_size + 4], outline=accent, width=4)
        
        img.paste(cam_img, (cpx, cpy), cam_mask)
        
        # Live indicator
        draw.rounded_rectangle([cpx + cam_size - 60, cpy + 10, cpx + cam_size + 5, cpy + 36], radius=6, fill=(220, 38, 38, 255))
        draw.text((cpx + cam_size - 52, cpy + 14), "● LIVE", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14), fill="white")

    # 5. Bottom Kinetic Subtitle Ribbon
    draw.rounded_rectangle([30, 1120, WIDTH - 30, 1220], radius=18, fill=(15, 20, 35, 255), outline=(34, 211, 238, 200), width=2)
    sub_text = cur_scene["script"]
    if len(sub_text) > 40:
        words = sub_text.split()
        half = len(words) // 2
        line1 = " ".join(words[:half])
        line2 = " ".join(words[half:])
        draw.text((50, 1132), line1, font=font_small, fill="white")
        draw.text((50, 1165), line2, font=font_small, fill=accent)
    else:
        draw.text((50, 1150), sub_text, font=font_small, fill="white")
        
    # 6. Bottom Continuous Progress Bar
    prog_pct = min(1.0, t / total_duration)
    draw.rectangle([0, HEIGHT - 10, int(WIDTH * prog_pct), HEIGHT], fill=accent)
    
    rgb_img = img.convert("RGB")
    proc.stdin.write(rgb_img.tobytes())

proc.stdin.close()
proc.wait()
print("\n" + "="*60)
print(f"🎉 SAMPLE VIDEO RENDERED SUCCESSFULLY!")
print(f"File: {output_mp4}")
print("="*60)
