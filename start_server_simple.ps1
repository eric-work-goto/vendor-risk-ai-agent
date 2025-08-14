# Simple Server Startup Script
# Vendor Risk Assessment Server

Write-Host "Starting Vendor Risk Assessment Server..." -ForegroundColor Green

# Function to kill existing processes on port 8028
function Stop-ExistingServer {
    Write-Host "Checking for existing processes on port 8028..." -ForegroundColor Yellow
    
    # Find and kill processes using port 8028
    $netstatOutput = netstat -ano | findstr ":8028"
    if ($netstatOutput) {
        $processes = $netstatOutput | ForEach-Object {
            if ($_ -match '\s+(\d+)$') {
                $matches[1]
            }
        }
        
        foreach ($processId in $processes) {
            if ($processId -and $processId -ne "") {
                try {
                    taskkill /PID $processId /F 2>$null
                    Write-Host "Killed process $processId using port 8028" -ForegroundColor Green
                } catch {
                    Write-Host "Could not kill process $processId" -ForegroundColor Yellow
                }
            }
        }
        Start-Sleep -Seconds 2
    } else {
        Write-Host "Port 8028 is available" -ForegroundColor Green
    }
}

# Function to start the server
function Start-VendorRiskServer {
    # Set directories
    $projectRoot = "C:\Users\eleeds\OneDrive - GoTo Inc\Desktop\vendor-risk-ai-agent"
    $apiDir = "$projectRoot\src\api"
    
    Write-Host "Setting working directory to: $apiDir" -ForegroundColor Cyan
    Set-Location $apiDir
    
    # Activate virtual environment if it exists
    $venvActivate = "$projectRoot\.venv\Scripts\Activate.ps1"
    if (Test-Path $venvActivate) {
        Write-Host "Activating Python virtual environment..." -ForegroundColor Cyan
        & $venvActivate
    }
    
    Write-Host "Starting Python web server..." -ForegroundColor Green
    Write-Host "Server will be available at: http://localhost:8028" -ForegroundColor Cyan
    Write-Host "Main App: http://localhost:8028/static/combined-ui.html" -ForegroundColor Cyan
    Write-Host "API Docs: http://localhost:8028/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
    Write-Host "============================================================"
    
    # Start the server
    python web_app.py
}

# Main execution
try {
    Stop-ExistingServer
    Start-VendorRiskServer
} catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
    Write-Host "Attempting to restart..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    Stop-ExistingServer
    Start-VendorRiskServer
}
