# 🚀 DEPLOY NOW - Step-by-Step with Exact Values

## ✅ Everything is Ready! Just Follow These Steps

Your repository: `https://github.com/Gujjarappagari-vineeth-kumar/plant-disease-detection.git`

---

## PART 1: Deploy Backend to Render (5 minutes)

### Step 1: Go to Render Dashboard
1. Open: **https://dashboard.render.com**
2. Click **"Sign Up"** or **"Log In"** (use free tier)
3. Sign up with **GitHub** (recommended)

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect GitHub"** (or "Connect GitLab")
4. Authorize Render to access your repositories
5. Find and select: **`plant-disease-detection`**

### Step 3: Configure Backend (Copy-Paste These Values)

**Basic Settings:**
- **Name:** `plant-disease-backend`
- **Environment:** `Python 3`
- **Region:** Choose closest (e.g., `Oregon (US West)`)
- **Branch:** `main`
- **Root Directory:** `backend` ⚠️ **VERY IMPORTANT!**

**Build & Deploy Settings:**
- **Runtime:** `Python 3`
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
  ```
- **Plan:** `Free` (or choose your plan)

### Step 4: Add Environment Variables

Click **"Environment"** tab and add these **one by one**:

1. **First Variable:**
   - **Key:** `PYTHONPATH`
   - **Value:** `/opt/render/project/src`
   - Click **"Add"**

2. **Second Variable:**
   - **Key:** `CORS_ORIGINS`
   - **Value:** `*`
   - Click **"Add"**

### Step 5: Deploy
1. Scroll down
2. Click **"Create Web Service"**
3. **Wait** for deployment (5-10 minutes first time)
4. Watch the build logs - it will show progress

### Step 6: Get Your Backend URL
1. After deployment completes, you'll see your service
2. At the top, you'll see a URL like: `https://plant-disease-backend.onrender.com`
3. **COPY THIS URL** - you'll need it for frontend!

### Step 7: Test Backend
Open this URL in your browser:
```
https://your-backend-url.onrender.com/health
```

You should see:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "available_classes": 38
}
```

✅ **Backend is now live!**

---

## PART 2: Deploy Frontend to Vercel (3 minutes)

### Step 1: Install Vercel CLI (if not installed)
Open **PowerShell** or **Command Prompt** and run:
```bash
npm install -g vercel
```

### Step 2: Navigate to Frontend
```bash
cd frontend
```

### Step 3: Deploy to Vercel
```bash
vercel --prod
```

**Follow the prompts:**
- Set up and deploy? → Type: `Y` and press Enter
- Which scope? → Select your account (usually option 1)
- Link to existing project? → Type: `N` and press Enter
- Project name? → Type: `plant-disease-frontend` and press Enter
- Directory? → Type: `./` and press Enter
- Override settings? → Type: `N` and press Enter

### Step 4: Set Environment Variable (IMPORTANT!)

1. Go to: **https://vercel.com/dashboard**
2. Click on your project: **`plant-disease-frontend`**
3. Click **"Settings"** (top menu)
4. Click **"Environment Variables"** (left sidebar)
5. Click **"Add New"** button
6. Fill in:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://your-backend-url.onrender.com` (paste your Render backend URL here!)
   - **Environment:** Select all three (Production, Preview, Development)
7. Click **"Save"**

### Step 5: Redeploy Frontend
1. Go to **"Deployments"** tab
2. Click **"..."** (three dots) on the latest deployment
3. Click **"Redeploy"**
4. Confirm redeployment

**OR** run this command:
```bash
vercel --prod
```

### Step 6: Get Your Frontend URL
1. Go to **"Deployments"** tab
2. Click on the latest deployment
3. You'll see your URL at the top: `https://plant-disease-frontend.vercel.app`
4. **COPY THIS URL** - this is your live app!

✅ **Frontend is now live!**

---

## PART 3: Final Configuration

### Update CORS in Render (Optional but Recommended)

1. Go back to **Render Dashboard**
2. Click on your **`plant-disease-backend`** service
3. Go to **"Environment"** tab
4. Find **`CORS_ORIGINS`** variable
5. Click **"Edit"**
6. Change value from `*` to your frontend URL:
   ```
   https://your-frontend-url.vercel.app
   ```
7. Click **"Save Changes"**
8. Service will automatically restart

---

## 🎉 SUCCESS! Your App is Live!

### Your Live URLs:
- **Frontend (User App):** `https://plant-disease-frontend.vercel.app`
- **Backend API:** `https://plant-disease-backend.onrender.com`
- **API Documentation:** `https://plant-disease-backend.onrender.com/docs`

### Test Your App:
1. Open your frontend URL in browser
2. Upload a plant leaf image
3. See the disease detection results!

---

## 📊 Monitoring

### View Backend Logs:
- Go to: **https://dashboard.render.com**
- Click your service → **"Logs"** tab

### View Frontend Logs:
- Go to: **https://vercel.com/dashboard**
- Click your project → **"Deployments"** → Click deployment → **"Logs"**

---

## 🆘 Troubleshooting

### Backend not working?
- Check Render logs for errors
- Verify `PYTHONPATH` is set correctly
- Ensure model file is in Git repository

### Frontend can't connect?
- Verify `VITE_API_URL` is set correctly in Vercel
- Check backend is running (test health endpoint)
- Make sure you redeployed after setting environment variable

### First request is slow?
- Normal on Render free tier (service spins down after 15 min)
- First request after spin-down takes longer (cold start)
- Consider upgrading for always-on service

---

**🎊 Congratulations! Your Plant Disease Detection app is now live on the internet!**

Share your frontend URL with anyone - they can access it from anywhere in the world! 🌍





