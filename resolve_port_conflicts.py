#!/usr/bin/env python3
"""
Port Conflict Resolver
=====================
Automatically resolves port 8026 conflicts and starts the application.
"""

import sys
import subprocess
import time
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from port_config import port_manager, get_base_url
except ImportError:
    print("❌ Could not import port_config. Make sure you're in the project directory.")
    sys.exit(1)

def main():
    """Resolve port conflicts and start the application."""
    
    print("🔍 Vendor Risk AI Agent - Port Conflict Resolver")
    print("=" * 60)
    
    # Step 1: Ensure port is available (will automatically kill conflicting processes)
    try:
        available_port = port_manager.ensure_port_available()
        print(f"✅ Port {available_port} is ready for use")
        
        if available_port != 8026:
            print(f"⚠️ Using alternative port {available_port} instead of default 8026")
        
    except Exception as e:
        print(f"❌ Could not resolve port conflicts: {e}")
        sys.exit(1)
    
    # Step 2: Show connection info
    base_url = get_base_url()
    print("\n🌐 Application URLs:")
    print(f"   • Main App: {base_url}/static/combined-ui.html")
    print(f"   • API Docs: {base_url}/docs")
    print(f"   • Health Check: {base_url}/health")
    
    # Step 3: Start the application
    print(f"\n🚀 Starting application on port {available_port}...")
    
    try:
        # Change to the project directory
        project_dir = Path(__file__).parent
        
        # Activate virtual environment and start uvicorn
        if sys.platform == "win32":
            activate_script = project_dir / ".venv" / "Scripts" / "Activate.ps1"
            cmd = [
                "powershell.exe", "-Command",
                f"cd '{project_dir}'; & '{activate_script}'; python -m uvicorn src.api.web_app:app --host 127.0.0.1 --port {available_port} --reload"
            ]
        else:
            cmd = [
                "bash", "-c",
                f"cd '{project_dir}' && source .venv/bin/activate && python -m uvicorn src.api.web_app:app --host 127.0.0.1 --port {available_port} --reload"
            ]
        
        print("📝 Starting server...")
        print("   Use Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the server
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
