"""
Risk Assessment Agent

This agent calculates risk scores based on compliance findings and predefined criteria.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

from ..models.schemas import (
    VendorAssessment, ComplianceFinding, RiskLevel, 
    FindingType, DocumentType, RiskScores
)
from ..config.settings import settings


@dataclass
class RiskCriteria:
    """Risk assessment criteria configuration"""
    data_sensitivity: str  # 'low', 'medium', 'high', 'critical'
    geographic_location: List[str]  # List of countries/regions
    regulatory_exposure: List[str]  # List of regulations (GDPR, HIPAA, etc.)
    data_types: List[str]  # Types of data processed
    vendor_access_level: str  # 'read_only', 'limited', 'full'
    business_criticality: str  # 'low', 'medium', 'high', 'critical'


class RiskAssessmentAgent:
    """Agent responsible for calculating vendor risk scores"""
    
    def __init__(self):
        # Risk scoring weights
        self.risk_weights = {
            'data_security': 0.3,
            'privacy_compliance': 0.25,
            'operational_security': 0.2,
            'compliance_certifications': 0.15,
            'incident_history': 0.1
        }
        
        # Geographic risk multipliers
        self.geographic_risk = {
            'US': 1.0,
            'EU': 1.0,
            'UK': 1.0,
            'CA': 1.0,
            'AU': 1.0,
            'other_high': 1.2,
            'medium_risk': 1.4,
            'high_risk': 1.8
        }
        
        # Regulatory complexity multipliers
        self.regulatory_multipliers = {
            'GDPR': 1.3,
            'HIPAA': 1.4,
            'PCI_DSS': 1.2,
            'SOX': 1.3,
            'CCPA': 1.1,
            'SOC2': 1.0,
            'ISO27001': 0.9
        }
        
        # Data sensitivity multipliers
        self.data_sensitivity_multipliers = {
            'low': 0.8,
            'medium': 1.0,
            'high': 1.3,
            'critical': 1.6
        }
    
    def calculate_overall_risk_score(
        self,
        findings: List[ComplianceFinding],
        risk_criteria: RiskCriteria,
        vendor_assessment: Optional[VendorAssessment] = None
    ) -> Tuple[float, RiskScores, Dict[str, Any]]:
        """
        Calculate comprehensive risk score for a vendor
        
        Args:
            findings: List of compliance findings
            risk_criteria: Risk assessment criteria
            vendor_assessment: Existing assessment data
            
        Returns:
            Tuple of (overall_score, detailed_scores, risk_breakdown)
        """
        # Calculate component scores
        data_security_score = self._calculate_data_security_score(findings, risk_criteria)
        privacy_score = self._calculate_privacy_score(findings, risk_criteria)
        compliance_score = self._calculate_compliance_score(findings, risk_criteria)
        operational_score = self._calculate_operational_score(findings, risk_criteria)
        
        # Calculate weighted overall score
        component_scores = {
            'data_security': data_security_score,
            'privacy': privacy_score,
            'compliance': compliance_score,
            'operational': operational_score
        }
        
        overall_score = sum(
            score * self.risk_weights.get(component, 0.25)
            for component, score in component_scores.items()
        )
        
        # Apply risk multipliers
        overall_score = self._apply_risk_multipliers(overall_score, risk_criteria)
        
        # Ensure score is within bounds
        overall_score = max(0.0, min(100.0, overall_score))
        
        # Create detailed risk scores object
        risk_scores = RiskScores(
            overall_risk_score=overall_score,
            data_security_score=data_security_score,
            privacy_score=privacy_score,
            compliance_score=compliance_score,
            operational_score=operational_score
        )
        
        # Generate risk breakdown for analysis
        risk_breakdown = self._generate_risk_breakdown(
            findings, risk_criteria, component_scores, overall_score
        )
        
        return overall_score, risk_scores, risk_breakdown
    
    def _calculate_data_security_score(
        self, 
        findings: List[ComplianceFinding], 
        criteria: RiskCriteria
    ) -> float:
        """Calculate data security component score"""
        security_categories = ['encryption', 'access_control', 'network_security', 'data_protection']
        
        category_scores = {}
        for category in security_categories:
            category_findings = [f for f in findings if f.category == category]
            category_score = self._score_findings_by_category(category_findings)
            category_scores[category] = category_score
        
        # Weight encryption more heavily for high sensitivity data
        if criteria.data_sensitivity in ['high', 'critical']:
            encryption_weight = 0.4
            other_weight = 0.2
        else:
            encryption_weight = 0.3
            other_weight = 0.23
        
        data_security_score = (
            category_scores.get('encryption', 50) * encryption_weight +
            category_scores.get('access_control', 50) * other_weight +
            category_scores.get('network_security', 50) * other_weight +
            category_scores.get('data_protection', 50) * other_weight
        )
        
        return data_security_score
    
    def _calculate_privacy_score(
        self, 
        findings: List[ComplianceFinding], 
        criteria: RiskCriteria
    ) -> float:
        """Calculate privacy compliance component score"""
        privacy_categories = ['privacy_compliance', 'data_subject_rights', 'consent_management']
        
        category_scores = {}
        for category in privacy_categories:
            category_findings = [f for f in findings if f.category == category]
            category_score = self._score_findings_by_category(category_findings)
            category_scores[category] = category_score
        
        # Base privacy score
        privacy_score = sum(category_scores.values()) / len(privacy_categories) if category_scores else 50
        
        # Adjust based on regulatory exposure
        regulatory_penalty = 0
        for regulation in criteria.regulatory_exposure:
            if regulation in ['GDPR', 'CCPA', 'PIPEDA']:
                regulatory_penalty += 10
        
        privacy_score += min(regulatory_penalty, 30)  # Cap penalty at 30 points
        
        return min(100, privacy_score)
    
    def _calculate_compliance_score(
        self, 
        findings: List[ComplianceFinding], 
        criteria: RiskCriteria
    ) -> float:
        """Calculate compliance framework component score"""
        compliance_categories = ['soc2_compliance', 'iso27001', 'compliance_frameworks']
        
        # Check for positive compliance indicators
        compliance_findings = [f for f in findings 
                             if f.category in compliance_categories and 
                             f.finding_type == FindingType.COMPLIANT]
        
        # Base score starts lower and improves with compliance findings
        base_score = 60
        
        # Improve score for each compliance finding
        improvement = len(compliance_findings) * 5
        compliance_score = base_score - improvement  # Lower score = better (less risk)
        
        # Penalize for missing compliance frameworks
        missing_frameworks = [f for f in findings 
                            if f.category in compliance_categories and 
                            f.finding_type == FindingType.MISSING]
        
        penalty = len(missing_frameworks) * 8
        compliance_score += penalty
        
        return max(0, min(100, compliance_score))
    
    def _calculate_operational_score(
        self, 
        findings: List[ComplianceFinding], 
        criteria: RiskCriteria
    ) -> float:
        """Calculate operational security component score"""
        operational_categories = ['incident_response', 'business_continuity', 'vendor_management']
        
        category_scores = {}
        for category in operational_categories:
            category_findings = [f for f in findings if f.category == category]
            category_score = self._score_findings_by_category(category_findings)
            category_scores[category] = category_score
        
        # Business criticality affects operational risk
        criticality_multiplier = {
            'low': 0.8,
            'medium': 1.0,
            'high': 1.2,
            'critical': 1.4
        }.get(criteria.business_criticality, 1.0)
        
        operational_score = (sum(category_scores.values()) / len(category_scores) 
                           if category_scores else 50) * criticality_multiplier
        
        return min(100, operational_score)
    
    def _score_findings_by_category(self, findings: List[ComplianceFinding]) -> float:
        """Score a set of findings within a category"""
        if not findings:
            return 50  # Neutral score if no findings
        
        total_score = 0
        total_weight = 0
        
        finding_scores = {
            FindingType.COMPLIANT: 20,
            FindingType.UNCLEAR: 60,
            FindingType.NON_COMPLIANT: 80,
            FindingType.MISSING: 90
        }
        
        for finding in findings:
            score = finding_scores.get(finding.finding_type, 50)
            weight = finding.confidence_score * (finding.impact_score / 10)
            
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 50
    
    def _apply_risk_multipliers(
        self, 
        base_score: float, 
        criteria: RiskCriteria
    ) -> float:
        """Apply geographic and regulatory risk multipliers"""
        
        # Geographic risk adjustment
        geographic_multiplier = 1.0
        for location in criteria.geographic_location:
            location_risk = self.geographic_risk.get(location, 1.2)
            geographic_multiplier = max(geographic_multiplier, location_risk)
        
        # Regulatory complexity adjustment
        regulatory_multiplier = 1.0
        for regulation in criteria.regulatory_exposure:
            reg_risk = self.regulatory_multipliers.get(regulation, 1.1)
            regulatory_multiplier = max(regulatory_multiplier, reg_risk)
        
        # Data sensitivity adjustment
        sensitivity_multiplier = self.data_sensitivity_multipliers.get(
            criteria.data_sensitivity, 1.0
        )
        
        # Vendor access level adjustment
        access_multipliers = {
            'read_only': 0.9,
            'limited': 1.0,
            'full': 1.2,
            'admin': 1.4
        }
        access_multiplier = access_multipliers.get(criteria.vendor_access_level, 1.0)
        
        # Apply all multipliers
        adjusted_score = (base_score * geographic_multiplier * 
                         regulatory_multiplier * sensitivity_multiplier * access_multiplier)
        
        return adjusted_score
    
    def _generate_risk_breakdown(
        self,
        findings: List[ComplianceFinding],
        criteria: RiskCriteria,
        component_scores: Dict[str, float],
        overall_score: float
    ) -> Dict[str, Any]:
        """Generate detailed risk breakdown for reporting"""
        
        # Count findings by type and risk level
        finding_summary = {
            'total_findings': len(findings),
            'by_type': {},
            'by_risk_level': {},
            'by_category': {}
        }
        
        for finding in findings:
            # By type
            finding_type = finding.finding_type.value
            finding_summary['by_type'][finding_type] = finding_summary['by_type'].get(finding_type, 0) + 1
            
            # By risk level
            risk_level = finding.risk_level.value
            finding_summary['by_risk_level'][risk_level] = finding_summary['by_risk_level'].get(risk_level, 0) + 1
            
            # By category
            category = finding.category
            finding_summary['by_category'][category] = finding_summary['by_category'].get(category, 0) + 1
        
        # Risk level determination
        risk_level = self._determine_risk_level(overall_score)
        
        # Key risk factors
        key_risk_factors = self._identify_key_risk_factors(findings, criteria)
        
        # Recommendations
        recommendations = self._generate_recommendations(findings, component_scores, criteria)
        
        return {
            'overall_score': overall_score,
            'risk_level': risk_level,
            'component_scores': component_scores,
            'finding_summary': finding_summary,
            'key_risk_factors': key_risk_factors,
            'recommendations': recommendations,
            'assessment_criteria': {
                'data_sensitivity': criteria.data_sensitivity,
                'geographic_locations': criteria.geographic_location,
                'regulatory_exposure': criteria.regulatory_exposure,
                'business_criticality': criteria.business_criticality
            },
            'requires_human_review': self._requires_human_review(overall_score, findings)
        }
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level category from numeric score"""
        if score >= 80:
            return RiskLevel.CRITICAL.value
        elif score >= 65:
            return RiskLevel.HIGH.value
        elif score >= 40:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.LOW.value
    
    def _identify_key_risk_factors(
        self, 
        findings: List[ComplianceFinding], 
        criteria: RiskCriteria
    ) -> List[str]:
        """Identify the most significant risk factors"""
        risk_factors = []
        
        # High-risk findings
        critical_findings = [f for f in findings if f.risk_level == RiskLevel.CRITICAL]
        high_risk_findings = [f for f in findings if f.risk_level == RiskLevel.HIGH]
        
        if critical_findings:
            risk_factors.append(f"{len(critical_findings)} critical security finding(s)")
        
        if high_risk_findings:
            risk_factors.append(f"{len(high_risk_findings)} high-risk finding(s)")
        
        # Missing critical controls
        missing_findings = [f for f in findings if f.finding_type == FindingType.MISSING]
        critical_missing = [f for f in missing_findings if 'encryption' in f.category or 'access_control' in f.category]
        
        if critical_missing:
            risk_factors.append("Missing critical security controls")
        
        # Regulatory exposure
        if 'GDPR' in criteria.regulatory_exposure and any('privacy' in f.category for f in missing_findings):
            risk_factors.append("GDPR compliance gaps identified")
        
        # High data sensitivity with weak controls
        if criteria.data_sensitivity in ['high', 'critical']:
            weak_encryption = any(f.category == 'encryption' and f.finding_type != FindingType.COMPLIANT for f in findings)
            if weak_encryption:
                risk_factors.append("Inadequate encryption for sensitive data")
        
        return risk_factors
    
    def _generate_recommendations(
        self,
        findings: List[ComplianceFinding],
        component_scores: Dict[str, float],
        criteria: RiskCriteria
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Component-specific recommendations
        if component_scores.get('data_security', 0) > 60:
            recommendations.append("Strengthen data security controls and encryption practices")
        
        if component_scores.get('privacy', 0) > 60:
            recommendations.append("Improve privacy compliance and data subject rights implementation")
        
        if component_scores.get('compliance', 0) > 60:
            recommendations.append("Obtain additional compliance certifications (SOC 2, ISO 27001)")
        
        # Finding-specific recommendations
        missing_soc2 = any(f.category == 'soc2_compliance' and f.finding_type == FindingType.MISSING for f in findings)
        if missing_soc2:
            recommendations.append("Request current SOC 2 Type II report")
        
        missing_encryption = any(f.category == 'encryption' and f.finding_type == FindingType.MISSING for f in findings)
        if missing_encryption:
            recommendations.append("Clarify data encryption practices and key management procedures")
        
        # Criteria-specific recommendations
        if criteria.data_sensitivity in ['high', 'critical']:
            recommendations.append("Conduct enhanced due diligence given high data sensitivity")
        
        if 'GDPR' in criteria.regulatory_exposure:
            recommendations.append("Verify GDPR compliance and DPA execution")
        
        return recommendations
    
    def _requires_human_review(
        self, 
        overall_score: float, 
        findings: List[ComplianceFinding]
    ) -> bool:
        """Determine if human review is required"""
        
        # Always require review for high-risk vendors
        if overall_score >= settings.high_risk_threshold:
            return True
        
        # Require review if critical findings exist
        critical_findings = [f for f in findings if f.risk_level == RiskLevel.CRITICAL]
        if critical_findings:
            return True
        
        # Require review if many high-risk findings
        high_risk_findings = [f for f in findings if f.risk_level == RiskLevel.HIGH]
        if len(high_risk_findings) >= 3:
            return True
        
        # Require review if confidence is low on key findings
        low_confidence_critical = [f for f in findings 
                                 if f.confidence_score < 0.6 and f.impact_score >= 7]
        if len(low_confidence_critical) >= 2:
            return True
        
        return False


def calculate_vendor_risk(
    findings: List[ComplianceFinding],
    data_sensitivity: str = "medium",
    geographic_locations: List[str] = None,
    regulatory_exposure: List[str] = None,
    business_criticality: str = "medium",
    vendor_access_level: str = "limited",
    data_types: List[str] = None
) -> Tuple[float, Dict[str, Any]]:
    """
    Convenience function to calculate vendor risk
    
    Args:
        findings: List of compliance findings
        data_sensitivity: Level of data sensitivity
        geographic_locations: List of geographic locations
        regulatory_exposure: List of applicable regulations
        business_criticality: Business criticality level
        vendor_access_level: Level of vendor access
        data_types: Types of data processed
        
    Returns:
        Tuple of (risk_score, risk_breakdown)
    """
    # Set defaults
    if geographic_locations is None:
        geographic_locations = ["US"]
    if regulatory_exposure is None:
        regulatory_exposure = ["SOC2"]
    if data_types is None:
        data_types = ["business_data"]
    
    # Create risk criteria
    criteria = RiskCriteria(
        data_sensitivity=data_sensitivity,
        geographic_location=geographic_locations,
        regulatory_exposure=regulatory_exposure,
        data_types=data_types,
        vendor_access_level=vendor_access_level,
        business_criticality=business_criticality
    )
    
    # Calculate risk
    agent = RiskAssessmentAgent()
    overall_score, risk_scores, risk_breakdown = agent.calculate_overall_risk_score(
        findings, criteria
    )
    
    return overall_score, risk_breakdown
