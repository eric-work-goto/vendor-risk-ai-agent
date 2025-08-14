# Simple PowerShell Launcher
param([switch]$SkipBrowser = $false)

Write-Host "🚀 Starting Vendor Risk Assessment Application" -ForegroundColor Green

# Get available port
$port = & python -c "from port_config import port_manager; print(port_manager.ensure_port_available())"
$baseUrl = "http://localhost:$port"

Write-Host "✅ Using port: $port" -ForegroundColor Green
Write-Host "🌐 Base URL: $baseUrl" -ForegroundColor Cyan

# Start server in background
Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "src.api.web_app:app", "--host", "127.0.0.1", "--port", $port -WindowStyle Hidden

# Wait for server to start
Start-Sleep -Seconds 3

# Open browser if requested
if (-not $SkipBrowser) {
    $url = "$baseUrl/static/combined-ui.html"
    Write-Host "🌐 Opening: $url" -ForegroundColor Cyan
    Start-Process $url
}

Write-Host ""
Write-Host "🎯 APPLICATION READY!" -ForegroundColor Green
Write-Host "📍 Main App: $baseUrl/static/combined-ui.html" -ForegroundColor White
Write-Host "📚 API Docs: $baseUrl/docs" -ForegroundColor White
Write-Host ""
Write-Host "Server is running independently in the background." -ForegroundColor Yellow
