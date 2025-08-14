#!/usr/bin/env python3
"""
🚀 Vendor Risk Assessment AI - Easy Launcher
==================================================

This script provides an easy way to launch the Vendor Risk Assessment AI application.
Simply run this script and it will handle all the setup and launch the web interface.

Usage:
    python launch.py
    
The application will be available at: http://localhost:8026/static/assessment.html
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("=" * 70)
    print("🚀 Vendor Risk Assessment AI - Application Launcher")
    print("=" * 70)
    print()

def check_directory():
    """Ensure we're in the correct directory"""
    if not Path("src/api/web_app.py").exists():
        print("❌ Error: This script must be run from the vendor-risk-ai-agent directory")
        print("Please navigate to the correct directory and try again.")
        input("Press Enter to exit...")
        sys.exit(1)

def activate_venv():
    """Check and activate virtual environment"""
    print("🔧 Checking virtual environment...")
    
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please run the setup script first to create the virtual environment.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check if we're already in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is already active")
        return True
    
    print("⚠️ Virtual environment exists but is not active")
    print("Please run this script from within the activated virtual environment")
    print("Or use launch.bat for automatic activation")
    return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'pandas', 'openpyxl', 'aiohttp'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🚨 Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "-r", "requirements.txt"
            ], check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please install them manually: pip install -r requirements.txt")
            input("Press Enter to exit...")
            sys.exit(1)

def run_health_check():
    """Run the health check"""
    print("🏥 Running health check...")
    
    try:
        result = subprocess.run([
            sys.executable, "health_check.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Health check passed!")
            return True
        else:
            print("⚠️ Health check found some issues:")
            print(result.stdout)
            
            response = input("Do you want to continue anyway? (y/N): ").lower()
            return response in ['y', 'yes']
            
    except Exception as e:
        print(f"⚠️ Could not run health check: {e}")
        response = input("Do you want to continue anyway? (y/N): ").lower()
        return response in ['y', 'yes']

def start_server():
    """Start the FastAPI server"""
    print("🌐 Starting Vendor Risk Assessment AI server...")
    print()
    print("📍 Server will be available at:")
    print("   • Web Interface: http://localhost:8026/static/assessment.html")
    print("   • API Documentation: http://localhost:8026/docs")
    print()
    print("⚠️ Keep this window open while using the application")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    # Wait a moment then open browser
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:8026/static/assessment.html")
        except:
            pass
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Change to API directory and start server
    os.chdir("src/api")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "web_app:app", 
            "--host", "0.0.0.0", 
            "--port", "8026",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
    
    print("\nPress Enter to exit...")
    input()

def main():
    """Main launcher function"""
    print_banner()
    
    # Step 1: Check directory
    check_directory()
    
    # Step 2: Check virtual environment
    if not activate_venv():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Step 3: Check dependencies
    check_dependencies()
    
    # Step 4: Run health check
    if not run_health_check():
        print("Exiting due to health check issues.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Step 5: Start server
    print("🚀 Starting application...")
    print()
    start_server()

if __name__ == "__main__":
    main()
