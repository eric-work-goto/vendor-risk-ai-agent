@echo off
title Vendor Risk Assessment Server

echo ========================================
echo  Vendor Risk Assessment Server Manager
echo ========================================
echo.

:menu
echo Select an option:
echo 1. Start Server
echo 2. Stop Server
echo 3. Restart Server
echo 4. Check Server Status
echo 5. Start with Monitoring
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto stop_server
if "%choice%"=="3" goto restart_server
if "%choice%"=="4" goto check_status
if "%choice%"=="5" goto start_with_monitor
if "%choice%"=="6" goto exit
goto menu

:start_server
echo Starting server...
powershell.exe -ExecutionPolicy Bypass -File "start_server.ps1"
goto menu

:stop_server
echo Stopping server...
powershell.exe -Command "Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {$_.MainModule.ModuleName -eq 'python.exe'} | Stop-Process -Force"
echo Server stopped.
pause
goto menu

:restart_server
echo Restarting server...
call :stop_server
timeout /t 3 /nobreak > nul
call :start_server
goto menu

:check_status
echo Checking server status...
powershell.exe -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8028/health' -TimeoutSec 5 -UseBasicParsing; Write-Host 'Server is running and healthy' -ForegroundColor Green } catch { Write-Host 'Server is not responding' -ForegroundColor Red }"
pause
goto menu

:start_with_monitor
echo Starting server with monitoring...
start "Vendor Risk Server" powershell.exe -ExecutionPolicy Bypass -File "start_server.ps1"
timeout /t 5 /nobreak > nul
start "Server Monitor" powershell.exe -ExecutionPolicy Bypass -File "monitor_server.ps1"
echo Server and monitor started in separate windows.
pause
goto menu

:exit
echo Goodbye!
exit /b
