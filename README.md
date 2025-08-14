# Vendor Risk Assessment AI Agent

An intelligent automation system for vendor risk assessment and compliance screening.

## Features

### 🔍 Document Retrieval
- Automated gathering of SOC 2 reports, data protection policies, and privacy statements
- Support for public trust centers and internal repositories
- Multi-format document parsing (PDF, HTML, JSON)

### 🔬 Initial Screening
- AI-powered scanning for compliance indicators
- Detection of encryption standards and breach notification protocols
- Automated flagging of missing or outdated items

### 📊 Risk Scoring
- Configurable risk assessment based on:
  - Data sensitivity levels
  - Geographic location
  - Regulatory exposure
- Preliminary risk scoring with human review flags

### ⚡ Workflow Automation
- Automated follow-up question generation
- Vendor contact management
- Comprehensive audit logging
- Integration-ready API endpoints

## Technology Stack

- **Python 3.11+** - Core application
- **FastAPI** - REST API framework
- **LangChain** - AI/LLM integration
- **SQLAlchemy** - Database ORM
- **Celery** - Background task processing
- **Redis** - Task queue and caching
- **PostgreSQL** - Primary database
- **Docker** - Containerization

## Quick Start

### Prerequisites
- Python 3.11+ installed
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Option 1: Automated Setup (Windows)
```cmd
# Run the setup script
setup.bat
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Verify setup
python check_environment.py
```

### Test the System
```bash
# Quick test
python test_basic.py

# Full demo
python demo.py

# Assess specific vendor
python src/main.py github.com "GitHub Inc"

# Start web API
python src/api/app.py
# Visit http://localhost:8026/docs for API documentation
```

## Project Structure

```
src/
├── agents/           # AI agent implementations
├── api/             # FastAPI routes and endpoints
├── core/            # Core business logic
├── models/          # Data models and schemas
├── services/        # External service integrations
├── utils/           # Utility functions
└── config/          # Configuration management
```

## Configuration

### Required Environment Variables
The system requires an OpenAI API key to function. Edit your `.env` file:

```bash
# REQUIRED: Your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional: Choose model (default: gpt-4)
OPENAI_MODEL=gpt-4

# Database (SQLite by default for development)
DATABASE_URL=sqlite:///./vendor_risk.db
```

### Optional Configuration
See `.env.example` for additional settings:
- Database connections (PostgreSQL for production)
- Redis for background tasks
- Email notifications (SMTP settings)
- Risk assessment thresholds
- Document storage settings

## License

MIT License
