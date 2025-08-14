# Vendor Risk Assessment AI - PowerShell Launcher
# Easy-to-use launcher for Windows PowerShell

Write-Host "==========================================" -ForegroundColor Blue
Write-Host "  Vendor Risk Assessment AI - Launcher" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Blue
Write-Host ""

# Check if we're in the correct directory
if (!(Test-Path "src\api\web_app.py")) {
    Write-Host "ERROR: This script must be run from the vendor-risk-ai-agent directory" -ForegroundColor Red
    Write-Host "Please navigate to the correct directory and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/4] Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please ensure the virtual environment is set up correctly" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[2/4] Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn, pandas, openpyxl" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install dependencies"
        }
    }
    Write-Host "✅ Dependencies verified" -ForegroundColor Green
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[3/4] Running health check..." -ForegroundColor Yellow
python health_check.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Health check found some issues" -ForegroundColor Yellow
    Write-Host "The application may still work, but please review the health check output" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
} else {
    Write-Host "✅ Health check passed" -ForegroundColor Green
}

Write-Host "[4/4] Starting the application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "✅ Application is starting..." -ForegroundColor Green
Write-Host "🌐 Web interface will be available at: http://localhost:8026" -ForegroundColor Cyan
Write-Host "📚 API documentation will be available at: http://localhost:8026/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  To stop the application, press Ctrl+C" -ForegroundColor Yellow
Write-Host ""

Set-Location "src\api"
try {
    python -m uvicorn web_app:app --host 0.0.0.0 --port 8026
} catch {
    Write-Host ""
    Write-Host "Application stopped." -ForegroundColor Yellow
} finally {
    Set-Location "..\..\"
    Read-Host "Press Enter to exit"
}
