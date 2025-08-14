@echo off
REM Quick Server Launcher - Vendor Risk Assessment
echo.
echo ==========================================
echo   Vendor Risk Assessment Server
echo ==========================================
echo.

REM Change to project directory
cd /d "C:\Users\eleeds\OneDrive - GoTo Inc\Desktop\vendor-risk-ai-agent"

REM Kill any existing Python processes on port 8028
echo Stopping any existing servers...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8028') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Set working directory and start server
echo Starting server...
cd src\api
python web_app.py

pause
