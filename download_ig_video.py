"""
Instagram Video & Reel Downloader Utility
Uses yt-dlp to download Instagram Reels, Posts, and Videos, saving them locally for playback and analysis.
"""
import os
import sys
import json
import yt_dlp

def download_instagram_video(url, output_dir=r"D:\Antigravity\Pro\instagram_downloads"):
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(id)s_%(title).50s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
    }
    
    print(f"[*] Fetching and downloading Instagram media from: {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # Ensure mp4 extension if merged
        base, _ = os.path.splitext(filename)
        mp4_path = base + ".mp4"
        final_path = mp4_path if os.path.exists(mp4_path) else filename
        
        print(f"\n[+] Successfully downloaded to: {final_path}")
        print(f"Title / Caption: {info.get('title', 'N/A')}")
        print(f"Uploader: {info.get('uploader', 'N/A')}")
        return final_path, info

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        download_instagram_video(target_url)
    else:
        print("Usage: python download_ig_video.py <INSTAGRAM_URL>")
