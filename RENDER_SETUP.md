# 🚀 Render.com Setup Guide

Quick setup guide for deploying Plant Disease Detection backend to Render.com.

## ✅ Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
3. **Model File** - Ensure `backend/app/models/best_model.pth` is committed to Git

## 🚀 Quick Setup Steps

### Step 1: Prepare Your Repository

1. **Ensure model file is committed:**
   ```bash
   git add backend/app/models/best_model.pth
   git commit -m "Add model file"
   git push
   ```

2. **Verify these files exist:**
   - ✅ `backend/requirements.txt`
   - ✅ `backend/Procfile`
   - ✅ `backend/runtime.txt`
   - ✅ `backend/app/models/best_model.pth`

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

### Step 3: Deploy Backend

1. **Go to Render Dashboard:**
   - Visit [dashboard.render.com](https://dashboard.render.com)

2. **Create New Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Choose "Connect GitHub" or "Connect GitLab"
   - Select your repository

3. **Configure Service:**
   - **Name**: `plant-disease-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend` ⚠️ **Important!**
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or choose your plan)

4. **Set Environment Variables:**
   Click "Environment" tab and add:
   ```
   PYTHONPATH = /opt/render/project/src
   CORS_ORIGINS = *
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Wait for deployment to complete (5-10 minutes first time)

### Step 4: Get Your Backend URL

Once deployed, Render will provide a URL:
- Example: `https://plant-disease-backend.onrender.com`
- Copy this URL for frontend configuration

### Step 5: Test Backend

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

## 🔧 Configuration Details

### Start Command
```
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables
| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHONPATH` | `/opt/render/project/src` | Python path for imports |
| `CORS_ORIGINS` | `*` or your frontend URL | CORS allowed origins |
| `PORT` | Auto-set | Render port (don't change) |

### Root Directory
Set to `backend` so Render knows to look in the backend folder.

## 🐛 Troubleshooting

### Model Not Loading
- Ensure model file is committed to Git
- Check Render logs: Dashboard → Your Service → Logs
- Verify file path is correct

### Import Errors
- Verify `PYTHONPATH` is set to `/opt/render/project/src`
- Check all dependencies in `requirements.txt`
- Review build logs

### Port Errors
- Render automatically sets `PORT` environment variable
- Use `$PORT` in start command
- Don't hardcode port numbers

### Service Spins Down
- Normal on free tier (spins down after 15 min inactivity)
- First request after spin-down takes longer (cold start)
- Consider upgrading for always-on service

## 📊 Monitoring

- **View Logs**: Dashboard → Your Service → Logs
- **View Metrics**: Dashboard → Your Service → Metrics
- **View Events**: Dashboard → Your Service → Events

## 🔗 Next Steps

1. ✅ Backend deployed on Render
2. ✅ Backend URL copied
3. ✅ Deploy frontend to Vercel
4. ✅ Set `VITE_API_URL` in Vercel dashboard
5. ✅ Test full application

## 📖 See Also

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment guide
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - 5-minute quick start
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Detailed Render guide

---

**Your backend is now live on Render!** 🎉

