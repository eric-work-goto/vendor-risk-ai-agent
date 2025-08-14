from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./vendor_risk.db"
    test_database_url: str = "sqlite:///./test.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # OpenAI
    openai_api_key: str = "dummy-key-for-testing"
    openai_model: str = "gpt-4"
    
    # LangChain
    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    app_name: str = "Vendor Risk AI Agent"
    app_version: str = "1.0.0"
    
    # Document Storage
    document_storage_path: str = "./storage/documents"
    max_file_size: int = 50000000  # 50MB
    
    # Risk Assessment
    default_risk_threshold: int = 70
    high_risk_threshold: int = 85
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: Optional[str] = None
    
    # Vendor Management
    vendor_followup_timeout_days: int = 7
    max_followup_attempts: int = 3
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "{time} | {level} | {message}"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Ensure storage directory exists
def ensure_storage_dirs():
    """Create necessary storage directories"""
    os.makedirs(settings.document_storage_path, exist_ok=True)
    os.makedirs("./storage/logs", exist_ok=True)
    os.makedirs("./storage/temp", exist_ok=True)


if __name__ == "__main__":
    ensure_storage_dirs()
    print(f"Settings loaded for environment: {settings.environment}")
    print(f"Database URL: {settings.database_url}")
