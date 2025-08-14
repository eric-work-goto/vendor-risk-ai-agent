#!/bin/bash
# Vendor Risk Assessment AI - Bash Launcher
# Cross-platform launcher for Unix-like systems (Linux, macOS, WSL)

echo "=================================================="
echo "  🛡️  Vendor Risk Assessment AI - Launcher"
echo "=================================================="
echo

# Check if we're in the correct directory
if [ ! -f "src/api/web_app.py" ]; then
    echo "❌ ERROR: This script must be run from the vendor-risk-ai-agent directory"
    echo "Please navigate to the correct directory and try again."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "[1/5] Checking virtual environment..."
# Check for virtual environment
if [ -f ".venv/bin/activate" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    echo "✅ Activating virtual environment (Windows-style)..."
    source .venv/Scripts/activate
else
    echo "⚠️  Virtual environment not found. Using system Python."
fi

echo "[2/5] Checking dependencies..."
# Check if required packages are installed
python -c "import fastapi, uvicorn, pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing missing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: Failed to install dependencies"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi
echo "✅ Dependencies verified"

echo "[3/5] Running health check..."
python health_check.py
if [ $? -ne 0 ]; then
    echo "⚠️  WARNING: Health check found some issues"
    echo "The application may still work, but please review the health check output"
    echo
    read -p "Do you want to continue anyway? (y/n): " continue_choice
    if [ "$continue_choice" != "y" ] && [ "$continue_choice" != "Y" ]; then
        exit 1
    fi
else
    echo "✅ Health check passed"
fi

echo "[4/5] Preparing browser launch..."
# Function to open browser (cross-platform)
open_browser() {
    sleep 3  # Wait for server to start
    if command -v xdg-open > /dev/null; then
        xdg-open "http://localhost:8026/static/assessment.html" 2>/dev/null
    elif command -v open > /dev/null; then
        open "http://localhost:8026/static/assessment.html" 2>/dev/null
    elif command -v start > /dev/null; then
        start "http://localhost:8026/static/assessment.html" 2>/dev/null
    else
        echo "🌐 Please manually open: http://localhost:8026/static/assessment.html"
    fi
}

echo "[5/5] Starting the application..."
echo
echo "✅ Application is starting..."
echo "🌐 Web interface: http://localhost:8026/static/assessment.html"
echo "📚 API documentation: http://localhost:8026/docs"
echo
echo "⚠️  To stop the application, press Ctrl+C"
echo

# Start browser in background
open_browser &

# Change to API directory and start server
cd src/api
python -m uvicorn web_app:app --host 0.0.0.0 --port 8026

# Cleanup
cd ../..
echo
echo "👋 Thank you for using Vendor Risk Assessment AI!"
