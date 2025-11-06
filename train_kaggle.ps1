# Plant Disease Model Training with Kaggle Dataset
Write-Host "🌱 Starting Plant Disease Model Training with Kaggle Dataset" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Change to backend directory
Set-Location backend

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "❌ Virtual environment not found. Please run setup first." -ForegroundColor Red
    exit 1
}

# Install/update dependencies
Write-Host "📦 Installing/updating dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "🚀 Starting training..." -ForegroundColor Green
python train_kaggle.py

Write-Host ""
Write-Host "✅ Training script completed!" -ForegroundColor Green
Read-Host "Press Enter to continue"
