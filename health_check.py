#!/usr/bin/env python3
"""
Comprehensive Program Health Check
This script checks for common errors, missing dependencies, and configuration issues
in the Vendor Risk Assessment AI system.
"""

import sys
import os
import importlib
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'), 
        ('python-multipart', 'multipart'),
        ('pandas', 'pandas'),
        ('openpyxl', 'openpyxl'),
        ('aiohttp', 'aiohttp'),
        ('beautifulsoup4', 'bs4'),
        ('requests', 'requests'),
        ('pydantic', 'pydantic')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            importlib.import_module(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n🚨 Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_project_structure():
    """Check if project structure is correct"""
    print("\n📁 Checking project structure...")
    
    required_paths = [
        'src/api/web_app.py',
        'src/api/static/assessment.html',
        'requirements.txt',
        '.env.example'
    ]
    
    missing_paths = []
    
    for path in required_paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - MISSING")
            missing_paths.append(path)
    
    return len(missing_paths) == 0

def check_syntax_errors():
    """Check for syntax errors in Python files"""
    print("\n🔍 Checking for syntax errors...")
    
    python_files = [
        'src/api/web_app.py'
    ]
    
    errors_found = False
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), file_path, 'exec')
                print(f"✅ {file_path} - No syntax errors")
            except SyntaxError as e:
                print(f"❌ {file_path} - Syntax error: {e}")
                errors_found = True
        else:
            print(f"❌ {file_path} - File not found")
            errors_found = True
    
    return not errors_found

def check_configuration():
    """Check configuration files"""
    print("\n⚙️ Checking configuration...")
    
    config_issues = []
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            env_content = f.read()
            if 'OPENAI_API_KEY' in env_content and 'your_openai_api_key_here' in env_content:
                config_issues.append("OPENAI_API_KEY not configured")
    else:
        config_issues.append(".env file missing")
    
    # Check requirements.txt
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt exists")
        with open('requirements.txt', 'r') as f:
            req_content = f.read()
            if 'pandas' not in req_content:
                config_issues.append("pandas missing from requirements.txt")
            if 'openpyxl' not in req_content:
                config_issues.append("openpyxl missing from requirements.txt")
    else:
        config_issues.append("requirements.txt missing")
    
    if config_issues:
        for issue in config_issues:
            print(f"⚠️ {issue}")
        return False
    
    return True

def check_server_startup():
    """Test if the server can start without errors"""
    print("\n🚀 Testing server startup...")
    
    try:
        # Test import of web_app module
        sys.path.insert(0, 'src/api')
        import web_app
        print("✅ web_app module imports successfully")
        
        # Check if FastAPI app is created
        if hasattr(web_app, 'app'):
            print("✅ FastAPI app instance created")
        else:
            print("❌ FastAPI app instance not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False

def check_api_endpoints():
    """Check if critical API endpoints are defined"""
    print("\n🔗 Checking API endpoints...")
    
    try:
        sys.path.insert(0, 'src/api')
        import web_app
        
        # Get all routes from FastAPI app
        routes = [route.path for route in web_app.app.routes if hasattr(route, 'path')]
        
        critical_endpoints = [
            '/',
            '/api/v1/assessments',
            '/api/v1/bulk/upload-vendors',
            '/api/v1/trust-center/discover/{domain}'
        ]
        
        all_present = True
        for endpoint in critical_endpoints:
            # Check for exact match or pattern match
            found = any(endpoint.replace('{domain}', '').replace('{', '').replace('}', '') in route 
                       for route in routes)
            if found:
                print(f"✅ {endpoint}")
            else:
                print(f"❌ {endpoint} - MISSING")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ API endpoint check failed: {e}")
        return False

def main():
    """Run comprehensive health check"""
    print("🔍 VENDOR RISK ASSESSMENT AI - COMPREHENSIVE HEALTH CHECK")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Syntax Errors", check_syntax_errors),
        ("Configuration", check_configuration),
        ("Server Startup", check_server_startup),
        ("API Endpoints", check_api_endpoints)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed_checks += 1
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 HEALTH CHECK SUMMARY: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 ALL CHECKS PASSED! System is ready for use.")
        return 0
    else:
        print("⚠️ Some issues found. Please address the failed checks above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
