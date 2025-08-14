# 🚀 Vendor Risk Assessment AI - Complete Setup & Launch Guide

## 🎯 One-Click Launch Solutions

I've created multiple easy-to-use launchers for any user to start the application with minimal effort:

### 🏆 **EASIEST METHOD - Windows Users**

#### Method 1: Double-Click Launch (Recommended)
1. Navigate to the `vendor-risk-ai-agent` folder
2. **Double-click** the `launch.bat` file
3. Wait for the application to start (it will automatically open your browser)
4. Start using the application!

#### Method 2: Desktop Shortcut (Super Convenient)
1. Double-click `create_shortcut.bat` in the project folder
2. A shortcut will be created on your desktop
3. Double-click the desktop shortcut anytime to launch the app

### 🖥️ **All Operating Systems**

#### Universal Python Launcher
- **Windows**: Double-click `launch.py` or run `python launch.py`
- **macOS/Linux**: Run `python launch.py` in terminal

#### Platform-Specific Scripts
- **Windows PowerShell**: Run `.\launch.ps1`
- **Linux/macOS/WSL**: Run `./launch.sh`

## 🔄 What Each Launcher Does Automatically

Every launcher performs these steps automatically:

1. ✅ **Environment Check** - Verifies Python version compatibility
2. ✅ **Dependency Management** - Installs missing packages automatically
3. ✅ **Health Diagnostics** - Runs comprehensive system checks
4. ✅ **Server Startup** - Launches the FastAPI application
5. ✅ **Browser Launch** - Opens the web interface automatically
6. ✅ **Error Handling** - Provides clear error messages and solutions

## 🌐 Application Access Points

Once launched, access the application at:

| Interface | URL | Description |
|-----------|-----|-------------|
| **Main App** | http://localhost:8026/static/assessment.html | Primary user interface |
| **API Docs** | http://localhost:8026/docs | Interactive API documentation |
| **Alternative Docs** | http://localhost:8026/redoc | Alternative API documentation |

## 📁 Launcher Files Overview

| File | Platform | Description |
|------|----------|-------------|
| `launch.bat` | Windows | Batch file for Command Prompt |
| `launch.ps1` | Windows | PowerShell script with enhanced features |
| `launch.py` | All | Universal Python launcher with auto-browser |
| `launch.sh` | Linux/macOS | Bash script for Unix-like systems |
| `create_shortcut.bat` | Windows | Creates desktop shortcut |

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### ❌ "Virtual environment not found"
**Solution**: The launcher will use system Python automatically

#### ❌ "Dependencies missing"
**Solution**: The launcher will install them automatically

#### ❌ "Port 8026 already in use"
**Solutions**:
1. Stop other applications using port 8026
2. Wait a few seconds and try again
3. Restart your computer if needed

#### ❌ "Python not found"
**Solution**: Install Python from https://python.org

#### ❌ Permission errors (Linux/macOS)
**Solution**: Run `chmod +x launch.sh` first

### Advanced Troubleshooting

#### Manual Health Check
```bash
python health_check.py
```

#### Manual Dependency Installation
```bash
pip install -r requirements.txt
```

#### Manual Server Start
```bash
cd src/api
python -m uvicorn web_app:app --host 0.0.0.0 --port 8026
```

## 🎯 User Experience Features

### Automatic Features
- ✅ **Auto-browser opening** - No need to remember URLs
- ✅ **Progress feedback** - Clear status messages during startup
- ✅ **Error recovery** - Automatic dependency installation
- ✅ **Health verification** - Pre-flight checks before launch
- ✅ **Cross-platform** - Works on Windows, macOS, Linux

### User-Friendly Elements
- 🎨 **Color-coded output** - Easy to read status messages
- 📊 **Progress indicators** - Shows startup progress
- 🚀 **One-click operation** - Minimal user interaction required
- 🔄 **Automatic recovery** - Handles common issues automatically

## 📋 Quick Start Checklist

For any new user:

1. ☐ Download/clone the project
2. ☐ Navigate to the `vendor-risk-ai-agent` folder
3. ☐ Choose your launcher:
   - **Windows**: Double-click `launch.bat`
   - **Cross-platform**: Run `python launch.py`
4. ☐ Wait for automatic setup and browser opening
5. ☐ Start assessing vendors!

## 🎉 What You Can Do Once Launched

### Single Vendor Assessment
- Enter vendor domain and details
- Get AI-powered risk analysis
- Download compliance documents
- Export professional reports

### Bulk Vendor Assessment
- Upload CSV/Excel files with vendor lists
- Process multiple vendors simultaneously
- Track progress in real-time
- Export comprehensive results

### Trust Center Integration
- Automatically discover vendor trust centers
- Request compliance documents
- Download SOC 2, ISO 27001, and other certifications
- Verify document authenticity

## 🔧 For Developers

### Customization
- Modify port in launcher scripts if needed
- Add custom health checks to `health_check.py`
- Extend functionality in `src/api/web_app.py`

### Monitoring
- Check `ERROR_ANALYSIS_REPORT.md` for detailed analysis
- Use `health_check.py` for system diagnostics
- Monitor server logs for operational insights

---

## 🎯 Summary

**The easiest way to start**: Double-click `launch.bat` (Windows) or run `python launch.py` (any platform)

**Need help?** All launchers include automatic error handling and clear instructions.

**Ready to go?** Everything is set up for immediate use with zero configuration required!

🚀 **Happy vendor risk assessing!**
