# Server Health Monitor Script
# Monitors the server and restarts it if it becomes unresponsive

param(
    [int]$CheckIntervalSeconds = 30,
    [int]$TimeoutSeconds = 10,
    [int]$MaxRetries = 3
)

Write-Host "🔍 Starting Vendor Risk Assessment Server Monitor..." -ForegroundColor Green
Write-Host "⏱️ Check interval: $CheckIntervalSeconds seconds" -ForegroundColor Cyan
Write-Host "⏰ Request timeout: $TimeoutSeconds seconds" -ForegroundColor Cyan
Write-Host "🔄 Max retries: $MaxRetries" -ForegroundColor Cyan
Write-Host ""

$serverUrl = "http://localhost:8028/health"
$restartScript = "C:\Users\eleeds\OneDrive - GoTo Inc\Desktop\vendor-risk-ai-agent\start_server.ps1"
$failureCount = 0

function Test-ServerHealth {
    try {
        $response = Invoke-WebRequest -Uri $serverUrl -TimeoutSec $TimeoutSeconds -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

function Restart-Server {
    Write-Host "🚨 Server is unresponsive. Attempting restart..." -ForegroundColor Red
    
    # Kill existing processes
    $processes = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
        $_.MainModule.ModuleName -eq "python.exe"
    }
    
    foreach ($process in $processes) {
        try {
            $process.Kill()
            Write-Host "✅ Stopped Python process $($process.Id)" -ForegroundColor Yellow
        } catch {
            Write-Host "⚠️ Could not stop process $($process.Id)" -ForegroundColor Yellow
        }
    }
    
    Start-Sleep -Seconds 3
    
    # Start the server script in a new process
    try {
        Start-Process -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy", "Bypass", "-File", $restartScript -WindowStyle Normal
        Write-Host "🚀 Server restart initiated" -ForegroundColor Green
        Start-Sleep -Seconds 15  # Give server time to start
        return $true
    } catch {
        Write-Host "❌ Failed to restart server: $_" -ForegroundColor Red
        return $false
    }
}

# Main monitoring loop
while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    if (Test-ServerHealth) {
        Write-Host "[$timestamp] ✅ Server is healthy" -ForegroundColor Green
        $failureCount = 0
    } else {
        $failureCount++
        Write-Host "[$timestamp] ❌ Server health check failed (attempt $failureCount/$MaxRetries)" -ForegroundColor Red
        
        if ($failureCount -ge $MaxRetries) {
            if (Restart-Server) {
                $failureCount = 0
                Write-Host "[$timestamp] 🔄 Server restart completed" -ForegroundColor Green
            } else {
                Write-Host "[$timestamp] 💀 Server restart failed. Waiting before retry..." -ForegroundColor Red
                Start-Sleep -Seconds 60
            }
        }
    }
    
    Start-Sleep -Seconds $CheckIntervalSeconds
}
