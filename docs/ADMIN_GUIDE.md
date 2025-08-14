# Vendor Risk Assessment Tool - Technical Administration Guide

## 🔧 System Overview

The Vendor Risk Assessment Tool is a FastAPI-based web application that provides automated vendor security and compliance assessments. It consists of a Python backend with a modern HTML/JavaScript frontend.

## 🏗️ Architecture

### Components
- **Backend**: FastAPI application (`web_app.py`)
- **Frontend**: Single-page application (`combined-ui.html`)
- **Database**: In-memory storage with file persistence
- **External APIs**: Real-time web scanning and data collection

### Technology Stack
- **Backend**: Python 3.8+, FastAPI, Uvicorn
- **Frontend**: HTML5, JavaScript (ES6+), Tailwind CSS
- **Dependencies**: requests, beautifulsoup4, dnspython, ssl, socket

## 🚀 Installation and Setup

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### Installation Steps
1. **Clone Repository**
   ```bash
   git clone [repository-url]
   cd vendor-risk-ai-agent
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Application**
   ```bash
   cd src/api
   python web_app.py
   ```

4. **Access Application**
   - Web Interface: `http://localhost:8028/static/combined-ui.html`
   - API Documentation: `http://localhost:8028/docs`
   - Health Check: `http://localhost:8028/health`

## ⚙️ Configuration

### Environment Variables
```bash
# Optional: Set custom port
PORT=8028

# Optional: Enable debug logging
DEBUG=true

# Optional: Configure external API timeouts
REQUEST_TIMEOUT=30
```

### Application Settings
Located in `web_app.py`:
```python
# Server configuration
HOST = "0.0.0.0"
PORT = 8028

# Assessment timeouts
DEFAULT_TIMEOUT = 30
MAX_CONCURRENT_ASSESSMENTS = 10

# Real data mode (vs mock data)
REAL_DATA_MODE = True
```

## 🔍 Monitoring and Logging

### Log Levels
- **INFO**: Normal operations, assessment starts/completions
- **DEBUG**: Detailed scanning operations
- **WARNING**: Non-critical issues, partial failures
- **ERROR**: Critical failures, assessment errors

### Key Log Patterns
```bash
# Successful assessment start
"🚀 Starting enhanced assessment for [domain]"

# Assessment completion
"✅ Assessment completed successfully"

# Data breach detection
"🚨 Data breach found for [vendor]"

# AI services detection
"🤖 Scanning AI services for [domain]"

# Compliance scanning
"📋 Scanning compliance documentation"
```

### Health Monitoring
Monitor these endpoints:
- `GET /health` - Application health status
- `GET /api/v1/assessments/history` - Assessment history
- `GET /api/v1/dashboard` - System metrics

## 📊 API Reference

### Core Endpoints

#### Start Single Assessment
```http
POST /api/v1/assessments
Content-Type: application/json

{
  "vendor_domain": "example.com",
  "requester_email": "user@company.com",
  "assessment_mode": "business_risk", // or "technical_due_diligence"
  "regulations": ["SOC2", "ISO27001", "GDPR"]
}
```

#### Get Assessment Results
```http
GET /api/v1/assessments/{assessment_id}
```

#### Start Bulk Assessment
```http
POST /api/v1/assessments/bulk
Content-Type: application/json

{
  "vendor_list": [
    {"domain": "vendor1.com", "name": "Vendor 1"},
    {"domain": "vendor2.com", "name": "Vendor 2"}
  ],
  "requester_email": "user@company.com",
  "assessment_mode": "business_risk"
}
```

#### Get Assessment History
```http
GET /api/v1/assessments/history?limit=50&offset=0
```

## 🛡️ Security Considerations

### Network Security
- Application performs **outbound requests only**
- No sensitive data storage or processing
- All assessments based on public information
- Rate limiting implemented for external requests

### Data Protection
- No persistent storage of sensitive data
- Assessment results stored temporarily in memory
- Email addresses used only for report delivery
- No authentication required (internal tool)

### Firewall Requirements
**Outbound Access Required**:
- HTTP/HTTPS (ports 80/443) for web scanning
- DNS resolution (port 53) for domain analysis
- WHOIS queries (port 43) for domain information

## 🔄 Maintenance and Updates

### Regular Maintenance Tasks

#### Weekly
- Review application logs for errors
- Monitor assessment completion rates
- Check disk space and memory usage

#### Monthly
- Update known vulnerability databases
- Review and update compliance frameworks
- Validate AI vendor detection accuracy

#### Quarterly
- Update Python dependencies
- Review and optimize performance
- Backup assessment history data

### Update Procedures

#### Application Updates
1. **Backup Current Version**
   ```bash
   cp -r vendor-risk-ai-agent vendor-risk-ai-agent-backup
   ```

2. **Pull Latest Changes**
   ```bash
   git pull origin main
   ```

3. **Update Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Test Application**
   ```bash
   python web_app.py
   # Verify at http://localhost:8028/health
   ```

5. **Deploy to Production**
   ```bash
   # Stop current application
   # Start updated application
   ```

#### Adding New Vendors to AI Detection
Edit `scan_ai_services()` function in `web_app.py`:
```python
known_ai_capabilities = {
    "newvendor.com": {
        "offers_ai_services": True,
        "ai_maturity_level": "Advanced",
        "ai_service_categories": ["Category1", "Category2"],
        "ai_services_detail": [
            {
                "category": "Category1",
                "services": ["Service A", "Service B"],
                "use_cases": ["Use case 1", "Use case 2"],
                "data_types": ["Data type 1", "Data type 2"]
            }
        ],
        "governance_score": 85
    }
}
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Assessment Timeouts
**Symptoms**: Assessments hang or fail to complete
**Solutions**:
- Check internet connectivity
- Verify target domain is accessible
- Increase timeout values in configuration
- Check for rate limiting from external services

#### 2. High Memory Usage
**Symptoms**: Application becomes slow or unresponsive
**Solutions**:
- Restart application to clear memory
- Reduce concurrent assessment limit
- Monitor for memory leaks in logs

#### 3. External Request Failures
**Symptoms**: "Failed to scan" errors in logs
**Solutions**:
- Check firewall rules for outbound access
- Verify DNS resolution is working
- Check if target sites are blocking requests

#### 4. Frontend Not Loading
**Symptoms**: Blank page or 404 errors
**Solutions**:
- Verify application is running on correct port
- Check static file serving configuration
- Clear browser cache

### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 404 | Assessment not found | Check assessment ID |
| 422 | Invalid input data | Validate request format |
| 500 | Internal server error | Check application logs |
| 503 | Service unavailable | Restart application |

## 📋 Performance Optimization

### Recommendations
- **Concurrent Assessments**: Limit to 10-20 simultaneous assessments
- **Caching**: Implement Redis for assessment result caching
- **Load Balancing**: Use multiple instances for high volume
- **Database**: Consider PostgreSQL for persistent storage

### Monitoring Metrics
- Assessment completion time (target: < 3 minutes)
- Success rate (target: > 95%)
- Memory usage (target: < 2GB)
- CPU usage (target: < 70%)

## 🔐 Backup and Recovery

### Backup Strategy
```bash
# Daily backup of assessment data
tar -czf backup-$(date +%Y%m%d).tar.gz assessment_data/

# Weekly backup of application configuration
cp web_app.py config_backup/web_app_$(date +%Y%m%d).py
```

### Recovery Procedures
1. **Application Failure**: Restart service from backup version
2. **Data Loss**: Restore from most recent backup
3. **Configuration Issues**: Restore configuration from backup

## 📞 Support and Escalation

### Log Collection
```bash
# Collect recent logs
tail -n 1000 application.log > support_logs.txt

# Include system information
python --version >> support_logs.txt
pip list >> support_logs.txt
```

### Escalation Contacts
- **Level 1**: IT Support Team
- **Level 2**: Security Engineering Team
- **Level 3**: Application Development Team

---

*Last Updated: August 2025*
*Version: 1.0*

For technical questions or issues, contact the IT Support Team or create an issue in the project repository.
