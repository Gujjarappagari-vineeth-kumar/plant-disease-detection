import os
import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import ImageFolder
from .models.disease_model import PlantDiseaseModel, DISEASE_CLASSES

def train_plant_disease_model():
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

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

    # Load dataset (resolve path relative to this file)
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dataset_path = os.path.normpath(os.path.join(repo_root, 'dataset', 'PlantVillage'))

    print(f"Using dataset path: {dataset_path}")
    if not os.path.exists(dataset_path):
        print(f"Please place your plant disease dataset in {os.path.abspath(dataset_path)}")
        print("Dataset should be organized as follows:")
        print("dataset/")
        print("  ├── Apple___Apple_scab/")
        print("  ├── Apple___Black_rot/")
        print("  ├── Apple___Cedar_apple_rust/")
        print("  └── ... (other disease classes)")
        return

    # Build a filtered and remapped dataset that only includes classes present in DISEASE_CLASSES
    target_names_order = [DISEASE_CLASSES[i]["name"] for i in sorted(DISEASE_CLASSES.keys())]
    target_name_to_idx = {name: i for i, name in enumerate(target_names_order)}

    base_ds = ImageFolder(dataset_path)  # no transform yet
    
    print(f"Found {len(base_ds.classes)} classes in dataset")

    class RemappedSubset(torch.utils.data.Dataset):
        def __init__(self, base, samples, transform):
            self.base = base
            self.samples = samples  # list[(path, new_idx)]
            self.transform = transform
            self.loader = base.loader
        def __len__(self):
            return len(self.samples)
        def __getitem__(self, index):
            path, target = self.samples[index]
            sample = self.loader(path)
            if self.transform is not None:
                sample = self.transform(sample)
            return sample, target

    filtered = []
    for path, orig_idx in base_ds.samples:
        class_name = base_ds.classes[orig_idx]
        if class_name in target_name_to_idx:
            filtered.append((path, target_name_to_idx[class_name]))

    if len(filtered) == 0:
        print("ERROR: No images matched the 15 target classes defined in DISEASE_CLASSES.")
        print("Classes expected:")
        print(target_names_order)
        return

    # Deterministic shuffle and split filtered samples
    g = torch.Generator().manual_seed(42)
    indices = torch.randperm(len(filtered), generator=g).tolist()
    split = int(0.8 * len(indices))
    train_idx = indices[:split]
    val_idx = indices[split:]

    train_samples = [filtered[i] for i in train_idx]
    val_samples = [filtered[i] for i in val_idx]

    train_dataset = RemappedSubset(base_ds, train_samples, transform=train_transform)
    val_dataset = RemappedSubset(base_ds, val_samples, transform=val_transform)

    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True,
        num_workers=0,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0,
        pin_memory=True
    )

    print(f"Number of training samples: {len(train_dataset)}")
    print(f"Number of validation samples: {len(val_dataset)}")
    print(f"Number of classes (target): {len(target_names_order)}")
    print(f"Classes (target order): {target_names_order}")

    # Initialize and train model
    model = PlantDiseaseModel()
    model.train_model(
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=5,
        learning_rate=0.0001
    )

    print("Training completed! Model saved to backend/app/models/best_model.pth")

if __name__ == "__main__":
    train_plant_disease_model() 