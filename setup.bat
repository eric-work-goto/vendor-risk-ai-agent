@echo off
REM Quick setup script for Windows

echo Setting up Vendor Risk AI Agent Environment...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+ first.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment and install packages
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

echo.
echo ✅ Setup completed!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: python check_environment.py
echo 3. Test: python test_basic.py
echo.
pause
