@echo off
echo ============================================
echo  Office Walk Animation - Remotion Renderer
echo ============================================
echo.
echo Starting render: 1080x1920 @ 60fps, 300 frames (5 seconds)
echo Output: out\office-walk.mp4
echo.

if not exist out mkdir out

npx remotion render src/Root.tsx OfficeWalk out/office-walk.mp4 --codec=h264 --image-format=jpeg --jpeg-quality=95

echo.
echo Done! Video saved to out\office-walk.mp4
pause
