"""
TaleBlox / Riyo 3D - Automated Instagram Reels Publisher
Uses instagrapi to automatically post master videos to Instagram as Reels.
"""
import os
import sys
import json
import argparse
from instagrapi import Client

SESSION_FILE = r"D:\Antigravity\Pro\instagram_session.json"
CREDENTIALS_FILE = r"D:\Antigravity\Pro\instagram_credentials.json"

def get_client(username=None, password=None):
    cl = Client()
    cl.delay_range = [2, 5]

    # Try loading existing session
    if os.path.exists(SESSION_FILE):
        try:
            print("[*] Loading existing Instagram session...")
            cl.load_settings(SESSION_FILE)
            cl.get_timeline_feed()
            print("[✓] Session loaded successfully!")
            return cl
        except Exception as e:
            print(f"[!] Session expired or invalid: {e}. Re-authenticating...")

    # Load credentials if not provided
    if not username or not password:
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                creds = json.load(f)
                username = creds.get('username')
                password = creds.get('password')
        else:
            print(f"[!] No credentials found. Please provide username and password or create {CREDENTIALS_FILE}")
            sys.exit(1)

    print(f"[*] Logging into Instagram as @{username}...")
    cl.login(username, password)
    cl.dump_settings(SESSION_FILE)
    print(f"[✓] Successfully logged in and saved session to {SESSION_FILE}!")
    return cl

def upload_reel(video_path, caption, cover_path=None, username=None, password=None):
    if not os.path.exists(video_path):
        print(f"[!] Video not found: {video_path}")
        return False

    cl = get_client(username, password)
    print(f"\n[*] Uploading Reel: {os.path.basename(video_path)} ({os.path.getsize(video_path) / (1024*1024):.2f} MB)...")
    print(f"    Caption: {caption[:100]}...")

    media = cl.clip_upload(
        path=video_path,
        caption=caption,
        thumbnail=cover_path
    )
    print("\n" + "="*50)
    print(f"[SUCCESS] Reel uploaded to Instagram!")
    print(f"    Media PK: {media.pk}")
    print(f"    Reel URL: https://www.instagram.com/reel/{media.code}/")
    print("="*50)
    return media.code

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload Reel to Instagram")
    parser.add_argument("--video", required=True, help="Path to MP4 video")
    parser.add_argument("--caption", default="", help="Reel caption")
    parser.add_argument("--cover", default=None, help="Cover image path")
    parser.add_argument("--username", default=None, help="Instagram username")
    parser.add_argument("--password", default=None, help="Instagram password")

    args = parser.parse_args()
    upload_reel(args.video, args.caption, args.cover, args.username, args.password)
