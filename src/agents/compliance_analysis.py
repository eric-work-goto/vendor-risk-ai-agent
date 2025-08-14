"""
Compliance Analysis Agent

This agent performs initial screening of compliance documents to identify
key compliance indicators, missing elements, and potential risk factors.
"""

import re
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from loguru import logger

from ..models.schemas import (
    ComplianceFinding, ComplianceFindingCreate, 
    FindingType, RiskLevel, DocumentType
)
from ..config.settings import settings


@dataclass
class ComplianceIndicator:
    """Represents a compliance indicator to search for"""
    category: str
    keywords: List[str]
    required_patterns: List[str]
    risk_weight: float
    description: str


class ComplianceAnalysisAgent:
    """Agent responsible for analyzing compliance documents"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.1
        )
        
        # Text splitter for large documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Compliance indicators to check
        self.compliance_indicators = self._get_compliance_indicators()
        
        # Analysis prompts
        self.analysis_prompts = self._get_analysis_prompts()
    
    def _get_compliance_indicators(self) -> Dict[str, List[ComplianceIndicator]]:
        """Define compliance indicators to search for"""
        return {
            "encryption": [
                ComplianceIndicator(
                    category="encryption",
                    keywords=["encryption", "encrypted", "TLS", "SSL", "AES", "RSA"],
                    required_patterns=[
                        r"AES[-\s]?256",
                        r"TLS\s*1\.[23]",
                        r"encryption\s+at\s+rest",
                        r"encryption\s+in\s+transit"
                    ],
                    risk_weight=0.25,
                    description="Data encryption standards and implementation"
                )
            ],
            "access_control": [
                ComplianceIndicator(
                    category="access_control",
                    keywords=["access control", "authentication", "authorization", "MFA", "2FA"],
                    required_patterns=[
                        r"multi[-\s]?factor\s+authentication",
                        r"role[-\s]?based\s+access",
                        r"principle\s+of\s+least\s+privilege",
                        r"access\s+reviews?"
                    ],
                    risk_weight=0.2,
                    description="Access control and authentication mechanisms"
                )
            ],
            "data_protection": [
                ComplianceIndicator(
                    category="data_protection",
                    keywords=["data protection", "GDPR", "CCPA", "personal data", "PII"],
                    required_patterns=[
                        r"GDPR\s+complian[ct]e?",
                        r"data\s+subject\s+rights",
                        r"data\s+retention\s+policy",
                        r"right\s+to\s+erasure"
                    ],
                    risk_weight=0.2,
                    description="Data protection and privacy compliance"
                )
            ],
            "incident_response": [
                ComplianceIndicator(
                    category="incident_response",
                    keywords=["incident response", "breach notification", "security incident"],
                    required_patterns=[
                        r"incident\s+response\s+plan",
                        r"breach\s+notification",
                        r"security\s+incident\s+management",
                        r"72\s+hour[s]?\s+notification"
                    ],
                    risk_weight=0.15,
                    description="Incident response and breach notification procedures"
                )
            ],
            "compliance_frameworks": [
                ComplianceIndicator(
                    category="compliance_frameworks",
                    keywords=["SOC 2", "ISO 27001", "PCI DSS", "HIPAA", "FedRAMP"],
                    required_patterns=[
                        r"SOC\s*2\s*Type\s*II",
                        r"ISO\s*27001",
                        r"PCI[-\s]?DSS",
                        r"HIPAA\s+complian[ct]e?"
                    ],
                    risk_weight=0.2,
                    description="Compliance with industry frameworks"
                )
            ]
        }
    
    def _get_analysis_prompts(self) -> Dict[str, ChatPromptTemplate]:
        """Get prompts for different types of analysis"""
        return {
            "general_analysis": ChatPromptTemplate.from_messages([
                ("system", """You are a compliance expert analyzing vendor security documentation. 
                Analyze the provided document content for compliance indicators and security practices.
                
                Focus on:
                1. Encryption practices (at rest, in transit, key management)
                2. Access controls and authentication
                3. Data protection and privacy measures
                4. Incident response procedures
                5. Compliance certifications and frameworks
                
                For each finding, provide:
                - Category (encryption, access_control, data_protection, incident_response, compliance_frameworks)
                - Finding type (compliant, non_compliant, missing, unclear)
                - Risk level (low, medium, high, critical)
                - Confidence score (0.0-1.0)
                - Description of the finding
                - Evidence text (exact quote from document)
                
                Return your analysis in structured JSON format."""),
                ("user", "Document Type: {document_type}\n\nDocument Content:\n{content}")
            ]),
            
            "soc2_analysis": ChatPromptTemplate.from_messages([
                ("system", """You are analyzing a SOC 2 report. Focus on the Trust Services Criteria:
                
                1. Security - Protection against unauthorized access
                2. Availability - System availability for operation and use
                3. Processing Integrity - System processing is complete, valid, accurate, timely
                4. Confidentiality - Information designated as confidential is protected
                5. Privacy - Personal information is collected, used, retained, disclosed, and disposed
                
                Look for:
                - Control descriptions and testing results
                - Any exceptions or deviations noted
                - Management responses to findings
                - Scope and boundaries of the examination
                - Type I vs Type II report details
                
                Identify any gaps, exceptions, or areas of concern."""),
                ("user", "SOC 2 Report Content:\n{content}")
            ]),
            
            "privacy_policy_analysis": ChatPromptTemplate.from_messages([
                ("system", """You are analyzing a privacy policy for compliance with data protection regulations.
                
                Check for:
                1. Legal basis for processing personal data
                2. Types of data collected and purposes
                3. Data sharing and third-party disclosures
                4. Data subject rights (access, rectification, erasure, portability)
                5. Data retention periods
                6. International data transfers and safeguards
                7. Contact information for data protection officer
                8. Cookies and tracking technologies
                9. Children's privacy protections
                10. Updates and notification procedures
                
                Assess compliance with GDPR, CCPA, and other major privacy laws."""),
                ("user", "Privacy Policy Content:\n{content}")
            ])
        }
    
    async def analyze_document(
        self, 
        content: str, 
        document_type: DocumentType,
        document_id: int,
        assessment_id: int
    ) -> List[ComplianceFindingCreate]:
        """
        Analyze a compliance document for key indicators
        
        Args:
            content: Document text content
            document_type: Type of document being analyzed
            document_id: Database document ID
            assessment_id: Database assessment ID
            
        Returns:
            List of compliance findings
        """
        logger.info(f"Analyzing {document_type} document (ID: {document_id})")
        
        findings = []
        
        try:
            # 1. Pattern-based analysis for quick wins
            pattern_findings = self._analyze_patterns(content, document_id, assessment_id)
            findings.extend(pattern_findings)
            
            # 2. AI-powered analysis for deeper insights
            ai_findings = await self._analyze_with_ai(content, document_type, document_id, assessment_id)
            findings.extend(ai_findings)
            
            # 3. Document-specific analysis
            if document_type == DocumentType.SOC2:
                soc2_findings = await self._analyze_soc2_specific(content, document_id, assessment_id)
                findings.extend(soc2_findings)
            elif document_type == DocumentType.PRIVACY_POLICY:
                privacy_findings = await self._analyze_privacy_specific(content, document_id, assessment_id)
                findings.extend(privacy_findings)
            
            # 4. Check for missing elements
            missing_findings = self._check_missing_elements(content, document_type, document_id, assessment_id)
            findings.extend(missing_findings)
            
            logger.info(f"Generated {len(findings)} findings for document {document_id}")
            return findings
            
        except Exception as e:
            logger.error(f"Error analyzing document {document_id}: {str(e)}")
            return []
    
    def _analyze_patterns(
        self, 
        content: str, 
        document_id: int, 
        assessment_id: int
    ) -> List[ComplianceFindingCreate]:
        """Perform pattern-based analysis using regular expressions"""
        findings = []
        content_lower = content.lower()
        
        for category, indicators in self.compliance_indicators.items():
            for indicator in indicators:
                # Check for keyword presence
                keyword_matches = sum(1 for keyword in indicator.keywords 
                                    if keyword.lower() in content_lower)
                
                # Check for pattern matches
                pattern_matches = []
                for pattern in indicator.required_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    pattern_matches.extend([match.group() for match in matches])
                
                # Determine finding type based on matches
                if pattern_matches:
                    finding_type = FindingType.COMPLIANT
                    risk_level = RiskLevel.LOW
                    confidence = 0.8
                    description = f"Found compliance indicators for {indicator.description}"
                    evidence = "; ".join(pattern_matches[:3])  # First 3 matches
                elif keyword_matches >= len(indicator.keywords) // 2:
                    finding_type = FindingType.UNCLEAR
                    risk_level = RiskLevel.MEDIUM
                    confidence = 0.6
                    description = f"Partial compliance indicators found for {indicator.description}"
                    evidence = f"Keywords found: {', '.join([kw for kw in indicator.keywords if kw.lower() in content_lower])}"
                else:
                    finding_type = FindingType.MISSING
                    risk_level = RiskLevel.HIGH
                    confidence = 0.7
                    description = f"Missing compliance indicators for {indicator.description}"
                    evidence = "No relevant patterns or keywords found"
                
                # Calculate impact score based on risk weight
                impact_score = int(indicator.risk_weight * 10)
                
                finding = ComplianceFindingCreate(
                    document_id=document_id,
                    assessment_id=assessment_id,
                    category=indicator.category,
                    finding_type=finding_type,
                    description=description,
                    evidence_text=evidence,
                    confidence_score=confidence,
                    risk_level=risk_level,
                    impact_score=impact_score
                )
                findings.append(finding)
        
        return findings
    
    async def _analyze_with_ai(
        self, 
        content: str, 
        document_type: DocumentType,
        document_id: int, 
        assessment_id: int
    ) -> List[ComplianceFindingCreate]:
        """Perform AI-powered analysis using LLM"""
        findings = []
        
        try:
            # Split content into chunks if too large
            if len(content) > 8000:
                chunks = self.text_splitter.split_text(content)
            else:
                chunks = [content]
            
            # Analyze each chunk
            for i, chunk in enumerate(chunks):
                prompt = self.analysis_prompts["general_analysis"]
                
                response = await self.llm.ainvoke(
                    prompt.format_messages(
                        document_type=document_type.value,
                        content=chunk
                    )
                )
                
                # Parse AI response and convert to findings
                ai_findings = self._parse_ai_response(
                    response.content, document_id, assessment_id, f"chunk_{i}"
                )
                findings.extend(ai_findings)
        
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
        
        return findings
    
    async def _analyze_soc2_specific(
        self, 
        content: str, 
        document_id: int, 
        assessment_id: int
    ) -> List[ComplianceFindingCreate]:
        """Perform SOC 2 specific analysis"""
        findings = []
        
        try:
            prompt = self.analysis_prompts["soc2_analysis"]
            response = await self.llm.ainvoke(prompt.format_messages(content=content))
            
            # Look for specific SOC 2 elements
            soc2_patterns = {
                "type_ii_report": r"type\s*ii\s*report",
                "trust_criteria": r"trust\s+services?\s+criteria",
                "control_exceptions": r"exception[s]?|deviation[s]?|deficienc[y|ies]",
                "testing_results": r"testing\s+results?|test\s+work\s+performed"
            }
            
            for pattern_name, pattern in soc2_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                if matches:
                    finding = ComplianceFindingCreate(
                        document_id=document_id,
                        assessment_id=assessment_id,
                        category="soc2_compliance",
                        finding_type=FindingType.COMPLIANT,
                        description=f"SOC 2 {pattern_name.replace('_', ' ')} identified",
                        evidence_text=next(matches).group(),
                        confidence_score=0.9,
                        risk_level=RiskLevel.LOW,
                        impact_score=3
                    )
                    findings.append(finding)
        
        except Exception as e:
            logger.error(f"Error in SOC 2 analysis: {str(e)}")
        
        return findings
    
    async def _analyze_privacy_specific(
        self, 
        content: str, 
        document_id: int, 
        assessment_id: int
    ) -> List[ComplianceFindingCreate]:
        """Perform privacy policy specific analysis"""
        findings = []
        
        try:
            prompt = self.analysis_prompts["privacy_policy_analysis"]
            response = await self.llm.ainvoke(prompt.format_messages(content=content))
            
            # Check for GDPR/CCPA requirements
            privacy_requirements = {
                "data_subject_rights": [
                    r"right\s+to\s+access", r"right\s+to\s+rectification",
                    r"right\s+to\s+erasure", r"right\s+to\s+portability"
                ],
                "legal_basis": [r"legal\s+basis", r"legitimate\s+interest"],
                "data_retention": [r"retention\s+period", r"how\s+long\s+we\s+keep"],
                "international_transfers": [r"international\s+transfer", r"adequacy\s+decision"]
            }
            
            for requirement, patterns in privacy_requirements.items():
                found = any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)
                
                if found:
                    finding_type = FindingType.COMPLIANT
                    risk_level = RiskLevel.LOW
                    description = f"Privacy requirement addressed: {requirement.replace('_', ' ')}"
                else:
                    finding_type = FindingType.MISSING
                    risk_level = RiskLevel.MEDIUM
                    description = f"Missing privacy requirement: {requirement.replace('_', ' ')}"
                
                finding = ComplianceFindingCreate(
                    document_id=document_id,
                    assessment_id=assessment_id,
                    category="privacy_compliance",
                    finding_type=finding_type,
                    description=description,
                    evidence_text="Pattern analysis",
                    confidence_score=0.7,
                    risk_level=risk_level,
                    impact_score=5 if finding_type == FindingType.MISSING else 2
                )
                findings.append(finding)
        
        except Exception as e:
            logger.error(f"Error in privacy analysis: {str(e)}")
        
        return findings
    
    def _check_missing_elements(
        self, 
        content: str, 
        document_type: DocumentType,
        document_id: int, 
        assessment_id: int
    ) -> List[ComplianceFindingCreate]:
        """Check for missing critical elements based on document type"""
        findings = []
        
        # Expected elements by document type
        expected_elements = {
            DocumentType.SOC2: [
                "management assertion", "service auditor's report",
                "description of controls", "testing procedures"
            ],
            DocumentType.PRIVACY_POLICY: [
                "data collection", "purpose of processing",
                "data sharing", "user rights", "contact information"
            ],
            DocumentType.SECURITY_POLICY: [
                "access controls", "encryption", "incident response",
                "security monitoring", "employee training"
            ]
        }
        
        if document_type in expected_elements:
            for element in expected_elements[document_type]:
                # Simple keyword check
                if element.lower() not in content.lower():
                    finding = ComplianceFindingCreate(
                        document_id=document_id,
                        assessment_id=assessment_id,
                        category="missing_elements",
                        finding_type=FindingType.MISSING,
                        description=f"Missing expected element: {element}",
                        evidence_text="Element not found in document",
                        confidence_score=0.8,
                        risk_level=RiskLevel.MEDIUM,
                        impact_score=6
                    )
                    findings.append(finding)
        
        return findings
    
    def _parse_ai_response(
        self, 
        response_text: str, 
        document_id: int, 
        assessment_id: int,
        context: str = ""
    ) -> List[ComplianceFindingCreate]:
        """Parse AI response and convert to finding objects"""
        findings = []
        
        try:
            # Try to extract structured information from the response
            # This is a simplified parser - in production, you'd want more robust JSON parsing
            
            # For now, create a general finding from the AI response
            finding = ComplianceFindingCreate(
                document_id=document_id,
                assessment_id=assessment_id,
                category="ai_analysis",
                finding_type=FindingType.UNCLEAR,  # Default, should be parsed from response
                description=f"AI Analysis Result {context}",
                evidence_text=response_text[:500],  # Truncate to fit
                confidence_score=0.7,
                risk_level=RiskLevel.MEDIUM,
                impact_score=5
            )
            findings.append(finding)
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
        
        return findings
    
    def calculate_document_risk_score(self, findings: List[ComplianceFinding]) -> float:
        """
        Calculate overall risk score for a document based on its findings
        
        Args:
            findings: List of compliance findings
            
        Returns:
            Risk score from 0-100 (higher = more risk)
        """
        if not findings:
            return 50.0  # Default medium risk if no findings
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        # Risk level to score mapping
        risk_scores = {
            RiskLevel.LOW: 10,
            RiskLevel.MEDIUM: 40,
            RiskLevel.HIGH: 70,
            RiskLevel.CRITICAL: 90
        }
        
        # Finding type to weight mapping
        finding_weights = {
            FindingType.COMPLIANT: 0.5,
            FindingType.UNCLEAR: 1.0,
            FindingType.NON_COMPLIANT: 1.5,
            FindingType.MISSING: 2.0
        }
        
        for finding in findings:
            score = risk_scores.get(finding.risk_level, 50)
            weight = finding_weights.get(finding.finding_type, 1.0)
            confidence = finding.confidence_score
            
            # Weight by confidence and finding importance
            weighted_score = score * weight * confidence
            total_weighted_score += weighted_score
            total_weight += weight * confidence
        
        if total_weight == 0:
            return 50.0
        
        final_score = total_weighted_score / total_weight
        return min(100.0, max(0.0, final_score))


# Convenience function for standalone usage
async def analyze_document_content(
    content: str,
    document_type: DocumentType,
    document_id: int,
    assessment_id: int
) -> Tuple[List[ComplianceFindingCreate], float]:
    """
    Convenience function to analyze document content
    
    Args:
        content: Document text content
        document_type: Type of document
        document_id: Database document ID
        assessment_id: Database assessment ID
        
    Returns:
        Tuple of (findings, risk_score)
    """
    agent = ComplianceAnalysisAgent()
    findings = await agent.analyze_document(content, document_type, document_id, assessment_id)
    
    # Convert to full finding objects for risk calculation
    full_findings = []
    for finding_create in findings:
        full_finding = ComplianceFinding(
            id=0,  # Placeholder
            document_id=finding_create.document_id,
            assessment_id=finding_create.assessment_id,
            category=finding_create.category,
            finding_type=finding_create.finding_type,
            description=finding_create.description,
            evidence_text=finding_create.evidence_text,
            confidence_score=finding_create.confidence_score,
            risk_level=finding_create.risk_level,
            impact_score=finding_create.impact_score,
            created_at=datetime.now()
        )
        full_findings.append(full_finding)
    
    risk_score = agent.calculate_document_risk_score(full_findings)
    
    return findings, risk_score
