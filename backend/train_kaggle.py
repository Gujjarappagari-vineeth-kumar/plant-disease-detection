#!/usr/bin/env python3
"""
Script to train the Plant Disease model using Kaggle PlantVillage dataset
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.train_kaggle import train_plant_disease_model

if __name__ == "__main__":
    print("🌱 Starting Plant Disease Model Training with Kaggle Dataset")
    print("=" * 60)
    
    try:
        train_plant_disease_model()
        print("\n🎉 Training completed successfully!")
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        sys.exit(1)
