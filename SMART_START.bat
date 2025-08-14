@echo off
setlocal enabledelayedexpansion

echo.
echo 🔍 Vendor Risk AI Agent - Smart Port Launcher
echo ================================================
echo.

cd /d "%~dp0"

echo 🔄 Checking Python virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Please run setup first.
    echo    Try running: python -m venv .venv
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo.

echo 🔍 Activating environment and resolving port conflicts...
call .venv\Scripts\activate.bat

echo 🚀 Starting application with automatic port management...
python resolve_port_conflicts.py

if errorlevel 1 (
    echo.
    echo ❌ Application failed to start
    echo.
    echo 📋 Troubleshooting options:
    echo    1. Check if Python virtual environment is activated
    echo    2. Run: pip install -r requirements.txt
    echo    3. Check for any error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo 👋 Application stopped
pause
