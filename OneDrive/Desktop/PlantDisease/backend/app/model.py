import torch
import torch.nn as nn
import torchvision.models as models

class PlantDiseaseModel(nn.Module):
    def __init__(self, num_classes=38):  # 38 common plant disease classes
        super(PlantDiseaseModel, self).__init__()
        self.resnet = models.resnet50(pretrained=True)
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        return self.resnet(x)

# Dictionary mapping class indices to disease names and details
DISEASE_CLASSES = {
    0: {
        "name": "Apple___Apple_scab",
        "details": "Apple scab is a common disease caused by Venturia inaequalis. Treatment includes fungicide application and proper orchard management."
    },
    1: {
        "name": "Apple___Black_rot",
        "details": "Black rot is caused by the fungus Botryosphaeria obtusa. Remove infected plant material and maintain good orchard hygiene."
    },
    # Add more classes as needed
} 