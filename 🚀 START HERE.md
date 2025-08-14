# 🚀 START HERE - Easy Application Launch

## The Simplest Way to Start the Application

### For Everyone (No Technical Knowledge Required)

**Just double-click this file:** `DOUBLE_CLICK_TO_START.bat`

That's it! The application will:
- ✅ Check and set up everything automatically
- ✅ Install any missing components
- ✅ Start the web server
- ✅ Open your web browser to the application
- ✅ Show you helpful tips

## Alternative Launch Methods

| Method | How to Use | Best For |
|--------|------------|----------|
| **DOUBLE_CLICK_TO_START.bat** | Double-click the file | **Everyone** |
| **launch.bat** | Run from Command Prompt | Windows command line users |
| **start_app.ps1** | Run from PowerShell | PowerShell users |
| **start_app.py** | `python start_app.py` | Python developers |

## What Happens When You Launch

1. **Environment Setup** (5-10 seconds)
   - Activates Python virtual environment
   - Checks for required software

2. **Dependency Check** (5-15 seconds)
   - Installs any missing components automatically
   - Verifies everything is ready

3. **Application Start** (5-10 seconds)
   - Starts the web server
   - Opens your browser automatically
   - Shows the application interface

## Using the Application

Once launched, you'll see two main options:

### 🔍 Single Vendor Assessment
- Enter one vendor's information
- Get instant risk assessment
- Download compliance documents

### 📊 Bulk Vendor Assessment  
- Upload CSV/Excel file with multiple vendors
- Process many assessments at once
- Track progress in real-time
- Download comprehensive results

## Stopping the Application

- **Close the terminal/command window** that opened when you launched
- Or press **Ctrl+C** in that window
- The web browser can be closed separately

## Troubleshooting

### If the application doesn't start:
1. **Try running as administrator** - Right-click the launcher and select "Run as administrator"
2. **Check if port 8026 is free** - Close any other web applications
3. **Restart your computer** if you're having persistent issues

### If your browser doesn't open automatically:
- Manually go to: http://localhost:8026/static/assessment.html

### If you see error messages:
- Take a screenshot of the error
- Try running `python health_check.py` for detailed diagnostics
- Restart the launcher

## System Requirements

- **Windows 10/11** (recommended)
- **Python 3.8+** (will be checked automatically)
- **2GB RAM** minimum
- **Internet connection** for AI features

## Need Help?

1. **Check the terminal window** for error messages
2. **Run the health check**: `python health_check.py`
3. **Review error logs** in the terminal output
4. **Try restarting** the application

---

## 🎉 Ready to Start?

**Double-click `DOUBLE_CLICK_TO_START.bat` and you're ready to go!**

The application will guide you through everything else.
