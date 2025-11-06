@echo off
echo 🌱 Starting Plant Disease Model Training with Kaggle Dataset
echo ============================================================
echo.

cd backend

echo 📦 Installing/updating dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo 🚀 Starting training...
python train_kaggle.py

echo.
echo ✅ Training script completed!
pause
