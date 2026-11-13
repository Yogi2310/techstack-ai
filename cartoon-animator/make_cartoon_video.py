import os
import re
import sys
import time
import urllib.parse
import urllib.request
import asyncio
import edge_tts
from PIL import Image
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ════════════════════════════════════════════════════════════════
# 🎬 TOONSCRIPT 3D PIXAR AUTOMATED VIDEO GENERATOR (100% FREE)
# ════════════════════════════════════════════════════════════════

SAMPLE_SCRIPT = """
(scene: sunny Indian village street with thatched roofs, palm trees, colorful houses)
Narrator: Deep in a beautiful sunny Indian village, Raju was walking with his drum.

Raju: Come on little bear! Let's play a fun beat together!

(scene: cute fluffy black bear cub dancing beside Raju in red kurta, bright vibrant morning light)
Narrator: The cute fluffy bear cub started dancing happily to the rhythm of the drum!

Bear: Yay! This is the happiest day in the village!

(scene: village kids and people waving and smiling at Raju and the bear cub under green trees)
Narrator: All the village children joined in and danced along under the shade of the banyan trees!
"""

async def generate_speech(text, voice, output_audio_path):
    """Generates natural AI voiceover audio using free Edge-TTS"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)

def download_3d_pixar_image(scene_desc, output_img_path, seed=42):
    """Generates high-definition 3D Pixar-style scene image via Pollinations AI (100% Free)"""
    prompt = f"3D Pixar Disney style animated cartoon scene, {scene_desc}, vibrant lighting, octane render, 8k resolution, highly detailed"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={seed}"
    
    print(f"Generating 3D Pixar scene image...")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(output_img_path, 'wb') as f:
                    f.write(response.read())
            print(f"Image successfully downloaded!")
            return
        except Exception as e:
            print(f"Attempt {attempt+1} failed ({e}), retrying...")
            time.sleep(2)
            
    # Fallback placeholder image if network drops
    img = Image.new('RGB', (1280, 720), color=(30, 40, 80))
    img.save(output_img_path)

def parse_script(script_text):
    """Parses a text script into distinct scene blocks with narration/dialogue"""
    scenes = []
    current_scene_desc = "sunny Indian village with colorful houses"
    current_lines = []
    
    for line in script_text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        scene_match = re.match(r'\(scene:\s*([^)]+)\)', line, re.IGNORECASE)
        if scene_match:
            if current_lines:
                scenes.append({'desc': current_scene_desc, 'text': " ".join(current_lines)})
                current_lines = []
            current_scene_desc = scene_match.group(1)
        else:
            clean_text = re.sub(r'^[A-Za-z0-9_ ]+:\s*', '', line)
            clean_text = re.sub(r'\([a-zA-Z]+\)', '', clean_text).strip()
            if clean_text:
                current_lines.append(clean_text)
                
    if current_lines:
        scenes.append({'desc': current_scene_desc, 'text': " ".join(current_lines)})
        
    return scenes

def build_cartoon_video(script_text=SAMPLE_SCRIPT, output_filename="3D_Pixar_Cartoon_Story.mp4"):
    print("\nStarting Free 3D Pixar Cartoon Video Generator...")
    os.makedirs("temp_build", exist_ok=True)
    
    scenes = parse_script(script_text)
    print(f"Parsed {len(scenes)} scenes from script.\n")
    
    video_clips = []
    voices = ["en-US-AnaNeural", "en-US-ChristopherNeural", "en-US-EricNeural"]
    
    for i, scene in enumerate(scenes):
        idx = i + 1
        print(f"----------------------------------------")
        print(f"Processing Scene {idx}/{len(scenes)}: {scene['desc'][:40]}...")
        
        img_path = f"temp_build/scene_{idx}.jpg"
        audio_path = f"temp_build/scene_{idx}.mp3"
        
        # 1. Download 3D Pixar Image
        download_3d_pixar_image(scene['desc'], img_path, seed=100+idx*25)
        time.sleep(1)
        
        # 2. Generate Voiceover Audio
        voice = voices[i % len(voices)]
        print(f"Generating voiceover narration...")
        asyncio.run(generate_speech(scene['text'], voice, audio_path))
        
        # 3. Create Video Clip matching audio duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration + 0.5
        
        img_clip = ImageClip(img_path).with_duration(duration)
        img_clip = img_clip.with_audio(audio_clip)
        
        video_clips.append(img_clip)
        print(f"Scene {idx} built successfully! Duration: {duration:.1f}s")

    print(f"\nConcatenating all scenes into final video output...")
    final_video = concatenate_videoclips(video_clips, method="compose")
    final_video.write_videofile(
        output_filename,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )
    
    print(f"\nSUCCESS! Your 3D Pixar Cartoon Video has been created:")
    print(f"Output file: {os.path.abspath(output_filename)}")
    
    if sys.platform == "win32":
        os.startfile(output_filename)

if __name__ == "__main__":
    build_cartoon_video()
