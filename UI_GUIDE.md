# Vendor Risk Assessment AI - User Interface Guide

## 🚀 Getting Started with the Web Interface

Your Vendor Risk Assessment AI system now includes a beautiful, user-friendly web interface that makes it easy for anyone to perform vendor risk assessments without technical knowledge.

## 🌐 Accessing the Interface

1. **Start the web application:**
   ```bash
   python -m uvicorn src.api.web_app:app --host 0.0.0.0 --port 8026
   ```

2. **Open your browser and navigate to:**
   - **Main Application:** http://localhost:8026
   - **API Documentation:** http://localhost:8026/docs
   - **Alternative API Docs:** http://localhost:8026/redoc

## 🎯 Using the Interface

### Quick Assessment
The simplest way to test a vendor:

1. Enter a vendor domain (e.g., `github.com`)
2. Enter the company name (e.g., `GitHub Inc`)
3. Click "Quick Assessment"
4. View the instant results

### Full Assessment
For comprehensive vendor evaluation:

1. **Vendor Information:**
   - Enter the vendor's domain/website
   - Provide the company name
   - The system will auto-fill the name based on the domain

2. **Assessment Criteria:**
   - **Data Sensitivity:** Choose the level of sensitive data the vendor will access
   - **Regulatory Requirements:** Select applicable regulations (GDPR, SOC 2, HIPAA, etc.)
   - **Business Criticality:** Rate how critical this vendor is to your operations

3. **Options:**
   - **Auto Follow-up:** Enable automatic follow-up actions
   - **Deep Scan:** Perform more thorough analysis (takes longer)

4. **Run Assessment:**
   - Click "Start Assessment"
   - Watch the real-time progress
   - View comprehensive results

## 📊 Understanding Results

### Risk Scores
- **Overall Score:** Combined risk assessment (0-100, higher is better)
- **Compliance Score:** Regulatory compliance rating
- **Security Score:** Security posture assessment
- **Data Protection Score:** Data handling and privacy rating

### Risk Levels
- 🟢 **LOW (70-100):** Minimal risk, recommended for approval
- 🟡 **MEDIUM (40-69):** Moderate risk, requires review
- 🔴 **HIGH (0-39):** High risk, needs significant remediation

### Findings
- **Compliance Findings:** SOC 2, GDPR, privacy policies, etc.
- **Security Analysis:** Encryption, access controls, incident response
- **Recommendations:** Prioritized action items

## 🔧 Features

### Assessment History
- View all previous assessments
- Track vendor risk over time
- Compare different vendors
- Export historical data

### Export & Sharing
- **Export Report:** Generate PDF or Excel reports
- **Set Monitoring:** Enable continuous vendor monitoring
- **Share Results:** Share assessment results with your team

### Real-time Features
- Live progress tracking during assessments
- Instant notifications for completed assessments
- Auto-refresh of assessment status

## 🎨 Interface Features

### Modern Design
- Beautiful gradient header with company branding
- Card-based layout for easy reading
- Responsive design works on desktop and mobile
- Hover effects and smooth animations

### User Experience
- Auto-complete vendor names from domains
- Form validation with helpful error messages
- Progress indicators for long-running assessments
- Success/error notifications

### Dashboard Elements
- Quick action buttons
- Visual risk indicators
- Color-coded findings
- Priority-based recommendations

## 🔌 API Integration

The web interface is built on top of a robust REST API. You can also:

1. **Use the API directly:** Visit `/docs` for interactive API documentation
2. **Integrate with other systems:** Use the REST endpoints for automation
3. **Build custom interfaces:** Create your own UI using our API

### Key API Endpoints
- `POST /api/v1/assessments` - Start new assessment
- `GET /api/v1/assessments/{id}` - Get assessment status/results
- `GET /health` - Check system health

## 🚨 Demo Mode

The system includes demo capabilities for testing:
- Mock assessment results for demonstration
- Sample vendor data for examples
- Simulated assessment progress
- Test data that doesn't require real API calls

## 🛠 Troubleshooting

### Common Issues

1. **"UI files not found"**
   - Ensure static files are in `src/api/static/`
   - Check file permissions

2. **API errors**
   - Verify OpenAI API key in `.env` file
   - Check network connectivity
   - Review logs for detailed error messages

3. **Port conflicts**
   - Change port: `--port 8001`
   - Check if port 8026 is already in use

### Getting Help
- Check the console logs for error details
- Visit `/docs` for API documentation
- Review the main README.md for setup instructions

## 🎯 Next Steps

1. **Production Setup:**
   - Configure proper database storage
   - Set up authentication and authorization
   - Enable HTTPS with SSL certificates
   - Configure proper CORS settings

2. **Customization:**
   - Modify the UI colors and branding
   - Add custom assessment criteria
   - Integrate with your existing systems
   - Set up automated reporting

3. **Scaling:**
   - Deploy to cloud infrastructure
   - Set up load balancing
   - Configure database clustering
   - Enable caching for better performance

Enjoy your new Vendor Risk Assessment AI web interface! 🎉
