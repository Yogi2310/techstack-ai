import os
import sys
import math
import wave
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import win32com.client
import pythoncom

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

workspace_dir = r"D:\Antigravity\Pro"
temp_dir = os.path.join(workspace_dir, "shorts_studio", "temp", "baby_comedy")
os.makedirs(temp_dir, exist_ok=True)

output_mp4 = os.path.join(workspace_dir, "cute_baby_golgappa_comedy.mp4")
baby_img_path = os.path.join(workspace_dir, "cute_ai_baby_golgappa.jpg")

scenes = [
    {
        "id": "scene_1",
        "audio_text": "Bhaiya! Ek plate golgappe lagao... aur suno, teekha thoda kam rakhna haan!",
        "headline": "GOLGAPPE KA LALACH 🤤",
        "sub_hi": "भैया! एक प्लेट गोलगप्पे लगाओ... तीखा कम!",
        "sub_en": "Bhaiya! 1 Plate Golgappe... Less Spicy!",
        "effect": "zoom_in",
        "accent": "#F59E0B"
    },
    {
        "id": "scene_2",
        "audio_text": "Mmm! Itna tasty pani puri! Ek aur... nahi nahi teen aur do bhaiya!",
        "headline": "WAH! ITNA TASTY! 😋",
        "sub_hi": "वाह! इतना टेस्टी! मज़ा आ गया!",
        "sub_en": "Mmm! So Tasty! Give 3 More!",
        "effect": "bounce",
        "accent": "#10B981"
    },
    {
        "id": "scene_3",
        "audio_text": "Arey baap re! Yeh to bohot teekha hai! Kaan se dhuan nikal gaya! Meetha paani do jaldi!",
        "headline": "BOHOT TEEKHA HAI! 🌶️🔥",
        "sub_hi": "अरे बाप रे! बहुत तीखा है! धुआं निकल गया!",
        "sub_en": "Too Spicy!! Ears On Fire! Sweet Water Fast!",
        "effect": "shake_fire",
        "accent": "#EF4444"
    },
    {
        "id": "scene_4",
        "audio_text": "Lekin fir bhi main poora plate khatam karunga! Golgappe se no compromise! Hehehe!",
        "headline": "NO COMPROMISE! 🤣😂",
        "sub_hi": "लेकिन फिर भी पूरा खाऊंगा! नो कॉम्प्रोमाइज़!",
        "sub_en": "Still Gonna Finish It All! Hehehe!",
        "effect": "triumph",
        "accent": "#EC4899"
    },
    {
        "id": "scene_5",
        "audio_text": "Golgappa lovers jaldi se Like aur Subscribe kar do!",
        "headline": "LIKE & SUBSCRIBE ❤️🔔",
        "sub_hi": "गोलगप्पे लवर हो तो लाइक करो!",
        "sub_en": "Golgappa Lovers Like & Subscribe!",
        "effect": "pulse_cta",
        "accent": "#8B5CF6"
    }
]

print("="*60)
print("[+] STEP 1: Synthesizing & Pitch-Shifting Cute Baby Voice...")
print("="*60)

pythoncom.CoInitialize()
try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = 1  # Slightly faster for cute kid delivery
    
    for sc in scenes:
        raw_wav = os.path.join(temp_dir, f"{sc['id']}_raw.wav")
        pitched_wav = os.path.join(temp_dir, f"{sc['id']}_pitched.wav")
        
        # 1. Synthesize raw voice
        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        stream.Open(raw_wav, 3, False)
        speaker.AudioOutputStream = stream
        speaker.Speak(sc["audio_text"])
        stream.Close()
        
        # 2. Pitch shift up by 32% to create cute baby / kid voice
        # asetrate shifts pitch up, aresample restores standard sample rate
        pitch_cmd = [
            ffmpeg_exe, "-y",
            "-i", raw_wav,
            "-af", "asetrate=22050*1.32,aresample=22050",
            pitched_wav
        ]
        subprocess.run(pitch_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
finally:
    pythoncom.CoUninitialize()

# Measure durations of pitched audio
audio_data_list = []
scene_schedule = []
current_start = 0.0

for sc in scenes:
    pitched_wav = os.path.join(temp_dir, f"{sc['id']}_pitched.wav")
    with wave.open(pitched_wav, 'rb') as w:
        nframes = w.getnframes()
        rate = w.getframerate()
        nchannels = w.getnchannels()
        sampwidth = w.getsampwidth()
        data = w.readframes(nframes)
        duration = nframes / float(rate)
        audio_data_list.append((data, nchannels, sampwidth, rate))
        
        sc_info = dict(sc)
        sc_info["start"] = current_start
        sc_info["end"] = current_start + duration
        sc_info["duration"] = duration
        scene_schedule.append(sc_info)
        current_start += duration
        print(f"  {sc['id']}: {duration:.2f}s | {sc['headline']}")

total_duration = current_start
master_audio_wav = os.path.join(temp_dir, "master_audio.wav")
with wave.open(master_audio_wav, 'wb') as out_w:
    out_w.setnchannels(audio_data_list[0][1])
    out_w.setsampwidth(audio_data_list[0][2])
    out_w.setframerate(audio_data_list[0][3])
    for data, _, _, _ in audio_data_list:
        out_w.writeframes(data)

print(f"[+] Total Master Audio Duration: {total_duration:.2f}s")

# Load 3D Cute Baby Image
raw_baby = Image.open(baby_img_path).convert("RGBA")

# Fonts
font_huge = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 44)
font_big = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 34)
font_sub_hi = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 36)  # Official Windows font for Hindi
font_sub_en = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)

WIDTH = 720
HEIGHT = 1280
FPS = 24
total_frames = int(math.ceil(total_duration * FPS))

print(f"\n[+] STEP 2: Rendering {total_frames} Frames with Pixar Animation Effects...")

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

for frame_idx in range(total_frames):
    t = frame_idx / float(FPS)
    
    cur_sc = scene_schedule[-1]
    for sc in scene_schedule:
        if sc["start"] <= t < sc["end"]:
            cur_sc = sc
            break
            
    rel_t = t - cur_sc["start"]
    sc_dur = cur_sc["duration"]
    progress_in_scene = rel_t / sc_dur
    effect = cur_sc["effect"]
    accent = cur_sc["accent"]
    
    # 1. Base Canvas - Warm Vibrant Street Food Palette
    img = Image.new("RGBA", (WIDTH, HEIGHT), color=(18, 12, 28, 255))
    draw = ImageDraw.Draw(img)
    
    # 2. Dynamic Camera Zoom / Pan on 3D Baby Image
    # Compute Zoom Factor based on effect
    if effect == "zoom_in":
        zoom = 1.0 + progress_in_scene * 0.15
        shake_x, shake_y = 0, 0
    elif effect == "shake_fire":
        zoom = 1.15 + math.sin(rel_t * 18.0) * 0.04
        # Hilarious spicy camera shake
        shake_x = int(math.sin(rel_t * 30.0) * 12)
        shake_y = int(math.cos(rel_t * 25.0) * 8)
    elif effect == "bounce":
        zoom = 1.05 + abs(math.sin(rel_t * 8.0)) * 0.06
        shake_x, shake_y = 0, int(math.sin(rel_t * 8.0) * -8)
    elif effect == "triumph":
        zoom = 1.1 + math.sin(rel_t * 5.0) * 0.05
        shake_x, shake_y = 0, 0
    else:  # pulse_cta
        zoom = 1.0 + math.sin(rel_t * 4.0) * 0.04
        shake_x, shake_y = 0, 0

    # Scale and center the 3D baby image
    base_w = 660
    base_h = 660
    curr_w = int(base_w * zoom)
    curr_h = int(base_h * zoom)
    
    scaled_baby = raw_baby.resize((curr_w, curr_h), Image.Resampling.LANCZOS)
    
    # Frame & Center Coordinates
    baby_cx = WIDTH // 2 + shake_x
    baby_cy = 490 + shake_y
    
    bx1 = baby_cx - curr_w // 2
    by1 = baby_cy - curr_h // 2
    
    # 3. Ambient Glow behind baby portrait
    if effect == "shake_fire":
        # Spicy Fiery Red Flash
        draw.ellipse([WIDTH//2 - 320, 200, WIDTH//2 + 320, 800], fill=(220, 38, 38, 140))
        draw.ellipse([WIDTH//2 - 200, 300, WIDTH//2 + 200, 700], fill=(245, 158, 11, 100))
    else:
        # Warm Golden Sunset Glow
        draw.ellipse([WIDTH//2 - 320, 200, WIDTH//2 + 320, 800], fill=(245, 158, 11, 120))
        draw.ellipse([WIDTH//2 - 200, 300, WIDTH//2 + 200, 700], fill=(236, 72, 153, 60))

    # Paste baby image with rounded decorative frame
    crop_w = 640
    crop_h = 640
    cropped_baby = ImageOps.fit(scaled_baby, (crop_w, crop_h), method=Image.Resampling.LANCZOS)
    
    # Outer Glowing Border
    draw.rounded_rectangle([36 + shake_x, 166 + shake_y, 684 + shake_x, 814 + shake_y], radius=32, fill=(24, 18, 38, 255), outline=accent, width=6)
    
    # Inner baby image
    mask_b = Image.new("L", (crop_w, crop_h), 0)
    ImageDraw.Draw(mask_b).rounded_rectangle([0, 0, crop_w, crop_h], radius=26, fill=255)
    img.paste(cropped_baby, (40 + shake_x, 170 + shake_y), mask_b)

    # 4. Spicy Fire / Steam overlays if spicy scene
    if effect == "shake_fire":
        # Draw comic steam puffs
        steam_y = 140 + int(math.sin(rel_t * 12.0) * 10)
        draw.ellipse([120, steam_y, 170, steam_y + 40], fill=(255, 255, 255, 200))
        draw.ellipse([WIDTH - 170, steam_y, WIDTH - 120, steam_y + 40], fill=(255, 255, 255, 200))

    # 5. TOP CRAWLER / VIRAL COMEDY TAG
    draw.rounded_rectangle([40, 45, 680, 115], radius=20, fill=(35, 20, 50, 250), outline=accent, width=3)
    draw.text((65, 58), cur_sc["headline"], font=font_huge, fill="white")
    
    # 6. BIG BOUNCY COMEDY SUBTITLES IN HINDI & ENGLISH (The 7M View Style)
    sub_y = 860
    draw.rounded_rectangle([30, sub_y, WIDTH - 30, sub_y + 240], radius=28, fill=(20, 12, 32, 250), outline=accent, width=4)
    
    # Hindi Punchline (Large bold yellow with shadow)
    hi_text = cur_sc["sub_hi"]
    draw.text((52, sub_y + 27), hi_text, font=font_sub_hi, fill=(20, 10, 5, 255))
    draw.text((50, sub_y + 25), hi_text, font=font_sub_hi, fill="#FBBF24")  # Bright Yellow
    
    # English Subtitle (Cyan / White)
    en_text = cur_sc["sub_en"]
    draw.text((50, sub_y + 105), en_text, font=font_sub_en, fill="#38BDF8")
    
    # Funny Reaction Emoji Ribbon
    emojis_str = "🤣 😂 🤤 🌶️ 🥟 👶 ❤️"
    draw.text((50, sub_y + 165), emojis_str, font=font_tag, fill="white")

    # 7. Bottom Subscribe / Follow Banner
    draw.rounded_rectangle([40, 1130, WIDTH - 40, 1220], radius=18, fill=(220, 38, 38, 240), outline="#FBBF24", width=3)
    pulse_btn = math.sin(t * 6.0) * 4
    draw.text((70, 1150), "▶ SUBSCRIBE FOR DAILY FUNNY SHORTS!", font=font_big, fill="white")

    # 8. Continuous Bottom Progress Bar
    prog_pct = min(1.0, t / total_duration)
    draw.rectangle([0, HEIGHT - 10, int(WIDTH * prog_pct), HEIGHT], fill=accent)

    rgb_img = img.convert("RGB")
    proc.stdin.write(rgb_img.tobytes())

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"🎉 3D PIXAR BABY COMEDY SHORT RENDERED SUCCESSFULLY!")
print(f"Output File: {output_mp4}")
print(f"Total Duration: {total_duration:.2f}s")
print("="*60)
