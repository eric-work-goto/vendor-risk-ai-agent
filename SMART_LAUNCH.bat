@echo off
title Vendor Risk Assessment AI - Smart Launcher

echo ========================================
echo  🚀 VENDOR RISK ASSESSMENT AI
echo     Smart Launcher
echo ========================================
echo.

REM Check if PowerShell is available
powershell -Command "Write-Host 'PowerShell available'" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PowerShell not found. Please install PowerShell.
    pause
    exit /b 1
)

REM Run the PowerShell launcher
powershell -ExecutionPolicy Bypass -File "smart_launch.ps1"

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo ❌ Launcher encountered an error.
    pause
)
