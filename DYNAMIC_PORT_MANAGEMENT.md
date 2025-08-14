# Dynamic Port Management System
## Overview

The vendor risk assessment application now includes a comprehensive dynamic port management system that automatically handles port conflicts and provides flexibility in port selection.

## Key Features

### 🔧 Centralized Configuration
- **Single Point of Control**: Change `DEFAULT_PORT` in `port_config.py` to update the entire application
- **Automatic Fallback**: If the default port is busy, automatically tries alternative ports
- **Smart Detection**: Detects available ports and handles conflicts gracefully

### 🚀 Smart Launchers
- **Python Launcher**: `smart_start.py` - Cross-platform Python launcher
- **PowerShell Launcher**: `smart_start.ps1` - Windows-optimized launcher with advanced features
- **Automatic Browser Opening**: Opens the application in your default browser
- **Dependency Management**: Automatically installs required packages

## Current Configuration

```python
DEFAULT_PORT = 8028          # Primary port to use
PORT_RANGE_START = 8028      # Start of fallback range
PORT_RANGE_END = 8032        # End of fallback range
```

## How to Use

### Option 1: Smart Python Launcher (Recommended)
```bash
python smart_start.py
```

### Option 2: Smart PowerShell Launcher (Windows)
```powershell
.\smart_start.ps1
```

### Option 3: PowerShell with Options
```powershell
# Use specific port
.\smart_start.ps1 -PreferredPort 8029

# Kill existing processes on the port
.\smart_start.ps1 -KillExisting

# Skip automatic browser opening
.\smart_start.ps1 -SkipBrowser

# Show help
.\smart_start.ps1 -Help
```

### Option 4: Manual Server Start
```bash
# This will now automatically use port 8028 or find an alternative
python -m uvicorn src.api.web_app:app --host 127.0.0.1 --port 8028
```

## Port Detection Logic

1. **Check Default Port (8028)**: Try to use the configured default port
2. **Automatic Fallback**: If port 8028 is busy, try ports 8029, 8030, 8031, 8032
3. **Process Management**: Optionally kill existing processes using the desired port
4. **Error Handling**: Clear error messages if no ports are available

## Frontend Compatibility

The frontend automatically detects the current port from the browser URL, so all API calls work regardless of which port is actually used:

```javascript
// api-config.js automatically detects the current port
this.port = window.location.port || '8028';
this.baseUrl = `${this.protocol}//${this.host}:${this.port}`;
```

## Changing the Default Port

To change the default port for the entire application:

1. **Edit `port_config.py`**:
   ```python
   DEFAULT_PORT = 8029          # Change to your preferred port
   PORT_RANGE_START = 8029      # Update range start
   PORT_RANGE_END = 8033        # Update range end
   ```

2. **Restart the application** using any of the smart launchers

That's it! All components will automatically use the new port configuration.

## Benefits

### ✅ No More Port Conflicts
- Automatically finds available ports
- Can kill existing processes if needed
- Clear error messages and troubleshooting

### ✅ Developer Friendly
- Single configuration file for all port settings
- Smart launchers handle all the complexity
- Consistent behavior across platforms

### ✅ Production Ready
- Robust error handling
- Comprehensive logging
- Graceful fallback mechanisms

### ✅ User Friendly
- Automatic browser opening
- Clear status messages
- Easy-to-use command-line options

## Troubleshooting

### Port Still Busy?
```powershell
# Force kill processes on the port
.\smart_start.ps1 -KillExisting
```

### Want to Use a Specific Port?
```powershell
# Use port 8035
.\smart_start.ps1 -PreferredPort 8035
```

### Need to See What's Using a Port?
```bash
# Windows
netstat -ano | findstr :8028

# Linux/Mac
lsof -ti:8028
```

### Manual Port Management
```python
# Test the port management system
python -c "from port_config import port_manager; print(f'Available port: {port_manager.get_available_port()}')"
```

## Migration from Old System

The new system is backward compatible with existing hardcoded references. However, for best results:

1. Use the smart launchers instead of manual uvicorn commands
2. Update any scripts to use `port_config.py` for port detection
3. The frontend will automatically adapt to any port used

## Files Updated

- ✅ `port_config.py` - Central port configuration (updated to use 8028)
- ✅ `smart_start.py` - New Python launcher
- ✅ `smart_start.ps1` - New PowerShell launcher  
- ✅ `api-config.js` - Already had dynamic port detection
- 📋 Legacy files still contain hardcoded 8026 references (for backward compatibility)

The system gracefully handles both new dynamic port management and legacy hardcoded references.
