# Vendor Risk AI Agent

## Python Dependencies

The import errors you're seeing are expected since we haven't installed the Python dependencies yet. To get started:

## 1. Setup Python Environment

First, make sure you have Python 3.11+ installed, then create a virtual environment:

```powershell
# Create virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\Activate.ps1

# If execution policy issues, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 2. Install Dependencies

```powershell
# Install all required packages
pip install -r requirements.txt
```

## 3. Configure Environment

```powershell
# Copy environment template
copy .env.example .env

# Edit .env with your API keys and settings
notepad .env
```

**Required Environment Variables:**
- `OPENAI_API_KEY` - Your OpenAI API key for AI analysis
- `DATABASE_URL` - Database connection string (SQLite by default)
- `REDIS_URL` - Redis connection for task queue (optional for development)

## 4. Run the Application

### CLI Mode (Test Single Vendor)
```powershell
# Run assessment for a vendor
python src/main.py example.com "Example Company"
```

### Web API Mode
```powershell
# Start the FastAPI server
cd src
python api/app.py
```

Then visit `http://localhost:8026/docs` for the interactive API documentation.

## 5. Project Structure

```
src/
├── agents/                 # AI agent implementations
│   ├── document_retrieval.py    # Finds and downloads compliance docs
│   ├── compliance_analysis.py   # Analyzes docs for compliance indicators
│   ├── risk_assessment.py       # Calculates risk scores
│   └── workflow_automation.py   # Manages follow-ups and notifications
├── api/                    # FastAPI web interface
│   └── app.py             # REST API endpoints
├── models/                 # Data models and schemas
│   ├── database.py        # SQLAlchemy database models
│   └── schemas.py         # Pydantic request/response schemas
├── services/              # External service integrations
│   └── storage_service.py # File storage management
├── utils/                 # Utility functions
│   └── logger.py          # Logging setup
├── config/                # Configuration management
│   └── settings.py        # Environment settings
└── main.py               # Main orchestrator and CLI interface
```

## 6. Key Features Implemented

### 🔍 Document Retrieval Agent
- Automatically discovers vendor trust centers
- Scrapes SOC 2 reports, privacy policies, security documentation
- Supports multiple document formats (PDF, HTML, JSON)
- Intelligent document classification

### 🔬 Compliance Analysis Agent
- AI-powered document analysis using GPT-4
- Pattern matching for compliance indicators
- Specialized analysis for SOC 2 reports and privacy policies
- Confidence scoring for findings

### 📊 Risk Assessment Agent
- Configurable risk scoring based on multiple factors
- Geographic and regulatory risk multipliers
- Component scoring (security, privacy, compliance, operational)
- Automated risk categorization

### ⚡ Workflow Automation Agent
- Automated follow-up question generation
- Email template system for vendor communications
- Escalation procedures for non-responsive vendors
- Comprehensive audit logging

## 7. Example Usage

### API Examples

```bash
# Start an assessment
curl -X POST "http://localhost:8026/api/v1/assessments" \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_domain": "example.com",
    "vendor_name": "Example Corp",
    "custom_criteria": {
      "data_sensitivity": "high",
      "regulatory_exposure": ["GDPR", "SOC2"],
      "business_criticality": "high"
    }
  }'

# Get assessment results
curl "http://localhost:8026/api/v1/assessments/1"

# Get risk summary
curl "http://localhost:8026/api/v1/reports/risk-summary"
```

### Python Examples

```python
from src.main import VendorRiskApp

# Create app instance
app = VendorRiskApp()
await app.start()

# Assess a vendor
result = await app.assess_vendor(
    vendor_domain="example.com",
    custom_criteria={
        'data_sensitivity': 'high',
        'regulatory_exposure': ['GDPR', 'SOC2'],
        'business_criticality': 'critical'
    }
)

print(f"Risk Score: {result.summary['overall_risk_score']}")
print(f"Risk Level: {result.summary['risk_category']}")
```

## 8. Next Steps

1. **Install Dependencies**: Run `pip install -r requirements.txt`
2. **Set API Keys**: Add your OpenAI API key to `.env`
3. **Test CLI**: Try `python src/main.py github.com`
4. **Start API**: Run `python src/api/app.py`
5. **Explore Docs**: Visit `http://localhost:8026/docs`

## 9. Production Considerations

For production deployment, you'll want to:

- Set up a proper database (PostgreSQL recommended)
- Configure Redis for background task processing
- Add authentication and authorization
- Implement proper error handling and monitoring
- Add rate limiting and security headers
- Set up Docker containers for deployment

The system is designed to be modular and scalable, so you can easily extend or modify components as needed.

## 10. Customization

The system is highly configurable:

- **Risk Criteria**: Modify `src/agents/risk_assessment.py` to adjust scoring
- **Document Patterns**: Update `src/agents/document_retrieval.py` for new doc types
- **AI Prompts**: Customize analysis prompts in `src/agents/compliance_analysis.py`
- **Email Templates**: Edit templates in `src/agents/workflow_automation.py`
