# Render.com Deployment Guide - Plant Disease Detection

This guide will help you deploy your Plant Disease Detection project to Render.com (free tier available).

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **Node.js**: For Vercel CLI installation (frontend)
4. **Git**: For version control

## Quick Deployment Steps

### Step 1: Deploy Backend to Render

1. **Go to Render Dashboard:**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign up or log in (free tier available)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Backend Service:**
   - **Name**: `plant-disease-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or choose your plan)

4. **Set Environment Variables:**
   Click "Environment" and add:
   - `PYTHONPATH`: `/opt/render/project/src`
   - `CORS_ORIGINS`: `*` (or your frontend URL like `https://your-app.vercel.app`)
   - `PORT`: Automatically set by Render (don't change)

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy
   - Wait for deployment to complete (5-10 minutes first time)

6. **Get Your Backend URL:**
   - Once deployed, Render will provide a URL like: `https://plant-disease-backend.onrender.com`
   - Copy this URL for the frontend configuration

### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to Frontend:**
   ```bash
   cd frontend
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

4. **Set Environment Variable:**
   - In Vercel dashboard → Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend.onrender.com`
   - Redeploy after adding the variable

---

## Manual Deployment Process

### Backend Configuration

The backend is already configured with:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Process configuration
- ✅ `runtime.txt` - Python version
- ✅ `render.yaml` - Render configuration (optional)

### Frontend Configuration

The frontend is configured with:
- ✅ `package.json` - Node.js dependencies
- ✅ `vercel.json` - Vercel configuration
- ✅ Environment variable support (`VITE_API_URL`)

---

## Project Structure

```
PlantDisease/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── model.py        # Model definition
│   │   └── models/
│   │       ├── disease_model.py
│   │       └── best_model.pth
│   ├── requirements.txt    # Python dependencies
│   ├── Procfile           # Process configuration
│   └── runtime.txt        # Python version
├── frontend/              # React Frontend
│   ├── src/
│   │   ├── App.tsx
│   │   └── components/
│   ├── package.json
│   └── vercel.json       # Vercel configuration
└── render.yaml          # Render configuration
```

---

## API Endpoints

Once deployed, your API will be available at:
- `https://your-backend.onrender.com/` - Health check
- `https://your-backend.onrender.com/health` - Detailed health check
- `https://your-backend.onrender.com/predict` - Disease prediction
- `https://your-backend.onrender.com/docs` - API documentation

---

## Testing Deployment

1. **Health Check:**
   ```bash
   curl https://your-backend.onrender.com/health
   ```

2. **Test Prediction:**
   ```bash
   curl -X POST "https://your-backend.onrender.com/predict" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@test_image.jpg"
   ```

---

## Troubleshooting

### Common Issues

1. **Import Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check `PYTHONPATH` is set correctly

2. **Model Loading Issues:**
   - Verify model file exists in `backend/app/models/`
   - Check file is committed to Git repository
   - Model file should be in repository (Render needs access)

3. **Port Issues:**
   - Render automatically sets `PORT` environment variable
   - Use `$PORT` in your start command
   - Don't hardcode port numbers

4. **CORS Errors:**
   - Update `CORS_ORIGINS` environment variable in Render
   - Add your frontend URL: `https://your-frontend.vercel.app`
   - Restart service after updating environment variables

### Logs

View deployment logs in Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. View real-time logs

### Debugging

1. **Check Render dashboard** for deployment status
2. **View logs** for error messages
3. **Test locally** before deploying:
   ```bash
   cd backend
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```

---

## Environment Variables

Set these in Render dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | Auto-set | Render port (don't change) |
| `PYTHONPATH` | `/opt/render/project/src` | Python path |
| `CORS_ORIGINS` | `*` or your frontend URL | CORS allowed origins |
| `ENVIRONMENT` | `production` | Environment type (optional) |

---

## Cost Optimization

- Render offers free tier with limited resources
- Free tier services may spin down after inactivity (15 minutes)
- First request after spin-down takes longer (cold start)
- Monitor usage in Render dashboard
- Consider upgrading for production use

---

## Security Notes

- Update CORS settings for production
- Use environment variables for sensitive data
- Don't use `*` for CORS in production (use specific domains)
- Implement rate limiting for production

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Update frontend API URLs
4. ✅ Test full application
5. ✅ Set up monitoring and logging
6. ✅ Configure custom domain (optional)

---

## Support

- Render Documentation: https://render.com/docs
- Render Support: https://render.com/support
- Project Issues: Create GitHub issue

---

## Free Tier Notes

Render's free tier includes:
- ✅ 750 hours per month (enough for 24/7 single service)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Services spin down after 15 minutes of inactivity
- ⚠️ Slower cold starts (first request after spin-down)

For production, consider upgrading to a paid plan for better performance.

