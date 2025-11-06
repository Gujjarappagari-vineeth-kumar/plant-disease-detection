
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
