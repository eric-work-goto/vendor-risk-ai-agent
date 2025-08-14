# Vendor Risk AI Agent - Smart Launcher
# =====================================
# Automatically resolves port conflicts and starts the application

param(
    [int]$PreferredPort = 8026,
    [switch]$KillConflicts = $true
)

# Colors for output
$ErrorColor = 'Red'
$WarningColor = 'Yellow'
$SuccessColor = 'Green'
$InfoColor = 'Cyan'

function Write-ColorMessage {
    param([string]$Message, [string]$Color = 'White')
    Write-Host $Message -ForegroundColor $Color
}

function Test-PortAvailable {
    param([int]$Port)
    try {
        $tcpConnection = New-Object System.Net.Sockets.TcpClient
        $tcpConnection.ConnectTimeout = 1000
        $connection = $tcpConnection.BeginConnect('localhost', $Port, $null, $null)
        $wait = $connection.AsyncWaitHandle.WaitOne(1000, $false)
        
        if ($wait) {
            $tcpConnection.EndConnect($connection)
            $tcpConnection.Close()
            return $false  # Port is in use
        } else {
            $tcpConnection.Close()
            return $true   # Port is available
        }
    }
    catch {
        return $true  # Port is available (connection failed)
    }
}

function Stop-PortProcesses {
    param([int]$Port)
    
    Write-ColorMessage "🔄 Attempting to free port $Port..." $WarningColor
    
    try {
        # Get processes using the port
        $netstatOutput = netstat -ano | Select-String ":$Port "
        $processesKilled = 0
        
        foreach ($line in $netstatOutput) {
            if ($line -match 'LISTENING') {
                $parts = $line.ToString().Split(' ', [StringSplitOptions]::RemoveEmptyEntries)
                if ($parts.Length -ge 5) {
                    $pid = $parts[-1]
                    try {
                        Stop-Process -Id $pid -Force -ErrorAction Stop
                        Write-ColorMessage "✅ Killed process $pid using port $Port" $SuccessColor
                        $processesKilled++
                    }
                    catch {
                        Write-ColorMessage "❌ Failed to kill process $pid" $ErrorColor
                    }
                }
            }
        }
        
        if ($processesKilled -gt 0) {
            Start-Sleep -Seconds 2  # Wait for ports to be freed
            return $true
        } else {
            Write-ColorMessage "ℹ️ No processes found using port $Port" $InfoColor
            return $false
        }
    }
    catch {
        Write-ColorMessage "❌ Error while freeing port $Port`: $_" $ErrorColor
        return $false
    }
}

function Get-AvailablePort {
    param([int]$PreferredPort = 8026)
    
    # Try preferred port first
    if (Test-PortAvailable $PreferredPort) {
        return $PreferredPort
    }
    
    # Try to free the preferred port if requested
    if ($KillConflicts) {
        if (Stop-PortProcesses $PreferredPort) {
            if (Test-PortAvailable $PreferredPort) {
                Write-ColorMessage "✅ Port $PreferredPort is now available" $SuccessColor
                return $PreferredPort
            }
        }
    }
    
    # Find alternative port
    Write-ColorMessage "🔍 Finding alternative port..." $InfoColor
    for ($port = 8026; $port -le 8030; $port++) {
        if (Test-PortAvailable $port) {
            if ($port -ne $PreferredPort) {
                Write-ColorMessage "⚠️ Using alternative port $port instead of $PreferredPort" $WarningColor
            }
            return $port
        }
    }
    
    throw "No available ports found in range 8026-8030"
}

# Main execution
try {
    Write-ColorMessage "🔍 Vendor Risk AI Agent - Smart Launcher" $InfoColor
    Write-ColorMessage ("=" * 60) $InfoColor
    Write-Host ""
    
    # Check if we're in the right directory
    if (-not (Test-Path "src\api\web_app.py")) {
        Write-ColorMessage "❌ Please run this script from the project root directory" $ErrorColor
        exit 1
    }
    
    # Check virtual environment
    if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
        Write-ColorMessage "❌ Virtual environment not found. Please run setup first." $ErrorColor
        Write-ColorMessage "   Try running: python -m venv .venv" $InfoColor
        exit 1
    }
    
    Write-ColorMessage "✅ Virtual environment found" $SuccessColor
    
    # Get available port
    $AvailablePort = Get-AvailablePort -PreferredPort $PreferredPort
    Write-ColorMessage "✅ Port $AvailablePort is ready for use" $SuccessColor
    
    # Show URLs
    Write-Host ""
    Write-ColorMessage "🌐 Application URLs:" $InfoColor
    Write-ColorMessage "   • Main App: http://localhost:$AvailablePort/static/combined-ui.html" $InfoColor
    Write-ColorMessage "   • API Docs: http://localhost:$AvailablePort/docs" $InfoColor
    Write-ColorMessage "   • Health Check: http://localhost:$AvailablePort/health" $InfoColor
    Write-Host ""
    
    # Activate virtual environment and start server
    Write-ColorMessage "🚀 Starting application on port $AvailablePort..." $InfoColor
    Write-ColorMessage "   Use Ctrl+C to stop the server" $InfoColor
    Write-ColorMessage ("-" * 60) $InfoColor
    
    & .\.venv\Scripts\Activate.ps1
    python -m uvicorn src.api.web_app:app --host 127.0.0.1 --port $AvailablePort --reload
}
catch {
    Write-Host ""
    Write-ColorMessage "❌ Error: $_" $ErrorColor
    Write-Host ""
    Write-ColorMessage "📋 Troubleshooting:" $InfoColor
    Write-ColorMessage "   1. Make sure you're in the project directory" $InfoColor
    Write-ColorMessage "   2. Check if virtual environment is set up: python -m venv .venv" $InfoColor
    Write-ColorMessage "   3. Install dependencies: pip install -r requirements.txt" $InfoColor
    exit 1
}
finally {
    Write-Host ""
    Write-ColorMessage "👋 Application stopped" $InfoColor
}
