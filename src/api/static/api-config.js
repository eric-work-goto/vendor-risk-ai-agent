// Dynamic Port Configuration for Frontend
// This script automatically detects the current port and updates all API calls

class APIConfig {
    constructor() {
        // Get the current port from the browser's location
        this.port = window.location.port || '8026';
        this.host = window.location.hostname || 'localhost';
        this.protocol = window.location.protocol || 'http:';
        this.baseUrl = `${this.protocol}//${this.host}:${this.port}`;
        
        console.log(`🔧 API Config initialized with base URL: ${this.baseUrl}`);
    }
    
    // Get the full API endpoint URL
    getApiUrl(endpoint) {
        // Ensure endpoint starts with /
        if (!endpoint.startsWith('/')) {
            endpoint = '/' + endpoint;
        }
        return `${this.baseUrl}${endpoint}`;
    }
    
    // Get base URL for the application
    getBaseUrl() {
        return this.baseUrl;
    }
    
    // Update all fetch calls to use the dynamic URL
    async fetch(endpoint, options = {}) {
        const url = this.getApiUrl(endpoint);
        console.log(`📡 API Call: ${options.method || 'GET'} ${url}`);
        
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            
            return response;
        } catch (error) {
            console.error(`❌ API Error for ${url}:`, error);
            throw error;
        }
    }
}

// Global API configuration instance
window.apiConfig = new APIConfig();

// Helper function for easy API calls
window.api = {
    get: (endpoint) => window.apiConfig.fetch(endpoint, { method: 'GET' }),
    post: (endpoint, data) => window.apiConfig.fetch(endpoint, { 
        method: 'POST', 
        body: JSON.stringify(data) 
    }),
    put: (endpoint, data) => window.apiConfig.fetch(endpoint, { 
        method: 'PUT', 
        body: JSON.stringify(data) 
    }),
    delete: (endpoint) => window.apiConfig.fetch(endpoint, { method: 'DELETE' }),
    upload: (endpoint, formData) => window.apiConfig.fetch(endpoint, {
        method: 'POST',
        body: formData,
        headers: {} // Let browser set content-type for FormData
    })
};

// Display current configuration
console.log(`
🌐 Frontend API Configuration
=============================
Protocol: ${window.apiConfig.protocol}
Host: ${window.apiConfig.host}
Port: ${window.apiConfig.port}
Base URL: ${window.apiConfig.baseUrl}
=============================
`);
