# Smart Application Launcher for Windows
# =====================================
# Automatically handles port management and starts the vendor risk assessment application.

param(
    [int]$PreferredPort = 0,  # 0 means use default from port_config.py
    [switch]$KillExisting = $false,
    [switch]$SkipBrowser = $false,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host @"
🚀 Smart Application Launcher
============================

USAGE:
    .\smart_start.ps1 [OPTIONS]

OPTIONS:
    -PreferredPort <number>  : Specify a preferred port (default: auto-detect)
    -KillExisting           : Kill any existing processes on the target port
    -SkipBrowser           : Don't open browser automatically
    -Help                  : Show this help message

EXAMPLES:
    .\smart_start.ps1                    # Start with default settings
    .\smart_start.ps1 -PreferredPort 8029  # Use specific port
    .\smart_start.ps1 -KillExisting        # Kill existing processes first
    .\smart_start.ps1 -SkipBrowser         # Don't open browser

"@ -ForegroundColor Cyan
    exit 0
}

function Write-Status {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Test-PythonVersion {
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            
            if ($major -ge 3 -and $minor -ge 8) {
                Write-Status "✅ Python $major.$minor detected" "Green"
                return $true
            } else {
                Write-Status "❌ Python 3.8 or higher required, found $major.$minor" "Red"
                return $false
            }
        } else {
            Write-Status "❌ Could not determine Python version" "Red"
            return $false
        }
    } catch {
        Write-Status "❌ Python not found in PATH" "Red"
        Write-Status "   Please install Python 3.8+ and add it to your PATH" "Yellow"
        return $false
    }
}

function Test-VirtualEnvironment {
    $venvPath = $env:VIRTUAL_ENV
    if ($venvPath) {
        Write-Status "✅ Virtual environment detected: $venvPath" "Green"
        return $true
    } else {
        Write-Status "⚠️ Not in a virtual environment - dependencies may conflict" "Yellow"
        return $false
    }
}

function Install-Dependencies {
    Write-Status "📦 Installing dependencies..." "Cyan"
    
    if (Test-Path "requirements.txt") {
        try {
            & python -m pip install -r requirements.txt
            if ($LASTEXITCODE -eq 0) {
                Write-Status "✅ Dependencies installed successfully" "Green"
                return $true
            } else {
                Write-Status "❌ Failed to install dependencies" "Red"
                return $false
            }
        } catch {
            Write-Status "❌ Error installing dependencies: $_" "Red"
            return $false
        }
    } else {
        Write-Status "⚠️ requirements.txt not found - assuming dependencies are installed" "Yellow"
        return $true
    }
}

function Get-ApplicationPort {
    Write-Status "🔌 Determining application port..." "Cyan"
    
    try {
        if ($PreferredPort -gt 0) {
            $portScript = @"
import sys
import os
sys.path.insert(0, os.getcwd())
from port_config import port_manager
try:
    port = port_manager.ensure_port_available($PreferredPort)
    print(port)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
"@
        } else {
            $portScript = @"
import sys
import os
sys.path.insert(0, os.getcwd())
from port_config import port_manager
try:
    port = port_manager.ensure_port_available()
    print(port)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
"@
        }
        
        $result = & python -c $portScript
        
        if ($LASTEXITCODE -eq 0 -and $result -match "^\d+$") {
            $port = [int]$result
            Write-Status "✅ Using port: $port" "Green"
            return $port
        } else {
            Write-Status "❌ Port management error: $result" "Red"
            return $null
        }
    } catch {
        Write-Status "❌ Error determining port: $_" "Red"
        return $null
    }
}

function Start-Server {
    param([int]$Port)
    
    Write-Status "🚀 Starting server on port $Port..." "Cyan"
    
    try {
        $process = Start-Process -FilePath "python" -ArgumentList @(
            "-m", "uvicorn", 
            "src.api.web_app:app", 
            "--host", "127.0.0.1", 
            "--port", $Port.ToString(),
            "--reload"
        ) -PassThru -NoNewWindow
        
        # Wait for server to start
        Write-Status "⏳ Waiting for server to start..." "Yellow"
        Start-Sleep -Seconds 3
        
        # Check if process is still running
        if (-not $process.HasExited) {
            Write-Status "✅ Server started successfully on port $Port" "Green"
            return $process
        } else {
            Write-Status "❌ Server failed to start (process exited)" "Red"
            return $null
        }
    } catch {
        Write-Status "❌ Error starting server: $_" "Red"
        return $null
    }
}

function Open-Browser {
    param([string]$BaseUrl)
    
    if ($SkipBrowser) {
        Write-Status "⏭️ Skipping browser launch" "Yellow"
        return
    }
    
    $mainUrl = "$BaseUrl/static/combined-ui.html"
    
    Write-Status "🌐 Opening browser at $mainUrl" "Cyan"
    
    try {
        Start-Process $mainUrl
        Write-Status "✅ Browser opened successfully" "Green"
    } catch {
        Write-Status "⚠️ Could not open browser automatically: $_" "Yellow"
        Write-Status "📍 Please manually navigate to: $mainUrl" "Cyan"
    }
}

function Show-ApplicationInfo {
    param([string]$BaseUrl)
    
    Write-Host ""
    Write-Host ("=" * 50) -ForegroundColor Cyan
    Write-Host "🎯 APPLICATION READY" -ForegroundColor Green
    Write-Host ("=" * 50) -ForegroundColor Cyan
    Write-Host "📍 Main Application: $BaseUrl/static/combined-ui.html" -ForegroundColor White
    Write-Host "📚 API Documentation: $BaseUrl/docs" -ForegroundColor White
    Write-Host "🔄 Alternative Docs: $BaseUrl/redoc" -ForegroundColor White
    Write-Host "🔍 Health Check: $BaseUrl/health" -ForegroundColor White
    Write-Host ("=" * 50) -ForegroundColor Cyan
    Write-Host "⚠️ Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ("=" * 50) -ForegroundColor Cyan
}

# Main execution
function Main {
    Write-Host "🚀 Smart Application Launcher" -ForegroundColor Cyan
    Write-Host ("=" * 40) -ForegroundColor Cyan
    
    # Check Python version
    if (-not (Test-PythonVersion)) {
        exit 1
    }
    
    # Check virtual environment
    Test-VirtualEnvironment | Out-Null
    
    # Install dependencies
    if (-not (Install-Dependencies)) {
        Write-Status "❌ Cannot proceed without dependencies" "Red"
        exit 1
    }
    
    # Get application port
    $port = Get-ApplicationPort
    if (-not $port) {
        Write-Status "❌ Could not determine application port" "Red"
        exit 1
    }
    
    $baseUrl = "http://localhost:$port"
    
    # Start server
    $serverProcess = Start-Server -Port $port
    if (-not $serverProcess) {
        Write-Status "❌ Failed to start server" "Red"
        exit 1
    }
    
    # Open browser
    Open-Browser -BaseUrl $baseUrl
    
    # Show application info
    Show-ApplicationInfo -BaseUrl $baseUrl
    
    try {
        # Keep script running and monitor server
        while (-not $serverProcess.HasExited) {
            Start-Sleep -Seconds 1
        }
        Write-Status "❌ Server process stopped unexpectedly" "Red"
    } catch {
        Write-Host ""
        Write-Status "🛑 Shutdown requested" "Yellow"
    } finally {
        # Cleanup
        if ($serverProcess -and -not $serverProcess.HasExited) {
            Write-Status "🔄 Stopping server..." "Yellow"
            try {
                $serverProcess.Kill()
                $serverProcess.WaitForExit(5000)
                Write-Status "✅ Server stopped" "Green"
            } catch {
                Write-Status "⚠️ Error stopping server: $_" "Yellow"
            }
        }
    }
}

# Run main function
Main
