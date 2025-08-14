# Vendor Risk Assessment AI - PowerShell Launcher
# This script provides an easy way to start the application

param(
    [switch]$SkipHealthCheck,
    [int]$Port = 8026
)

# Set up colors and formatting
$Host.UI.RawUI.WindowTitle = "Vendor Risk Assessment AI Launcher"

function Write-Banner {
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "🚀 Vendor Risk Assessment AI - PowerShell Launcher" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param($StepNumber, $StepName)
    Write-Host "[$StepNumber/5] $StepName..." -ForegroundColor Yellow
}

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️ $Message" -ForegroundColor Yellow
}

function Write-Info {
    param($Message)
    Write-Host "ℹ️ $Message" -ForegroundColor Blue
}

# Main execution
try {
    Clear-Host
    Write-Banner
    
    # Step 1: Check directory
    Write-Step 1 "Checking application directory"
    if (-not (Test-Path "src\api\web_app.py")) {
        Write-Error "Application files not found!"
        Write-Host "Please ensure you're running this script from the vendor-risk-ai-agent directory."
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Success "Application directory verified"
    
    # Step 2: Activate virtual environment
    Write-Step 2 "Setting up Python environment"
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        try {
            & ".\.venv\Scripts\Activate.ps1"
            Write-Success "Virtual environment activated"
        }
        catch {
            Write-Warning "Could not activate virtual environment, using system Python"
        }
    }
    else {
        Write-Warning "Virtual environment not found, using system Python"
    }
    
    # Step 3: Check and install dependencies
    Write-Step 3 "Checking dependencies"
    
    $requiredPackages = @("fastapi", "uvicorn", "pandas", "openpyxl")
    $missingPackages = @()
    
    foreach ($package in $requiredPackages) {
        try {
            python -c "import $($package.Replace('-', '_'))" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ $package" -ForegroundColor Green
            }
            else {
                Write-Host "  ❌ $package - MISSING" -ForegroundColor Red
                $missingPackages += $package
            }
        }
        catch {
            Write-Host "  ❌ $package - MISSING" -ForegroundColor Red
            $missingPackages += $package
        }
    }
    
    if ($missingPackages.Count -gt 0) {
        Write-Warning "Installing missing packages: $($missingPackages -join ', ')"
        pip install $missingPackages
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install dependencies"
            Read-Host "Press Enter to exit"
            exit 1
        }
        Write-Success "Dependencies installed"
    }
    
    # Step 4: Health check (optional)
    if (-not $SkipHealthCheck) {
        Write-Step 4 "Running health check"
        try {
            python health_check.py
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Health check passed"
            }
            else {
                Write-Warning "Health check found issues"
                $continue = Read-Host "Continue anyway? (y/N)"
                if ($continue -notmatch "^[yY]") {
                    Write-Host "Exiting..."
                    exit 1
                }
            }
        }
        catch {
            Write-Warning "Could not run health check"
        }
    }
    else {
        Write-Host "[4/5] Skipping health check..." -ForegroundColor Yellow
    }
    
    # Step 5: Start the server
    Write-Step 5 "Starting application server"
    Write-Host ""
    Write-Success "Application is starting..."
    Write-Info "Web interface: http://localhost:$Port/static/assessment.html"
    Write-Info "API documentation: http://localhost:$Port/docs"
    Write-Host ""
    Write-Warning "Keep this window open while using the application"
    Write-Warning "Press Ctrl+C to stop the server"
    Write-Host ""
    
    # Open browser after a delay
    Start-Job {
        Start-Sleep 3
        Start-Process "http://localhost:$using:Port/static/assessment.html"
    } | Out-Null
    
    # Change to API directory and start server
    Set-Location "src\api"
    python -m uvicorn web_app:app --host 0.0.0.0 --port $Port --reload
    
}
catch {
    Write-Error "An error occurred: $_"
}
finally {
    Write-Host ""
    Write-Host "👋 Application stopped." -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
}
