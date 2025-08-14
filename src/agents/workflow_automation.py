"""
Workflow Automation Agent

This agent handles the automation of follow-up actions, vendor communications,
and audit logging throughout the assessment process.
"""

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from ..models.schemas import (
    FollowUpAction, FollowUpActionCreate, FollowUpActionUpdate,
    VendorAssessment, ComplianceFinding, RiskLevel, FindingType
)
from ..config.settings import settings


class WorkflowAutomationAgent:
    """Agent responsible for automating workflows and communications"""
    
    def __init__(self):
        self.email_templates = self._get_email_templates()
        self.follow_up_rules = self._get_follow_up_rules()
    
    def _get_email_templates(self) -> Dict[str, str]:
        """Get email templates for different types of communications"""
        return {
            "document_request": """
Subject: Security Documentation Request - {vendor_name}

Dear {contact_name},

We are conducting a vendor risk assessment for {vendor_name} as part of our standard security review process. 

We were unable to locate the following documents and would appreciate if you could provide them:

{missing_documents}

Please share these documents at your earliest convenience. If any of these documents are not applicable or available, please let us know.

For any questions, please don't hesitate to reach out.

Best regards,
Vendor Risk Assessment Team
""",
            
            "clarification_request": """
Subject: Security Controls Clarification - {vendor_name}

Dear {contact_name},

During our review of {vendor_name}'s security documentation, we identified some areas that require clarification:

{clarification_items}

Could you please provide additional information on these items? This will help us complete our assessment more accurately.

Thank you for your cooperation.

Best regards,
Vendor Risk Assessment Team
""",
            
            "compliance_gaps": """
Subject: Compliance Gap Follow-up - {vendor_name}

Dear {contact_name},

Our assessment has identified potential compliance gaps that we'd like to discuss:

{compliance_gaps}

We would appreciate the opportunity to discuss these findings and understand your remediation plans.

Please let us know your availability for a brief call this week.

Best regards,
Vendor Risk Assessment Team
""",
            
            "follow_up_reminder": """
Subject: Follow-up: Security Assessment - {vendor_name}

Dear {contact_name},

This is a follow-up to our previous communication regarding the security assessment for {vendor_name}.

We are still awaiting:
{pending_items}

To ensure timely completion of the assessment, please provide the requested information by {due_date}.

Best regards,
Vendor Risk Assessment Team
""",
            
            "escalation": """
Subject: URGENT: Vendor Assessment Response Required - {vendor_name}

Dear {contact_name},

Despite multiple attempts to obtain the required security documentation and information for {vendor_name}, we have not received a response.

This is impacting our ability to complete the vendor assessment and may affect our business relationship.

Please respond immediately or contact us to discuss.

Best regards,
Vendor Risk Assessment Team
"""
        }
    
    def _get_follow_up_rules(self) -> Dict[str, Dict[str, Any]]:
        """Define rules for automated follow-up actions"""
        return {
            "missing_soc2": {
                "trigger": lambda findings: any(
                    f.category == "soc2_compliance" and f.finding_type == FindingType.MISSING 
                    for f in findings
                ),
                "action_type": "document_request",
                "priority": "high",
                "due_days": 5,
                "message_key": "document_request"
            },
            
            "missing_privacy_policy": {
                "trigger": lambda findings: any(
                    f.category == "privacy_compliance" and f.finding_type == FindingType.MISSING 
                    for f in findings
                ),
                "action_type": "document_request",
                "priority": "medium",
                "due_days": 7,
                "message_key": "document_request"
            },
            
            "unclear_encryption": {
                "trigger": lambda findings: any(
                    f.category == "encryption" and f.finding_type == FindingType.UNCLEAR 
                    for f in findings
                ),
                "action_type": "clarification",
                "priority": "high",
                "due_days": 3,
                "message_key": "clarification_request"
            },
            
            "critical_compliance_gaps": {
                "trigger": lambda findings: any(
                    f.risk_level == RiskLevel.CRITICAL for f in findings
                ),
                "action_type": "urgent_clarification",
                "priority": "urgent",
                "due_days": 2,
                "message_key": "compliance_gaps"
            },
            
            "high_risk_vendor": {
                "trigger": lambda findings: len([
                    f for f in findings if f.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
                ]) >= 3,
                "action_type": "risk_review",
                "priority": "high",
                "due_days": 5,
                "message_key": "compliance_gaps"
            }
        }
    
    async def generate_follow_up_actions(
        self,
        assessment: VendorAssessment,
        findings: List[ComplianceFinding],
        vendor_contact_email: str,
        vendor_contact_name: str = "Vendor Contact",
        vendor_name: str = "Vendor"
    ) -> List[FollowUpActionCreate]:
        """
        Generate automated follow-up actions based on assessment findings
        
        Args:
            assessment: Vendor assessment object
            findings: List of compliance findings
            vendor_contact_email: Contact email for vendor
            vendor_contact_name: Contact name for vendor
            vendor_name: Vendor name
            
        Returns:
            List of follow-up action creation objects
        """
        follow_up_actions = []
        
        # Check each rule against the findings
        for rule_name, rule in self.follow_up_rules.items():
            if rule["trigger"](findings):
                # Generate follow-up action
                action = self._create_follow_up_action(
                    assessment.id,
                    rule,
                    rule_name,
                    findings,
                    vendor_contact_email,
                    vendor_contact_name,
                    vendor_name
                )
                follow_up_actions.append(action)
        
        # Generate custom actions for specific missing documents
        missing_doc_actions = self._generate_missing_document_actions(
            assessment.id, findings, vendor_contact_email, vendor_contact_name, vendor_name
        )
        follow_up_actions.extend(missing_doc_actions)
        
        return follow_up_actions
    
    def _create_follow_up_action(
        self,
        assessment_id: int,
        rule: Dict[str, Any],
        rule_name: str,
        findings: List[ComplianceFinding],
        vendor_email: str,
        vendor_name_contact: str,
        vendor_name: str
    ) -> FollowUpActionCreate:
        """Create a follow-up action based on a rule"""
        
        # Generate message content
        message_content = self._generate_message_content(
            rule["message_key"], rule_name, findings, vendor_name_contact, vendor_name
        )
        
        # Calculate due date
        due_date = datetime.now() + timedelta(days=rule["due_days"])
        
        return FollowUpActionCreate(
            assessment_id=assessment_id,
            action_type=rule["action_type"],
            priority=rule["priority"],
            subject=f"Security Assessment Follow-up: {rule_name.replace('_', ' ').title()}",
            message=message_content,
            recipient_email=vendor_email,
            due_date=due_date
        )
    
    def _generate_missing_document_actions(
        self,
        assessment_id: int,
        findings: List[ComplianceFinding],
        vendor_email: str,
        vendor_name_contact: str,
        vendor_name: str
    ) -> List[FollowUpActionCreate]:
        """Generate actions for missing documents"""
        actions = []
        
        # Group missing findings by document type
        missing_documents = {}
        for finding in findings:
            if finding.finding_type == FindingType.MISSING:
                doc_category = finding.category
                if doc_category not in missing_documents:
                    missing_documents[doc_category] = []
                missing_documents[doc_category].append(finding.description)
        
        # Create action for each category of missing documents
        for doc_category, descriptions in missing_documents.items():
            if len(descriptions) >= 2:  # Only if multiple items missing in category
                message = self._format_document_request_message(
                    doc_category, descriptions, vendor_name_contact, vendor_name
                )
                
                action = FollowUpActionCreate(
                    assessment_id=assessment_id,
                    action_type="document_request",
                    priority="medium",
                    subject=f"Missing {doc_category.replace('_', ' ').title()} Documentation",
                    message=message,
                    recipient_email=vendor_email,
                    due_date=datetime.now() + timedelta(days=7)
                )
                actions.append(action)
        
        return actions
    
    def _generate_message_content(
        self,
        template_key: str,
        rule_name: str,
        findings: List[ComplianceFinding],
        vendor_contact: str,
        vendor_name: str
    ) -> str:
        """Generate message content from template"""
        
        template = self.email_templates.get(template_key, self.email_templates["clarification_request"])
        
        # Extract relevant findings for this rule
        relevant_findings = self._extract_relevant_findings(rule_name, findings)
        
        # Format findings for message
        if "missing" in rule_name:
            formatted_items = "\n".join([f"- {f.description}" for f in relevant_findings])
        elif "unclear" in rule_name:
            formatted_items = "\n".join([f"- {f.description}: {f.evidence_text[:100]}..." for f in relevant_findings])
        else:
            formatted_items = "\n".join([f"- {f.description}" for f in relevant_findings])
        
        # Format template
        return template.format(
            vendor_name=vendor_name,
            contact_name=vendor_contact,
            missing_documents=formatted_items,
            clarification_items=formatted_items,
            compliance_gaps=formatted_items,
            pending_items=formatted_items,
            due_date=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        )
    
    def _format_document_request_message(
        self,
        doc_category: str,
        descriptions: List[str],
        vendor_contact: str,
        vendor_name: str
    ) -> str:
        """Format a document request message"""
        template = self.email_templates["document_request"]
        
        formatted_docs = "\n".join([f"- {desc}" for desc in descriptions])
        
        return template.format(
            vendor_name=vendor_name,
            contact_name=vendor_contact,
            missing_documents=formatted_docs
        )
    
    def _extract_relevant_findings(
        self, 
        rule_name: str, 
        findings: List[ComplianceFinding]
    ) -> List[ComplianceFinding]:
        """Extract findings relevant to a specific rule"""
        
        if "soc2" in rule_name:
            return [f for f in findings if "soc2" in f.category]
        elif "privacy" in rule_name:
            return [f for f in findings if "privacy" in f.category]
        elif "encryption" in rule_name:
            return [f for f in findings if "encryption" in f.category]
        elif "critical" in rule_name:
            return [f for f in findings if f.risk_level == RiskLevel.CRITICAL]
        elif "high_risk" in rule_name:
            return [f for f in findings if f.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        else:
            return findings
    
    async def send_follow_up_email(
        self,
        follow_up_action: FollowUpAction
    ) -> bool:
        """
        Send follow-up email to vendor
        
        Args:
            follow_up_action: Follow-up action to execute
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not settings.smtp_host or not settings.from_email:
            print(f"Email simulation: Would send email to {follow_up_action.recipient_email}")
            print(f"Subject: {follow_up_action.subject}")
            print(f"Message: {follow_up_action.message[:200]}...")
            return True
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = settings.from_email
            msg['To'] = follow_up_action.recipient_email
            msg['Subject'] = follow_up_action.subject
            
            # Add body
            msg.attach(MIMEText(follow_up_action.message, 'plain'))
            
            # Send email
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_username and settings.smtp_password:
                    server.starttls()
                    server.login(settings.smtp_username, settings.smtp_password)
                
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    async def process_follow_up_queue(
        self,
        pending_actions: List[FollowUpAction]
    ) -> Dict[str, int]:
        """
        Process a queue of pending follow-up actions
        
        Args:
            pending_actions: List of pending follow-up actions
            
        Returns:
            Dictionary with processing statistics
        """
        stats = {
            "processed": 0,
            "sent": 0,
            "failed": 0,
            "overdue": 0
        }
        
        for action in pending_actions:
            stats["processed"] += 1
            
            # Check if action is overdue
            if action.due_date and datetime.now() > action.due_date:
                stats["overdue"] += 1
                
                # Escalate if too many attempts
                if action.attempt_count >= settings.max_followup_attempts:
                    await self._escalate_action(action)
                    continue
            
            # Send email
            success = await self.send_follow_up_email(action)
            
            if success:
                stats["sent"] += 1
                # Update action status (this would be done in the service layer)
                # action.status = "sent"
                # action.sent_at = datetime.now()
                # action.attempt_count += 1
            else:
                stats["failed"] += 1
        
        return stats
    
    async def _escalate_action(self, action: FollowUpAction):
        """Escalate an overdue action"""
        escalation_message = self.email_templates["escalation"].format(
            vendor_name="Vendor",  # Would get from database
            contact_name="Vendor Contact",
            pending_items=action.message[:200] + "..."
        )
        
        # Create escalation email (would integrate with management notification system)
        print(f"ESCALATION: Action {action.id} requires management attention")
        print(f"Vendor has not responded after {action.attempt_count} attempts")
    
    def generate_audit_log_entry(
        self,
        event_type: str,
        entity_type: str,
        entity_id: int,
        description: str,
        user_id: str = "system",
        changes: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate audit log entry
        
        Args:
            event_type: Type of event (assessment_started, document_retrieved, etc.)
            entity_type: Type of entity (vendor, assessment, document, etc.)
            entity_id: ID of the entity
            description: Human-readable description
            user_id: User who performed the action
            changes: Before/after data for changes
            metadata: Additional context
            
        Returns:
            Audit log entry dictionary
        """
        return {
            "event_type": event_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user_id": user_id,
            "description": description,
            "changes": changes or {},
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "ip_address": "system",  # Would get from request context
            "user_agent": "Vendor-Risk-Agent/1.0"
        }
    
    async def process_assessment_workflow(
        self,
        assessment: VendorAssessment,
        findings: List[ComplianceFinding],
        vendor_contact_email: str,
        vendor_contact_name: str = "Vendor Contact",
        vendor_name: str = "Vendor"
    ) -> Dict[str, Any]:
        """
        Process the complete assessment workflow
        
        Args:
            assessment: Vendor assessment
            findings: Compliance findings
            vendor_contact_email: Vendor contact email
            vendor_contact_name: Vendor contact name
            vendor_name: Vendor name
            
        Returns:
            Workflow processing results
        """
        workflow_results = {
            "follow_up_actions_generated": 0,
            "emails_sent": 0,
            "audit_entries": [],
            "requires_human_review": False,
            "escalations": 0
        }
        
        try:
            # Generate follow-up actions
            follow_up_actions = await self.generate_follow_up_actions(
                assessment, findings, vendor_contact_email, vendor_contact_name, vendor_name
            )
            
            workflow_results["follow_up_actions_generated"] = len(follow_up_actions)
            
            # Log workflow start
            audit_entry = self.generate_audit_log_entry(
                "workflow_started",
                "assessment",
                assessment.id,
                f"Started automated workflow for assessment {assessment.id}",
                metadata={"vendor_name": vendor_name, "findings_count": len(findings)}
            )
            workflow_results["audit_entries"].append(audit_entry)
            
            # Send follow-up emails (simulation for now)
            for action in follow_up_actions:
                # In a real implementation, these would be saved to database first
                success = await self.send_follow_up_email(action)
                if success:
                    workflow_results["emails_sent"] += 1
                
                # Log email sent
                audit_entry = self.generate_audit_log_entry(
                    "follow_up_sent",
                    "follow_up_action",
                    0,  # Would be action.id
                    f"Follow-up email sent: {action.subject}",
                    metadata={"recipient": vendor_contact_email, "action_type": action.action_type}
                )
                workflow_results["audit_entries"].append(audit_entry)
            
            # Determine if human review is required
            workflow_results["requires_human_review"] = self._requires_human_review(assessment, findings)
            
            # Log workflow completion
            audit_entry = self.generate_audit_log_entry(
                "workflow_completed",
                "assessment",
                assessment.id,
                f"Automated workflow completed for assessment {assessment.id}",
                metadata=workflow_results
            )
            workflow_results["audit_entries"].append(audit_entry)
            
        except Exception as e:
            # Log error
            audit_entry = self.generate_audit_log_entry(
                "workflow_error",
                "assessment",
                assessment.id,
                f"Workflow error: {str(e)}",
                metadata={"error": str(e)}
            )
            workflow_results["audit_entries"].append(audit_entry)
        
        return workflow_results
    
    def _requires_human_review(
        self, 
        assessment: VendorAssessment, 
        findings: List[ComplianceFinding]
    ) -> bool:
        """Determine if human review is required based on assessment and findings"""
        
        # High overall risk score
        if hasattr(assessment, 'overall_risk_score') and assessment.overall_risk_score >= 80:
            return True
        
        # Critical findings
        critical_findings = [f for f in findings if f.risk_level == RiskLevel.CRITICAL]
        if critical_findings:
            return True
        
        # Many high-risk findings
        high_risk_findings = [f for f in findings if f.risk_level == RiskLevel.HIGH]
        if len(high_risk_findings) >= 3:
            return True
        
        # Low confidence on important findings
        low_confidence_important = [
            f for f in findings 
            if f.confidence_score < 0.6 and f.impact_score >= 7
        ]
        if len(low_confidence_important) >= 2:
            return True
        
        return False


# Convenience function for standalone usage
async def automate_vendor_workflow(
    assessment: VendorAssessment,
    findings: List[ComplianceFinding],
    vendor_contact_email: str,
    vendor_contact_name: str = "Vendor Contact",
    vendor_name: str = "Vendor"
) -> Dict[str, Any]:
    """
    Convenience function to automate vendor assessment workflow
    
    Args:
        assessment: Vendor assessment
        findings: Compliance findings
        vendor_contact_email: Vendor contact email
        vendor_contact_name: Vendor contact name
        vendor_name: Vendor name
        
    Returns:
        Workflow processing results
    """
    agent = WorkflowAutomationAgent()
    return await agent.process_assessment_workflow(
        assessment, findings, vendor_contact_email, vendor_contact_name, vendor_name
    )
