#!/usr/bin/env python3
"""
Web application startup script for Vendor Risk Assessment AI
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("🚀 Starting Vendor Risk Assessment AI Web Application...")
    print("📍 URL: http://localhost:8026")
    print("📚 API Docs: http://localhost:8026/docs")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Use the module import string for reload functionality
        uvicorn.run(
            "src.api.web_app:app",
            host="0.0.0.0",
            port=8026,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)
