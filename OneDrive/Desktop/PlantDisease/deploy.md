# 🚀 Plant Disease Detection App - Deployment Guide

This guide will help you deploy your Plant Disease Detection app to Railway (backend) and Vercel (frontend) so it's accessible worldwide!

## 🌐 **Deployment Overview**

- **Backend**: Railway (Python FastAPI)
- **Frontend**: Vercel (React + TypeScript)
- **Database**: Railway (if needed)
- **File Storage**: Railway (for model files)

## 📋 **Prerequisites**

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Railway Account** - [railway.app](https://railway.app)
3. **Vercel Account** - [vercel.com](https://vercel.com)
4. **Node.js & npm** - For CLI tools

## 🚀 **Quick Deployment (Automated)**

### **Option 1: Use the deployment script**
```bash
# On Windows
deploy.bat

# On Mac/Linux
chmod +x deploy.sh
./deploy.sh
```

### **Option 2: Manual deployment steps**

## 🔧 **Step 1: Deploy Backend to Railway**

### **1.1 Install Railway CLI**
```bash
npm install -g @railway/cli
```

### **1.2 Login to Railway**
```bash
railway login
```

### **1.3 Navigate to backend directory**
```bash
cd backend
```

### **1.4 Deploy to Railway**
```bash
railway up
```

### **1.5 Get your Railway URL**
- Go to [railway.app](https://railway.app)
- Find your project
- Copy the generated URL (e.g., `https://your-app.up.railway.app`)

## 🌐 **Step 2: Deploy Frontend to Vercel**

### **2.1 Install Vercel CLI**
```bash
npm install -g vercel
```

### **2.2 Navigate to frontend directory**
```bash
cd frontend
```

### **2.3 Create environment file**
Create `.env.production` file:
```env
VITE_API_URL=https://your-railway-url.up.railway.app
```

### **2.4 Deploy to Vercel**
```bash
vercel --prod
```

### **2.5 Get your Vercel URL**
- Go to [vercel.com](https://vercel.com)
- Find your project
- Copy the generated URL (e.g., `https://your-app.vercel.app`)

## 🔗 **Step 3: Connect Frontend to Backend**

### **3.1 Update CORS in backend**
In `backend/app/main.py`, ensure CORS allows your Vercel domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **3.2 Redeploy backend**
```bash
cd backend
railway up
```

## 🧪 **Step 4: Test Your Deployment**

### **4.1 Test Backend**
Visit: `https://your-railway-url.up.railway.app/health`
Should show: `{"status": "healthy", "model_loaded": true}`

### **4.2 Test Frontend**
Visit your Vercel URL and try uploading an image!

## 🔧 **Environment Variables**

### **Railway (Backend)**
- `PORT`: Automatically set by Railway
- `MODEL_PATH`: Path to your trained model

### **Vercel (Frontend)**
- `VITE_API_URL`: Your Railway backend URL

## 📁 **File Structure After Deployment**

```
your-app/
├── backend/          # Deployed to Railway
│   ├── app/
│   ├── requirements.txt
│   ├── railway.json
│   └── Procfile
├── frontend/         # Deployed to Vercel
│   ├── src/
│   ├── package.json
│   └── vercel.json
└── deploy.sh         # Deployment script
```

## 🚨 **Troubleshooting**

### **Backend Issues**
- **Port binding error**: Railway sets `$PORT` automatically
- **Model not found**: Ensure model file is in the correct path
- **CORS errors**: Check CORS settings in `main.py`

### **Frontend Issues**
- **API connection error**: Verify `VITE_API_URL` in environment
- **Build errors**: Check for TypeScript/React errors
- **Deployment failed**: Check Vercel logs

## 🌍 **Making Your App Public**

### **1. Share your Vercel URL**
Your app is now accessible at: `https://your-app.vercel.app`

### **2. Custom Domain (Optional)**
- Go to Vercel dashboard
- Add custom domain
- Configure DNS settings

### **3. SEO & Analytics**
- Add Google Analytics
- Configure meta tags
- Submit to search engines

## 🎯 **Next Steps**

1. **Train your model** and upload to Railway
2. **Test with real images** from different devices
3. **Monitor performance** in Railway/Vercel dashboards
4. **Share your app** with the world! 🌍

## 📞 **Support**

- **Railway**: [docs.railway.app](https://docs.railway.app)
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

**🎉 Congratulations! Your Plant Disease Detection app is now live on the internet!**
