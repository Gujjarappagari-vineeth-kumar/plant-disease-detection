# 🌱 Plant Disease Detection - Kaggle Dataset Training

This guide explains how to train the Plant Disease Detection model using the PlantVillage dataset from Kaggle.

## 🚀 Quick Start

### Option 1: Windows Batch File (Recommended for Windows)
```bash
# Double-click or run from command prompt
train_kaggle.bat
```

### Option 2: PowerShell Script
```bash
# Run in PowerShell
.\train_kaggle.ps1
```

### Option 3: Manual Command
```bash
cd backend
# Activate virtual environment
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run training
python train_kaggle.py
```

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Virtual environment** set up in the `backend` folder
3. **Internet connection** for downloading the dataset
4. **Sufficient disk space** (~2-3 GB for the dataset)

## 🔑 Kaggle Setup (First Time Only)

If this is your first time using Kaggle datasets, you may need to authenticate:

1. **Install Kaggle CLI** (if not using kagglehub):
   ```bash
   pip install kaggle
   ```

2. **Get your Kaggle API credentials**:
   - Go to [Kaggle Settings](https://www.kaggle.com/settings/account)
   - Click "Create New API Token"
   - Download `kaggle.json`

3. **Place credentials** (if using kaggle CLI):
   - Windows: `C:\Users\<username>\.kaggle\kaggle.json`
   - Linux/Mac: `~/.kaggle/kaggle.json`

## 📊 Dataset Information

The training script will automatically:

- ✅ Download the PlantVillage dataset from Kaggle
- ✅ Extract and organize the images
- ✅ Filter images to match your 15 target disease classes
- ✅ Split data into training (80%) and validation (20%) sets
- ✅ Apply data augmentation for better training

## 🎯 Target Disease Classes

Your model is configured to recognize these 15 classes:

1. **Pepper__bell___Bacterial_spot**
2. **Pepper__bell___healthy**
3. **Potato___Early_blight**
4. **Potato___Late_blight**
5. **Potato___healthy**
6. **Tomato_Bacterial_spot**
7. **Tomato_Early_blight**
8. **Tomato_Late_blight**
9. **Tomato_Leaf_Mold**
10. **Tomato_Septoria_leaf_spot**
11. **Tomato_Spider_mites_Two_spotted_spider_mite**
12. **Tomato__Target_Spot**
13. **Tomato__Tomato_YellowLeaf__Curl_Virus**
14. **Tomato__Tomato_mosaic_virus**
15. **Tomato_healthy**

## 🏋️ Training Configuration

- **Model**: ResNet50 with custom head
- **Epochs**: 10 (configurable)
- **Learning Rate**: 0.0001
- **Batch Size**: 32
- **Data Augmentation**: Yes (rotation, flip, color jitter)
- **Validation Split**: 80/20

## 📁 File Structure After Training

```
backend/
├── app/
│   ├── models/
│   │   ├── best_model.pth          # ← Your trained model
│   │   └── disease_model.py
│   └── train_kaggle.py
├── dataset/
│   └── PlantVillage/               # ← Downloaded dataset
│       ├── Pepper__bell___Bacterial_spot/
│       ├── Pepper__bell___healthy/
│       └── ... (other classes)
└── train_kaggle.py
```

## 🔍 Monitoring Training

The training script provides detailed output:

- 📊 Dataset statistics
- 🎯 Class matching information
- 📈 Training progress per epoch
- 💾 Model saving confirmation

## 🚨 Troubleshooting

### Common Issues:

1. **"No images matched target classes"**
   - Check if the dataset downloaded correctly
   - Verify class names match exactly (including underscores)

2. **"Failed to download dataset"**
   - Check internet connection
   - Verify Kaggle credentials (if required)
   - Try running again

3. **"Out of memory"**
   - Reduce batch size in `train_kaggle.py`
   - Close other applications
   - Use CPU if GPU memory is insufficient

4. **"Module not found"**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

### Getting Help:

- Check the console output for specific error messages
- Verify all dependencies are installed
- Ensure sufficient disk space
- Check Python version compatibility

## 🎉 After Training

Once training completes:

1. **Model is saved** to `backend/app/models/best_model.pth`
2. **Restart your FastAPI server** to use the new model
3. **Test predictions** with your frontend
4. **Monitor performance** and adjust if needed

## 🔄 Retraining

To retrain with updated data:

1. Delete the existing `best_model.pth`
2. Run the training script again
3. The dataset will be re-downloaded if needed

## 📚 Additional Resources

- [PlantVillage Dataset on Kaggle](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Happy Training! 🌱🤖**
