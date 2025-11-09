"""
Optimized model loading for Render/Railway deployment.
- Downloads model from an external URL (GitHub attachments or releases).
- Supports .zip: extracts and finds best_model.pth even if nested.
- Falls back to ImageNet weights if download/parse fails.
"""

import os
import torch
import requests
import zipfile
import hashlib
import shutil

class ModelLoader:
    def __init__(self):
        # Expected final location of your model once present
        # (main.py expects to load from exactly this path)
        self.model_path = "app/models/best_model.pth"

        # ✅ USE YOUR ACTUAL WORKING LINK (you said this downloads)
        # If you later switch to a GitHub Release asset, just update this URL.
        self.model_url = "https://github.com/user-attachments/files/23437455/best_model.zip"

        # Optional checksum of .pth (leave blank to skip)
        self.model_checksum = ""

    # -------------------------
    # Internals / helpers
    # -------------------------
    def _ensure_models_dir(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def _verify_checksum(self, pth_path: str) -> bool:
        """If a checksum is configured, verify .pth integrity; else return True."""
        if not os.path.exists(pth_path):
            return False
        if not self.model_checksum:
            return True
        try:
            with open(pth_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash != self.model_checksum:
                print("⚠️ Model checksum mismatch (continuing anyway)")
            return True
        except Exception as e:
            print(f"❌ Checksum verification error: {e}")
            return False

    def _find_and_place_pth(self, root_dir: str) -> bool:
        """
        Search 'root_dir' recursively for the first .pth file.
        If found, copy/move it to self.model_path. Returns True if placed.
        """
        for dirpath, _, filenames in os.walk(root_dir):
            for name in filenames:
                if name.lower().endswith(".pth"):
                    src = os.path.join(dirpath, name)
                    # Normalize to expected file name/location
                    try:
                        shutil.move(src, self.model_path)
                    except Exception:
                        # If cross-device or permission issues, copy then remove
                        shutil.copy2(src, self.model_path)
                        try:
                            os.remove(src)
                        except Exception:
                            pass
                    return True
        return False

    # -------------------------
    # Public steps
    # -------------------------
    def download_model(self) -> bool:
        """
        Download the model file from self.model_url.
        - If URL ends with .pth, save directly.
        - If URL ends with .zip, download and extract; then locate best_model.pth.
        """
        self._ensure_models_dir()

        # Already present
        if os.path.exists(self.model_path):
            print("✅ Model already exists locally")
            return True

        if not self.model_url:
            print("⚠️ No model URL configured")
            return False

        print(f"📥 Downloading model from: {self.model_url}")

        try:
            resp = requests.get(self.model_url, stream=True)
            resp.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            return False

        # Direct .pth URL case
        if self.model_url.lower().endswith(".pth"):
            try:
                with open(self.model_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("✅ Model (.pth) downloaded successfully")
                return True
            except Exception as e:
                print(f"❌ Could not save .pth: {e}")
                return False

        # .zip URL case
        zip_path = self.model_path.replace(".pth", ".zip")
        try:
            with open(zip_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("✅ Model ZIP downloaded, extracting...")
        except Exception as e:
            print(f"❌ Could not write ZIP file: {e}")
            return False

        # Extract and locate .pth
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(os.path.dirname(self.model_path))
        except Exception as e:
            print(f"❌ Failed to extract ZIP: {e}")
            return False

        # After extraction, ensure best_model.pth ends up exactly at self.model_path
        if os.path.exists(self.model_path):
            print("✅ Model extracted to expected path")
            return True

        # If the zip had subfolders, search for any .pth
        placed = self._find_and_place_pth(os.path.dirname(self.model_path))
        if placed and os.path.exists(self.model_path):
            print("✅ Model extracted and placed successfully")
            return True

        print("❌ Extracted ZIP but could not find a .pth file")
        return False

    def load_model(self, model_class, num_classes: int = 38):
        """
        Load the model in this order:
        1) Local best_model.pth (if exists)
        2) Download from self.model_url (zip or pth) → then load
        3) Fallback to pretrained ImageNet weights via model_class
        """
        self._ensure_models_dir()

        # 1) Try local
        try:
            if os.path.exists(self.model_path) and self._verify_checksum(self.model_path):
                model = model_class(num_classes=num_classes)
                state = torch.load(self.model_path, map_location=torch.device("cpu"))
                model.load_state_dict(state)
                model.eval()
                print("✅ Model loaded successfully from local file")
                return model
        except Exception as e:
            print(f"⚠️ Failed loading local model, will try download: {e}")

        # 2) Try download → then load
        try:
            if self.download_model() and os.path.exists(self.model_path):
                if self._verify_checksum(self.model_path):
                    model = model_class(num_classes=num_classes)
                    state = torch.load(self.model_path, map_location=torch.device("cpu"))
                    model.load_state_dict(state)
                    model.eval()
                    print("✅ Model loaded successfully after download")
                    return model
        except Exception as e:
            print(f"⚠️ Failed loading downloaded model, will fallback: {e}")

        # 3) Fallback
        print("⚠️ Falling back to pre-trained ImageNet weights (reduced accuracy expected)")
        return model_class(num_classes=num_classes)


# Optional: Hugging Face Hub loader for later
class HuggingFaceModelLoader:
    def __init__(self):
        self.model_id = "your-username/plant-disease-model"  # Replace if you publish to HF

    def load_model(self, model_class, num_classes: int = 38):
        try:
            from huggingface_hub import hf_hub_download
            print("📥 Downloading model from Hugging Face Hub...")
            model_path = hf_hub_download(
                repo_id=self.model_id,
                filename="best_model.pth",
                cache_dir="./models"
            )
            model = model_class(num_classes=num_classes)
            model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
            model.eval()
            print("✅ Model loaded successfully from Hugging Face Hub")
            return model
        except Exception as e:
            print(f"❌ Error loading model from HF Hub: {e}")
            print("⚠️ Falling back to pre-trained weights")
            return model_class(num_classes=num_classes)
