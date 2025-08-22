import torch
import os
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from torchvision.models import ResNet50_Weights
import io



DISEASE_CLASSES = {
    0: {
        "name": "Pepper__bell___Bacterial_spot",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "symptoms": "Small, water-soaked spots on leaves that enlarge and turn brown with a yellow halo.",
        "treatment": "Use disease-free seeds, practice crop rotation, and apply copper-based fungicides."
    },
    1: {
        "name": "Pepper__bell___healthy",
        "scientific_name": "N/A",
        "symptoms": "Leaves and stems are green and upright, with no visible spots, discoloration, or wilting.",
        "treatment": "Maintain proper watering, nutrition, and sunlight exposure."
    },
    2: {
        "name": "Potato___Early_blight",
        "scientific_name": "Alternaria solani",
        "symptoms": "Dark brown to black lesions with concentric rings on leaves, often surrounded by a yellow halo.",
        "treatment": "Crop rotation, proper plant spacing, and timely application of fungicides."
    },
    3: {
        "name": "Potato___Late_blight",
        "scientific_name": "Phytophthora infestans",
        "symptoms": "Irregular, water-soaked lesions on leaves that rapidly enlarge and turn brown/black, often with a fuzzy white mold on the underside in humid conditions.",
        "treatment": "Remove infected plants, use resistant varieties, and apply preventative fungicides."
    },
    4: {
        "name": "Potato___healthy",
        "scientific_name": "N/A",
        "symptoms": "Foliage is green and vigorous, with no signs of spots, blight, or discoloration.",
        "treatment": "Ensure adequate water, nutrients, and sunlight; practice good field hygiene."
    },
    5: {
        "name": "Tomato_Bacterial_spot",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "symptoms": "Small, dark, greasy spots on leaves that may enlarge and coalesce, and raised, scab-like lesions on fruit.",
        "treatment": "Use disease-free seeds, rotate crops, and apply copper-based bactericides."
    },
    6: {
        "name": "Tomato_Early_blight",
        "scientific_name": "Alternaria solani",
        "symptoms": "Dark brown spots with concentric rings (target-like) on older leaves, and sometimes on stems and fruit.",
        "treatment": "Remove infected lower leaves, improve air circulation, and apply fungicides."
    },
    7: {
        "name": "Tomato_Late_blight",
        "scientific_name": "Phytophthora infestans",
        "symptoms": "Large, water-soaked, irregular lesions on leaves and stems, rapidly expanding and turning brown, with white fuzzy growth on the undersides in moist conditions.",
        "treatment": "Remove infected plants, use resistant varieties, and apply fungicides preventatively."
    },
    8: {
        "name": "Tomato_Leaf_Mold",
        "scientific_name": "Fulvia fulva (formerly Cladosporium fulvum)",
        "symptoms": "Pale green or yellow spots on upper leaf surfaces, with olive-green to brown velvety patches on the corresponding undersides.",
        "treatment": "Improve air circulation, reduce humidity, and use resistant varieties or fungicides."
    },
    9: {
        "name": "Tomato_Septoria_leaf_spot",
        "scientific_name": "Septoria lycopersici",
        "symptoms": "Small, circular, dark spots with a tiny black dot in the center (pycnidium) on leaves, starting from the oldest leaves.",
        "treatment": "Remove infected leaves, avoid overhead watering, and apply fungicides."
    },
    10: {
        "name": "Tomato_Spider_mites_Two_spotted_spider_mite",
        "scientific_name": "Tetranychus urticae",
        "symptoms": "Tiny yellow or white spots on leaves, fine webbing on the undersides, and bronzing or yellowing of foliage.",
        "treatment": "Hose down plants, use insecticidal soaps or oils, and introduce predatory mites."
    },
    11: {
        "name": "Tomato__Target_Spot",
        "scientific_name": "Corynespora cassiicola",
        "symptoms": "Small, dark, circular spots with a light brown center and dark border, often with concentric rings, on leaves, stems, and fruit.",
        "treatment": "Crop rotation, proper sanitation, and fungicide application."
    },
    12: {
        "name": "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "scientific_name": "Tomato yellow leaf curl virus (TYLCV)",
        "symptoms": "Leaves become small, curled upwards, and turn yellow with purple veins; plants are stunted.",
        "treatment": "Manage whitefly vectors, use resistant varieties, and remove infected plants."
    },
    13: {
        "name": "Tomato__Tomato_mosaic_virus",
        "scientific_name": "Tomato mosaic virus (ToMV)",
        "symptoms": "Mosaic patterns of light and dark green on leaves, blistering, and distortion; fruit may be discolored.",
        "treatment": "Use resistant varieties, practice good sanitation, and remove infected plants."
    },
    14: {
        "name": "Tomato_healthy",
        "scientific_name": "N/A",
        "symptoms": "Leaves are uniformly green and vibrant, stems are strong, and fruit production is normal, with no signs of disease or pests.",
        "treatment": "Provide adequate sunlight, water, and nutrients; regular monitoring for pests and diseases."
    }
}

class PlantDiseaseModel(nn.Module):
    def __init__(self):
        super(PlantDiseaseModel, self).__init__()
        # Load pre-trained ResNet50 with improved weights
        self.model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        
        # Unfreeze more layers for better fine-tuning
        for name, param in self.model.named_parameters():
            if "layer3" not in name and "layer4" not in name and "fc" not in name:
                param.requires_grad = False
        
        # Enhanced model architecture for plant disease classification
        num_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Linear(num_features, 2048),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.BatchNorm1d(2048),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.BatchNorm1d(1024),
            nn.Linear(1024, len(DISEASE_CLASSES))
        )
        
        # Initialize weights properly
        for m in self.model.fc.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        """Forward pass of the model"""
        return self.model(x)

    def train_model(self, train_loader, val_loader, num_epochs=10, learning_rate=0.001):
        """Train the model on plant disease dataset"""
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(device)
        

        
        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=3)
        
        best_val_loss = float('inf')
        
        for epoch in range(num_epochs):
            self.train()
            train_loss = 0
            correct = 0
            total = 0
            
            for batch_idx, (images, labels) in enumerate(train_loader):
                images, labels = images.to(device), labels.to(device)
                
                optimizer.zero_grad()
                outputs = self(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()


            
            avg_train_loss = train_loss / len(train_loader)
            train_acc = 100. * correct / total
            


            # Validation phase
            self.eval()
            val_loss = 0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for v_batch_idx, (images, labels) in enumerate(val_loader):
                    images, labels = images.to(device), labels.to(device)
                    outputs = self(images)
                    loss = criterion(outputs, labels)
                    
                    val_loss += loss.item()
                    _, predicted = outputs.max(1)
                    val_total += labels.size(0)
                    val_correct += predicted.eq(labels).sum().item()


            
            avg_val_loss = val_loss / len(val_loader)
            val_acc = 100. * val_correct / val_total
            

            
            print(f'Epoch [{epoch+1}/{num_epochs}]')
            print(f'Train Loss: {avg_train_loss:.4f}, Train Acc: {train_acc:.2f}%')
            print(f'Val Loss: {avg_val_loss:.4f}, Val Acc: {val_acc:.2f}%')
            
            scheduler.step(avg_val_loss)
            
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                # Save inside backend/app/models/best_model.pth
                models_dir = os.path.dirname(__file__)
                save_path = os.path.join(models_dir, 'best_model.pth')
                torch.save(self.state_dict(), save_path)
        


    def predict(self, image_tensor):
        """Make prediction with improved confidence calculation"""
        self.eval()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(device)
        image_tensor = image_tensor.to(device)
        
        with torch.no_grad():
            outputs = self(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            
            # Get top 5 predictions
            top_probs, top_indices = torch.topk(probabilities[0], k=min(5, len(DISEASE_CLASSES)))
            
            # Convert to percentages and create prediction list
            predictions = []
            total_prob = torch.sum(probabilities[0])
            
            for prob, idx in zip(top_probs, top_indices):
                normalized_prob = (prob / total_prob) * 100
                predictions.append((idx.item(), float(normalized_prob)))
            
            # Temporarily disable confidence gating for testing while training completes
            # if len(predictions) >= 2:
            #     top_prob = predictions[0][1] / 100.0  # convert to 0..1
            #     second_prob = predictions[1][1] / 100.0
            #     margin = top_prob - second_prob
            #     # Require a minimum top probability and separation (more relaxed thresholds)
            #     if top_prob < 0.15 or margin < 0.02:
            #         return [(-1, 0.0)]

            print(f"Debug - Top 5 Predictions: {predictions}")
            return predictions

    def preprocess_image(self, image_bytes):
        """Preprocess the image with improved augmentation."""
        try:
            # Open image and convert to RGB
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # Define preprocessing pipeline
            preprocess = transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.CenterCrop(224),
                transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            
            # Apply preprocessing
            image_tensor = preprocess(image)
            return image_tensor.unsqueeze(0)
            
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return None

def get_transform():
    """Get the transformation pipeline for input images"""
    return transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def predict_disease(model, image):
    """
    Predict the disease from an image and return data formatted for the frontend.
    """
    try:
        model.eval()
        transform = get_transform()
        image_tensor = transform(image).unsqueeze(0)
        
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            
            # Get all predictions sorted by probability
            values, indices = torch.sort(probabilities, dim=1, descending=True)
            values = values[0]
            indices = indices[0]
            
            # Calculate more robust confidence metrics
            top_prob = values[0].item()
            second_prob = values[1].item()
            mean_other_probs = torch.mean(values[1:]).item()
            std_other_probs = torch.std(values[1:]).item()
            
            # Multiple confidence checks
            prob_diff = top_prob - second_prob
            prob_ratio = top_prob / (second_prob + 1e-6)
            distribution_score = (top_prob - mean_other_probs) / (std_other_probs + 1e-6)
            
            # Combined confidence calculation with adjusted weights
            confidence_score = (
                (prob_diff * 0.5) +  # Increased weight for probability difference
                (prob_ratio * 0.3) +  # Weight for probability ratio
                (distribution_score * 0.2)  # Reduced weight for distribution score
            ) * 100
            
            # Get prediction details
            disease_idx = indices[0].item()
            
            # Add debug information with more detail
            predictions = [(DISEASE_CLASSES[idx.item()]['name'], prob.item() * 100) 
                         for idx, prob in zip(indices[:5], values[:5])]  # Show top 5 predictions
            print(f"Debug - Top 5 Predictions: {predictions}")
            print(f"Debug - Confidence Score: {confidence_score:.2f}%")
            print(f"Debug - Probability Distribution: diff={prob_diff:.3f}, ratio={prob_ratio:.3f}, dist_score={distribution_score:.3f}")
            
            # Temporarily disable confidence thresholds while training completes
            # if confidence_score < 15 or top_prob < 0.2:  # Much more relaxed thresholds
            #     disease_idx = len(DISEASE_CLASSES) - 1  # Use Unknown class
            #     confidence_score = 0
            
            disease_info = DISEASE_CLASSES[disease_idx]

            return {
                "disease_name": disease_info["name"],
                "confidence": float(min(100, max(0, confidence_score))),
                "scientific_name": disease_info["scientific_name"],
                "symptoms": disease_info["symptoms"],
                "treatment": disease_info["treatment"],
                "all_predictions": [
                    {
                        "disease": DISEASE_CLASSES[idx.item()]["name"],
                        "confidence": float(round(prob.item() * 100, 2))
                    } for idx, prob in zip(indices[:5], values[:5])
                ]
            }
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return {
            "disease_name": "Unknown",
            "confidence": 0.0,
            "scientific_name": "N/A",
            "symptoms": "Unable to process the image.",
            "treatment": "Try a clearer image with good lighting.",
            "all_predictions": []
        }