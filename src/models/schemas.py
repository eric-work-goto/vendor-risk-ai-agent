from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AssessmentStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_REVIEW = "needs_review"


class DocumentType(str, Enum):
    SOC2 = "soc2"
    PRIVACY_POLICY = "privacy_policy"
    DPA = "dpa"
    SECURITY_POLICY = "security_policy"
    INCIDENT_RESPONSE = "incident_response"
    OTHER = "other"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingType(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    MISSING = "missing"
    UNCLEAR = "unclear"


# Vendor Schemas
class VendorBase(BaseModel):
    name: str = Field(..., max_length=255)
    domain: str = Field(..., max_length=255)
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    trust_center_url: Optional[HttpUrl] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    domain: Optional[str] = Field(None, max_length=255)
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    trust_center_url: Optional[HttpUrl] = None


class Vendor(VendorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Document Schemas
class ComplianceDocumentBase(BaseModel):
    document_type: DocumentType
    title: str = Field(..., max_length=500)
    url: Optional[HttpUrl] = None
    version: Optional[str] = Field(None, max_length=50)
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None


class ComplianceDocumentCreate(ComplianceDocumentBase):
    vendor_id: int


class ComplianceDocument(ComplianceDocumentBase):
    id: int
    vendor_id: int
    file_path: Optional[str] = None
    file_hash: Optional[str] = None
    status: str = "pending"
    last_retrieved: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Finding Schemas
class ComplianceFindingBase(BaseModel):
    category: str = Field(..., max_length=100)
    finding_type: FindingType
    description: str
    evidence_text: Optional[str] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: RiskLevel
    impact_score: int = Field(..., ge=1, le=10)


class ComplianceFindingCreate(ComplianceFindingBase):
    document_id: int
    assessment_id: int


class ComplianceFinding(ComplianceFindingBase):
    id: int
    document_id: int
    assessment_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Assessment Schemas
class RiskScores(BaseModel):
    overall_risk_score: float = Field(..., ge=0.0, le=100.0)
    data_security_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    privacy_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    compliance_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    operational_score: Optional[float] = Field(None, ge=0.0, le=100.0)


class VendorAssessmentBase(BaseModel):
    assessment_type: str = "automated"
    assessment_criteria: Optional[Dict[str, Any]] = None
    reviewer_notes: Optional[str] = None


class VendorAssessmentCreate(VendorAssessmentBase):
    vendor_id: int


class VendorAssessmentUpdate(BaseModel):
    status: Optional[AssessmentStatus] = None
    reviewer_notes: Optional[str] = None
    human_reviewer: Optional[str] = None
    risk_scores: Optional[RiskScores] = None


class VendorAssessment(VendorAssessmentBase):
    id: int
    vendor_id: int
    status: AssessmentStatus
    overall_risk_score: Optional[float] = None
    risk_category: Optional[RiskLevel] = None
    data_security_score: Optional[float] = None
    privacy_score: Optional[float] = None
    compliance_score: Optional[float] = None
    operational_score: Optional[float] = None
    requires_human_review: bool = False
    human_reviewer: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Follow-up Action Schemas
class FollowUpActionBase(BaseModel):
    action_type: str = Field(..., max_length=50)
    priority: str = "medium"
    subject: str = Field(..., max_length=500)
    message: str
    recipient_email: str = Field(..., max_length=255)
    due_date: Optional[datetime] = None


class FollowUpActionCreate(FollowUpActionBase):
    assessment_id: int


class FollowUpActionUpdate(BaseModel):
    status: Optional[str] = None
    response_content: Optional[str] = None
    escalated: Optional[bool] = None


class FollowUpAction(FollowUpActionBase):
    id: int
    assessment_id: int
    status: str = "pending"
    sent_at: Optional[datetime] = None
    response_received_at: Optional[datetime] = None
    response_content: Optional[str] = None
    attempt_count: int = 0
    escalated: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Assessment Request Schema
class AssessmentRequest(BaseModel):
    vendor_domain: str = Field(..., description="Vendor domain to assess")
    vendor_name: Optional[str] = Field(None, description="Vendor name (optional)")
    priority: str = Field("medium", description="Assessment priority")
    custom_criteria: Optional[Dict[str, Any]] = Field(None, description="Custom assessment criteria")


# Assessment Result Schema
class AssessmentResult(BaseModel):
    assessment: VendorAssessment
    vendor: Vendor
    documents: List[ComplianceDocument]
    findings: List[ComplianceFinding]
    follow_ups: List[FollowUpAction]
    summary: Dict[str, Any]


# Monitoring Schemas
class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(str, Enum):
    DATA_BREACH = "data_breach"
    SERVICE_OUTAGE = "service_outage"
    VULNERABILITY = "vulnerability"
    CERTIFICATE_ISSUE = "certificate_issue"
    INFRASTRUCTURE_CHANGE = "infrastructure_change"
    REPUTATION_CHANGE = "reputation_change"
    REGULATORY_ISSUE = "regulatory_issue"
    BUSINESS_RISK = "business_risk"


class MonitoringStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    DISABLED = "disabled"
    ERROR = "error"


class MonitoringConfigBase(BaseModel):
    vendor_domain: str = Field(..., max_length=255)
    vendor_name: Optional[str] = Field(None, max_length=255)
    assessment_id: Optional[str] = Field(None, max_length=100)
    status: MonitoringStatus = MonitoringStatus.ACTIVE
    check_frequency_minutes: int = Field(default=300, ge=5, le=1440)  # 5 minutes to 24 hours
    alert_thresholds: Optional[Dict[str, Any]] = Field(default_factory=dict)


class MonitoringConfigCreate(MonitoringConfigBase):
    pass


class MonitoringConfig(MonitoringConfigBase):
    id: str
    created_at: datetime
    updated_at: datetime
    last_checked: Optional[datetime] = None
    next_check: Optional[datetime] = None
    total_checks: int = 0
    total_alerts: int = 0

    class Config:
        from_attributes = True


class MonitoringAlertBase(BaseModel):
    vendor_domain: str = Field(..., max_length=255)
    vendor_name: str = Field(..., max_length=255)
    alert_type: AlertType
    severity: AlertSeverity
    title: str = Field(..., max_length=255)
    description: str
    details: Dict[str, Any] = Field(default_factory=dict)
    source: str = Field(..., max_length=100)
    confidence: float = Field(..., ge=0, le=100)
    recommended_actions: List[str] = Field(default_factory=list)


class MonitoringAlertCreate(MonitoringAlertBase):
    monitoring_config_id: str


class MonitoringAlert(MonitoringAlertBase):
    id: str
    monitoring_config_id: str
    created_at: datetime
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved: bool = False
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MonitoringCheckBase(BaseModel):
    monitoring_config_id: str
    check_type: str = "scheduled"
    status: str = "completed"
    alerts_found: int = 0
    duration_seconds: float
    intelligence_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None


class MonitoringCheckCreate(MonitoringCheckBase):
    pass


class MonitoringCheck(MonitoringCheckBase):
    id: str
    started_at: datetime
    completed_at: datetime

    class Config:
        from_attributes = True


# API Response Schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int


class MonitoringStatusResponse(BaseModel):
    monitoring_available: bool
    active_monitors: int
    total_alerts_today: int
    system_health: str
    last_check: datetime
    version: str
