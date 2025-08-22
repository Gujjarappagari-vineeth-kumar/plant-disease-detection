# Plant Disease Detection System

A comprehensive plant disease detection system using deep learning with a modern web interface. This system can identify various plant diseases from leaf images with high accuracy.

## 🌿 Features

- **15 Disease Classes**: Supports detection of common plant diseases including:
  - Tomato diseases (Early blight, Late blight, Bacterial spot, Leaf mold, etc.)
  - Potato diseases (Early blight, Late blight)
  - Pepper diseases (Bacterial spot)
  - Healthy plant detection for all crops

- **Modern Web Interface**: 
  - Drag-and-drop image upload
  - Real-time disease detection
  - Detailed results with confidence scores
  - Treatment recommendations and symptoms
  - Responsive design

- **Advanced AI Model**:
  - ResNet50-based deep learning model
  - Fine-tuned on PlantVillage dataset
  - High accuracy disease classification
  - Confidence-based predictions

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd PlantDisease
   ```

2. **Install all dependencies**:
   ```bash
   npm run install-all
   ```

3. **Train the model** (first time only):
   ```bash
   npm run train
   ```
   This will take 10-20 minutes depending on your system.

4. **Start the application**:
   ```bash
   npm run dev
   ```

5. **Open your browser** and navigate to `http://localhost:5173`

## 📁 Project Structure

```
PlantDisease/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── train.py        # Model training script
│   │   └── models/
│   │       └── disease_model.py  # Neural network model
│   ├── dataset/            # PlantVillage dataset
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.tsx         # Main application
│   │   └── types.ts        # TypeScript types
│   └── package.json        # Node.js dependencies
└── README.md              # This file
```

## 🔧 Development

### Backend Development

The backend is built with FastAPI and PyTorch:

- **Model**: ResNet50 fine-tuned for plant disease classification
- **API**: RESTful API with automatic documentation
- **Training**: Custom training script with TensorBoard logging

### Frontend Development

The frontend is built with React and Material-UI:

- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI)
- **File Upload**: React Dropzone for drag-and-drop functionality
- **HTTP Client**: Axios for API communication

## 📊 Model Performance

The model achieves high accuracy on the PlantVillage dataset:

- **Training Samples**: ~16,500 images
- **Validation Samples**: ~4,100 images
- **Classes**: 15 disease categories
- **Architecture**: ResNet50 with custom classification head

## 🎯 Usage

1. **Upload an Image**: Drag and drop or click to select a plant leaf image
2. **Wait for Analysis**: The model will analyze the image (usually 2-5 seconds)
3. **View Results**: See the detected disease, confidence score, and treatment recommendations

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- Maximum file size: 10MB

### Result Interpretation

- **High Confidence (70%+)**: Reliable disease detection
- **Medium Confidence (40-70%)**: Probable disease detection
- **Low Confidence (<40%)**: Uncertain detection
- **Unknown**: Model cannot confidently identify the disease

## 🛠️ Troubleshooting

### Common Issues

1. **"Unknown" Results**: 
   - Ensure the image shows a clear view of the leaf
   - Check that the plant species is in our training dataset
   - Try uploading a higher quality image

2. **Model Not Loading**:
   - Ensure the training completed successfully
   - Check that `backend/app/models/best_model.pth` exists
   - Restart the backend server

3. **Upload Errors**:
   - Verify the image format is supported
   - Check file size is under 10MB
   - Ensure the backend server is running

### Training Issues

If the model training fails:

1. Check that the dataset is properly organized
2. Ensure sufficient disk space
3. Verify all Python dependencies are installed
4. Check the console output for specific error messages

## 🔬 Technical Details

### Model Architecture

- **Base Model**: ResNet50 (ImageNet pre-trained)
- **Classification Head**: Custom fully connected layers
- **Output**: 15-class softmax probabilities
- **Training**: Adam optimizer with learning rate scheduling

### API Endpoints

- `GET /`: Health check
- `GET /status`: Model readiness check
- `POST /predict`: Disease prediction endpoint
- `GET /docs`: Interactive API documentation

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the console logs
3. Open an issue on GitHub

---

**Note**: This system is designed for educational and research purposes. For commercial agricultural use, please consult with agricultural experts and validate results in your specific context. 