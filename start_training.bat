@echo off
echo 🌱 Starting Plant Disease Model Training...
echo =========================================
echo.

cd backend

echo 📦 Activating virtual environment...
call venv\Scripts\activate

echo 🚀 Starting training with full Kaggle dataset...
python -m app.train_kaggle

echo.
echo ✅ Training script completed!
pause
