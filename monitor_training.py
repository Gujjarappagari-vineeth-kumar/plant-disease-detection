#!/usr/bin/env python3
"""
Monitor the training progress of the 38-class Plant Disease model
"""

import os
import time
import psutil
from datetime import datetime

def check_training_status():
    """Check if training is running and monitor progress"""
    print("🔍 Monitoring 38-Class Plant Disease Model Training...")
    print("=" * 60)
    
    # Check for running Python processes
    python_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python.exe':
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'train_kaggle' in cmdline or 'app.train_kaggle' in cmdline:
                    python_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if python_processes:
        print("✅ Training is RUNNING!")
        print(f"📊 Found {len(python_processes)} training process(es):")
        for proc in python_processes:
            print(f"   PID: {proc['pid']}")
            print(f"   Command: {proc['cmdline']}")
    else:
        print("❌ No training process found")
    
    print("\n📁 Checking model file status...")
    
    # Check model file
    model_path = "backend/app/models/best_model.pth"
    if os.path.exists(model_path):
        model_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        mod_time = datetime.fromtimestamp(os.path.getmtime(model_path))
        print(f"✅ Model file exists: {model_size:.1f} MB")
        print(f"📅 Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check if it's a 38-class model
        try:
            import torch
            from backend.app.models.disease_model import PlantDiseaseModel
            
            # Try to load the model
            model = PlantDiseaseModel(num_classes=38)
            model.load_state_dict(torch.load(model_path, map_location='cpu'))
            print("✅ Model loads successfully with 38 classes!")
            
            # Check output size
            output_size = model.model.fc[-1].out_features
            print(f"🎯 Model output size: {output_size} classes")
            
            if output_size == 38:
                print("🎉 SUCCESS: 38-class model is ready!")
            else:
                print(f"⚠️ Warning: Expected 38 classes, got {output_size}")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    else:
        print("❌ Model file not found - training may not have started")
    
    print("\n📊 Dataset Status:")
    dataset_path = "backend/dataset/PlantVillage_Full"
    if os.path.exists(dataset_path):
        classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
        print(f"✅ Full dataset found: {len(classes)} classes")
        print(f"📁 Dataset path: {dataset_path}")
        
        # Show first few classes
        print("📋 Sample classes:")
        for i, class_name in enumerate(sorted(classes)[:10]):
            print(f"   {i+1:2d}. {class_name}")
        if len(classes) > 10:
            print(f"   ... and {len(classes) - 10} more classes")
    else:
        print("❌ Full dataset not found")
    
    print("\n" + "=" * 60)
    
    if python_processes:
        print("🔄 Training is in progress...")
        print("💡 Run this script again to check updated status")
    else:
        print("⏹️ No training process detected")
        print("💡 To start training: cd backend && python -m app.train_kaggle")

if __name__ == "__main__":
    check_training_status()
