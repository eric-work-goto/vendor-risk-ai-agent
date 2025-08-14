from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any

Base = declarative_base()


class Vendor(Base):
    """Vendor information and contact details"""
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), unique=True, index=True)
    contact_email = Column(String(255))
    contact_name = Column(String(255))
    industry = Column(String(100))
    country = Column(String(100))
    trust_center_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    assessments = relationship("VendorAssessment", back_populates="vendor")
    documents = relationship("ComplianceDocument", back_populates="vendor")


class ComplianceDocument(Base):
    """Compliance documents (SOC 2, privacy policies, etc.)"""
    __tablename__ = "compliance_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    document_type = Column(String(50))  # 'soc2', 'privacy_policy', 'dpa', etc.
    title = Column(String(500))
    url = Column(String(1000))
    file_path = Column(String(500))
    file_hash = Column(String(64))  # SHA-256 hash
    
    # Document metadata
    version = Column(String(50))
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime)
    last_retrieved = Column(DateTime(timezone=True), server_default=func.now())
    
    # Processing status
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    processed_content = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vendor = relationship("Vendor", back_populates="documents")
    findings = relationship("ComplianceFinding", back_populates="document")


class ComplianceFinding(Base):
    """Individual compliance findings from document analysis"""
    __tablename__ = "compliance_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("compliance_documents.id"))
    assessment_id = Column(Integer, ForeignKey("vendor_assessments.id"))
    
    # Finding details
    category = Column(String(100))  # 'encryption', 'breach_notification', 'access_control', etc.
    finding_type = Column(String(50))  # 'compliant', 'non_compliant', 'missing', 'unclear'
    description = Column(Text)
    evidence_text = Column(Text)
    confidence_score = Column(Float)  # 0.0 to 1.0
    
    # Risk assessment
    risk_level = Column(String(20))  # 'low', 'medium', 'high', 'critical'
    impact_score = Column(Integer)  # 1-10
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("ComplianceDocument", back_populates="findings")
    assessment = relationship("VendorAssessment", back_populates="findings")


class VendorAssessment(Base):
    """Overall vendor risk assessment"""
    __tablename__ = "vendor_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    
    # Assessment details
    assessment_type = Column(String(50), default="automated")  # automated, manual, hybrid
    status = Column(String(20), default="in_progress")  # in_progress, completed, needs_review
    
    # Risk scoring
    overall_risk_score = Column(Float)  # 0-100
    risk_category = Column(String(20))  # 'low', 'medium', 'high', 'critical'
    
    # Scoring breakdown
    data_security_score = Column(Float)
    privacy_score = Column(Float)
    compliance_score = Column(Float)
    operational_score = Column(Float)
    
    # Assessment metadata
    assessment_criteria = Column(JSON)  # Configurable criteria used
    reviewer_notes = Column(Text)
    requires_human_review = Column(Boolean, default=False)
    human_reviewer = Column(String(255))
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    reviewed_at = Column(DateTime(timezone=True))
    
    # Relationships
    vendor = relationship("Vendor", back_populates="assessments")
    findings = relationship("ComplianceFinding", back_populates="assessment")
    followups = relationship("FollowUpAction", back_populates="assessment")


class FollowUpAction(Base):
    """Follow-up actions and vendor communications"""
    __tablename__ = "followup_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("vendor_assessments.id"))
    
    # Action details
    action_type = Column(String(50))  # 'question', 'document_request', 'clarification'
    status = Column(String(20), default="pending")  # pending, sent, responded, overdue
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    
    # Communication
    subject = Column(String(500))
    message = Column(Text)
    recipient_email = Column(String(255))
    sent_at = Column(DateTime(timezone=True))
    response_received_at = Column(DateTime(timezone=True))
    response_content = Column(Text)
    
    # Tracking
    attempt_count = Column(Integer, default=0)
    due_date = Column(DateTime(timezone=True))
    escalated = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    assessment = relationship("VendorAssessment", back_populates="followups")


class AuditLog(Base):
    """Comprehensive audit logging"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Event details
    event_type = Column(String(100))  # 'assessment_started', 'document_retrieved', etc.
    entity_type = Column(String(50))  # 'vendor', 'assessment', 'document', etc.
    entity_id = Column(Integer)
    
    # User and system info
    user_id = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Event data
    description = Column(Text)
    changes = Column(JSON)  # Before/after data for changes
    metadata = Column(JSON)  # Additional context
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


# Database utility functions
def create_tables(engine):
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def drop_tables(engine):
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
