#!/usr/bin/env python3
"""
Vendor Risk Assessment AI - Python Launcher
Cross-platform launcher that works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("=" * 50)
    print("  🛡️  Vendor Risk Assessment AI - Launcher")
    print("=" * 50)
    print()

def check_directory():
    """Check if we're in the correct directory"""
    if not Path("src/api/web_app.py").exists():
        print("❌ ERROR: This script must be run from the vendor-risk-ai-agent directory")
        print("Please navigate to the correct directory and try again.")
        input("Press Enter to exit...")
        sys.exit(1)

def activate_virtual_environment():
    """Activate virtual environment based on platform"""
    print("[1/5] Checking virtual environment...")
    
    # Check if virtual environment exists
    venv_paths = {
        'Windows': Path('.venv/Scripts/python.exe'),
        'Linux': Path('.venv/bin/python'),
        'Darwin': Path('.venv/bin/python')  # macOS
    }
    
    system = platform.system()
    venv_python = venv_paths.get(system)
    
    if not venv_python or not venv_python.exists():
        print("⚠️  Virtual environment not found. Using system Python.")
        return sys.executable
    
    print("✅ Virtual environment found")
    return str(venv_python)

def check_dependencies(python_exe):
    """Check and install dependencies"""
    print("[2/5] Checking dependencies...")
    
    # Test critical imports
    test_cmd = [python_exe, "-c", "import fastapi, uvicorn, pandas, openpyxl"]
    result = subprocess.run(test_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("📦 Installing missing dependencies...")
        install_cmd = [python_exe, "-m", "pip", "install", "-r", "requirements.txt"]
        result = subprocess.run(install_cmd)
        
        if result.returncode != 0:
            print("❌ ERROR: Failed to install dependencies")
            input("Press Enter to exit...")
            sys.exit(1)
    
    print("✅ Dependencies verified")

def run_health_check(python_exe):
    """Run health check"""
    print("[3/5] Running health check...")
    
    result = subprocess.run([python_exe, "health_check.py"])
    
    if result.returncode != 0:
        print("⚠️  WARNING: Health check found some issues")
        print("The application may still work, but please review the health check output")
        print()
        response = input("Do you want to continue anyway? (y/n): ").lower()
        if response not in ['y', 'yes']:
            sys.exit(1)
    else:
        print("✅ Health check passed")

def open_browser():
    """Open browser to application URL"""
    print("[4/5] Preparing to open browser...")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    try:
        webbrowser.open('http://localhost:8026/static/assessment.html')
        print("🌐 Browser opened to application interface")
    except Exception as e:
        print(f"⚠️  Could not automatically open browser: {e}")
        print("Please manually open: http://localhost:8026/static/assessment.html")

def start_server(python_exe):
    """Start the FastAPI server"""
    print("[5/5] Starting the application...")
    print()
    print("✅ Application is starting...")
    print("🌐 Web interface: http://localhost:8026/static/assessment.html")
    print("📚 API documentation: http://localhost:8026/docs")
    print()
    print("⚠️  To stop the application, press Ctrl+C")
    print()
    
    # Start server with auto-browser opening
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Change to API directory and start uvicorn server
        original_dir = os.getcwd()
        os.chdir("src/api")
        
        cmd = [python_exe, "-m", "uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8026"]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Trying alternative startup method...")
        try:
            # Alternative method using Python path
            import sys
            if python_exe != sys.executable:
                # If using venv, try with current Python
                cmd = [sys.executable, "-m", "uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8026"]
                subprocess.run(cmd)
            else:
                raise e
        except Exception as e2:
            print(f"❌ Alternative startup also failed: {e2}")
    finally:
        # Return to original directory
        os.chdir(original_dir)
        print("\n👋 Thank you for using Vendor Risk Assessment AI!")

def main():
    """Main launcher function"""
    try:
        print_banner()
        check_directory()
        python_exe = activate_virtual_environment()
        check_dependencies(python_exe)
        run_health_check(python_exe)
        start_server(python_exe)
    except KeyboardInterrupt:
        print("\n\n🛑 Launch cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
