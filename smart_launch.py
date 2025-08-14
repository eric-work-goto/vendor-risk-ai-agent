#!/usr/bin/env python3
"""
Smart Application Launcher
==========================
Intelligent launcher that ensures consistent port usage and prevents conflicts.
"""

import sys
import os
import webbrowser
import time
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from port_config import ensure_app_port, get_base_url, port_manager
except ImportError:
    print("❌ Error: Could not import port_config. Make sure you're running from the project root.")
    sys.exit(1)

def print_banner():
    """Print application banner."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 🚀 VENDOR RISK ASSESSMENT AI                 ║
║                      Smart Launcher v2.0                    ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import fastapi
        import uvicorn
        import langchain
        print("✅ All required dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def start_server():
    """Start the FastAPI server with smart port management."""
    try:
        # Ensure port is available
        app_port = ensure_app_port()
        base_url = get_base_url()
        
        print(f"🔧 Port Manager Status:")
        print(f"   └─ Using port: {app_port}")
        print(f"   └─ Base URL: {base_url}")
        
        # Change to API directory
        api_dir = project_root / "src" / "api"
        os.chdir(api_dir)
        
        print(f"\n🚀 Starting server...")
        print(f"📍 Main Application: {base_url}/static/combined-ui.html")
        print(f"📚 API Documentation: {base_url}/docs")
        print(f"🔄 Alternative Docs: {base_url}/redoc")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 70)
        
        # Start the server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "web_app:app", 
            "--host", "0.0.0.0", 
            "--port", str(app_port),
            "--reload"
        ]
        
        # Start server process
        process = subprocess.Popen(cmd)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        try:
            main_url = f"{base_url}/static/combined-ui.html"
            print(f"🌐 Opening browser: {main_url}")
            webbrowser.open(main_url)
        except Exception as e:
            print(f"⚠️ Could not open browser automatically: {e}")
            print(f"💡 Please manually visit: {main_url}")
        
        # Wait for the server process
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main launcher function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start the server
    if not start_server():
        sys.exit(1)

if __name__ == "__main__":
    main()
