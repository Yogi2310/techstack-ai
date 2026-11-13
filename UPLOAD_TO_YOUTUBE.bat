@echo off
title YouTube Shorts Auto-Uploader
cd /d "D:\Antigravity\Pro"
echo ========================================================
echo        Auto-Uploading Video to YouTube
echo ========================================================
echo.
"C:\Users\Yogesh\AppData\Local\Programs\Python\Python313\python.exe" manual_auth_and_upload.py
echo.
pause
