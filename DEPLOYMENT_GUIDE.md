# 🌐 Plant Disease Detection - Complete Deployment Guide

This guide will help you deploy your Plant Disease Detection application so **anyone can access it through a browser via a public link**.

**Now using Render.com (free tier) instead of Railway!**

## 📋 Table of Contents

1. [Quick Deployment](#quick-deployment)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Testing Your Deployment](#testing-your-deployment)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Deployment

### Option 1: Render + Vercel (Recommended) ⭐

**Backend on Render, Frontend on Vercel:**

1. **Deploy Backend to Render:**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure and deploy (see Step-by-Step below)

2. **Deploy Frontend to Vercel:**
   ```bash
   cd frontend
   npm install -g vercel
   vercel --prod
   # Set VITE_API_URL to your Render backend URL
   ```

---

## 📦 Prerequisites

Before deploying, ensure you have:

- ✅ **Git** installed and repository pushed to GitHub
- ✅ **Node.js** 16+ installed (for Vercel CLI)
- ✅ **Python 3.9+** installed (for local testing)
- ✅ **Model file** (`backend/app/models/best_model.pth`) exists and is committed to Git
- ✅ **Accounts** on deployment platforms:
  - [Render](https://render.com) - Free tier available ⭐
  - [Vercel](https://vercel.com) - Free tier available

---

## 🎯 Deployment Options

### Option A: Render (Backend) + Vercel (Frontend) ⭐ Recommended

**Pros:**
- Both platforms have free tiers
- Render is simple for backend deployment
- Vercel excellent for frontend (CDN, fast)
- Good performance
- Easy environment variable management

**Cons:**
- Requires managing two platforms
- Render free tier services spin down after inactivity

### Option B: Render (All-in-One)

**Pros:**
- Single platform
- Simple deployment
- Free tier available

**Cons:**
- Slower for frontend (no CDN)
- Services spin down after inactivity

---

## 📝 Step-by-Step Deployment

### Part 1: Deploy Backend to Render

#### Step 1: Prepare Backend

1. **Verify these files exist:**
   - ✅ `requirements.txt`
   - ✅ `Procfile`
   - ✅ `runtime.txt`
   - ✅ `backend/app/models/best_model.pth` (model file - must be committed to Git)

2. **Ensure model file is committed:**
   ```bash
   git add backend/app/models/best_model.pth
   git commit -m "Add model file"
   git push
   ```

#### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up for free account
3. Connect your GitHub account

#### Step 3: Deploy Backend Service

1. **Go to Render Dashboard:**
   - Visit [dashboard.render.com](https://dashboard.render.com)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service:**
   - **Name**: `plant-disease-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend` (important!)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or choose your plan)

4. **Set Environment Variables:**
   Click "Environment" tab and add:
   - `PYTHONPATH`: `/opt/render/project/src`
   - `CORS_ORIGINS`: `*` (or your frontend URL like `https://your-app.vercel.app`)
   - `PORT`: Automatically set by Render (don't change)

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Wait for deployment to complete (5-10 minutes first time)

6. **Get Your Backend URL:**
   - Once deployed, Render provides a URL like: `https://plant-disease-backend.onrender.com`
   - **Copy this URL!** You'll need it for frontend configuration

#### Step 4: Test Backend

```bash
curl https://your-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "available_classes": 38
}
```

---

### Part 2: Deploy Frontend

#### Option A: Deploy Frontend to Vercel (Recommended)

##### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

##### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

##### Step 3: Build Frontend

```bash
npm install
npm run build
```

##### Step 4: Deploy to Vercel

```bash
vercel --prod
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? (Select your account)
- Link to existing project? **No**
- Project name? (e.g., "plant-disease-frontend")
- Directory? **./**
- Override settings? **No**

##### Step 5: Set Environment Variable

In Vercel dashboard:
1. Go to your project
2. Click "Settings" → "Environment Variables"
3. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend.onrender.com` (your Render backend URL)
   - **Environment**: Production, Preview, Development

##### Step 6: Redeploy

After adding environment variable:
- Go to "Deployments" tab
- Click "Redeploy" on latest deployment
- Or trigger new deployment: `vercel --prod`

##### Step 7: Get Your Frontend URL

Your app will be available at:
`https://your-project.vercel.app`

---

## 🧪 Testing Your Deployment

### 1. Test Backend Health

```bash
curl https://your-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "available_classes": 38
}
```

### 2. Test Frontend

1. Open your frontend URL in browser
2. You should see the Plant Disease Detection interface
3. Upload a test image
4. Check if prediction works

### 3. Test API Endpoint

```bash
curl -X POST https://your-backend.onrender.com/predict \
  -F "file=@test_image.jpg"
```

---

## 🔧 Troubleshooting

### Backend Issues

#### Problem: "Model not loaded"
**Solution:**
- Verify `backend/app/models/best_model.pth` exists in Git repository
- Check Render logs: Dashboard → Logs
- Ensure model file is committed and pushed to GitHub

#### Problem: "CORS errors"
**Solution:**
- Update `CORS_ORIGINS` environment variable in Render
- Add your frontend URL: `https://your-frontend.vercel.app`
- Restart service after updating

#### Problem: "Port errors"
**Solution:**
- Render automatically sets `PORT` environment variable
- Ensure start command uses `$PORT`
- Check `Procfile` configuration

#### Problem: "Import errors"
**Solution:**
- Verify all dependencies in `requirements.txt`
- Check `PYTHONPATH` is set to `/opt/render/project/src`
- Review Render build logs

### Frontend Issues

#### Problem: "Cannot connect to API"
**Solution:**
- Verify `VITE_API_URL` environment variable is set correctly in Vercel
- Check if backend is running and accessible
- Test backend URL directly in browser
- Check browser console for errors
- Ensure no trailing slash in backend URL

#### Problem: "Build fails"
**Solution:**
- Ensure all dependencies are in `package.json`
- Check build logs in Vercel dashboard
- Test build locally: `npm run build`

#### Problem: "Environment variables not working"
**Solution:**
- Vite requires `VITE_` prefix for environment variables
- Rebuild after setting environment variables
- Check Vercel environment variable settings
- Redeploy after adding variables

#### Problem: "Render service spins down"
**Solution:**
- This is normal on free tier (spins down after 15 min inactivity)
- First request after spin-down takes longer (cold start)
- Consider upgrading to paid plan for always-on service

---

## 📊 Monitoring Your Deployment

### Render Dashboard

1. Visit [dashboard.render.com](https://dashboard.render.com)
2. View deployment logs
3. Monitor resource usage
4. Check deployment status
5. View service logs

### Vercel Dashboard

1. Visit [vercel.com](https://vercel.com)
2. View deployment analytics
3. Check build logs
4. Monitor performance

---

## 🔐 Security Best Practices

1. **CORS Configuration:**
   - Don't use `*` in production
   - Set specific frontend URLs in `CORS_ORIGINS`

2. **Environment Variables:**
   - Never commit `.env` files
   - Use platform environment variable settings

3. **API Keys:**
   - Store sensitive data in environment variables
   - Don't expose in frontend code

---

## 📱 Sharing Your Application

Once deployed, share these links:

1. **Frontend URL:** `https://your-frontend.vercel.app`
2. **Backend API:** `https://your-backend.onrender.com`
3. **API Docs:** `https://your-backend.onrender.com/docs`

---

## 🎉 Success Checklist

- [ ] Backend deployed and accessible on Render
- [ ] Frontend deployed and accessible on Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Health check passing
- [ ] Image upload working
- [ ] Prediction working
- [ ] Application accessible via public URL

---

## 📞 Getting Help

1. **Check Logs:**
   - Render: Dashboard → Your Service → Logs
   - Vercel: Dashboard → Deployments → View Logs

2. **Render Support:**
   - [Render Docs](https://render.com/docs)
   - [Render Support](https://render.com/support)

3. **Vercel Support:**
   - [Vercel Docs](https://vercel.com/docs)
   - [Vercel Community](https://github.com/vercel/vercel/discussions)

---

## 🚀 Next Steps

After successful deployment:

1. ✅ Test with multiple users
2. ✅ Monitor performance
3. ✅ Set up custom domain (optional)
4. ✅ Configure analytics (optional)
5. ✅ Set up error monitoring (optional)

---

**Congratulations!** Your Plant Disease Detection application is now live and accessible to anyone via a public URL! 🌱
