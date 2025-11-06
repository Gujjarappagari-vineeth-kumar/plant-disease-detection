# 🚀 Quick Deploy - Plant Disease Detection

Get your application live in **5 minutes**!

**Now using Render.com (free tier) instead of Railway!**

## ⚡ Fastest Method (Render + Vercel)

### Step 1: Deploy Backend to Render (3 minutes)

1. **Go to Render Dashboard:**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign up or log in (free tier available)

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure:**
   - **Name**: `plant-disease-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Set Environment Variables:**
   - `PYTHONPATH`: `/opt/render/project/src`
   - `CORS_ORIGINS`: `*`

5. **Click "Create Web Service"**

6. **Copy your backend URL** from Render dashboard (e.g., `https://your-app.onrender.com`)

**Copy the backend URL** - you'll need it in Step 2!

### Step 2: Deploy Frontend to Vercel (2 minutes)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel --prod

# When prompted, set environment variable:
# VITE_API_URL = https://your-backend.onrender.com
```

**Done!** Your app is live! 🎉

---

## 📋 What You Need

- ✅ GitHub account (for code hosting)
- ✅ Render account (free): [render.com](https://render.com)
- ✅ Vercel account (free): [vercel.com](https://vercel.com)

---

## 🔗 Your URLs

After deployment, you'll have:

- **Frontend:** `https://your-app.vercel.app`
- **Backend API:** `https://your-app.onrender.com`
- **API Docs:** `https://your-app.onrender.com/docs`

---

## 🐛 Troubleshooting

### Backend not working?
- Check Render dashboard → Logs
- Verify `PYTHONPATH` is set correctly
- Ensure model file is in Git repository

### Frontend can't connect?
- Check `VITE_API_URL` environment variable in Vercel dashboard
- Make sure backend URL is correct (no trailing slash)
- Redeploy frontend after setting environment variable

### Service spins down?
- Normal on Render free tier (spins down after 15 min inactivity)
- First request after spin-down takes longer (cold start)
- Consider upgrading for always-on service

### Need help?
See `DEPLOYMENT_GUIDE.md` for detailed instructions.

---

## 📝 Quick Checklist

- [ ] Backend deployed on Render
- [ ] Backend URL copied
- [ ] Frontend deployed on Vercel
- [ ] `VITE_API_URL` environment variable set
- [ ] Application tested and working

---

**That's it!** Share your frontend URL with anyone! 🌱
