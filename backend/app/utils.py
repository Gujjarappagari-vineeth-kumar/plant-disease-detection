import torch
import torchvision.transforms as transforms
from PIL import Image
from .model import PlantDiseaseModel, DISEASE_CLASSES
import os

def load_model():
    """Load the trained model."""
    model = PlantDiseaseModel()
    
    # In production, load the trained weights
    # model.load_state_dict(torch.load('path_to_weights.pth'))
    
    model.eval()
    return model

def transform_image(image):
    """Transform image to model input format."""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    return transform(image).unsqueeze(0)

def get_prediction(image, model):
    """Get prediction for an image."""
    # Transform image
    tensor = transform_image(image)
    
    # Get prediction
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted = torch.max(outputs.data, 1)
        
        # Get confidence scores
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence = probabilities[0][predicted].item()
        
        # Get class details
        class_idx = predicted.item()
        class_info = DISEASE_CLASSES.get(class_idx, {
            "name": "Unknown",
            "details": "Class information not available"
        })
        
        return {
            "class": class_info["name"],
            "confidence": round(confidence * 100, 2),
            "disease_details": class_info["details"]
        } 