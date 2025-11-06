@echo off
REM Plant Disease Detection - Windows Deployment Script

echo 🌱 Plant Disease Detection - Deployment Script
echo ==============================================
echo.

REM Check if Vercel CLI is installed
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Vercel CLI not found. Installing...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Vercel CLI
        pause
        exit /b 1
    )
)

echo.
echo Select deployment option:
echo 1) Deploy Backend only (Render - via web dashboard)
echo 2) Deploy Frontend only (Vercel)
echo 3) Deploy Both (Full Stack)
echo 4) Exit
echo.
set /p choice="Enter choice [1-4]: "

if "%choice%"=="1" goto deploy_backend
if "%choice%"=="2" goto deploy_frontend
if "%choice%"=="3" goto deploy_both
if "%choice%"=="4" goto end
goto invalid

:deploy_backend
echo.
echo 📦 Deploying Backend to Render...
echo -----------------------------------
echo.
echo Render deployment is done via web dashboard:
echo.
echo 1. Go to https://dashboard.render.com
echo 2. Click 'New +' → 'Web Service'
echo 3. Connect your GitHub repository
echo 4. Select the 'backend' directory
echo 5. Configure:
echo    - Name: plant-disease-backend
echo    - Runtime: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
echo    - Environment: Python 3.9
echo 6. Add Environment Variables:
echo    - PYTHONPATH: /opt/render/project/src
echo    - CORS_ORIGINS: * (or your frontend URL)
echo 7. Click 'Create Web Service'
echo.
echo After deployment, copy your Render backend URL from the dashboard
echo.
set /p BACKEND_URL="Enter your Render backend URL (or press Enter to skip): "
if not "%BACKEND_URL%"=="" (
    echo BACKEND_URL=%BACKEND_URL% > .deployment.env
    echo ✅ Backend URL saved: %BACKEND_URL%
)
goto end

:deploy_frontend
echo.
echo 🎨 Deploying Frontend to Vercel...
echo -----------------------------------
if exist ".deployment.env" (
    for /f "tokens=2 delims==" %%a in ('.deployment.env') do set BACKEND_URL=%%a
)
if "%BACKEND_URL%"=="" (
    set /p BACKEND_URL="Enter your backend URL: "
)
if "%BACKEND_URL%"=="" (
    echo ❌ Backend URL is required!
    pause
    exit /b 1
)
if not exist "frontend" (
    echo ❌ Frontend directory not found!
    pause
    exit /b 1
)
cd frontend
call npm install
call npm run build
set VITE_API_URL=%BACKEND_URL%
call vercel --prod --yes
echo.
echo ✅ Frontend deployed! Check Vercel dashboard for URL
cd ..
goto end

:deploy_both
call :deploy_backend
echo.
echo Please note your backend URL from Render dashboard, then press any key to continue...
pause >nul
call :deploy_frontend
goto end

:invalid
echo ❌ Invalid choice
pause
exit /b 1

:end
echo.
echo ✅ Deployment completed!
echo.
echo 📋 Next Steps:
echo 1. Verify backend is accessible at your Render URL
echo 2. Verify frontend is accessible at your Vercel URL
echo 3. Test the application end-to-end
echo 4. Share your public URL with others!
echo.
echo 📖 For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
pause
