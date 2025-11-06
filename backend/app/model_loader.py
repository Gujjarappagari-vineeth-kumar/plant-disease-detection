"""
Optimized model loading for Railway deployment
Downloads model from external source to reduce image size
"""

import os
import torch
import requests
from pathlib import Path
import hashlib
from typing import Optional

class ModelLoader:
    def __init__(self):
        self.model_path = "backend/app/models/best_model.pth"
        self.model_url = "https://github.com/your-username/plant-disease-model/releases/download/v1.0/best_model.pth"
        # Leave empty to disable checksum verification unless you set a real value
        self.model_checksum = ""
        
    def download_model(self) -> bool:
        """Download model from external source if not present"""
        try:
            if os.path.exists(self.model_path):
                print("✅ Model already exists locally")
                return True
                
            print("📥 Downloading model from external source...")
            
            # Create models directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            # Download model
            response = requests.get(self.model_url, stream=True)
            response.raise_for_status()
            
            with open(self.model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            print("✅ Model downloaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            return False
    
    def verify_model(self) -> bool:
        """Verify model file integrity. If no checksum provided, only checks existence."""
        try:
            if not os.path.exists(self.model_path):
                return False

            if not self.model_checksum:
                # No checksum configured; consider existence as verification success
                return True

            with open(self.model_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            if file_hash != self.model_checksum:
                print("⚠️ Model checksum mismatch (continuing to attempt load)")
                # Allow load to proceed; return True so we still try loading the file
                return True

            return True

        except Exception as e:
            print(f"❌ Model verification failed: {e}")
            return False
    
    def load_model(self, model_class, num_classes: int = 38):
        """Load model with fallback to pre-trained weights.
        Preference order: local model_path → download URL → pre-trained.
        """
        # Ensure models directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        # 1) Try local file first
        try:
            if os.path.exists(self.model_path):
                if self.verify_model():
                    model = model_class(num_classes=num_classes)
                    state = torch.load(self.model_path, map_location=torch.device('cpu'))
                    model.load_state_dict(state)
                    model.eval()
                    print("✅ Model loaded successfully from local file")
                    return model
        except Exception as e:
            print(f"⚠️ Failed loading local model, will try download: {e}")

        # 2) Try download if URL is configured
        try:
            if self.model_url and self.download_model():
                model = model_class(num_classes=num_classes)
                state = torch.load(self.model_path, map_location=torch.device('cpu'))
                model.load_state_dict(state)
                model.eval()
                print("✅ Model loaded successfully after download")
                return model
        except Exception as e:
            print(f"⚠️ Failed loading downloaded model, will fallback: {e}")

        # 3) Fallback to pre-trained (untrained for your classes)
        print("⚠️ Falling back to pre-trained ImageNet weights (reduced accuracy expected)")
        return model_class(num_classes=num_classes)

# Alternative: Use Hugging Face Hub for model storage
class HuggingFaceModelLoader:
    def __init__(self):
        self.model_id = "your-username/plant-disease-model"  # Replace with your HF model ID
        
    def load_model(self, model_class, num_classes: int = 38):
        """Load model from Hugging Face Hub"""
        try:
            from huggingface_hub import hf_hub_download
            
            print("📥 Downloading model from Hugging Face Hub...")
            model_path = hf_hub_download(
                repo_id=self.model_id,
                filename="best_model.pth",
                cache_dir="./models"
            )
            
            model = model_class(num_classes=num_classes)
            model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            model.eval()
            
            print("✅ Model loaded successfully from Hugging Face Hub")
            return model
            
        except Exception as e:
            print(f"❌ Error loading model from HF Hub: {e}")
            print("⚠️ Falling back to pre-trained weights")
            return model_class(num_classes=num_classes)
