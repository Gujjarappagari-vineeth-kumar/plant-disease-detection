#!/usr/bin/env python3
"""
Plant Disease Detection Startup Script
"""
import os
import sys
import subprocess
import time
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed or not in PATH")
    print("   Please install Node.js 16+ from https://nodejs.org/")
    return False

def check_model_file():
    """Check if the trained model exists"""
    model_path = "backend/app/models/best_model.pth"
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"✅ Trained model found: {file_size_mb:.2f} MB")
        return True
    else:
        print("❌ Trained model not found")
        print("   Run: npm run train")
        return False

def install_dependencies():
    """Install project dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Install root dependencies
    try:
        subprocess.run(['npm', 'install'], check=True)
        print("✅ Root dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install root dependencies")
        return False
    
    # Install frontend dependencies
    try:
        subprocess.run(['npm', 'install'], cwd='frontend', check=True)
        print("✅ Frontend dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False
    
    # Install backend dependencies
    try:
        if platform.system() == "Windows":
            subprocess.run(['pip', 'install', '-r', 'requirements.txt'], cwd='backend', check=True)
        else:
            subprocess.run(['pip3', 'install', '-r', 'requirements.txt'], cwd='backend', check=True)
        print("✅ Backend dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False
    
    return True

def start_application():
    """Start the application"""
    print("\n🚀 Starting Plant Disease Detection System...")
    print("   Frontend: http://localhost:5173")
    print("   Backend:  http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n   Press Ctrl+C to stop")
    
    try:
        # Start both frontend and backend
        subprocess.run(['npm', 'run', 'dev'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def main():
    print("🌿 Plant Disease Detection System")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_node_version():
        return
    
    # Check if dependencies need to be installed
    if not os.path.exists('node_modules'):
        if not install_dependencies():
            return
    
    # Check if model needs to be trained
    if not check_model_file():
        print("\n🎯 Training the model...")
        print("   This will take 10-20 minutes")
        print("   You can monitor progress in the terminal")
        
        try:
            subprocess.run(['npm', 'run', 'train'], check=True)
            print("✅ Training completed!")
        except subprocess.CalledProcessError:
            print("❌ Training failed")
            return
        except KeyboardInterrupt:
            print("\n⏹️ Training interrupted")
            return
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()
