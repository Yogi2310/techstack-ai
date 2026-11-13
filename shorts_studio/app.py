import os
import sys
import re
import datetime
from flask import Flask, render_template, request, jsonify, send_file, Response

# Add parent directory to sys.path so we can import upload_to_youtube
WORKSPACE_DIR = r"D:\Antigravity\Pro"
STUDIO_DIR = os.path.join(WORKSPACE_DIR, "shorts_studio")
EXPORTS_DIR = os.path.join(STUDIO_DIR, "exports")
TEMP_DIR = os.path.join(STUDIO_DIR, "temp")
LOGO_PATH = os.path.join(WORKSPACE_DIR, "youtube-shorts-factory", "yts-logo.png")

if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)
if STUDIO_DIR not in sys.path:
    sys.path.insert(0, STUDIO_DIR)

os.makedirs(EXPORTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

from video_engine import generate_video_from_scenes
from upload_to_youtube import upload_video

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    token_path = os.path.join(WORKSPACE_DIR, "youtube_token.pickle")
    has_token = os.path.exists(token_path)
    
    # List existing MP4s
    videos = []
    for root in [WORKSPACE_DIR, EXPORTS_DIR]:
        if os.path.exists(root):
            for f in os.listdir(root):
                if f.endswith(".mp4"):
                    full_p = os.path.join(root, f)
                    stat = os.stat(full_p)
                    videos.append({
                        "name": f,
                        "size_mb": round(stat.st_size / (1024 * 1024), 2),
                        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
    return jsonify({
        "youtube_connected": has_token,
        "videos": videos
    })

@app.route("/videos/<filename>")
def serve_video(filename):
    # Check in EXPORTS_DIR first, then WORKSPACE_DIR
    p1 = os.path.join(EXPORTS_DIR, filename)
    p2 = os.path.join(WORKSPACE_DIR, filename)
    target = p1 if os.path.exists(p1) else (p2 if os.path.exists(p2) else None)
    
    if not target:
        return "Video not found", 404
        
    return send_file(target, mimetype="video/mp4")

@app.route("/api/generate", methods=["POST"])
def api_generate():
    try:
        data = request.json or {}
        title = data.get("title", "Untitled Short")
        scenes = data.get("scenes", [])
        
        if not scenes:
            return jsonify({"success": False, "error": "No scenes provided"}), 400
            
        # Clean safe filename
        safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', title.lower())[:30].strip('_')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"short_{safe_title}_{timestamp}.mp4"
        out_path = os.path.join(EXPORTS_DIR, filename)
        
        print(f"\n[STUDIO] Rendering short: {filename} with {len(scenes)} scenes...")
        result = generate_video_from_scenes(
            scenes=scenes,
            output_mp4=out_path,
            temp_dir=TEMP_DIR,
            logo_path=LOGO_PATH
        )
        
        # Also copy to root workspace for easy access
        root_copy = os.path.join(WORKSPACE_DIR, filename)
        try:
            import shutil
            shutil.copy2(out_path, root_copy)
        except Exception as e:
            print(f"Copy note: {e}")
            
        return jsonify({
            "success": True,
            "filename": filename,
            "duration": round(result["total_duration"], 2),
            "frames": result["total_frames"]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/upload", methods=["POST"])
def api_upload():
    try:
        data = request.json or {}
        video_filename = data.get("video_filename")
        title = data.get("title")
        description = data.get("description", "")
        tags = data.get("tags", ["shorts"])
        publish_at = data.get("publish_at") # ISO 8601 UTC string or null
        
        # Locate video file
        p1 = os.path.join(EXPORTS_DIR, video_filename)
        p2 = os.path.join(WORKSPACE_DIR, video_filename)
        file_path = p1 if os.path.exists(p1) else (p2 if os.path.exists(p2) else None)
        
        if not file_path:
            return jsonify({"success": False, "error": f"File {video_filename} not found."}), 404
            
        print(f"\n[STUDIO] Uploading '{title}' (Publish at: {publish_at})...")
        video_id = upload_video(
            file_path=file_path,
            title=title,
            description=description,
            tags=tags,
            publish_at=publish_at
        )
        
        if not video_id:
            return jsonify({"success": False, "error": "Upload failed. Check console log."}), 500
            
        return jsonify({
            "success": True,
            "video_id": video_id,
            "watch_url": f"https://youtu.be/{video_id}",
            "shorts_url": f"https://www.youtube.com/shorts/{video_id}",
            "publish_at": publish_at
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = 5050
    print(f"\n" + "="*60)
    print(f"🎬 SHORTS STUDIO PRO STARTED!")
    print(f"👉 Open in browser: http://localhost:{port}")
    print(f"="*60 + "\n")
    app.run(host="127.0.0.1", port=port, debug=False)
