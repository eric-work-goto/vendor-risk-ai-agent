# Service Configuration for Vendor Risk Assessment
# This file contains settings for running as a Windows service

# Server Configuration
$ServerConfig = @{
    Name = "VendorRiskAssessment"
    DisplayName = "Vendor Risk Assessment Service"
    Description = "AI-powered vendor risk assessment and compliance monitoring service"
    Port = 8028
    Host = "0.0.0.0"
    WorkingDirectory = "C:\Users\eleeds\OneDrive - GoTo Inc\Desktop\vendor-risk-ai-agent\src\api"
    PythonPath = "python"
    ScriptPath = "web_app.py"
    LogPath = "C:\Users\eleeds\OneDrive - GoTo Inc\Desktop\vendor-risk-ai-agent\logs"
    MaxRestarts = 3
    RestartDelaySeconds = 10
}

# Export configuration for use by other scripts
Export-ModuleMember -Variable ServerConfig
