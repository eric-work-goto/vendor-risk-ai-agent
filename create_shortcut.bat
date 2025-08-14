@echo off
echo Creating desktop shortcut for Vendor Risk Assessment AI...

set "SCRIPT_DIR=%~dp0"
set "TARGET=%SCRIPT_DIR%launch.bat"
set "SHORTCUT=%USERPROFILE%\Desktop\Vendor Risk Assessment AI.lnk"

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%TARGET%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,21'; $Shortcut.Description = 'Launch Vendor Risk Assessment AI'; $Shortcut.Save()}"

if exist "%SHORTCUT%" (
    echo ✅ Desktop shortcut created successfully!
    echo You can now launch the application from your desktop.
) else (
    echo ❌ Failed to create desktop shortcut.
)

pause
