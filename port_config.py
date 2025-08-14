"""
Port Configuration Management
=============================
Centralized port configuration to prevent port conflicts and ensure consistency.
"""

import os
import socket
from typing import Optional

# Default application port - change this ONE place to update everywhere
DEFAULT_PORT = 8028

# Port range for fallback options
PORT_RANGE_START = 8028
PORT_RANGE_END = 8032

class PortManager:
    """Manages port configuration and availability checking."""
    
    def __init__(self):
        self.default_port = DEFAULT_PORT
        self.current_port = None
    
    def is_port_available(self, port: int) -> bool:
        """Check if a port is available for use."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                return result != 0  # Port is available if connection fails
        except Exception:
            return False
    
    def get_available_port(self, preferred_port: Optional[int] = None) -> int:
        """
        Get an available port, preferring the default port.
        
        Args:
            preferred_port: Port to try first (defaults to DEFAULT_PORT)
            
        Returns:
            Available port number
            
        Raises:
            RuntimeError: If no ports are available in the range
        """
        if preferred_port is None:
            preferred_port = self.default_port
        
        # First try the preferred port
        if self.is_port_available(preferred_port):
            self.current_port = preferred_port
            return preferred_port
        
        # If preferred port is busy, try range
        for port in range(PORT_RANGE_START, PORT_RANGE_END + 1):
            if self.is_port_available(port):
                self.current_port = port
                print(f"⚠️ Default port {preferred_port} is busy, using port {port}")
                return port
        
        raise RuntimeError(f"No available ports in range {PORT_RANGE_START}-{PORT_RANGE_END}")
    
    def kill_port_process(self, port: int) -> bool:
        """
        Kill any process using the specified port.
        
        Args:
            port: Port number to clear
            
        Returns:
            True if process was killed or port was already free
        """
        try:
            import subprocess
            import sys
            
            if sys.platform == "win32":
                # Windows: Find and kill process using the port
                result = subprocess.run(
                    f'netstat -ano | findstr :{port}',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if f':{port}' in line and 'LISTENING' in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                pid = parts[-1]
                                try:
                                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, check=True)
                                    print(f"✅ Killed process {pid} using port {port}")
                                    return True
                                except subprocess.CalledProcessError:
                                    print(f"❌ Failed to kill process {pid}")
                                    return False
            else:
                # Unix/Linux/Mac: Kill process using the port
                result = subprocess.run(
                    f"lsof -ti:{port}",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.stdout:
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid:
                            try:
                                subprocess.run(f"kill -9 {pid}", shell=True, check=True)
                                print(f"✅ Killed process {pid} using port {port}")
                                return True
                            except subprocess.CalledProcessError:
                                print(f"❌ Failed to kill process {pid}")
                                return False
            
            return True  # Port was already free
            
        except Exception as e:
            print(f"❌ Error killing process on port {port}: {e}")
            return False
    
    def ensure_port_available(self, port: Optional[int] = None) -> int:
        """
        Ensure a port is available, killing existing processes if necessary.
        
        Args:
            port: Port to ensure is available (defaults to DEFAULT_PORT)
            
        Returns:
            Available port number
        """
        if port is None:
            port = self.default_port
        
        if not self.is_port_available(port):
            print(f"🔄 Port {port} is busy, attempting to free it...")
            if self.kill_port_process(port):
                # Wait a moment for the port to be freed
                import time
                time.sleep(2)
                
                if self.is_port_available(port):
                    print(f"✅ Port {port} is now available")
                    self.current_port = port
                    return port
                else:
                    print(f"❌ Could not free port {port}, finding alternative...")
                    return self.get_available_port()
            else:
                return self.get_available_port()
        else:
            self.current_port = port
            return port

# Global port manager instance
port_manager = PortManager()

def get_app_port() -> int:
    """Get the current application port."""
    return port_manager.current_port or DEFAULT_PORT

def ensure_app_port() -> int:
    """Ensure the application port is available."""
    return port_manager.ensure_port_available()

def get_base_url() -> str:
    """Get the base URL for the application."""
    return f"http://localhost:{get_app_port()}"

if __name__ == "__main__":
    # Test the port manager
    print("🔍 Testing Port Manager...")
    print(f"Default port: {DEFAULT_PORT}")
    
    available_port = port_manager.get_available_port()
    print(f"Available port: {available_port}")
    
    base_url = get_base_url()
    print(f"Base URL: {base_url}")
