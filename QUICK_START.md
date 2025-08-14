# 🚀 Quick Start Guide - Vendor Risk Assessment AI

## Easy Launch Options

Choose the method that works best for your system:

### 🖥️ Windows Users

#### Option 1: Double-Click Launch (Easiest)
1. Navigate to the `vendor-risk-ai-agent` folder
2. **Double-click** `launch.bat` to start the application
3. The application will automatically open in your browser

#### Option 2: PowerShell Launch
1. Right-click in the `vendor-risk-ai-agent` folder
2. Select "Open PowerShell window here"
3. Run: `.\launch.ps1`

#### Option 3: Command Prompt Launch
1. Open Command Prompt in the `vendor-risk-ai-agent` folder
2. Run: `launch.bat`

### 🐧 Linux/WSL Users
1. Open terminal in the `vendor-risk-ai-agent` folder
2. Run: `./launch.sh`
3. (First time only: may need to run `chmod +x launch.sh`)

### 🍎 macOS Users
1. Open Terminal in the `vendor-risk-ai-agent` folder
2. Run: `./launch.sh`
3. (First time only: may need to run `chmod +x launch.sh`)

### 🐍 Universal Python Launch (All Platforms)
1. Open terminal/command prompt in the `vendor-risk-ai-agent` folder
2. Run: `python launch.py`

## What Happens When You Launch?

The launcher will automatically:

1. ✅ **Check your environment** - Verify Python and dependencies
2. 🔍 **Run health checks** - Ensure everything is working correctly
3. 📦 **Install missing packages** - Automatically install what's needed
4. 🚀 **Start the server** - Launch the FastAPI application
5. 🌐 **Open your browser** - Navigate to the application interface

## Access URLs

Once launched, you can access:

- **🎯 Main Application**: http://localhost:8026/static/assessment.html
- **📚 API Documentation**: http://localhost:8026/docs
- **🔄 Alternative API Docs**: http://localhost:8026/redoc

## Stopping the Application

- Press **Ctrl+C** in the terminal/command prompt
- Or simply close the terminal window

## Troubleshooting

### Virtual Environment Issues
If you get virtual environment errors:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
If port 8026 is busy, the launcher will show an error. You can:
1. Stop other applications using port 8026
2. Or modify the port in the launch scripts

### Permission Errors (Linux/macOS)
```bash
chmod +x launch.sh
./launch.sh
```

## Features Available

- ✅ **Single Vendor Assessment** - Assess individual vendors
- ✅ **Bulk Assessment** - Upload CSV/Excel files for batch processing
- ✅ **Trust Center Integration** - Automated document retrieval
- ✅ **Document Export** - Download compliance documents
- ✅ **Real-time Progress** - Track assessment progress
- ✅ **Professional Reports** - Generate detailed risk reports

## Need Help?

1. **Health Check**: Run `python health_check.py` for system diagnostics
2. **Error Reports**: Check `ERROR_ANALYSIS_REPORT.md` for detailed information
3. **Logs**: Check terminal output for detailed error messages

---

**🎉 That's it! Your Vendor Risk Assessment AI is ready to use!**
