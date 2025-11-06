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

# Import the complete DISEASE_CLASSES from disease_model.py
from .models.disease_model import DISEASE_CLASSES