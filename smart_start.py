#!/usr/bin/env python3
"""
Smart Application Launcher
==========================
Automatically handles port management and starts the vendor risk assessment application.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from port_config import port_manager, get_base_url
    print("✅ Port configuration loaded successfully")
except ImportError as e:
    print(f"❌ Error loading port configuration: {e}")
    sys.exit(1)

def check_python_version():
    """Ensure we have a compatible Python version."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_virtual_environment():
    """Check if we're in a virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✅ Virtual environment detected")
    else:
        print("⚠️ Not in a virtual environment - dependencies may conflict")
    
    return in_venv

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, cwd=project_root)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("⚠️ requirements.txt not found - assuming dependencies are already installed")
        return True

def start_server(port: int):
    """Start the FastAPI server on the specified port."""
    print(f"🚀 Starting server on port {port}...")
    
    # Change to project directory
    os.chdir(project_root)
    
    # Start uvicorn server
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.api.web_app:app", 
        "--host", "127.0.0.1", 
        "--port", str(port),
        "--reload"
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Check if server started successfully
        if process.poll() is None:
            print(f"✅ Server started successfully on port {port}")
            return process
        else:
            print("❌ Server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None

def open_browser(base_url: str):
    """Open the application in the default browser."""
    main_url = f"{base_url}/static/combined-ui.html"
    
    print(f"🌐 Opening browser at {main_url}")
    
    try:
        webbrowser.open(main_url)
        print("✅ Browser opened successfully")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print(f"📍 Please manually navigate to: {main_url}")

def main():
    """Main launcher function."""
    print("🚀 Smart Application Launcher")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Check virtual environment
    in_venv = check_virtual_environment()
    
    # Install dependencies if needed
    if not install_dependencies():
        print("❌ Cannot proceed without dependencies")
        sys.exit(1)
    
    # Get available port
    try:
        available_port = port_manager.ensure_port_available()
        base_url = f"http://localhost:{available_port}"
        
        print(f"🔌 Using port: {available_port}")
        print(f"🌐 Base URL: {base_url}")
        
    except RuntimeError as e:
        print(f"❌ Port management error: {e}")
        sys.exit(1)
    
    # Start the server
    server_process = start_server(available_port)
    
    if server_process is None:
        print("❌ Failed to start server")
        sys.exit(1)
    
    # Open browser
    open_browser(base_url)
    
    # Display information
    print("\n" + "=" * 50)
    print("🎯 APPLICATION READY")
    print("=" * 50)
    print(f"📍 Main Application: {base_url}/static/combined-ui.html")
    print(f"📚 API Documentation: {base_url}/docs")
    print(f"🔄 Alternative Docs: {base_url}/redoc")
    print(f"🔍 Health Check: {base_url}/health")
    print("=" * 50)
    print("⚠️ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Keep the script running and monitor the server
        while True:
            time.sleep(1)
            if server_process.poll() is not None:
                print("❌ Server process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
        
    finally:
        # Clean up
        if server_process and server_process.poll() is None:
            print("🔄 Stopping server...")
            server_process.terminate()
            
            # Wait for graceful shutdown
            try:
                server_process.wait(timeout=5)
                print("✅ Server stopped gracefully")
            except subprocess.TimeoutExpired:
                print("⚠️ Force killing server...")
                server_process.kill()
                server_process.wait()
                print("✅ Server force stopped")

if __name__ == "__main__":
    main()
