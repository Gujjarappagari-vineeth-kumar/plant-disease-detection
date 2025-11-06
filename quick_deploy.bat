@echo off
REM Quick Deployment Script for Plant Disease Detection
echo ============================================================
echo   Plant Disease Detection - Quick Deployment
echo ============================================================
echo.

echo Step 1: Checking Git status...
git status --short
echo.

echo Step 2: Adding all files...
git add .
echo.

echo Step 3: Committing changes...
git commit -m "Ready for deployment - Render + Vercel"
echo.

echo Step 4: Pushing to GitHub...
git push origin main
echo.

echo ============================================================
echo   Git Push Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Open DEPLOY_NOW.md for step-by-step deployment guide
echo 2. Deploy backend to Render: https://dashboard.render.com
echo 3. Deploy frontend to Vercel: https://vercel.com
echo.
echo ============================================================
pause

