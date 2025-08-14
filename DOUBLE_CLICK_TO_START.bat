@echo off
title Vendor Risk Assessment AI Launcher

:: Set colors for better visibility
color 0A

echo.
echo    ╔════════════════════════════════════════════════════════════╗
echo    ║            🚀 Vendor Risk Assessment AI                    ║
echo    ║                   Easy Launcher                            ║
echo    ╚════════════════════════════════════════════════════════════╝
echo.

:: Change to script directory
cd /d "%~dp0"

:: Quick check if we have the right files
if not exist "src\api\web_app.py" (
    echo ❌ Application files not found!
    echo Please ensure this script is in the vendor-risk-ai-agent folder.
    echo.
    pause
    exit /b 1
)

:: Try to activate virtual environment
echo 🔧 Setting up environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️ Virtual environment not found, using system Python
)

:: Quick dependency check and install if needed
echo 📦 Checking dependencies...
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo Installing FastAPI and Uvicorn...
    pip install fastapi uvicorn python-multipart
)

python -c "import pandas, openpyxl" 2>nul
if errorlevel 1 (
    echo Installing data processing libraries...
    pip install pandas openpyxl
)

echo.
echo ✅ Dependencies ready!
echo.
echo 🌐 Starting web server...
echo 📍 Your application will open automatically in your web browser
echo 📍 If it doesn't open, go to: http://localhost:8026/static/assessment.html
echo.
echo 💡 TIPS:
echo   • Keep this window open while using the application
echo   • Press Ctrl+C here to stop the application
echo   • Use the web interface for all interactions
echo.

:: Start server and open browser
cd src\api

:: Open browser after a short delay
timeout /t 3 /nobreak >nul
start http://localhost:8026/static/assessment.html

:: Start the server (this will block until stopped)
python -m uvicorn web_app:app --host 0.0.0.0 --port 8026

echo.
echo 👋 Application stopped.
echo.
pause
