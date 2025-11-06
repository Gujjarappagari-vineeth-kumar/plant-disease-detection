# Plant Disease Model Training Status Checker
Write-Host "Plant Disease Model Training Status Checker" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend")) {
    Write-Host "Error: 'backend' directory not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory." -ForegroundColor Yellow
    exit 1
}

# Change to backend directory
Set-Location backend

Write-Host "Checking Training Status..." -ForegroundColor Yellow
Write-Host ""

# Check Python processes
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "Python processes found:" -ForegroundColor Green
    $pythonProcesses | ForEach-Object {
        $runtime = (Get-Date) - $_.StartTime
        $runtimeStr = "{0:D2}:{1:D2}:{2:D2}" -f $runtime.Hours, $runtime.Minutes, $runtime.Seconds
        
        Write-Host "  Process ID: $($_.Id)" -ForegroundColor Cyan
        Write-Host "  CPU Time: $($_.CPU) seconds" -ForegroundColor Cyan
        Write-Host "  Memory: $([math]::Round($_.WorkingSet / 1MB, 2)) MB" -ForegroundColor Cyan
        Write-Host "  Running for: $runtimeStr" -ForegroundColor Cyan
        Write-Host "  Started: $($_.StartTime.ToString('HH:mm:ss'))" -ForegroundColor Cyan
        Write-Host ""
    }
} else {
    Write-Host "No Python processes found" -ForegroundColor Red
}

# Check model file status
Write-Host "Model File Status:" -ForegroundColor Yellow
$modelPath = "app\models\best_model.pth"
if (Test-Path $modelPath) {
    $modelInfo = Get-ChildItem $modelPath
    $modelSize = [math]::Round($modelInfo.Length / 1MB, 2)
    $lastModified = $modelInfo.LastWriteTime
    
    Write-Host "  Model file exists" -ForegroundColor Green
    Write-Host "  Path: $modelPath" -ForegroundColor Cyan
    Write-Host "  Size: $modelSize MB" -ForegroundColor Cyan
    Write-Host "  Last modified: $lastModified" -ForegroundColor Cyan
    
    # Check if model was updated recently (within last 10 minutes)
    $timeSinceUpdate = (Get-Date) - $lastModified
    if ($timeSinceUpdate.TotalMinutes -lt 10) {
        Write-Host "  Model updated recently - Training is active!" -ForegroundColor Green
    } else {
        Write-Host "  Model not updated recently - Training may be paused/completed" -ForegroundColor Yellow
    }
} else {
    Write-Host "  Model file not found" -ForegroundColor Red
    Write-Host "  Training may not have started yet" -ForegroundColor Yellow
}

Write-Host ""

# Check dataset status
Write-Host "Dataset Status:" -ForegroundColor Yellow
$datasetPath = "dataset\PlantVillage_Full"
if (Test-Path $datasetPath) {
    $classes = Get-ChildItem $datasetPath -Directory
    $totalClasses = $classes.Count
    
    Write-Host "  Full dataset found" -ForegroundColor Green
    Write-Host "  Classes: $totalClasses" -ForegroundColor Cyan
    Write-Host "  Path: $datasetPath" -ForegroundColor Cyan
} else {
    Write-Host "  Full dataset not found" -ForegroundColor Red
}

Write-Host ""

# Overall status summary
Write-Host "Status Summary:" -ForegroundColor Yellow
if ($pythonProcesses -and (Test-Path $modelPath)) {
    $modelInfo = Get-ChildItem $modelPath
    $timeSinceUpdate = (Get-Date) - $modelInfo.LastWriteTime
    
    if ($timeSinceUpdate.TotalMinutes -lt 10) {
        Write-Host "  TRAINING IS ACTIVE AND PROGRESSING" -ForegroundColor Green
    } else {
        Write-Host "  TRAINING MAY BE PAUSED OR COMPLETED" -ForegroundColor Yellow
    }
} elseif ($pythonProcesses) {
    Write-Host "  TRAINING PROCESSES RUNNING BUT NO MODEL FILE" -ForegroundColor Yellow
} elseif (Test-Path $modelPath) {
    Write-Host "  TRAINING COMPLETED - MODEL READY" -ForegroundColor Green
} else {
    Write-Host "  NO TRAINING IN PROGRESS" -ForegroundColor Red
}

Write-Host ""
Write-Host "Tips:" -ForegroundColor Blue
Write-Host "  Run 'cd backend; python -m app.train_kaggle' to start training" -ForegroundColor Cyan
Write-Host "  Run this script again to check updated status" -ForegroundColor Cyan

Write-Host ""
Read-Host "Press Enter to continue"
