# 🚀 START HERE - Deploy Your App to www

## ✅ Everything is Ready! Just Follow These Steps

Your project is **100% configured** and ready to deploy. Follow these steps to get your app live on the internet!

---

## 📋 Pre-Deployment Checklist

✅ All code is ready  
✅ All configurations are perfect  
✅ Model file is prepared  
✅ Backend config is ready  
✅ Frontend config is ready  

**Just need to:**
1. Push to Git (if not done)
2. Deploy backend to Render
3. Deploy frontend to Vercel

---

## 🎯 STEP 1: Push to GitHub (1 minute)

### Option A: Use the Script
Double-click: **`quick_deploy.bat`**

### Option B: Manual (PowerShell)
```powershell
git add .
git commit -m "Ready for deployment"
git push origin main
```

**Verify:** Go to https://github.com/Gujjarappagari-vineeth-kumar/plant-disease-detection and make sure all files are there.

---

## 🎯 STEP 2: Deploy Backend to Render (5 minutes)

### Go to Render Dashboard
**Open:** https://dashboard.render.com

### Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. **Connect GitHub** → Select your repository
3. **Configure with these EXACT values:**

```
Name: plant-disease-backend
Environment: Python 3
Region: (Choose closest)
Branch: main
Root Directory: backend ⚠️ IMPORTANT!

Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

### Add Environment Variables
Click **"Environment"** tab and add:

```
Variable 1:
  Key: PYTHONPATH
  Value: /opt/render/project/src

Variable 2:
  Key: CORS_ORIGINS
  Value: *
```

### Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes (first deployment)
3. **Copy your backend URL** (e.g., `https://plant-disease-backend.onrender.com`)

### Test Backend
Open in browser: `https://your-backend-url.onrender.com/health`

Should see: `{"status": "healthy", "model_loaded": true}`

✅ **Backend is live!**

---

## 🎯 STEP 3: Deploy Frontend to Vercel (3 minutes)

### Install Vercel CLI (if needed)
```powershell
npm install -g vercel
```

### Deploy Frontend
```powershell
cd frontend
vercel --prod
```

**Answer prompts:**
- Set up and deploy? **Y**
- Which scope? **1** (your account)
- Link to existing? **N**
- Project name? **plant-disease-frontend**
- Directory? **./**
- Override settings? **N**

### Set Environment Variable (CRITICAL!)

1. Go to: **https://vercel.com/dashboard**
2. Click your project: **`plant-disease-frontend`**
3. **Settings** → **Environment Variables**
4. Click **"Add New"**
5. Fill in:
   ```
   Name: VITE_API_URL
   Value: https://your-backend-url.onrender.com (paste your Render URL!)
   Environment: Select all three (Production, Preview, Development)
   ```
6. Click **"Save"**

### Redeploy
1. Go to **"Deployments"** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**

**OR** run:
```powershell
vercel --prod
```

### Get Your Frontend URL
Go to **"Deployments"** → Click latest deployment → Copy URL

✅ **Frontend is live!**

---

## 🎉 SUCCESS! Your App is Live!

### Your Live URLs:
- **Frontend:** `https://your-project.vercel.app` ← **Share this with users!**
- **Backend:** `https://your-backend.onrender.com`
- **API Docs:** `https://your-backend.onrender.com/docs`

### Test Your App:
1. Open your frontend URL
2. Upload a plant leaf image
3. See disease detection results!

---

## 📚 Detailed Guides

- **DEPLOY_NOW.md** - Complete step-by-step guide with all details
- **DEPLOYMENT_CHECKLIST.md** - Track your progress
- **DEPLOYMENT_INSTRUCTIONS.md** - Detailed reference

---

## 🆘 Need Help?

### Backend Issues?
- Check Render logs: Dashboard → Your Service → Logs
- Verify `PYTHONPATH` is set correctly
- Ensure model file is in Git repository

### Frontend Issues?
- Verify `VITE_API_URL` is set correctly
- Make sure you redeployed after setting variable
- Test backend health endpoint first

---

## 📝 Quick Reference

### Backend Settings (Render)
```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
Environment Variables:
  - PYTHONPATH = /opt/render/project/src
  - CORS_ORIGINS = *
```

### Frontend Settings (Vercel)
```
Environment Variable:
  - VITE_API_URL = https://your-backend.onrender.com
```

---

**🚀 Ready? Start with STEP 1 above!**

Your app will be live on the internet in just 10 minutes! 🌍





