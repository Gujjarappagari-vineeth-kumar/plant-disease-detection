import os
import sys
import torch
from .main import is_training, is_trained
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import ImageFolder
from .models.disease_model import PlantDiseaseModel, DISEASE_CLASSES
import zipfile
import shutil
import time

def download_full_kaggle_dataset(max_retries=3, timeout=600):
    """Download the full PlantVillage dataset from Kaggle with 38 classes"""
    print("Downloading FULL PlantVillage dataset from Kaggle (38 classes)...")
    
    try:
        import kagglehub
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}")
                print("This will download ~2GB of data. Please be patient...")
                
                # Download latest version of the dataset
                path = kagglehub.dataset_download("abdallahalidev/plantvillage-dataset")
                print(f"Dataset downloaded to: {path}")
                
                # The dataset structure is: path/plantvillage dataset/color/
                # We need to find the color directory which contains the class folders
                color_path = os.path.join(path, "plantvillage dataset", "color")
                
                if os.path.exists(color_path):
                    print(f"Found color images at: {color_path}")
                    
                    # Copy to our dataset directory
                    dataset_dir = os.path.join(os.path.dirname(__file__), '..', 'dataset')
                    os.makedirs(dataset_dir, exist_ok=True)
                    
                    target_path = os.path.join(dataset_dir, 'PlantVillage_Full')
                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)
                    
                    print(f"Copying dataset to: {target_path}")
                    shutil.copytree(color_path, target_path)
                    
                    print(f"Full dataset copied successfully to: {target_path}")
                    return target_path
                else:
                    print(f"Color directory not found at: {color_path}")
                    return None
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print(f"Waiting 10 seconds before retry...")
                    time.sleep(10)
                else:
                    print(f"All {max_retries} attempts failed. Please check your internet connection.")
                    return None
                    
    except ImportError:
        print("kagglehub not available. Please install it with: pip install kagglehub")
        return None
    
    return None

def create_extended_model(num_classes):
    """Create a model that can handle the full number of classes"""
    print(f"Creating extended model for {num_classes} classes...")
    
    # Import here to avoid circular imports
    from .models.disease_model import PlantDiseaseModel
    
    # Create a new model instance with the correct number of classes
    model = PlantDiseaseModel(num_classes=num_classes)
    
    return model

def train_plant_disease_model():
    """Train the plant disease model using the FULL Kaggle dataset"""
    global is_training
    global is_trained
    is_training = True
    is_trained = False  # Reset the trained flag at the start of training

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Check for existing dataset first
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'PlantVillage_Full')
    
    if os.path.exists(dataset_path):
        print(f"Using existing dataset at: {dataset_path}")
    else:
        print("Existing dataset not found. Downloading from Kaggle...")
        # Download the full dataset from Kaggle
        dataset_path = download_full_kaggle_dataset(max_retries=3, timeout=600)  # 10 minute timeout
        
        if not dataset_path:
            print("Failed to download full dataset from Kaggle.")
            print("Please check your internet connection and try again.")
            is_training = False  # Set training to False if download fails
            return

    # Data augmentation and preprocessing
    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    val_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    print(f"Using dataset path: {dataset_path}")
    if not os.path.exists(dataset_path):
        print(f"Dataset path does not exist: {dataset_path}")
        is_training = False # Set training to False if the path does not exist.
        return

    # Load the full dataset without filtering
    print("Loading full dataset with all available classes...")
    base_ds = ImageFolder(dataset_path)  # no transform yet
    
    print(f"Found {len(base_ds.classes)} classes in full dataset")
    print(f"All classes: {base_ds.classes}")
    
    # Count total images
    total_images = len(base_ds.samples)
    print(f"Total images in dataset: {total_images}")

    # Split the dataset into train and validation
    print("Splitting dataset into train/validation sets...")
    
    # Create train/validation split
    g = torch.Generator().manual_seed(42) #Add manual seed
    indices = torch.randperm(len(base_ds), generator=g).tolist()
    split = int(0.8 * len(indices))
    train_idx = indices[:split]
    val_idx = indices[split:]

    # Create datasets
    train_dataset = torch.utils.data.Subset(base_ds, train_idx)
    val_dataset = torch.utils.data.Subset(base_ds, val_idx)

    # Apply transforms
    class TransformedSubset(torch.utils.data.Dataset):
        def __init__(self, subset, transform):
            self.subset = subset
            self.transform = transform
        def __len__(self):
            return len(self.subset)
        def __getitem__(self, index):
            sample, target = self.subset[index]
            if self.transform is not None:
                sample = self.transform(sample)
            return sample, target

    train_dataset = TransformedSubset(train_dataset, train_transform)
    val_dataset = TransformedSubset(val_dataset, val_transform)

    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=16,  # Reduced batch size for more classes
        shuffle=True,
        num_workers=0,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        shuffle=False,
        batch_size=16,  # Reduced batch size for more classes
        num_workers=0,
        pin_memory=True
    )

    print(f"Number of training samples: {len(train_dataset)}")
    print(f"Number of validation samples: {len(val_dataset)}")
    print(f"Number of classes: {len(base_ds.classes)}")

    # Create extended model for all classes
    model = create_extended_model(len(base_ds.classes))
    
    print("Starting training on FULL dataset...")
    print(f"Training on {len(base_ds.classes)} classes with {total_images} total images")
    
    # Train the model
    model.train_model(
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=15,  # More epochs for larger dataset
        learning_rate=0.0001
    )

    print("Training completed! Model saved to backend/app/models/best_model.pth")
    print(f"Model trained on {len(base_ds.classes)} classes!")
    is_training = False
    is_trained = True

if __name__ == "__main__":
    train_plant_disease_model()
