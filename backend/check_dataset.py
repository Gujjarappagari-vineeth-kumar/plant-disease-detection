#!/usr/bin/env python3
"""
Script to check if the PlantVillage dataset is available locally
"""

import os
import sys

def check_dataset():
    """Check if the PlantVillage dataset exists locally"""
    print("🔍 Checking PlantVillage dataset availability...")
    print("=" * 50)
    
    # Check various possible locations
    possible_paths = [
        "dataset/PlantVillage",
        "app/../dataset/PlantVillage",
        "PlantVillage"
    ]
    
    dataset_found = False
    dataset_path = None
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Dataset found at: {os.path.abspath(path)}")
            dataset_found = True
            dataset_path = path
            break
    
    if not dataset_found:
        print("❌ Dataset not found locally")
        print("📋 You need to:")
        print("   1. Download from Kaggle, OR")
        print("   2. Place dataset in: backend/dataset/PlantVillage/")
        return False
    
    # Check dataset structure
    print(f"\n📊 Analyzing dataset structure...")
    
    try:
        # Count classes and images
        classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
        print(f"🏷️ Found {len(classes)} classes")
        
        total_images = 0
        class_counts = {}
        
        for class_name in classes:
            class_path = os.path.join(dataset_path, class_name)
            images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            class_counts[class_name] = len(images)
            total_images += len(images)
        
        print(f"🖼️ Total images: {total_images}")
        print(f"\n📋 Class breakdown:")
        
        # Sort by image count
        sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
        for class_name, count in sorted_classes[:10]:  # Show top 10
            print(f"   {class_name}: {count} images")
        
        if len(sorted_classes) > 10:
            print(f"   ... and {len(sorted_classes) - 10} more classes")
        
        # Check if target classes are present
        target_classes = [
            "Pepper__bell___Bacterial_spot",
            "Pepper__bell___healthy", 
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato_Bacterial_spot",
            "Tomato_Early_blight",
            "Tomato_Late_blight",
            "Tomato_Leaf_Mold",
            "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite",
            "Tomato__Target_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus",
            "Tomato__Tomato_mosaic_virus",
            "Tomato_healthy"
        ]
        
        print(f"\n🎯 Checking target classes:")
        missing_classes = []
        for target_class in target_classes:
            if target_class in class_counts:
                print(f"   ✅ {target_class}: {class_counts[target_class]} images")
            else:
                print(f"   ❌ {target_class}: NOT FOUND")
                missing_classes.append(target_class)
        
        if missing_classes:
            print(f"\n⚠️ Warning: {len(missing_classes)} target classes are missing!")
            print("   This may affect training performance.")
        else:
            print(f"\n🎉 All target classes found! Dataset is ready for training.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing dataset: {e}")
        return False

if __name__ == "__main__":
    success = check_dataset()
    if success:
        print("\n✅ Dataset check completed successfully!")
    else:
        print("\n❌ Dataset check failed!")
        sys.exit(1)
