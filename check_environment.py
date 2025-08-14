#!/usr/bin/env python3
"""
Environment setup verification script
"""

import sys
import os
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("🔧 Checking Vendor Risk AI Agent Environment...")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python Version: {sys.version}")
    
    # Check if we're in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment: Active")
    else:
        print("⚠️  Virtual environment: Not detected")
    
    # Check required packages
    required_packages = [
        'fastapi', 'uvicorn', 'openai', 'langchain', 'sqlalchemy', 
        'pydantic', 'requests', 'aiohttp', 'bs4', 'PyPDF2'
    ]
    
    print("\n📦 Checking Required Packages:")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing_packages.append(package)
    
    # Check .env file
    print("\n⚙️  Checking Configuration:")
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ .env file exists")
        
        # Check for OpenAI API key
        with open(env_file, 'r') as f:
            content = f.read()
            if "your_openai_api_key_here" in content:
                print("   ⚠️  OpenAI API key needs to be set in .env file")
            elif "OPENAI_API_KEY=" in content and len(content.split("OPENAI_API_KEY=")[1].split("\n")[0].strip()) > 10:
                print("   ✅ OpenAI API key appears to be configured")
            else:
                print("   ⚠️  OpenAI API key not found in .env file")
    else:
        print("   ❌ .env file missing")
    
    # Check project structure
    print("\n📁 Checking Project Structure:")
    required_dirs = [
        "src", "src/agents", "src/api", "src/models", 
        "src/services", "src/utils", "src/config"
    ]
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"   ✅ {directory}/")
        else:
            print(f"   ❌ {directory}/ (missing)")
    
    # Summary
    print("\n" + "=" * 50)
    if missing_packages:
        print("❌ Setup Issues Found:")
        print(f"   Missing packages: {', '.join(missing_packages)}")
        print("\n💡 To fix missing packages, run:")
        print(f"   pip install {' '.join(missing_packages)}")
    else:
        print("✅ Environment Setup Complete!")
    
    print("\n🚀 Next Steps:")
    print("   1. Add your OpenAI API key to .env file")
    print("   2. Test the system: python test_basic.py")
    print("   3. Run full demo: python demo.py")
    print("   4. Start web API: python src/api/app.py")
    
    return len(missing_packages) == 0


if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)
