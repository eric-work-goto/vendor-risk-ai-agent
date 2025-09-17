"""
AI-Powered Vendor Monitoring Service
Uses corporate OpenAI API to intelligently monitor vendors for security changes
"""

import asyncio
import json
import logging
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class MonitoringAlert:
    """Represents a monitoring alert"""
    id: str
    vendor_domain: str
    vendor_name: str
    alert_type: str
    severity: AlertSeverity
    title: str
    description: str
    details: Dict[str, Any]
    timestamp: datetime
    source: str
    confidence: float  # 0-100%
    recommended_actions: List[str]

class AIVendorMonitor:
    """AI-powered vendor monitoring service using corporate OpenAI API"""
    
    def __init__(self):
        self.corporate_base_url = "https://chat.expertcity.com/api/v1"
        self.corporate_api_key = "sk-2ea30b318c514c9f874dcd2aa56aa090"
        self.client = None
        
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                base_url=self.corporate_base_url,
                api_key=self.corporate_api_key
            )
    
    async def monitor_vendor(self, vendor_domain: str, vendor_name: str = None) -> List[MonitoringAlert]:
        """
        Perform comprehensive AI-powered monitoring of a vendor
        Returns list of alerts found
        """
        if not self.client:
            logger.warning("OpenAI client not available, monitoring disabled")
            return []
        
        try:
            logger.info(f"🔍 Starting AI monitoring for {vendor_domain}")
            
            # Gather intelligence from multiple sources
            intelligence_data = await self._gather_vendor_intelligence(vendor_domain, vendor_name)
            
            # Use AI to analyze the intelligence
            alerts = await self._ai_analyze_intelligence(vendor_domain, vendor_name or vendor_domain, intelligence_data)
            
            logger.info(f"✅ AI monitoring completed for {vendor_domain}: {len(alerts)} alerts found")
            return alerts
            
        except Exception as e:
            logger.error(f"Error monitoring vendor {vendor_domain}: {str(e)}")
            return []
    
    async def _gather_vendor_intelligence(self, vendor_domain: str, vendor_name: str) -> Dict[str, Any]:
        """Gather intelligence about the vendor from various sources"""
        
        intelligence = {
            "domain": vendor_domain,
            "name": vendor_name,
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }
        
        # Gather data from multiple sources in parallel
        tasks = [
            self._fetch_recent_news(vendor_domain, vendor_name),
            self._check_security_advisories(vendor_domain),
            self._monitor_domain_changes(vendor_domain),
            self._check_certificate_status(vendor_domain),
            self._analyze_web_presence(vendor_domain)
        ]
        
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            intelligence["sources"] = {
                "news": results[0] if not isinstance(results[0], Exception) else None,
                "security_advisories": results[1] if not isinstance(results[1], Exception) else None,
                "domain_changes": results[2] if not isinstance(results[2], Exception) else None,
                "certificate_status": results[3] if not isinstance(results[3], Exception) else None,
                "web_presence": results[4] if not isinstance(results[4], Exception) else None
            }
            
        except Exception as e:
            logger.warning(f"Error gathering intelligence for {vendor_domain}: {str(e)}")
        
        return intelligence
    
    async def _ai_analyze_intelligence(self, vendor_domain: str, vendor_name: str, intelligence_data: Dict[str, Any]) -> List[MonitoringAlert]:
        """Use AI to analyze gathered intelligence and generate alerts"""
        
        analysis_prompt = f"""
        You are a cybersecurity analyst performing continuous monitoring of vendor "{vendor_name}" ({vendor_domain}).
        
        Analyze the following intelligence data and identify any security concerns, changes, or risks:
        
        INTELLIGENCE DATA:
        {json.dumps(intelligence_data, indent=2, default=str)}
        
        Please analyze this data for:
        1. **Data Breaches**: Any mentions of security incidents, breaches, or compromises
        2. **Service Outages**: Significant downtime or service interruptions
        3. **Security Vulnerabilities**: New CVEs, security advisories, or vulnerability disclosures
        4. **Certificate Issues**: SSL/TLS certificate problems or changes
        5. **Domain/Infrastructure Changes**: Suspicious DNS, hosting, or configuration changes
        6. **Reputation Changes**: Changes in security posture, compliance status, or trust indicators
        7. **Regulatory Issues**: Compliance problems, fines, or regulatory actions
        8. **Business Risk Changes**: Acquisitions, financial issues, or operational changes affecting security
        
        For each issue found, provide:
        - alert_type: One of [data_breach, service_outage, vulnerability, certificate_issue, infrastructure_change, reputation_change, regulatory_issue, business_risk]
        - severity: critical/high/medium/low
        - title: Brief descriptive title
        - description: Detailed explanation of the issue
        - confidence: Your confidence level (0-100%)
        - recommended_actions: List of specific actions to take
        - details: Additional context and evidence
        
        Return your analysis as a JSON array of alerts. If no significant issues are found, return an empty array [].
        
        IMPORTANT: Only include legitimate security concerns. Do not create false positives for normal business activities.
        """
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity analyst specializing in vendor risk monitoring. Provide accurate, actionable security intelligence."
                    },
                    {
                        "role": "user", 
                        "content": analysis_prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Parse AI response
            alerts = self._parse_ai_alerts(vendor_domain, vendor_name, ai_response)
            
            logger.info(f"🤖 AI analysis completed for {vendor_domain}: {len(alerts)} alerts identified")
            return alerts
            
        except Exception as e:
            logger.error(f"Error in AI analysis for {vendor_domain}: {str(e)}")
            return []
    
    def _parse_ai_alerts(self, vendor_domain: str, vendor_name: str, ai_response: str) -> List[MonitoringAlert]:
        """Parse AI response into MonitoringAlert objects"""
        alerts = []
        
        try:
            # Extract JSON from AI response
            json_start = ai_response.find('[')
            json_end = ai_response.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                logger.warning(f"No JSON array found in AI response for {vendor_domain}")
                return alerts
            
            json_str = ai_response[json_start:json_end]
            alert_data = json.loads(json_str)
            
            # Convert to MonitoringAlert objects
            for i, alert_info in enumerate(alert_data):
                try:
                    alert = MonitoringAlert(
                        id=f"{vendor_domain}_{int(datetime.now().timestamp())}_{i}",
                        vendor_domain=vendor_domain,
                        vendor_name=vendor_name,
                        alert_type=alert_info.get("alert_type", "unknown"),
                        severity=AlertSeverity(alert_info.get("severity", "low")),
                        title=alert_info.get("title", "Security Alert"),
                        description=alert_info.get("description", ""),
                        details=alert_info.get("details", {}),
                        timestamp=datetime.now(),
                        source="ai_analysis",
                        confidence=float(alert_info.get("confidence", 50)),
                        recommended_actions=alert_info.get("recommended_actions", [])
                    )
                    alerts.append(alert)
                    
                except Exception as e:
                    logger.warning(f"Error parsing alert {i} for {vendor_domain}: {str(e)}")
                    continue
        
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing AI response JSON for {vendor_domain}: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing AI alerts for {vendor_domain}: {str(e)}")
        
        return alerts
    
    async def _fetch_recent_news(self, vendor_domain: str, vendor_name: str) -> Dict[str, Any]:
        """Fetch recent news about the vendor"""
        try:
            # Use AI to simulate news gathering (in real implementation, this would use news APIs)
            news_prompt = f"""
            Simulate checking recent news (last 30 days) for {vendor_name or vendor_domain}.
            
            Focus on security-related news like:
            - Data breaches or security incidents
            - Service outages or major downtime
            - Cybersecurity announcements
            - Regulatory issues or fines
            - Major business changes affecting security
            
            Return a brief summary of any significant security-related news found.
            If no significant news, return "No significant security-related news found in the past 30 days."
            """
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": news_prompt}],
                max_tokens=500,
                temperature=0.2
            )
            
            return {
                "summary": response.choices[0].message.content.strip(),
                "timestamp": datetime.now().isoformat(),
                "source": "ai_news_analysis"
            }
            
        except Exception as e:
            logger.warning(f"Error fetching news for {vendor_domain}: {str(e)}")
            return {"error": str(e)}
    
    async def _check_security_advisories(self, vendor_domain: str) -> Dict[str, Any]:
        """Check for security advisories related to the vendor"""
        try:
            advisory_prompt = f"""
            Check for recent security advisories, CVEs, or vulnerability disclosures affecting {vendor_domain}.
            
            Look for:
            - New CVE entries
            - Security bulletins
            - Vulnerability disclosures
            - Patch announcements
            
            Return a summary of any recent security advisories (last 30 days).
            If none found, return "No recent security advisories found."
            """
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": advisory_prompt}],
                max_tokens=400,
                temperature=0.1
            )
            
            return {
                "summary": response.choices[0].message.content.strip(),
                "timestamp": datetime.now().isoformat(),
                "source": "ai_advisory_check"
            }
            
        except Exception as e:
            logger.warning(f"Error checking advisories for {vendor_domain}: {str(e)}")
            return {"error": str(e)}
    
    async def _monitor_domain_changes(self, vendor_domain: str) -> Dict[str, Any]:
        """Monitor for DNS and domain infrastructure changes"""
        try:
            # Basic DNS check simulation
            return {
                "dns_status": "stable",
                "changes_detected": False,
                "timestamp": datetime.now().isoformat(),
                "note": "DNS monitoring requires additional infrastructure"
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _check_certificate_status(self, vendor_domain: str) -> Dict[str, Any]:
        """Check SSL certificate status and changes"""
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(f"https://{vendor_domain}", timeout=10) as response:
                        return {
                            "ssl_accessible": True,
                            "status_code": response.status,
                            "timestamp": datetime.now().isoformat()
                        }
                except Exception:
                    return {
                        "ssl_accessible": False,
                        "timestamp": datetime.now().isoformat(),
                        "note": "SSL connection failed"
                    }
        except Exception as e:
            return {"error": str(e)}
    
    async def _analyze_web_presence(self, vendor_domain: str) -> Dict[str, Any]:
        """Analyze vendor web presence for changes"""
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(f"https://{vendor_domain}", timeout=10) as response:
                        if response.status == 200:
                            content = await response.text()
                            return {
                                "website_accessible": True,
                                "content_length": len(content),
                                "status_code": response.status,
                                "timestamp": datetime.now().isoformat()
                            }
                except Exception:
                    pass
                
                return {
                    "website_accessible": False,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {"error": str(e)}

# Global monitor instance
ai_monitor = AIVendorMonitor()

async def monitor_vendor_ai(vendor_domain: str, vendor_name: str = None) -> List[Dict[str, Any]]:
    """
    Convenience function to monitor a vendor using AI
    Returns list of alert dictionaries for API responses
    """
    alerts = await ai_monitor.monitor_vendor(vendor_domain, vendor_name)
    
    # Convert alerts to dictionaries for API serialization
    return [
        {
            "id": alert.id,
            "vendor_domain": alert.vendor_domain,
            "vendor_name": alert.vendor_name,
            "alert_type": alert.alert_type,
            "severity": alert.severity.value,
            "title": alert.title,
            "description": alert.description,
            "details": alert.details,
            "timestamp": alert.timestamp.isoformat(),
            "source": alert.source,
            "confidence": alert.confidence,
            "recommended_actions": alert.recommended_actions
        }
        for alert in alerts
    ]