#!/bin/bash

echo "🚀 Starting Plant Disease Detection App Deployment..."
echo "=================================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
else
    echo "✅ Railway CLI found"
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
else
    echo "✅ Vercel CLI found"
fi

echo ""
echo "🌐 Deploying Backend to Railway..."
echo "=================================="
cd backend

# Deploy to Railway
echo "📤 Deploying backend to Railway..."
railway up

# Get the Railway URL
echo "🔗 Getting Railway deployment URL..."
RAILWAY_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)

if [ -n "$RAILWAY_URL" ]; then
    echo "✅ Backend deployed to: $RAILWAY_URL"
    
    # Update frontend environment
    cd ../frontend
    echo "🔧 Updating frontend environment variables..."
    
    # Create .env.production file
    cat > .env.production << EOF
VITE_API_URL=$RAILWAY_URL
EOF
    
    echo "✅ Frontend environment updated with backend URL: $RAILWAY_URL"
else
    echo "❌ Failed to get Railway URL"
    exit 1
fi

echo ""
echo "🌐 Deploying Frontend to Vercel..."
echo "=================================="

# Deploy to Vercel
echo "📤 Deploying frontend to Vercel..."
vercel --prod

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "🔗 Backend URL: $RAILWAY_URL"
echo "🌐 Frontend URL: Check Vercel dashboard for your domain"
echo ""
echo "💡 Next Steps:"
echo "1. Test your backend at: $RAILWAY_URL/health"
echo "2. Test your frontend at the Vercel URL"
echo "3. Share your app with the world! 🌍"
