
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
