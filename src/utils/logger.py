"""
Logging utility for the application
"""

import sys
from pathlib import Path


def setup_logger(name: str):
    """
    Setup logger for the application
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    # Simple print-based logger for now
    # In production, would use proper logging framework
    
    class SimpleLogger:
        def __init__(self, name):
            self.name = name
        
        def info(self, message):
            print(f"[INFO] {self.name}: {message}")
        
        def error(self, message):
            print(f"[ERROR] {self.name}: {message}", file=sys.stderr)
        
        def warning(self, message):
            print(f"[WARNING] {self.name}: {message}")
        
        def debug(self, message):
            print(f"[DEBUG] {self.name}: {message}")
    
    return SimpleLogger(name)
