from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io
from PIL import Image
import torch
import os
from backend.app.models.disease_model import PlantDiseaseModel, DISEASE_CLASSES, predict_disease as infer_disease
from backend.app.model_loader import ModelLoader

app = FastAPI(
    title="Plant Disease Detection API",
    description="AI-powered plant disease detection using deep learning",
    version="1.0.0"
)

# Get CORS origins from environment variable or use wildcard for development
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins == "*":
    allow_origins = ["*"]
else:
    # Split comma-separated origins
    allow_origins = [origin.strip() for origin in cors_origins.split(",")]

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model = None

def load_model():
    """Load the trained model with optimized loading"""
    global model
    try:
        # Use optimized model loader
        model_loader = ModelLoader()
        model = model_loader.load_model(PlantDiseaseModel, num_classes=38)
        
        print("✅ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup"""
    print("🚀 Starting Plant Disease Detection API...")
    load_model()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Plant Disease Detection API",
        "status": "running",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "available_classes": len(DISEASE_CLASSES) if model else 0,
        "endpoints": [
            "/",
            "/health", 
            "/predict",
            "/docs"
        ]
    }

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """Predict plant disease from uploaded image"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and validate image
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Load image and convert to RGB
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Check if model is loaded
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Make prediction using utility function from disease_model
        result = infer_disease(model, image)
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/classes")
async def get_classes():
    """Get available disease classes"""
    # Return all 38 classes from the full PlantVillage dataset
    from .models.disease_model import DISEASE_CLASSES
    
    disease_classes = [DISEASE_CLASSES[i]["name"] for i in sorted(DISEASE_CLASSES.keys())]
    
    return {
        "classes": disease_classes,
        "count": len(disease_classes)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
