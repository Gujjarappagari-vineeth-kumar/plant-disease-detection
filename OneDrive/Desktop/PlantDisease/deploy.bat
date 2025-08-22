@echo off
echo 🚀 Starting Plant Disease Detection App Deployment...
echo ==================================================

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found. Installing...
    npm install -g @railway/cli
) else (
    echo ✅ Railway CLI found
)

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
) else (
    echo ✅ Vercel CLI found
)

echo.
echo 🌐 Deploying Backend to Railway...
echo ==================================
cd backend

REM Deploy to Railway
echo 📤 Deploying backend to Railway...
railway up

REM Get the Railway URL (you'll need to check Railway dashboard)
echo 🔗 Backend deployed! Check Railway dashboard for URL
echo ✅ Backend deployment complete!

REM Update frontend environment
cd ..\frontend
echo 🔧 Please manually update frontend environment variables:
echo    Create .env.production file with your Railway backend URL

echo.
echo 🌐 Deploying Frontend to Vercel...
echo ==================================

REM Deploy to Vercel
echo 📤 Deploying frontend to Vercel...
vercel --prod

echo.
echo 🎉 Deployment Complete!
echo ======================
echo 🔗 Backend URL: Check Railway dashboard
echo 🌐 Frontend URL: Check Vercel dashboard
echo.
echo 💡 Next Steps:
echo 1. Get your backend URL from Railway dashboard
echo 2. Update frontend .env.production with backend URL
echo 3. Test your deployed application
echo 4. Share your app with the world! 🌍

pause
