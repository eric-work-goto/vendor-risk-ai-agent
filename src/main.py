"""
Main application entry point and orchestration
"""

import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

from .agents.document_retrieval import DocumentRetrievalAgent, retrieve_vendor_documents
from .agents.compliance_analysis import ComplianceAnalysisAgent, analyze_document_content
from .agents.risk_assessment import RiskAssessmentAgent, calculate_vendor_risk
from .agents.workflow_automation import WorkflowAutomationAgent, automate_vendor_workflow
from .models.schemas import (
    VendorCreate, VendorAssessment, AssessmentRequest, 
    AssessmentResult, DocumentType, AssessmentStatus
)
from .config.settings import settings
from .services.storage_service import StorageService
from .utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)


class VendorRiskAssessmentOrchestrator:
    """Main orchestrator for the vendor risk assessment process"""
    
    def __init__(self):
        self.storage_service = StorageService()
        self.document_agent = None
        self.analysis_agent = ComplianceAnalysisAgent()
        self.risk_agent = RiskAssessmentAgent()
        self.workflow_agent = WorkflowAutomationAgent()
    
    async def assess_vendor(
        self,
        request: AssessmentRequest
    ) -> AssessmentResult:
        """
        Perform complete vendor risk assessment
        
        Args:
            request: Assessment request with vendor details and criteria
            
        Returns:
            Complete assessment result
        """
        logger.info(f"Starting vendor assessment for {request.vendor_domain}")
        
        try:
            # 1. Create or get vendor record
            vendor = await self._create_vendor_record(request)
            
            # 2. Create assessment record
            assessment = await self._create_assessment_record(vendor.id, request)
            
            # 3. Document Retrieval Phase
            logger.info("Phase 1: Document Retrieval")
            documents = await self._retrieve_documents(vendor, assessment)
            
            # 4. Compliance Analysis Phase
            logger.info("Phase 2: Compliance Analysis")
            all_findings = await self._analyze_documents(documents, assessment)
            
            # 5. Risk Assessment Phase
            logger.info("Phase 3: Risk Assessment")
            risk_scores, risk_breakdown = await self._calculate_risk_scores(
                all_findings, request, assessment
            )
            
            # 6. Workflow Automation Phase
            logger.info("Phase 4: Workflow Automation")
            workflow_results = await self._automate_workflow(
                assessment, all_findings, vendor
            )
            
            # 7. Compile Results
            result = await self._compile_assessment_result(
                vendor, assessment, documents, all_findings, 
                risk_scores, risk_breakdown, workflow_results
            )
            
            logger.info(f"Assessment completed for {request.vendor_domain}")
            return result
            
        except Exception as e:
            logger.error(f"Error in vendor assessment: {str(e)}")
            raise
    
    async def _create_vendor_record(self, request: AssessmentRequest) -> VendorCreate:
        """Create or retrieve vendor record"""
        # In a real implementation, this would interact with the database
        vendor = VendorCreate(
            name=request.vendor_name or request.vendor_domain,
            domain=request.vendor_domain,
            contact_email=None,  # Would be populated from database or discovery
            contact_name=None,
            industry=None,
            country=None,
            trust_center_url=None
        )
        
        # Simulate database ID assignment
        vendor.id = 1  # Would come from database
        
        logger.info(f"Created vendor record for {vendor.name}")
        return vendor
    
    async def _create_assessment_record(
        self, 
        vendor_id: int, 
        request: AssessmentRequest
    ) -> VendorAssessment:
        """Create assessment record"""
        # In a real implementation, this would create a database record
        assessment = VendorAssessment(
            id=1,  # Would come from database
            vendor_id=vendor_id,
            assessment_type="automated",
            status=AssessmentStatus.IN_PROGRESS,
            assessment_criteria=request.custom_criteria or {},
            requires_human_review=False,
            started_at=datetime.now()
        )
        
        logger.info(f"Created assessment record {assessment.id}")
        return assessment
    
    async def _retrieve_documents(
        self, 
        vendor: VendorCreate, 
        assessment: VendorAssessment
    ) -> List[Dict[str, Any]]:
        """Retrieve and process vendor documents"""
        try:
            # Use the document retrieval agent
            processed_docs = await retrieve_vendor_documents(
                vendor.domain, vendor.id, self.storage_service
            )
            
            logger.info(f"Retrieved {len(processed_docs)} documents")
            return processed_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    async def _analyze_documents(
        self, 
        documents: List[Dict[str, Any]], 
        assessment: VendorAssessment
    ) -> List[Any]:
        """Analyze documents for compliance findings"""
        all_findings = []
        
        for doc_data in documents:
            if not doc_data.get('content'):
                continue
            
            try:
                # Simulate document ID
                doc_id = len(all_findings) + 1
                
                # Determine document type
                doc_type = doc_data['schema'].document_type
                
                # Analyze document content
                findings, risk_score = await analyze_document_content(
                    doc_data['content'],
                    doc_type,
                    doc_id,
                    assessment.id
                )
                
                all_findings.extend(findings)
                logger.info(f"Analyzed document {doc_id}: {len(findings)} findings, risk score: {risk_score}")
                
            except Exception as e:
                logger.error(f"Error analyzing document: {str(e)}")
                continue
        
        logger.info(f"Total findings across all documents: {len(all_findings)}")
        return all_findings
    
    async def _calculate_risk_scores(
        self,
        findings: List[Any],
        request: AssessmentRequest,
        assessment: VendorAssessment
    ) -> Tuple[Dict[str, float], Dict[str, Any]]:
        """Calculate risk scores and breakdown"""
        try:
            # Extract risk criteria from request
            criteria = request.custom_criteria or {}
            
            data_sensitivity = criteria.get('data_sensitivity', 'medium')
            geographic_locations = criteria.get('geographic_locations', ['US'])
            regulatory_exposure = criteria.get('regulatory_exposure', ['SOC2'])
            business_criticality = criteria.get('business_criticality', 'medium')
            vendor_access_level = criteria.get('vendor_access_level', 'limited')
            
            # Calculate risk using the risk assessment agent
            overall_score, risk_breakdown = calculate_vendor_risk(
                findings,
                data_sensitivity=data_sensitivity,
                geographic_locations=geographic_locations,
                regulatory_exposure=regulatory_exposure,
                business_criticality=business_criticality,
                vendor_access_level=vendor_access_level
            )
            
            # Extract component scores from breakdown
            component_scores = risk_breakdown.get('component_scores', {})
            
            risk_scores = {
                'overall_risk_score': overall_score,
                'data_security_score': component_scores.get('data_security', 50.0),
                'privacy_score': component_scores.get('privacy', 50.0),
                'compliance_score': component_scores.get('compliance', 50.0),
                'operational_score': component_scores.get('operational', 50.0)
            }
            
            logger.info(f"Risk assessment completed. Overall score: {overall_score}")
            return risk_scores, risk_breakdown
            
        except Exception as e:
            logger.error(f"Error calculating risk scores: {str(e)}")
            # Return default scores
            return {
                'overall_risk_score': 50.0,
                'data_security_score': 50.0,
                'privacy_score': 50.0,
                'compliance_score': 50.0,
                'operational_score': 50.0
            }, {}
    
    async def _automate_workflow(
        self,
        assessment: VendorAssessment,
        findings: List[Any],
        vendor: VendorCreate
    ) -> Dict[str, Any]:
        """Automate workflow and follow-up actions"""
        try:
            # Use placeholder contact info (in real implementation, get from database)
            vendor_contact_email = "contact@vendor.com"
            vendor_contact_name = "Vendor Contact"
            
            workflow_results = await automate_vendor_workflow(
                assessment,
                findings,
                vendor_contact_email,
                vendor_contact_name,
                vendor.name
            )
            
            logger.info(f"Workflow automation completed: {workflow_results['follow_up_actions_generated']} actions generated")
            return workflow_results
            
        except Exception as e:
            logger.error(f"Error in workflow automation: {str(e)}")
            return {}
    
    async def _compile_assessment_result(
        self,
        vendor: VendorCreate,
        assessment: VendorAssessment,
        documents: List[Dict[str, Any]],
        findings: List[Any],
        risk_scores: Dict[str, float],
        risk_breakdown: Dict[str, Any],
        workflow_results: Dict[str, Any]
    ) -> AssessmentResult:
        """Compile final assessment result"""
        
        # Update assessment with final scores
        assessment.overall_risk_score = risk_scores['overall_risk_score']
        assessment.data_security_score = risk_scores['data_security_score']
        assessment.privacy_score = risk_scores['privacy_score']
        assessment.compliance_score = risk_scores['compliance_score']
        assessment.operational_score = risk_scores['operational_score']
        assessment.requires_human_review = risk_breakdown.get('requires_human_review', False)
        assessment.status = AssessmentStatus.COMPLETED
        assessment.completed_at = datetime.now()
        
        # Determine risk category
        overall_score = risk_scores['overall_risk_score']
        if overall_score >= 80:
            risk_category = "critical"
        elif overall_score >= 65:
            risk_category = "high"
        elif overall_score >= 40:
            risk_category = "medium"
        else:
            risk_category = "low"
        
        assessment.risk_category = risk_category
        
        # Create summary
        summary = {
            "assessment_id": assessment.id,
            "vendor_name": vendor.name,
            "vendor_domain": vendor.domain,
            "overall_risk_score": overall_score,
            "risk_category": risk_category,
            "total_documents_analyzed": len(documents),
            "total_findings": len(findings),
            "critical_findings": len([f for f in findings if hasattr(f, 'risk_level') and f.risk_level == 'critical']),
            "requires_human_review": assessment.requires_human_review,
            "follow_up_actions_generated": workflow_results.get('follow_up_actions_generated', 0),
            "assessment_date": datetime.now().isoformat(),
            "key_risk_factors": risk_breakdown.get('key_risk_factors', []),
            "recommendations": risk_breakdown.get('recommendations', [])
        }
        
        # In a real implementation, these would be proper model objects from database
        result = AssessmentResult(
            assessment=assessment,
            vendor=vendor,
            documents=[doc['schema'] for doc in documents],
            findings=findings,
            follow_ups=[],  # Would be populated from database
            summary=summary
        )
        
        return result


# Main application class
class VendorRiskApp:
    """Main application class for the Vendor Risk Assessment system"""
    
    def __init__(self):
        self.orchestrator = VendorRiskAssessmentOrchestrator()
    
    async def start(self):
        """Start the application"""
        logger.info("Starting Vendor Risk Assessment System")
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"Debug mode: {settings.debug}")
    
    async def assess_vendor(self, vendor_domain: str, **kwargs) -> AssessmentResult:
        """
        Assess a vendor by domain
        
        Args:
            vendor_domain: Vendor domain to assess
            **kwargs: Additional assessment criteria
            
        Returns:
            Assessment result
        """
        request = AssessmentRequest(
            vendor_domain=vendor_domain,
            vendor_name=kwargs.get('vendor_name'),
            priority=kwargs.get('priority', 'medium'),
            custom_criteria=kwargs.get('custom_criteria')
        )
        
        return await self.orchestrator.assess_vendor(request)
    
    async def get_assessment_status(self, assessment_id: int) -> Dict[str, Any]:
        """Get status of an assessment"""
        # In a real implementation, this would query the database
        return {
            "assessment_id": assessment_id,
            "status": "completed",
            "progress": 100
        }


# CLI interface for testing
async def main():
    """Main function for CLI testing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <vendor_domain> [vendor_name]")
        sys.exit(1)
    
    vendor_domain = sys.argv[1]
    vendor_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create app instance
    app = VendorRiskApp()
    await app.start()
    
    # Run assessment
    print(f"Assessing vendor: {vendor_domain}")
    result = await app.assess_vendor(
        vendor_domain=vendor_domain,
        vendor_name=vendor_name,
        custom_criteria={
            'data_sensitivity': 'high',
            'regulatory_exposure': ['GDPR', 'SOC2'],
            'business_criticality': 'high'
        }
    )
    
    # Print results
    print("\n" + "="*60)
    print("VENDOR RISK ASSESSMENT RESULTS")
    print("="*60)
    print(f"Vendor: {result.summary['vendor_name']}")
    print(f"Domain: {result.summary['vendor_domain']}")
    print(f"Overall Risk Score: {result.summary['overall_risk_score']:.1f}")
    print(f"Risk Category: {result.summary['risk_category'].upper()}")
    print(f"Documents Analyzed: {result.summary['total_documents_analyzed']}")
    print(f"Total Findings: {result.summary['total_findings']}")
    print(f"Critical Findings: {result.summary['critical_findings']}")
    print(f"Requires Human Review: {result.summary['requires_human_review']}")
    print(f"Follow-up Actions: {result.summary['follow_up_actions_generated']}")
    
    if result.summary.get('key_risk_factors'):
        print("\nKey Risk Factors:")
        for factor in result.summary['key_risk_factors']:
            print(f"  • {factor}")
    
    if result.summary.get('recommendations'):
        print("\nRecommendations:")
        for rec in result.summary['recommendations']:
            print(f"  • {rec}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(main())
