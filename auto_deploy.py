#!/usr/bin/env python3
"""
Automated Deployment Script for Plant Disease Detection
This script prepares everything for deployment and provides step-by-step instructions
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} NOT FOUND: {filepath}")
        return False

def check_git_repo():
    """Check if this is a git repository"""
    try:
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("Git repository detected")
            return True
        else:
            print_warning("Not a git repository")
            print_info("Run: git init")
            return False
    except FileNotFoundError:
        print_error("Git not installed")
        return False

def check_git_remote():
    """Check if GitHub remote is configured"""
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            print_success(f"GitHub remote configured: {remote_url}")
            return True
        else:
            print_warning("GitHub remote not configured")
            print_info("Run: git remote add origin <your-github-repo-url>")
            return False
    except:
        return False

def check_model_file():
    """Check if model file exists"""
    model_path = Path("backend/app/models/best_model.pth")
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print_success(f"Model file found: {model_path} ({size_mb:.2f} MB)")
        return True
    else:
        print_error(f"Model file NOT FOUND: {model_path}")
        print_warning("Model file must exist and be committed to Git for Render deployment")
        return False

def check_git_status():
    """Check git status and uncommitted changes"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print_warning("You have uncommitted changes")
            print_info("Files with changes:")
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
            return False
        else:
            print_success("All changes committed")
            return True
    except:
        return False

def verify_backend_config():
    """Verify backend configuration files"""
    print_header("Verifying Backend Configuration")
    
    files_to_check = [
        ("backend/requirements.txt", "Requirements file"),
        ("backend/Procfile", "Procfile"),
        ("backend/runtime.txt", "Runtime file"),
        ("backend/app/main.py", "Main application file"),
        ("backend/app/models/disease_model.py", "Model file"),
    ]
    
    all_ok = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    # Check model file separately
    model_ok = check_model_file()
    
    return all_ok and model_ok

def verify_frontend_config():
    """Verify frontend configuration files"""
    print_header("Verifying Frontend Configuration")
    
    files_to_check = [
        ("frontend/package.json", "Package.json"),
        ("frontend/vite.config.ts", "Vite config"),
        ("frontend/vercel.json", "Vercel config"),
        ("frontend/src/App.tsx", "Main app component"),
        ("frontend/src/config.ts", "Config file"),
    ]
    
    all_ok = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    return all_ok

def create_deployment_instructions():
    """Create deployment instructions file"""
    instructions = """
# 🚀 Automated Deployment Instructions

## Prerequisites Checklist
- [ ] GitHub account created
- [ ] Render account created (https://render.com)
- [ ] Vercel account created (https://vercel.com)
- [ ] Repository pushed to GitHub
- [ ] Model file committed to Git

## Step 1: Prepare Repository

### 1.1 Commit Model File (if not already committed)
```bash
git add backend/app/models/best_model.pth
git commit -m "Add model file for deployment"
git push origin main
```

### 1.2 Verify Repository is on GitHub
- Go to your GitHub repository
- Ensure all files are pushed
- Verify `backend/app/models/best_model.pth` exists in repository

## Step 2: Deploy Backend to Render

### 2.1 Go to Render Dashboard
1. Visit: https://dashboard.render.com
2. Sign up or log in (free tier available)

### 2.2 Create New Web Service
1. Click "New +" button
2. Select "Web Service"
3. Click "Connect GitHub" (or "Connect GitLab")
4. Authorize Render to access your repositories
5. Select your repository

### 2.3 Configure Backend Service
Fill in these settings:

**Basic Settings:**
- **Name**: `plant-disease-backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Branch**: `main` (or your default branch)
- **Root Directory**: `backend` ⚠️ **IMPORTANT!**

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: Free (or choose your plan)

**Environment Variables:**
Click "Environment" tab and add:
- `PYTHONPATH` = `/opt/render/project/src`
- `CORS_ORIGINS` = `*` (or your frontend URL later)

### 2.4 Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes first time)
3. Monitor build logs
4. Copy your backend URL (e.g., `https://plant-disease-backend.onrender.com`)

### 2.5 Test Backend
```bash
curl https://your-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Step 3: Deploy Frontend to Vercel

### 3.1 Install Vercel CLI
```bash
npm install -g vercel
```

### 3.2 Deploy Frontend
```bash
cd frontend
vercel --prod
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? (Select your account)
- Link to existing project? **No**
- Project name? (e.g., `plant-disease-frontend`)
- Directory? **./**
- Override settings? **No**

### 3.3 Set Environment Variable
1. Go to Vercel Dashboard: https://vercel.com
2. Select your project
3. Go to "Settings" → "Environment Variables"
4. Add new variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend.onrender.com` (your Render backend URL)
   - **Environment**: Production, Preview, Development
5. Click "Save"

### 3.4 Redeploy
1. Go to "Deployments" tab
2. Click "Redeploy" on latest deployment
   OR
   Run: `vercel --prod`

### 3.5 Get Frontend URL
Your app will be available at:
`https://your-project.vercel.app`

## Step 4: Test Full Application

1. Open your frontend URL in browser
2. Upload a test image
3. Verify prediction works
4. Check browser console for errors

## Step 5: Update CORS (Optional)

In Render dashboard, update `CORS_ORIGINS`:
- Remove `*`
- Add your frontend URL: `https://your-project.vercel.app`

Then restart the service in Render dashboard.

## 🎉 Success!

Your application is now live and accessible to anyone!

**Frontend URL:** https://your-project.vercel.app
**Backend URL:** https://your-backend.onrender.com
**API Docs:** https://your-backend.onrender.com/docs

## 📊 Monitoring

- **Render Logs:** Dashboard → Your Service → Logs
- **Vercel Logs:** Dashboard → Deployments → View Logs

## 🆘 Troubleshooting

If backend doesn't load:
- Check Render logs
- Verify model file is in Git repository
- Check `PYTHONPATH` is set correctly

If frontend can't connect:
- Verify `VITE_API_URL` is set correctly
- Check backend is running
- Test backend URL directly

## 📝 Notes

- Render free tier spins down after 15 min inactivity
- First request after spin-down takes longer (cold start)
- Consider upgrading for always-on service
"""
    
    with open("DEPLOYMENT_INSTRUCTIONS.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print_success("Deployment instructions created: DEPLOYMENT_INSTRUCTIONS.md")

def create_deployment_checklist():
    """Create deployment checklist"""
    checklist = """
# ✅ Deployment Checklist

## Pre-Deployment
- [ ] All files committed to Git
- [ ] Repository pushed to GitHub
- [ ] Model file (`backend/app/models/best_model.pth`) exists and is committed
- [ ] Backend requirements.txt is up to date
- [ ] Frontend package.json is up to date
- [ ] All tests pass locally

## Backend Deployment (Render)
- [ ] Render account created
- [ ] GitHub repository connected to Render
- [ ] Web service created with correct settings:
  - [ ] Root Directory: `backend`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables set:
  - [ ] `PYTHONPATH`: `/opt/render/project/src`
  - [ ] `CORS_ORIGINS`: `*` (or frontend URL)
- [ ] Service deployed successfully
- [ ] Backend URL copied
- [ ] Health check passes: `curl https://your-backend.onrender.com/health`

## Frontend Deployment (Vercel)
- [ ] Vercel account created
- [ ] Vercel CLI installed
- [ ] Frontend deployed to Vercel
- [ ] Environment variable set: `VITE_API_URL`
- [ ] Frontend redeployed after setting environment variable
- [ ] Frontend URL copied

## Post-Deployment
- [ ] Frontend accessible at Vercel URL
- [ ] Backend accessible at Render URL
- [ ] Image upload works
- [ ] Prediction works
- [ ] CORS updated (if needed)
- [ ] Application tested end-to-end
- [ ] URLs shared with team/users

## Optional
- [ ] Custom domain configured
- [ ] Analytics added
- [ ] Error monitoring set up
- [ ] Performance monitoring configured
"""
    
    with open("DEPLOYMENT_CHECKLIST.md", "w", encoding="utf-8") as f:
        f.write(checklist)
    
    print_success("Deployment checklist created: DEPLOYMENT_CHECKLIST.md")

def generate_deployment_summary():
    """Generate deployment summary"""
    print_header("Deployment Summary")
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "backend": {
            "platform": "Render.com",
            "config_files": [
                "backend/requirements.txt",
                "backend/Procfile",
                "backend/runtime.txt",
                "backend/render.yaml"
            ],
            "environment_variables": {
                "PYTHONPATH": "/opt/render/project/src",
                "CORS_ORIGINS": "* (or frontend URL)",
                "PORT": "Auto-set by Render"
            },
            "start_command": "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT"
        },
        "frontend": {
            "platform": "Vercel",
            "config_files": [
                "frontend/package.json",
                "frontend/vite.config.ts",
                "frontend/vercel.json"
            ],
            "environment_variables": {
                "VITE_API_URL": "https://your-backend.onrender.com"
            },
            "build_command": "npm run build"
        },
        "model_file": "backend/app/models/best_model.pth"
    }
    
    with open("deployment_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    
    print_success("Deployment summary saved: deployment_summary.json")
    print_info("See DEPLOYMENT_INSTRUCTIONS.md for detailed steps")
    print_info("See DEPLOYMENT_CHECKLIST.md for checklist")

def main():
    print_header("Plant Disease Detection - Automated Deployment Preparation")
    
    # Check prerequisites
    print_header("Checking Prerequisites")
    
    git_repo = check_git_repo()
    git_remote = check_git_remote() if git_repo else False
    model_exists = check_model_file()
    git_clean = check_git_status() if git_repo else False
    
    # Verify configurations
    backend_ok = verify_backend_config()
    frontend_ok = verify_frontend_config()
    
    # Create deployment files
    print_header("Creating Deployment Files")
    create_deployment_instructions()
    create_deployment_checklist()
    generate_deployment_summary()
    
    # Final summary
    print_header("Deployment Readiness")
    
    issues = []
    if not git_repo:
        issues.append("Git repository not initialized")
    if not git_remote:
        issues.append("GitHub remote not configured")
    if not model_exists:
        issues.append("Model file not found")
    if not git_clean:
        issues.append("Uncommitted changes detected")
    if not backend_ok:
        issues.append("Backend configuration issues")
    if not frontend_ok:
        issues.append("Frontend configuration issues")
    
    if issues:
        print_warning("⚠️  Issues found:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n⚠️  Please fix these issues before deploying")
    else:
        print_success("✅ All checks passed!")
        print_success("✅ Ready for deployment!")
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("=" * 60)
    print("\n1. Review DEPLOYMENT_INSTRUCTIONS.md")
    print("2. Follow the step-by-step guide")
    print("3. Use DEPLOYMENT_CHECKLIST.md to track progress")
    print("\n🚀 Your application is ready to deploy!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

