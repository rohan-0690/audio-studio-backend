@echo off
echo ========================================
echo   Push Backend to GitHub
echo ========================================
echo.
echo Your code is ready to push!
echo.
echo IMPORTANT: First create the repository on GitHub:
echo 1. Go to: https://github.com/new
echo 2. Repository name: audio-splitter-backend
echo 3. Make it PUBLIC
echo 4. DO NOT initialize with README
echo 5. Click "Create repository"
echo.
pause
echo.
echo Now pushing your code...
echo.

git remote add origin https://github.com/rohan-0690/audio-splitter-backend.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   Done!
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://railway.app
echo 2. Login with GitHub
echo 3. New Project - Deploy from GitHub
echo 4. Select: audio-splitter-backend
echo 5. Wait for deployment
echo 6. Generate Domain
echo 7. Copy the URL
echo.
echo Then update Flutter app with the Railway URL!
echo.
pause
