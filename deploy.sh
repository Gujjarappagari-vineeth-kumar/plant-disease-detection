#!/bin/bash

# Plant Disease Detection - Complete Deployment Script
# This script helps deploy both backend and frontend

set -e

echo "🌱 Plant Disease Detection - Deployment Script"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Render CLI is installed (optional)
check_render_cli() {
    if command -v render &> /dev/null; then
        print_info "Render CLI found"
        return 0
    else
        print_warning "Render CLI not found (optional - you can deploy via web dashboard)"
        return 1
    fi
}

# Check if Vercel CLI is installed
check_vercel_cli() {
    if command -v vercel &> /dev/null; then
        print_info "Vercel CLI found"
        return 0
    else
        print_warning "Vercel CLI not found. Installing..."
        npm install -g vercel || {
            print_error "Failed to install Vercel CLI"
            return 1
        }
    fi
}

# Deploy Backend (Instructions for Render)
deploy_backend() {
    echo ""
    echo "📦 Deploying Backend to Render..."
    echo "-----------------------------------"
    
    if [ ! -d "backend" ]; then
        print_error "Backend directory not found!"
        return 1
    fi
    
    # Check if model file exists
    if [ ! -f "backend/app/models/best_model.pth" ]; then
        print_warning "Model file not found at backend/app/models/best_model.pth"
        print_warning "Deployment will continue, but model may not load correctly"
    fi
    
    print_info "Render deployment is done via web dashboard:"
    echo ""
    echo "1. Go to https://dashboard.render.com"
    echo "2. Click 'New +' → 'Web Service'"
    echo "3. Connect your GitHub repository"
    echo "4. Select the 'backend' directory"
    echo "5. Configure:"
    echo "   - Name: plant-disease-backend"
    echo "   - Runtime: Python 3"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port \$PORT"
    echo "   - Environment: Python 3.9"
    echo "6. Add Environment Variables:"
    echo "   - PYTHONPATH: /opt/render/project/src"
    echo "   - CORS_ORIGINS: * (or your frontend URL)"
    echo "7. Click 'Create Web Service'"
    echo ""
    print_info "After deployment, copy your Render backend URL from the dashboard"
    
    read -p "Enter your Render backend URL (or press Enter to skip): " BACKEND_URL
    if [ ! -z "$BACKEND_URL" ]; then
        echo "BACKEND_URL=$BACKEND_URL" > .deployment.env
        print_info "Backend URL saved: $BACKEND_URL"
    fi
    
    return 0
}

# Deploy Frontend
deploy_frontend() {
    echo ""
    echo "🎨 Deploying Frontend to Vercel..."
    echo "-----------------------------------"
    
    if [ ! -d "frontend" ]; then
        print_error "Frontend directory not found!"
        return 1
    fi
    
    cd frontend
    
    # Read backend URL
    if [ -f "../.deployment.env" ]; then
        source ../.deployment.env
    else
        read -p "Enter your backend URL: " BACKEND_URL
    fi
    
    if [ -z "$BACKEND_URL" ]; then
        print_error "Backend URL is required!"
        cd ..
        return 1
    fi
    
    # Build frontend
    print_info "Building frontend..."
    npm install
    npm run build
    
    # Deploy to Vercel
    print_info "Deploying to Vercel..."
    
    # Set environment variable
    export VITE_API_URL=$BACKEND_URL
    
    # Deploy
    vercel --prod --yes || {
        print_warning "Deployment may require manual configuration"
        print_info "Please set VITE_API_URL=$BACKEND_URL in Vercel dashboard"
    }
    
    cd ..
    print_info "Frontend deployment initiated!"
    print_info "Check Vercel dashboard for deployment URL"
    
    return 0
}

# Main deployment function
main() {
    echo "Select deployment option:"
    echo "1) Deploy Backend only (Render - via web dashboard)"
    echo "2) Deploy Frontend only (Vercel)"
    echo "3) Deploy Both (Full Stack)"
    echo "4) Exit"
    echo ""
    read -p "Enter choice [1-4]: " choice
    
    case $choice in
        1)
            deploy_backend
            ;;
        2)
            check_vercel_cli
            deploy_frontend
            ;;
        3)
            deploy_backend
            if [ $? -eq 0 ]; then
                check_vercel_cli
                deploy_frontend
            fi
            ;;
        4)
            print_info "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    echo ""
    print_info "Deployment completed!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Verify backend is accessible at your Render URL"
    echo "2. Verify frontend is accessible at your Vercel URL"
    echo "3. Test the application end-to-end"
    echo "4. Share your public URL with others!"
    echo ""
    echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
}

# Run main function
main
