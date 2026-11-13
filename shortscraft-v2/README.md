# ShortsCraft 2.0 — YouTube Shorts Generator

Auto-generate viral YouTube Shorts with **unique photo backgrounds** per segment using live Picsum photos + Unsplash topic scenes.

## 🚀 Live Demo
**[https://yogi2310.github.io/ShortsCraft/](https://yogi2310.github.io/ShortsCraft/)**

## ✨ Features
- 🎬 Auto-generates complete YouTube Shorts (60s videos)
- 🖼️ **Every segment gets a DIFFERENT background image** — no repeats
- 📷 Picsum Photos for canvas (CORS-safe, unique per generation)
- 🔥 Topic categories: BJP Watch 🪳, CJP Justice ⚖️, Politics 🏛️, Science 🔬, Sports ⚽, Tech 💻, Nature 🌿, Facts 🧠
- 🎵 Auto-generated background music per mood
- ⬇️ Export as `.webm` video files
- 🌗 Glassmorphism dark-mode UI

## 🛠️ Tech Stack
- Vanilla HTML + CSS + JavaScript (ES Modules)
- Canvas API for video rendering
- MediaRecorder API for video export
- Web Audio API for music generation
- No build step — runs directly in browser

## 📦 Run Locally
```bash
python -m http.server 3000
# Open http://localhost:3000
```

## 📁 Structure
```
shortscraft-v2/
├── index.html          # Main app
├── style.css           # Glassmorphism dark UI
└── src/
    ├── main.js         # App orchestrator
    ├── backgrounds.js  # Photo URL builder (Picsum + Unsplash)
    ├── templates.js    # Canvas video renderer (cinematic grading)
    ├── generator.js    # Content database
    ├── animations.js   # Canvas animation helpers
    └── music.js        # Web Audio music generator
```
