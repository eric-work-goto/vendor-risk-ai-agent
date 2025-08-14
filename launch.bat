@echo off
echo ==========================================
echo   Vendor Risk Assessment AI - Launcher
echo ==========================================
echo.

REM Check if we're in the correct directory
if not exist "src\api\web_app.py" (
    echo ERROR: This script must be run from the vendor-risk-ai-agent directory
    echo Please navigate to the correct directory and try again.
    pause
    exit /b 1
)

echo [1/4] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please ensure the virtual environment is set up correctly
    pause
    exit /b 1
)

echo [2/4] Checking dependencies...
python -c "import fastapi, uvicorn, pandas, openpyxl" 2>nul
if errorlevel 1 (
    echo Installing missing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [3/4] Running health check...
python health_check.py
if errorlevel 1 (
    echo WARNING: Health check found some issues
    echo The application may still work, but please review the health check output
    echo.
    choice /C YN /M "Do you want to continue anyway"
    if errorlevel 2 exit /b 1
)

echo [4/4] Starting the application...
echo.
echo ✅ Application is starting...
echo 🌐 Web interface will be available at: http://localhost:8026
echo 📚 API documentation will be available at: http://localhost:8026/docs
echo.
echo ⚠️  To stop the application, press Ctrl+C
echo.

cd src\api
python -m uvicorn web_app:app --host 0.0.0.0 --port 8026

echo.
echo Application has stopped.
pause
