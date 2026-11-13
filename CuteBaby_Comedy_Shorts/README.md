# 👶 3D Pixar Cute Baby Comedy Shorts Project

Welcome to the **Cute Baby Comedy Shorts** automated production project. This project implements the proven, viral formula that generated **~7 Million views** on YouTube Shorts (Reference: `https://www.youtube.com/shorts/6Rw0hfwF1KE` - *Golgappe Ka Lalach*).

---

## 📁 Project Directory Structure

```
CuteBaby_Comedy_Shorts/
├── characters/
│   └── cute_ai_baby_golgappa.jpg      # Master 3D Pixar character asset (1024x1024)
├── audio/
│   ├── master_audio.wav               # Raw voiceover track (22.9s)
│   ├── demo_video_master_audio.wav    # Full mixed audio (Voice + SFX + Cartoon BGM, 28s)
│   ├── baby_comedy_full_master.mp3    # Standalone MP3 for web/mobile playback
│   └── scene_1..5_pitched.wav / mp3   # Individual scene dialogue clips
├── sfx/
│   ├── crunch.wav                     # Crispy golgappa crunch bite sound effect
│   ├── fire_sizzle.wav                # Spicy steam/fire sizzle sound effect
│   ├── boing.wav                      # Cartoon bounce boing sound effect
│   ├── chime.wav                      # Delight / bell chime sound effect
│   └── comedy_bgm.wav                 # Cheerful cartoon marimba background music loop
├── scripts/
│   ├── build_cute_baby_comedy_short.py# Direct 23s comedy short renderer
│   └── render_demo_video.py           # Complete 28s showcase demo video renderer
├── videos/
│   ├── cute_baby_golgappa_comedy.mp4  # The primary comedy Short (22.9s, 9:16)
│   └── demo_cute_baby_comedy_short.mp4# The complete demo reel with intro, outro, SFX & BGM
└── preview/
    ├── cute_baby_player.html          # Web video player
    ├── cute_baby_sampler_hub.html     # Audio & Visual interactive sampler
    └── sample_frame_1..4.jpg          # Extracted 9:16 high-res video stills
```

---

## 🎬 How to Run & Re-render

### 1. Render the Primary Comedy Short (23s)
```bash
python scripts/build_cute_baby_comedy_short.py
```

### 2. Render the Demo Video (with SFX + BGM + Intro/Outro) (28s)
```bash
python scripts/render_demo_video.py
```

---

## 🚀 YouTube SEO & Upload Strategy

- **Title:** `🤣 Golgappe Ka Lalach 😂 | Cute AI Baby Funny Comedy #shorts #funny #viral`
- **Category:** `23` (Comedy) or `24` (Entertainment)
- **Description:**
  ```
  Jab chote bache ne pehli baar spicy golgappa khaya! 🤣 Golgappe ka lalach bache ko bohot bhari pad gaya! 😂
  Like and Subscribe for daily 3D AI cute baby comedy videos! ❤️🔔
  
  #shorts #funny #ai #animation #trending #viral #cutebaby #comedy #golgappe #streetfood
  ```
- **Tags:** `cute baby, funny comedy, ai animation, pixar 3d, golgappe ka lalach, pani puri funny, viral shorts, trending shorts, hindi comedy shorts`
