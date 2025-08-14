# 🔧 Port Management System

## Overview

This system implements intelligent port management to prevent the frustrating port conflicts we've been experiencing. No more manual port switching or hunting for available ports!

## Key Features

### 🎯 **Consistent Port Usage**
- **Default Port**: 8026 (configured in one place)
- **Automatic Fallback**: Ports 8026-8030 if default is busy
- **Smart Conflict Resolution**: Automatically kills conflicting processes
- **Dynamic Frontend**: Frontend automatically detects the current port

### 🛡️ **Conflict Prevention**
- Checks port availability before starting
- Kills existing processes using the target port
- Provides clear feedback about port status
- Falls back to alternative ports if needed

### 🚀 **Smart Launchers**
- **Python**: `smart_launch.py` - Cross-platform launcher
- **PowerShell**: `smart_launch.ps1` - Windows-optimized launcher  
- **Batch**: `SMART_LAUNCH.bat` - Simple double-click launcher
- **Legacy**: Original launch scripts still work

## Quick Start

### Method 1: Smart Launcher (Recommended)
```bash
# Double-click this file on Windows:
SMART_LAUNCH.bat

# Or run manually:
python smart_launch.py
```

### Method 2: Direct Python
```bash
cd src/api
python web_app.py  # Now uses smart port management
```

### Method 3: PowerShell (Windows)
```powershell
.\smart_launch.ps1
```

## How It Works

### 🔧 Port Configuration (`port_config.py`)
```python
# Single source of truth for port configuration
DEFAULT_PORT = 8026
PORT_RANGE_START = 8026
PORT_RANGE_END = 8030

# Smart port manager handles:
# - Port availability checking
# - Process conflict resolution
# - Alternative port selection
```

### 🌐 Dynamic Frontend (`api-config.js`)
```javascript
// Frontend automatically detects current port
window.apiConfig = new APIConfig();  // Auto-detects port
window.api.get('/api/v1/assessments'); // Uses detected port
```

### 🚀 Smart Backend (`web_app.py`)
```python
# Backend uses port manager
app_port = ensure_app_port()  # Ensures port is available
uvicorn.run(app, port=app_port)  # Starts on available port
```

## Port Resolution Process

1. **Check Default Port (8026)**
   - ✅ Available → Use it
   - ❌ Busy → Try to free it

2. **Free Busy Port**
   - Find process using the port
   - Kill the process
   - Wait for port to become available
   - ✅ Success → Use default port
   - ❌ Failed → Find alternative

3. **Find Alternative Port**
   - Check ports 8027, 8028, 8029, 8030
   - Use first available port
   - Warn user about alternative port

4. **Start Application**
   - Display clear port information
   - Show all relevant URLs
   - Open browser automatically

## Benefits

### ✅ **No More Port Conflicts**
- Automatically resolves port conflicts
- Clear feedback about what's happening
- Consistent behavior across runs

### ✅ **Developer Friendly**
- Single configuration point (`DEFAULT_PORT = 8026`)
- Smart fallback system
- Clear error messages and status updates

### ✅ **User Friendly**
- Double-click to start (Windows)
- Automatic browser opening
- Clear URLs displayed

### ✅ **Testing Friendly**
- Consistent port usage prevents confusion
- Easy to update port configuration
- No manual port hunting during development

## Configuration

### Change Default Port
Edit `port_config.py`:
```python
DEFAULT_PORT = 8027  # Change this line only
```

### Extend Port Range
Edit `port_config.py`:
```python
PORT_RANGE_END = 8035  # Allow more fallback ports
```

### Disable Auto-Port-Killing
Edit `port_config.py`:
```python
def ensure_port_available(self, port=None):
    # Comment out the kill_port_process call
    # if self.kill_port_process(port):
    return self.get_available_port()
```

## Files Updated

### ✅ **Core Application**
- `port_config.py` - New centralized port management
- `src/api/web_app.py` - Uses smart port management  
- `src/api/static/api-config.js` - Dynamic frontend configuration
- `src/api/static/combined-ui.html` - Includes dynamic API config

### ✅ **Smart Launchers**
- `smart_launch.py` - Python cross-platform launcher
- `smart_launch.ps1` - PowerShell Windows launcher
- `SMART_LAUNCH.bat` - Batch file for double-click launching

### ⚠️ **Legacy Files** (Still reference old ports)
- Documentation files (*.md)
- Old launch scripts (launch.py, launch.bat, etc.)
- Legacy HTML files

## Usage Examples

### Starting the Application
```bash
# Preferred method - smart launcher
python smart_launch.py

# Alternative - direct run (also smart now)
cd src/api && python web_app.py

# Windows double-click
# Just double-click SMART_LAUNCH.bat
```

### Example Output
```
🚀 VENDOR RISK ASSESSMENT AI
    Smart Launcher v2.0

✅ All required dependencies found
🔧 Port Manager Status:
   └─ Using port: 8026
   └─ Base URL: http://localhost:8026

🚀 Starting server...
📍 Main Application: http://localhost:8026/static/combined-ui.html
📚 API Documentation: http://localhost:8026/docs
🔄 Alternative Docs: http://localhost:8026/redoc
🛑 Press Ctrl+C to stop
```

## Troubleshooting

### Port Still Conflicts?
```bash
# Manually check what's using the port
netstat -ano | findstr :8026

# Kill specific process
taskkill /F /PID <process_id>

# Use smart launcher to auto-resolve
python smart_launch.py
```

### Frontend API Errors?
- Check that `api-config.js` is loaded
- Verify the port in browser console: `console.log(window.apiConfig.baseUrl)`
- Check network tab for actual API call URLs

### Want to Use Different Port?
- Edit `DEFAULT_PORT` in `port_config.py`
- Restart the application
- Frontend will automatically adapt

## Next Steps

1. **Test the smart launcher**: `python smart_launch.py`
2. **Verify port consistency**: Check that frontend uses detected port
3. **Update documentation**: Eventually update legacy files to reference 8026
4. **Create shortcuts**: Pin `SMART_LAUNCH.bat` to taskbar for easy access

**Result**: No more port switching headaches! The system now intelligently manages ports and provides a consistent experience. 🎉
