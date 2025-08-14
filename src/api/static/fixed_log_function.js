// Fixed logging function with proper FontAwesome icons
function log(message, type = 'info') {
    const logContainer = document.getElementById('activityLog');
    const timestamp = new Date().toLocaleTimeString();
    const icon = type === 'error' ? '<i class="fas fa-times-circle text-red-500"></i>' : 
                type === 'success' ? '<i class="fas fa-check-circle text-green-500"></i>' : 
                type === 'warning' ? '<i class="fas fa-exclamation-triangle text-yellow-500"></i>' : 
                '<i class="fas fa-info-circle text-blue-500"></i>';
    
    const logEntry = document.createElement('div');
    logEntry.className = 'mb-1 text-sm';
    logEntry.innerHTML = `${icon} <span class="text-xs text-gray-500">[${timestamp}]</span> ${message}`;
    
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}
