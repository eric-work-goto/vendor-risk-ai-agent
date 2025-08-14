# Simple Smart Launcher for Windows
# ==================================

param(
    [int]$PreferredPort = 0,
    [switch]$SkipBrowser = $false
)

Write-Host "🚀 Smart Application Launcher" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Check Python
try {
    $pythonVersion = & python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -ge 3 -and $minor -ge 8) {
            Write-Host "✅ Python $major.$minor detected" -ForegroundColor Green
        } else {
            Write-Host "❌ Python 3.8+ required, found $major.$minor" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
try {
    & python -m pip install -r requirements.txt | Out-Null
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Some dependencies may have failed to install" -ForegroundColor Yellow
}

# Get available port
Write-Host "🔌 Finding available port..." -ForegroundColor Cyan
try {
    if ($PreferredPort -gt 0) {
        $portScript = "from port_config import port_manager; print(port_manager.ensure_port_available($PreferredPort))"
    } else {
        $portScript = "from port_config import port_manager; print(port_manager.ensure_port_available())"
    }
    
    $port = & python -c $portScript
    
    if ($port -match "^\d+$") {
        $port = [int]$port
        Write-Host "✅ Using port: $port" -ForegroundColor Green
    } else {
        Write-Host "❌ Could not determine port: $port" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Port management error: $_" -ForegroundColor Red
    exit 1
}

# Start server
Write-Host "🚀 Starting server on port $port..." -ForegroundColor Cyan
$baseUrl = "http://localhost:$port"

try {
    $process = Start-Process -FilePath "python" -ArgumentList @(
        "-m", "uvicorn", 
        "src.api.web_app:app", 
        "--host", "127.0.0.1", 
        "--port", $port.ToString()
    ) -PassThru -WindowStyle Hidden
    
    Start-Sleep -Seconds 3
    
    if (-not $process.HasExited) {
        Write-Host "✅ Server started successfully on port $port" -ForegroundColor Green
    } else {
        Write-Host "❌ Server failed to start" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    exit 1
}

# Open browser
if (-not $SkipBrowser) {
    $mainUrl = "$baseUrl/static/combined-ui.html"
    Write-Host "🌐 Opening browser at $mainUrl" -ForegroundColor Cyan
    try {
        Start-Process $mainUrl
        Write-Host "✅ Browser opened successfully" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not open browser automatically" -ForegroundColor Yellow
        Write-Host "📍 Please navigate to: $mainUrl" -ForegroundColor Cyan
    }
} else {
    Write-Host "⏭️ Skipping browser launch" -ForegroundColor Yellow
}

# Display info
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🎯 APPLICATION READY" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "📍 Main Application: $baseUrl/static/combined-ui.html" -ForegroundColor White
Write-Host "📚 API Documentation: $baseUrl/docs" -ForegroundColor White
Write-Host "🔄 Alternative Docs: $baseUrl/redoc" -ForegroundColor White
Write-Host "🔍 Health Check: $baseUrl/health" -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "⚠️ Press Ctrl+C to stop this script (server runs independently)" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

# Keep script running
try {
    Write-Host "🔄 Monitoring server (Press Ctrl+C to stop monitoring)..." -ForegroundColor Yellow
    while (-not $process.HasExited) {
        Start-Sleep -Seconds 2
    }
    Write-Host "❌ Server process stopped unexpectedly" -ForegroundColor Red
} catch {
    Write-Host ""
    Write-Host "🛑 Monitoring stopped by user" -ForegroundColor Yellow
    Write-Host "📝 Note: Server is still running independently" -ForegroundColor Cyan
}
