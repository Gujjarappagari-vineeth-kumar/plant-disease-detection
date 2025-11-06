"""
Test script to verify the 38-class Plant Disease model is working correctly
"""

import sys
import os

# Add the backend/app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_model():
    """Test the model loading and basic functionality"""
    try:
        print("🧪 Testing 38-Class Plant Disease Model...")
        print("=" * 50)
        
# Import the model
        from backend.app.models.disease_model import PlantDiseaseModel
        
        print("✅ Successfully imported PlantDiseaseModel")
        
        # Create model with 38 classes
        model = PlantDiseaseModel(num_classes=38)
        print("✅ Model created with 38 classes")
        
        # Check model structure
        print(f"📊 Model output size: {model.model.fc[-1].out_features}")
        print(f"🎯 Expected classes: 38")
        
        if model.model.fc[-1].out_features == 38:
            print("✅ Model architecture is correct!")
        else:
            print("❌ Model architecture mismatch!")
            return False
        
        # Test model loading
        model_path = "backend/app/models/best_model.pth"
        if os.path.exists(model_path):
            print("✅ Model file found")
            
            # Load the trained weights
            import torch
            model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            model.eval()
            print("✅ Model weights loaded successfully!")
            
            # Test forward pass with dummy input
            dummy_input = torch.randn(1, 3, 224, 224)
            with torch.no_grad():
                output = model(dummy_input)
                print(f"✅ Forward pass successful! Output shape: {output.shape}")
                
                # Test softmax
                probabilities = torch.softmax(output, dim=1)
                print(f"✅ Softmax successful! Probabilities sum: {probabilities.sum().item():.4f}")
                
                # Get top prediction
                top_prob, top_idx = torch.topk(probabilities[0], k=1)
                print(f"✅ Top prediction: Class {top_idx.item()} with probability {top_prob.item():.4f}")
                
        else:
            print("❌ Model file not found!")
            return False
        
        print("\n🎉 All tests passed! Model is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model()
    if success:
        print("\n✅ Model test completed successfully!")
    else:
        print("\n❌ Model test failed!")
        sys.exit(1)
