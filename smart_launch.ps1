# Smart Application Launcher - PowerShell Version
# ================================================
# Intelligent launcher that ensures consistent port usage and prevents conflicts.

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                 🚀 VENDOR RISK ASSESSMENT AI                 ║" -ForegroundColor Cyan
Write-Host "║                      Smart Launcher v2.0                    ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Function to check if a port is available
function Test-Port {
    param([int]$Port)
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.ConnectAsync("localhost", $Port).Wait(1000)
        $tcpClient.Close()
        return $false  # Port is in use
    }
    catch {
        return $true   # Port is available
    }
}

# Function to kill process using a specific port
function Stop-PortProcess {
    param([int]$Port)
    try {
        $netstat = netstat -ano | findstr ":$Port"
        if ($netstat) {
            foreach ($line in $netstat) {
                if ($line -match ":$Port.*LISTENING.*\s+(\d+)$") {
                    $pid = $matches[1]
                    Write-Host "🔄 Stopping process $pid using port $Port..." -ForegroundColor Yellow
                    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                    Start-Sleep -Seconds 2
                    return $true
                }
            }
        }
        return $true
    }
    catch {
        Write-Host "❌ Error stopping process on port $Port" -ForegroundColor Red
        return $false
    }
}

# Function to find available port
function Get-AvailablePort {
    $defaultPort = 8026
    $portRangeStart = 8026
    $portRangeEnd = 8030
    
    # Try default port first
    if (Test-Port $defaultPort) {
        return $defaultPort
    }
    
    # Try to free the default port
    Write-Host "⚠️ Port $defaultPort is busy, attempting to free it..." -ForegroundColor Yellow
    if (Stop-PortProcess $defaultPort) {
        Start-Sleep -Seconds 2
        if (Test-Port $defaultPort) {
            Write-Host "✅ Port $defaultPort is now available" -ForegroundColor Green
            return $defaultPort
        }
    }
    
    # Find alternative port
    Write-Host "🔍 Finding alternative port..." -ForegroundColor Yellow
    for ($port = $portRangeStart; $port -le $portRangeEnd; $port++) {
        if (Test-Port $port) {
            if ($port -ne $defaultPort) {
                Write-Host "⚠️ Using alternative port $port" -ForegroundColor Yellow
            }
            return $port
        }
    }
    
    throw "No available ports in range $portRangeStart-$portRangeEnd"
}

# Main execution
try {
    # Check if we're in the right directory
    if (-not (Test-Path "src\api\web_app.py")) {
        Write-Host "❌ Error: web_app.py not found. Please run from the project root directory." -ForegroundColor Red
        exit 1
    }
    
    # Check Python availability
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Python not found. Please install Python and add it to PATH." -ForegroundColor Red
        exit 1
    }
    
    # Get available port
    $appPort = Get-AvailablePort
    $baseUrl = "http://localhost:$appPort"
    
    Write-Host "🔧 Port Manager Status:" -ForegroundColor Cyan
    Write-Host "   └─ Using port: $appPort" -ForegroundColor White
    Write-Host "   └─ Base URL: $baseUrl" -ForegroundColor White
    Write-Host ""
    
    Write-Host "🚀 Starting server..." -ForegroundColor Green
    Write-Host "📍 Main Application: $baseUrl/static/combined-ui.html" -ForegroundColor Cyan
    Write-Host "📚 API Documentation: $baseUrl/docs" -ForegroundColor Cyan
    Write-Host "🔄 Alternative Docs: $baseUrl/redoc" -ForegroundColor Cyan
    Write-Host "🛑 Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host "-" * 70
    
    # Change to API directory
    Set-Location "src\api"
    
    # Start the server
    $process = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", $appPort, "--reload" -PassThru -NoNewWindow
    
    # Wait for server to start
    Start-Sleep -Seconds 3
    
    # Open browser
    try {
        $mainUrl = "$baseUrl/static/combined-ui.html"
        Write-Host "🌐 Opening browser: $mainUrl" -ForegroundColor Green
        Start-Process $mainUrl
    }
    catch {
        Write-Host "⚠️ Could not open browser automatically" -ForegroundColor Yellow
        Write-Host "💡 Please manually visit: $mainUrl" -ForegroundColor Cyan
    }
    
    # Wait for user to stop the server
    Write-Host "Press any key to stop the server..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Stop the server
    Write-Host "`n🛑 Shutting down server..." -ForegroundColor Yellow
    Stop-Process -Id $process.Id -Force
    Write-Host "✅ Server stopped" -ForegroundColor Green
    
}
catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}
finally {
    # Return to original directory
    Set-Location $PSScriptRoot
}
