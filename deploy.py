#!/usr/bin/env python3
"""
Plant Disease Detection - Python Deployment Script
Helps deploy both backend and frontend with a simple interface
Now using Render (free tier) instead of Railway
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_info(msg):
    print(f"✅ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def check_command(cmd):
    """Check if a command exists"""
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_vercel_cli():
    """Install Vercel CLI"""
    print_warning("Installing Vercel CLI...")
    try:
        subprocess.run(["npm", "install", "-g", "vercel"], check=True)
        print_info("Vercel CLI installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install Vercel CLI")
        print_info("Please install manually: npm install -g vercel")
        return False

def deploy_backend():
    """Deploy backend to Render (instructions)"""
    print("\n📦 Deploying Backend to Render...")
    print("-" * 40)
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print_error("Backend directory not found!")
        return None
    
    # Check if model exists
    model_path = backend_dir / "app" / "models" / "best_model.pth"
    if not model_path.exists():
        print_warning(f"Model file not found at {model_path}")
        print_warning("Deployment will continue, but model may not load")
    
    print_info("Render deployment is done via web dashboard:")
    print()
    print("1. Go to https://dashboard.render.com")
    print("2. Click 'New +' → 'Web Service'")
    print("3. Connect your GitHub repository")
    print("4. Select the 'backend' directory")
    print("5. Configure:")
    print("   - Name: plant-disease-backend")
    print("   - Runtime: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT")
    print("   - Environment: Python 3.9")
    print("6. Add Environment Variables:")
    print("   - PYTHONPATH: /opt/render/project/src")
    print("   - CORS_ORIGINS: * (or your frontend URL)")
    print("7. Click 'Create Web Service'")
    print()
    print_info("After deployment, copy your Render backend URL from the dashboard")
    
    backend_url = input("Enter your Render backend URL (or press Enter to skip): ").strip()
    if backend_url:
        with open(".deployment.env", "w") as f:
            f.write(f"BACKEND_URL={backend_url}\n")
        print_info(f"Backend URL saved: {backend_url}")
        return backend_url
    
    return None

def deploy_frontend(backend_url=None):
    """Deploy frontend to Vercel"""
    print("\n🎨 Deploying Frontend to Vercel...")
    print("-" * 40)
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print_error("Frontend directory not found!")
        return None
    
    # Get backend URL
    if not backend_url:
        # Try to read from .deployment.env
        env_file = Path(".deployment.env")
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("BACKEND_URL="):
                        backend_url = line.split("=", 1)[1].strip()
                        break
        
        if not backend_url:
            backend_url = input("Enter your backend URL: ").strip()
            if not backend_url:
                print_error("Backend URL is required")
                return None
    
    # Check Vercel CLI
    if not check_command("vercel"):
        if not install_vercel_cli():
            return None
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    try:
        # Build frontend
        print_info("Building frontend...")
        subprocess.run(["npm", "install"], check=True)
        subprocess.run(["npm", "run", "build"], check=True)
        
        # Set environment variable
        env = os.environ.copy()
        env["VITE_API_URL"] = backend_url
        
        # Deploy
        print_info("Deploying to Vercel...")
        subprocess.run(["vercel", "--prod", "--yes"], env=env, check=True)
        
        print_info("Frontend deployed! Check Vercel dashboard for URL")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Deployment failed: {e}")
        print_warning("You may need to set VITE_API_URL in Vercel dashboard manually")
        return None
    finally:
        # Return to original directory
        os.chdir("..")

def main():
    print("🌱 Plant Disease Detection - Deployment Script")
    print("=" * 50)
    print("Using Render (free tier) for backend deployment")
    print()
    
    print("Select deployment option:")
    print("1) Deploy Backend only (Render - via web dashboard)")
    print("2) Deploy Frontend only (Vercel)")
    print("3) Deploy Both (Full Stack)")
    print("4) Exit")
    print()
    
    choice = input("Enter choice [1-4]: ").strip()
    
    if choice == "1":
        deploy_backend()
        
    elif choice == "2":
        if not check_command("vercel"):
            if not install_vercel_cli():
                sys.exit(1)
        deploy_frontend()
        
    elif choice == "3":
        # Deploy backend first
        backend_url = deploy_backend()
        if backend_url:
            print("\nProceeding to frontend deployment...")
            input("Press Enter to continue...")
            if not check_command("vercel"):
                if not install_vercel_cli():
                    sys.exit(1)
            deploy_frontend(backend_url)
        
    elif choice == "4":
        print_info("Exiting...")
        sys.exit(0)
        
    else:
        print_error("Invalid choice")
        sys.exit(1)
    
    print()
    print_info("Deployment completed!")
    print()
    print("📋 Next Steps:")
    print("1. Verify backend is accessible at your Render URL")
    print("2. Verify frontend is accessible at your Vercel URL")
    print("3. Test the application end-to-end")
    print("4. Share your public URL with others!")
    print()
    print("📖 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
