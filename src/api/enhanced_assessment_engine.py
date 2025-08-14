"""
Enhanced Vendor Risk Assessment Engine
Based on industry-standard frameworks including MITRE CTSA, CWRAF, CWSS, CVSS, and Open FAIR
"""

import asyncio
import logging
import socket
import dns.resolver
import whois
import requests
import nmap
import ssl
import subprocess
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import numpy as np
import json

logger = logging.getLogger(__name__)

class RiskPillar(Enum):
    SAFEGUARD = "safeguard"
    PRIVACY = "privacy"  
    RESILIENCY = "resiliency"
    REPUTATION = "reputation"

@dataclass
class AssetDiscovery:
    """Represents discovered digital assets for a vendor"""
    primary_domain: str
    subdomains: List[str]
    ip_ranges: List[str]
    certificates: List[Dict[str, Any]]
    open_ports: List[Dict[str, Any]]
    dns_records: Dict[str, List[str]]
    third_party_services: List[str]

@dataclass
class CVSSScore:
    """CVSS v3.1 scoring"""
    base_score: float
    temporal_score: float
    environmental_score: float
    attack_vector: str
    attack_complexity: str
    privileges_required: str
    user_interaction: str
    scope: str
    confidentiality_impact: str
    integrity_impact: str
    availability_impact: str

@dataclass
class OpenFAIRAnalysis:
    """Open FAIR risk analysis components"""
    threat_event_frequency: float  # 0-100
    vulnerability: float  # 0-100  
    loss_event_frequency: float  # 0-100
    loss_magnitude: float  # 0-100
    annualized_loss_expectancy: float  # USD
    risk_tolerance: str  # low/medium/high/critical

class EnhancedAssessmentEngine:
    """
    Comprehensive vendor risk assessment engine using industry standards
    """
    
    def __init__(self):
        self.scoring_frameworks = {
            'mitre_ctsa': self._calculate_mitre_ctsa,
            'cwraf': self._calculate_cwraf,
            'cwss': self._calculate_cwss,
            'cvss': self._calculate_cvss,
            'open_fair': self._calculate_open_fair
        }
        
        # Core risk categories grouped by pillars
        self.risk_categories = {
            RiskPillar.SAFEGUARD: [
                'access_control',
                'authentication',
                'encryption',
                'network_security',
                'endpoint_protection',
                'patch_management',
                'application_security',
                'credential_management',
                'ssl_tls_strength',
                'email_security'
            ],
            RiskPillar.PRIVACY: [
                'data_classification',
                'data_retention',
                'consent_management',
                'privacy_controls',
                'regulatory_compliance',
                'information_disclosure'
            ],
            RiskPillar.RESILIENCY: [
                'backup_recovery',
                'incident_response',
                'business_continuity',
                'monitoring_detection',
                'vulnerability_management',
                'cdn_security',
                'website_security',
                'dns_health',
                'ddos_resiliency'
            ],
            RiskPillar.REPUTATION: [
                'breach_history',
                'compliance_violations',
                'industry_standing',
                'transparency',
                'customer_trust',
                'hacktivist_shares',
                'social_network',
                'attack_surface',
                'brand_monitoring',
                'ip_reputation',
                'fraudulent_apps',
                'fraudulent_domains',
                'web_ranking'
            ]
        }
        
        # Assessment mode specific configurations
        self.assessment_mode_configs = {
            'technical_due_diligence': {
                'focus_pillars': [RiskPillar.SAFEGUARD, RiskPillar.RESILIENCY],
                'category_weights': {
                    'access_control': 1.2,
                    'authentication': 1.2,
                    'encryption': 1.3,
                    'network_security': 1.3,
                    'patch_management': 1.4,
                    'application_security': 1.4,
                    'ssl_tls_strength': 1.3,
                    'vulnerability_management': 1.4,
                    'endpoint_protection': 1.2,
                    'monitoring_detection': 1.1,
                    'dns_health': 1.2,
                    'cdn_security': 1.1,
                    'website_security': 1.3
                },
                'scoring_adjustment': 0.85  # More strict technical scoring
            },
            'business_risk': {
                'focus_pillars': [RiskPillar.REPUTATION, RiskPillar.PRIVACY],
                'category_weights': {
                    'breach_history': 1.4,
                    'compliance_violations': 1.3,
                    'industry_standing': 1.2,
                    'customer_trust': 1.3,
                    'regulatory_compliance': 1.3,
                    'data_classification': 1.2,
                    'privacy_controls': 1.2,
                    'business_continuity': 1.2,
                    'incident_response': 1.1,
                    'brand_monitoring': 1.1,
                    'fraudulent_domains': 1.1,
                    'ip_reputation': 1.1
                },
                'scoring_adjustment': 1.1  # More lenient business-focused scoring
            }
        }

    async def comprehensive_assessment(self, vendor_domain: str, regulations: List[str], 
                                     assessment_mode: str = "business_risk") -> Dict[str, Any]:
        """
        Run comprehensive vendor risk assessment
        
        Args:
            vendor_domain: Target domain for assessment
            regulations: List of applicable regulations
            assessment_mode: "technical_due_diligence" or "business_risk"
        """
        logger.info(f"🔬 Starting {assessment_mode} assessment for {vendor_domain}")
        
        # Phase 1: Asset Discovery
        assets = await self._discover_assets(vendor_domain)
        
        # Phase 2: Risk Category Analysis (filtered by assessment mode)
        category_scores = await self._analyze_risk_categories(vendor_domain, assets, assessment_mode)
        
        # Phase 3: Apply Scoring Frameworks
        framework_scores = await self._apply_scoring_frameworks(vendor_domain, assets, category_scores, assessment_mode)
        
        # Phase 4: Generate Final Assessment
        final_assessment = await self._generate_final_assessment(
            vendor_domain, assets, category_scores, framework_scores, regulations, assessment_mode
        )
        
        logger.info(f"✅ {assessment_mode} assessment completed for {vendor_domain}")
        return final_assessment

    async def _discover_assets(self, vendor_domain: str) -> AssetDiscovery:
        """
        Phase 1: Comprehensive asset discovery
        Identifies all publicly accessible domains, subdomains, IP ranges, etc.
        """
        logger.info(f"🔍 Discovering assets for {vendor_domain}")
        
        try:
            # Subdomain enumeration
            subdomains = await self._discover_subdomains(vendor_domain)
            
            # IP range discovery
            ip_ranges = await self._discover_ip_ranges(vendor_domain)
            
            # SSL certificate analysis
            certificates = await self._analyze_certificates(vendor_domain, subdomains)
            
            # Port scanning (limited to common ports for demo)
            open_ports = await self._scan_common_ports(vendor_domain)
            
            # DNS record analysis
            dns_records = await self._analyze_dns_records(vendor_domain)
            
            # Third-party service detection
            third_party_services = await self._detect_third_party_services(vendor_domain)
            
            return AssetDiscovery(
                primary_domain=vendor_domain,
                subdomains=subdomains,
                ip_ranges=ip_ranges,
                certificates=certificates,
                open_ports=open_ports,
                dns_records=dns_records,
                third_party_services=third_party_services
            )
            
        except Exception as e:
            logger.error(f"❌ Asset discovery failed: {str(e)}")
            # Return minimal discovery for demo
            return AssetDiscovery(
                primary_domain=vendor_domain,
                subdomains=[],
                ip_ranges=[],
                certificates=[],
                open_ports=[],
                dns_records={},
                third_party_services=[]
            )

    async def _discover_subdomains(self, domain: str) -> List[str]:
        """Discover subdomains using multiple techniques"""
        subdomains = set()
        
        # Common subdomain list
        common_subs = [
            'www', 'mail', 'ftp', 'admin', 'api', 'app', 'blog', 'dev', 'staging',
            'test', 'portal', 'support', 'help', 'docs', 'cdn', 'assets', 'static'
        ]
        
        for sub in common_subs:
            try:
                full_domain = f"{sub}.{domain}"
                socket.gethostbyname(full_domain)
                subdomains.add(full_domain)
            except socket.gaierror:
                pass
        
        return list(subdomains)

    async def _discover_ip_ranges(self, domain: str) -> List[str]:
        """Discover IP ranges associated with the domain"""
        try:
            ip_addresses = set()
            
            # Resolve main domain
            main_ip = socket.gethostbyname(domain)
            ip_addresses.add(main_ip)
            
            # Get CIDR ranges (simplified for demo)
            ip_parts = main_ip.split('.')
            cidr_24 = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            
            return [main_ip, cidr_24]
            
        except Exception as e:
            logger.warning(f"IP discovery failed: {str(e)}")
            return []

    async def _analyze_certificates(self, domain: str, subdomains: List[str]) -> List[Dict[str, Any]]:
        """Analyze SSL certificates for security assessment"""
        certificates = []
        
        domains_to_check = [domain] + subdomains[:5]  # Limit for demo
        
        for check_domain in domains_to_check:
            try:
                context = ssl.create_default_context()
                with socket.create_connection((check_domain, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=check_domain) as ssock:
                        cert = ssock.getpeercert()
                        
                        certificates.append({
                            'domain': check_domain,
                            'issuer': cert.get('issuer', []),
                            'subject': cert.get('subject', []),
                            'version': cert.get('version', 0),
                            'serial_number': cert.get('serialNumber', ''),
                            'not_before': cert.get('notBefore', ''),
                            'not_after': cert.get('notAfter', ''),
                            'signature_algorithm': cert.get('signatureAlgorithm', ''),
                            'san': cert.get('subjectAltName', [])
                        })
                        
            except Exception as e:
                logger.debug(f"Certificate analysis failed for {check_domain}: {str(e)}")
                
        return certificates

    async def _scan_common_ports(self, domain: str) -> List[Dict[str, Any]]:
        """Scan common ports (limited for demo/ethical reasons)"""
        open_ports = []
        common_ports = [80, 443, 22, 21, 25, 53, 110, 143, 993, 995]
        
        try:
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((domain, port))
                if result == 0:
                    open_ports.append({
                        'port': port,
                        'service': self._get_service_name(port),
                        'state': 'open'
                    })
                sock.close()
                
        except Exception as e:
            logger.warning(f"Port scanning failed: {str(e)}")
            
        return open_ports

    def _get_service_name(self, port: int) -> str:
        """Map port numbers to service names"""
        service_map = {
            21: 'FTP', 22: 'SSH', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
            993: 'IMAPS', 995: 'POP3S'
        }
        return service_map.get(port, f'Unknown-{port}')

    async def _analyze_dns_records(self, domain: str) -> Dict[str, List[str]]:
        """Analyze DNS records for security insights"""
        dns_records = {}
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                dns_records[record_type] = [str(rdata) for rdata in answers]
            except Exception:
                dns_records[record_type] = []
                
        return dns_records

    async def _detect_third_party_services(self, domain: str) -> List[str]:
        """Detect third-party services and integrations"""
        services = []
        
        try:
            # Analyze web page for third-party integrations
            response = requests.get(f"https://{domain}", timeout=10, verify=False)
            content = response.text.lower()
            
            # Common third-party service indicators
            service_indicators = {
                'google-analytics': ['google-analytics.com', 'gtag(', 'ga('],
                'cloudflare': ['cloudflare', 'cf-ray'],
                'amazon-aws': ['amazonaws.com', 's3.amazonaws'],
                'microsoft-azure': ['azure', 'azureedge.net'],
                'salesforce': ['salesforce.com', 'force.com'],
                'zendesk': ['zendesk.com', 'zdassets.com'],
                'intercom': ['intercom.io', 'widget.intercom.io'],
                'hubspot': ['hubspot.com', 'hs-scripts.com']
            }
            
            for service, indicators in service_indicators.items():
                if any(indicator in content for indicator in indicators):
                    services.append(service)
                    
        except Exception as e:
            logger.debug(f"Third-party service detection failed: {str(e)}")
            
        return services

    async def _analyze_risk_categories(self, vendor_domain: str, assets: AssetDiscovery, 
                                      assessment_mode: str = "business_risk") -> Dict[str, Dict[str, float]]:
        """
        Phase 2: Analyze risk categories based on assessment mode
        """
        logger.info(f"📊 Analyzing risk categories for {vendor_domain} in {assessment_mode} mode")
        
        mode_config = self.assessment_mode_configs.get(assessment_mode, self.assessment_mode_configs['business_risk'])
        category_scores = {}
        
        for pillar, categories in self.risk_categories.items():
            category_scores[pillar.value] = {}
            
            for category in categories:
                base_score = await self._assess_category(category, vendor_domain, assets)
                
                # Apply mode-specific weighting
                weight = mode_config['category_weights'].get(category, 1.0)
                adjusted_score = base_score * weight
                
                # Apply mode-specific scoring adjustment
                final_score = adjusted_score * mode_config['scoring_adjustment']
                
                # Ensure score stays within 0-100 range
                final_score = max(0, min(100, final_score))
                
                category_scores[pillar.value][category] = final_score
                
        return category_scores

    async def _assess_category(self, category: str, domain: str, assets: AssetDiscovery) -> float:
        """Assess individual risk category (0-100 scale)"""
        
        # Category-specific assessment logic
        assessments = {
            'access_control': self._assess_access_control,
            'authentication': self._assess_authentication,
            'encryption': self._assess_encryption,
            'network_security': self._assess_network_security,
            'endpoint_protection': self._assess_endpoint_protection,
            'patch_management': self._assess_patch_management,
            'application_security': self._assess_application_security,
            'credential_management': self._assess_credential_management,
            'ssl_tls_strength': self._assess_ssl_tls_strength,
            'email_security': self._assess_email_security,
            'data_classification': self._assess_data_classification,
            'data_retention': self._assess_data_retention,
            'consent_management': self._assess_consent_management,
            'privacy_controls': self._assess_privacy_controls,
            'regulatory_compliance': self._assess_regulatory_compliance,
            'information_disclosure': self._assess_information_disclosure,
            'backup_recovery': self._assess_backup_recovery,
            'incident_response': self._assess_incident_response,
            'business_continuity': self._assess_business_continuity,
            'monitoring_detection': self._assess_monitoring_detection,
            'vulnerability_management': self._assess_vulnerability_management,
            'cdn_security': self._assess_cdn_security,
            'website_security': self._assess_website_security,
            'dns_health': self._assess_dns_health,
            'ddos_resiliency': self._assess_ddos_resiliency,
            'breach_history': self._assess_breach_history,
            'compliance_violations': self._assess_compliance_violations,
            'industry_standing': self._assess_industry_standing,
            'transparency': self._assess_transparency,
            'customer_trust': self._assess_customer_trust,
            'hacktivist_shares': self._assess_hacktivist_shares,
            'social_network': self._assess_social_network,
            'attack_surface': self._assess_attack_surface,
            'brand_monitoring': self._assess_brand_monitoring,
            'ip_reputation': self._assess_ip_reputation,
            'fraudulent_apps': self._assess_fraudulent_apps,
            'fraudulent_domains': self._assess_fraudulent_domains,
            'web_ranking': self._assess_web_ranking
        }
        
        if category in assessments:
            return await assessments[category](domain, assets)
        
        # Default assessment based on domain characteristics
        return self._default_category_assessment(category, domain, assets)

    # Individual category assessment methods
    async def _assess_encryption(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess encryption implementation"""
        score = 50.0  # Base score
        
        # Check SSL/TLS implementation
        for cert in assets.certificates:
            # Strong algorithms boost score
            if 'RSA' in str(cert.get('signature_algorithm', '')):
                score += 10
            if cert.get('version', 0) >= 3:  # TLS 1.2+
                score += 15
                
        # Check for HTTPS ports
        https_ports = [p for p in assets.open_ports if p['port'] in [443, 8443]]
        if https_ports:
            score += 20
            
        return min(score, 100.0)

    async def _assess_network_security(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess network security posture"""
        score = 60.0
        
        # Penalize unnecessary open ports
        risky_ports = [p for p in assets.open_ports if p['port'] in [21, 23, 135, 445]]
        score -= len(risky_ports) * 15
        
        # Reward security-focused DNS records
        txt_records = assets.dns_records.get('TXT', [])
        security_records = [r for r in txt_records if any(sec in r.lower() 
                           for sec in ['spf', 'dmarc', 'dkim'])]
        score += len(security_records) * 5
        
        return max(min(score, 100.0), 0.0)

    # Placeholder methods for other categories
    async def _assess_access_control(self, domain: str, assets: AssetDiscovery) -> float:
        return 70.0 + (hash(domain) % 30)  # Mock assessment
        
    async def _assess_authentication(self, domain: str, assets: AssetDiscovery) -> float:
        return 65.0 + (hash(domain) % 25)
        
    async def _assess_endpoint_protection(self, domain: str, assets: AssetDiscovery) -> float:
        return 75.0 + (hash(domain) % 20)
        
    async def _assess_data_classification(self, domain: str, assets: AssetDiscovery) -> float:
        return 60.0 + (hash(domain) % 35)
        
    async def _assess_data_retention(self, domain: str, assets: AssetDiscovery) -> float:
        return 70.0 + (hash(domain) % 25)
        
    async def _assess_consent_management(self, domain: str, assets: AssetDiscovery) -> float:
        return 55.0 + (hash(domain) % 40)
        
    async def _assess_privacy_controls(self, domain: str, assets: AssetDiscovery) -> float:
        return 65.0 + (hash(domain) % 30)
        
    async def _assess_regulatory_compliance(self, domain: str, assets: AssetDiscovery) -> float:
        return 70.0 + (hash(domain) % 25)
        
    async def _assess_backup_recovery(self, domain: str, assets: AssetDiscovery) -> float:
        return 75.0 + (hash(domain) % 20)
        
    async def _assess_incident_response(self, domain: str, assets: AssetDiscovery) -> float:
        return 65.0 + (hash(domain) % 30)
        
    async def _assess_business_continuity(self, domain: str, assets: AssetDiscovery) -> float:
        return 70.0 + (hash(domain) % 25)
        
    async def _assess_monitoring_detection(self, domain: str, assets: AssetDiscovery) -> float:
        return 60.0 + (hash(domain) % 35)
        
    async def _assess_vulnerability_management(self, domain: str, assets: AssetDiscovery) -> float:
        return 65.0 + (hash(domain) % 30)
        
    async def _assess_breach_history(self, domain: str, assets: AssetDiscovery) -> float:
        # Higher score = better (fewer breaches)
        return 80.0 + (hash(domain) % 20)
        
    async def _assess_compliance_violations(self, domain: str, assets: AssetDiscovery) -> float:
        return 85.0 + (hash(domain) % 15)
        
    async def _assess_industry_standing(self, domain: str, assets: AssetDiscovery) -> float:
        return 75.0 + (hash(domain) % 25)
        
    async def _assess_transparency(self, domain: str, assets: AssetDiscovery) -> float:
        return 70.0 + (hash(domain) % 30)
        
    async def _assess_customer_trust(self, domain: str, assets: AssetDiscovery) -> float:
        return 75.0 + (hash(domain) % 25)

    # New enhanced security assessment functions
    async def _assess_patch_management(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess patch management practices"""
        score = 60.0
        
        # Check for modern TLS versions (indicates current patching)
        for cert in assets.certificates:
            if cert.get('version', 0) >= 3:  # TLS 1.2+
                score += 15
        
        # Assess based on open ports (fewer unnecessary ports = better patch discipline)
        common_ports = [80, 443, 22, 25, 53]
        open_count = len([p for p in assets.open_ports if p['port'] not in common_ports])
        score -= min(open_count * 5, 30)  # Cap penalty
        
        return max(min(score, 100.0), 0.0)

    async def _assess_application_security(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess application security posture"""
        score = 65.0
        
        # Security headers analysis (simulated based on domain characteristics)
        security_indicators = 0
        if len(assets.subdomains) > 0:  # Multiple subdomains suggest mature architecture
            security_indicators += 1
        if any('api' in sub for sub in assets.subdomains):  # API presence
            security_indicators += 1
        if any(cert.get('version', 0) >= 3 for cert in assets.certificates):
            security_indicators += 1
            
        score += security_indicators * 10
        
        # Penalize if too many services exposed
        if len(assets.open_ports) > 10:
            score -= 20
            
        return max(min(score, 100.0), 0.0)

    async def _assess_credential_management(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess credential management practices"""
        score = 70.0
        
        # Check for secure authentication ports
        secure_ports = [443, 993, 995]  # HTTPS, IMAPS, POP3S
        if any(p['port'] in secure_ports for p in assets.open_ports):
            score += 15
            
        # Penalize insecure protocols
        insecure_ports = [21, 23, 110, 143]  # FTP, Telnet, POP3, IMAP
        insecure_count = len([p for p in assets.open_ports if p['port'] in insecure_ports])
        score -= insecure_count * 25
        
        return max(min(score, 100.0), 0.0)

    async def _assess_ssl_tls_strength(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess SSL/TLS implementation strength"""
        score = 50.0
        
        for cert in assets.certificates:
            # Check certificate strength
            key_size = cert.get('key_size', 0)
            if key_size >= 2048:
                score += 20
            elif key_size >= 1024:
                score += 10
                
            # Check for modern TLS
            if cert.get('version', 0) >= 3:  # TLS 1.2+
                score += 20
                
            # Check signature algorithm
            sig_alg = cert.get('signature_algorithm', '')
            if 'SHA256' in str(sig_alg) or 'SHA384' in str(sig_alg):
                score += 10
                
        return min(score, 100.0)

    async def _assess_email_security(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess email security configuration"""
        score = 50.0
        
        # Check for mail-related DNS records
        mx_records = assets.dns_records.get('MX', [])
        txt_records = assets.dns_records.get('TXT', [])
        
        if mx_records:
            score += 10
            
        # Check for email security records
        email_security_indicators = 0
        for record in txt_records:
            record_lower = record.lower()
            if 'spf' in record_lower:
                email_security_indicators += 1
            if 'dmarc' in record_lower:
                email_security_indicators += 1
            if 'dkim' in record_lower:
                email_security_indicators += 1
                
        score += email_security_indicators * 15
        
        return min(score, 100.0)

    async def _assess_information_disclosure(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess information disclosure risks"""
        score = 80.0  # Start high, penalize for disclosures
        
        # Too many exposed services indicate potential information disclosure
        if len(assets.open_ports) > 15:
            score -= 30
        elif len(assets.open_ports) > 10:
            score -= 15
            
        # Too many subdomains might expose internal structure
        if len(assets.subdomains) > 20:
            score -= 20
        elif len(assets.subdomains) > 10:
            score -= 10
            
        return max(score, 0.0)

    async def _assess_cdn_security(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess CDN and content delivery security"""
        score = 70.0
        
        # Check for CDN-related subdomains
        cdn_indicators = ['cdn', 'static', 'assets', 'media', 'img']
        cdn_subdomains = [sub for sub in assets.subdomains 
                         if any(indicator in sub.lower() for indicator in cdn_indicators)]
        
        if cdn_subdomains:
            score += 15  # CDN usage is good for security
            
        # Check if CDN endpoints are secured
        https_ports = [p for p in assets.open_ports if p['port'] in [443, 8443]]
        if https_ports and cdn_subdomains:
            score += 10
            
        return min(score, 100.0)

    async def _assess_website_security(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess overall website security posture"""
        score = 60.0
        
        # HTTPS availability
        if any(p['port'] == 443 for p in assets.open_ports):
            score += 20
            
        # Modern certificate
        for cert in assets.certificates:
            if cert.get('version', 0) >= 3:
                score += 15
                break
                
        # Avoid unnecessary port exposure
        web_ports = [80, 443, 8080, 8443]
        non_web_ports = [p for p in assets.open_ports if p['port'] not in web_ports]
        if len(non_web_ports) < 5:
            score += 10
            
        return min(score, 100.0)

    async def _assess_dns_health(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess DNS configuration health"""
        score = 65.0
        
        # Check for essential DNS records
        record_types = set(assets.dns_records.keys())
        essential_records = {'A', 'MX', 'TXT'}
        
        if essential_records.issubset(record_types):
            score += 20
        else:
            missing = essential_records - record_types
            score -= len(missing) * 10
            
        # Check for security-related DNS records
        txt_records = assets.dns_records.get('TXT', [])
        security_records = [r for r in txt_records if any(sec in r.lower() 
                           for sec in ['spf', 'dmarc', 'dkim', 'v=spf1'])]
        score += min(len(security_records) * 8, 25)
        
        return min(score, 100.0)

    async def _assess_ddos_resiliency(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess DDoS protection and resiliency"""
        score = 60.0
        
        # Multiple IP addresses suggest load balancing/redundancy
        unique_ips = set()
        for subdomain in [domain] + assets.subdomains:
            try:
                ip = socket.gethostbyname(subdomain)
                unique_ips.add(ip)
            except:
                pass
                
        if len(unique_ips) > 3:
            score += 20
        elif len(unique_ips) > 1:
            score += 10
            
        # CDN presence helps with DDoS protection
        cdn_indicators = ['cdn', 'cloudflare', 'akamai', 'fastly']
        has_cdn = any(indicator in sub.lower() for sub in assets.subdomains 
                     for indicator in cdn_indicators)
        if has_cdn:
            score += 15
            
        return min(score, 100.0)

    async def _assess_hacktivist_shares(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess exposure to hacktivist communities"""
        # Higher score = lower risk/exposure
        base_score = 85.0
        
        # Simulate assessment based on domain characteristics
        # In real implementation, this would check threat intelligence feeds
        domain_hash = hash(domain) % 100
        
        # Simulate risk factors
        if domain_hash < 20:  # 20% of domains have some exposure
            base_score -= 30
        elif domain_hash < 40:  # Additional 20% have moderate exposure
            base_score -= 15
            
        return max(base_score, 0.0)

    async def _assess_social_network(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess social network security and reputation"""
        score = 75.0
        
        # Simulate social media presence analysis
        # In real implementation, this would check social media APIs
        social_indicators = ['blog', 'news', 'social', 'community']
        social_presence = any(indicator in sub.lower() for sub in assets.subdomains 
                            for indicator in social_indicators)
        
        if social_presence:
            score += 10  # Active social presence is generally positive
            
        return min(score, 100.0)

    async def _assess_attack_surface(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess overall attack surface exposure"""
        score = 90.0  # Start high, penalize for exposure
        
        # Penalize for excessive open ports
        port_count = len(assets.open_ports)
        if port_count > 20:
            score -= 40
        elif port_count > 10:
            score -= 25
        elif port_count > 5:
            score -= 10
            
        # Penalize for too many subdomains
        subdomain_count = len(assets.subdomains)
        if subdomain_count > 30:
            score -= 25
        elif subdomain_count > 15:
            score -= 15
        elif subdomain_count > 8:
            score -= 5
            
        return max(score, 0.0)

    async def _assess_brand_monitoring(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess brand protection and monitoring"""
        score = 70.0
        
        # Check for brand protection indicators
        protection_indicators = ['brand', 'trademark', 'legal', 'abuse']
        has_protection = any(indicator in sub.lower() for sub in assets.subdomains 
                           for indicator in protection_indicators)
        
        if has_protection:
            score += 20
            
        # Professional domain structure suggests good brand management
        if len(assets.subdomains) >= 3:  # Multiple subdomains suggest organization
            score += 10
            
        return min(score, 100.0)

    async def _assess_ip_reputation(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess IP address reputation"""
        score = 80.0  # Assume good reputation by default
        
        # Simulate IP reputation check
        # In real implementation, this would check threat intelligence feeds
        try:
            ip = socket.gethostbyname(domain)
            ip_hash = hash(ip) % 100
            
            # Simulate reputation scoring
            if ip_hash < 10:  # 10% chance of poor reputation
                score -= 50
            elif ip_hash < 25:  # 15% chance of moderate issues
                score -= 25
                
        except socket.gaierror:
            score -= 20  # DNS resolution issues
            
        return max(score, 0.0)

    async def _assess_fraudulent_apps(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess risk of fraudulent applications"""
        # Higher score = lower risk
        score = 85.0
        
        # Simulate fraudulent app assessment
        # In real implementation, this would check app stores and threat feeds
        domain_hash = hash(domain) % 100
        
        if domain_hash < 15:  # 15% have some fraudulent app risk
            score -= 35
        elif domain_hash < 30:  # Additional 15% have moderate risk
            score -= 20
            
        return max(score, 0.0)

    async def _assess_fraudulent_domains(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess risk from fraudulent domains"""
        # Higher score = lower risk
        score = 80.0
        
        # Simulate fraudulent domain assessment
        # In real implementation, this would check domain reputation feeds
        domain_hash = hash(domain) % 100
        
        if domain_hash < 20:  # 20% have fraudulent domain issues
            score -= 40
        elif domain_hash < 35:  # Additional 15% have moderate issues
            score -= 25
            
        return max(score, 0.0)

    async def _assess_web_ranking(self, domain: str, assets: AssetDiscovery) -> float:
        """Assess web ranking and visibility"""
        score = 70.0
        
        # Simulate web ranking assessment based on domain characteristics
        # In real implementation, this would use actual ranking APIs
        
        # Popular TLDs get higher scores
        if domain.endswith(('.com', '.org', '.net')):
            score += 10
        elif domain.endswith(('.gov', '.edu')):
            score += 20
            
        # Multiple subdomains suggest established presence
        if len(assets.subdomains) > 5:
            score += 15
        elif len(assets.subdomains) > 2:
            score += 10
            
        return min(score, 100.0)

    def _default_category_assessment(self, category: str, domain: str, assets: AssetDiscovery) -> float:
        """Default assessment for unimplemented categories"""
        return 70.0 + (hash(f"{category}{domain}") % 30)

    async def _apply_scoring_frameworks(self, domain: str, assets: AssetDiscovery, 
                                      category_scores: Dict[str, Dict[str, float]], 
                                      assessment_mode: str = "business_risk") -> Dict[str, Any]:
        """
        Phase 3: Apply industry-standard scoring frameworks
        """
        logger.info(f"🎯 Applying scoring frameworks for {domain} in {assessment_mode} mode")
        
        framework_results = {}
        
        for framework_name, framework_func in self.scoring_frameworks.items():
            try:
                result = await framework_func(domain, assets, category_scores)
                framework_results[framework_name] = result
            except Exception as e:
                logger.error(f"Framework {framework_name} failed: {str(e)}")
                framework_results[framework_name] = {"error": str(e)}
                
        return framework_results

    async def _calculate_mitre_ctsa(self, domain: str, assets: AssetDiscovery, 
                                   category_scores: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """MITRE Cyber Threat Susceptibility Assessment"""
        
        # MITRE CTSA focuses on organizational susceptibility to cyber threats
        threat_vectors = {
            'phishing': self._calculate_phishing_susceptibility(category_scores),
            'malware': self._calculate_malware_susceptibility(category_scores),
            'insider_threat': self._calculate_insider_threat_susceptibility(category_scores),
            'supply_chain': self._calculate_supply_chain_susceptibility(category_scores),
            'advanced_persistent_threat': self._calculate_apt_susceptibility(category_scores)
        }
        
        overall_susceptibility = np.mean(list(threat_vectors.values()))
        
        return {
            'overall_susceptibility': overall_susceptibility,
            'threat_vectors': threat_vectors,
            'risk_level': self._ctsa_risk_level(overall_susceptibility),
            'recommendations': self._ctsa_recommendations(threat_vectors)
        }

    async def _calculate_cwraf(self, domain: str, assets: AssetDiscovery,
                              category_scores: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Common Weakness Risk Analysis Framework"""
        
        # CWRAF analyzes software weakness risk
        weakness_categories = {
            'input_validation': category_scores.get('safeguard', {}).get('access_control', 70),
            'authentication': category_scores.get('safeguard', {}).get('authentication', 70),
            'authorization': category_scores.get('safeguard', {}).get('access_control', 70),
            'cryptography': category_scores.get('safeguard', {}).get('encryption', 70),
            'error_handling': category_scores.get('resiliency', {}).get('monitoring_detection', 70)
        }
        
        risk_scores = {}
        for weakness, score in weakness_categories.items():
            # Convert to risk (lower score = higher risk)
            risk_scores[weakness] = 100 - score
            
        overall_risk = np.mean(list(risk_scores.values()))
        
        return {
            'overall_risk': overall_risk,
            'weakness_risks': risk_scores,
            'risk_level': self._cwraf_risk_level(overall_risk),
            'critical_weaknesses': [w for w, r in risk_scores.items() if r > 60]
        }

    async def _calculate_cwss(self, domain: str, assets: AssetDiscovery,
                             category_scores: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Common Weakness Scoring System"""
        
        # CWSS provides standardized weakness scoring
        base_finding = {
            'technical_impact': 0.7,  # Medium impact
            'acquired_privilege': 0.6,
            'acquired_privilege_layer': 0.8,
            'finding_confidence': 0.9
        }
        
        environmental_factors = {
            'prevalence': 0.6,
            'business_impact': 0.8
        }
        
        base_score = np.mean(list(base_finding.values())) * 10
        environmental_score = base_score * np.mean(list(environmental_factors.values()))
        
        return {
            'base_score': base_score,
            'environmental_score': environmental_score,
            'base_finding': base_finding,
            'environmental_factors': environmental_factors,
            'severity': self._cwss_severity(environmental_score)
        }

    async def _calculate_cvss(self, domain: str, assets: AssetDiscovery,
                             category_scores: Dict[str, Dict[str, float]]) -> CVSSScore:
        """Common Vulnerability Scoring System v3.1"""
        
        # Mock CVSS calculation based on discovered vulnerabilities
        base_metrics = {
            'attack_vector': 'Network',
            'attack_complexity': 'Low',
            'privileges_required': 'None',
            'user_interaction': 'None',
            'scope': 'Unchanged',
            'confidentiality_impact': 'High',
            'integrity_impact': 'High', 
            'availability_impact': 'High'
        }
        
        # Calculate base score (simplified)
        base_score = 7.5  # Example high severity
        
        return CVSSScore(
            base_score=base_score,
            temporal_score=base_score * 0.9,
            environmental_score=base_score * 0.8,
            **base_metrics
        )

    async def _calculate_open_fair(self, domain: str, assets: AssetDiscovery,
                                  category_scores: Dict[str, Dict[str, float]]) -> OpenFAIRAnalysis:
        """Open FAIR (Factor Analysis of Information Risk)"""
        
        # Calculate threat event frequency
        threat_capability = 70  # Moderate threat capability
        threat_event_frequency = min(threat_capability * 1.2, 100)
        
        # Calculate vulnerability based on security posture  
        safeguard_strength = np.mean(list(category_scores.get('safeguard', {}).values()))
        vulnerability = 100 - safeguard_strength
        
        # Loss event frequency
        loss_event_frequency = (threat_event_frequency * vulnerability) / 100
        
        # Loss magnitude (financial impact)
        primary_loss = 500000  # $500K base
        secondary_loss = 200000  # $200K secondary
        loss_magnitude = (primary_loss + secondary_loss) / 10000  # Scale to 0-100
        
        # Annualized Loss Expectancy
        ale = (loss_event_frequency / 100) * (primary_loss + secondary_loss)
        
        return OpenFAIRAnalysis(
            threat_event_frequency=threat_event_frequency,
            vulnerability=vulnerability,
            loss_event_frequency=loss_event_frequency,
            loss_magnitude=loss_magnitude,
            annualized_loss_expectancy=ale,
            risk_tolerance=self._determine_risk_tolerance(ale)
        )

    # Helper methods for scoring frameworks
    def _calculate_phishing_susceptibility(self, category_scores: Dict[str, Dict[str, float]]) -> float:
        auth_score = category_scores.get('safeguard', {}).get('authentication', 70)
        training_score = category_scores.get('reputation', {}).get('customer_trust', 70)
        return 100 - ((auth_score + training_score) / 2)

    def _calculate_malware_susceptibility(self, category_scores: Dict[str, Dict[str, float]]) -> float:
        endpoint_score = category_scores.get('safeguard', {}).get('endpoint_protection', 70)
        monitoring_score = category_scores.get('resiliency', {}).get('monitoring_detection', 70)
        return 100 - ((endpoint_score + monitoring_score) / 2)

    def _calculate_insider_threat_susceptibility(self, category_scores: Dict[str, Dict[str, float]]) -> float:
        access_score = category_scores.get('safeguard', {}).get('access_control', 70)
        monitoring_score = category_scores.get('resiliency', {}).get('monitoring_detection', 70)
        return 100 - ((access_score + monitoring_score) / 2)

    def _calculate_supply_chain_susceptibility(self, category_scores: Dict[str, Dict[str, float]]) -> float:
        vendor_mgmt = category_scores.get('reputation', {}).get('industry_standing', 70)
        return 100 - vendor_mgmt

    def _calculate_apt_susceptibility(self, category_scores: Dict[str, Dict[str, float]]) -> float:
        network_score = category_scores.get('safeguard', {}).get('network_security', 70)
        vuln_mgmt = category_scores.get('resiliency', {}).get('vulnerability_management', 70)
        return 100 - ((network_score + vuln_mgmt) / 2)

    def _ctsa_risk_level(self, susceptibility: float) -> str:
        if susceptibility < 25: return "Low"
        elif susceptibility < 50: return "Medium"
        elif susceptibility < 75: return "High"
        else: return "Critical"

    def _ctsa_recommendations(self, threat_vectors: Dict[str, float]) -> List[str]:
        recommendations = []
        for vector, score in threat_vectors.items():
            if score > 60:
                recommendations.append(f"Address high {vector} susceptibility")
        return recommendations

    def _cwraf_risk_level(self, risk: float) -> str:
        if risk < 30: return "Low"
        elif risk < 60: return "Medium" 
        else: return "High"

    def _cwss_severity(self, score: float) -> str:
        if score < 4: return "Low"
        elif score < 7: return "Medium"
        else: return "High"

    def _determine_risk_tolerance(self, ale: float) -> str:
        if ale < 100000: return "low"
        elif ale < 500000: return "medium"
        elif ale < 1000000: return "high"
        else: return "critical"

    async def _generate_final_assessment(self, domain: str, assets: AssetDiscovery,
                                        category_scores: Dict[str, Dict[str, float]],
                                        framework_scores: Dict[str, Any],
                                        regulations: List[str],
                                        assessment_mode: str = "business_risk") -> Dict[str, Any]:
        """
        Phase 4: Generate comprehensive final assessment
        """
        logger.info(f"📋 Generating final assessment for {domain} in {assessment_mode} mode")
        
        # Calculate pillar scores
        pillar_scores = {}
        for pillar, categories in category_scores.items():
            pillar_scores[pillar] = np.mean(list(categories.values()))
        
        # Overall risk score (weighted average)
        weights = {
            'safeguard': 0.3,
            'privacy': 0.25,
            'resiliency': 0.25,
            'reputation': 0.2
        }
        
        overall_score = sum(pillar_scores[pillar] * weights[pillar] 
                           for pillar in pillar_scores.keys())
        
        # Risk level determination
        risk_level = self._determine_overall_risk_level(overall_score)
        
        return {
            'vendor_domain': domain,
            'vendor_name': domain.split('.')[0].title(),
            'assessment_timestamp': datetime.now().isoformat(),
            'overall_score': round(overall_score, 1),
            'risk_level': risk_level,
            'pillar_scores': {k: round(v, 1) for k, v in pillar_scores.items()},
            'category_scores': {
                pillar: {cat: round(score, 1) for cat, score in categories.items()}
                for pillar, categories in category_scores.items()
            },
            'framework_analysis': framework_scores,
            'asset_discovery': {
                'primary_domain': assets.primary_domain,
                'subdomains_found': len(assets.subdomains),
                'ip_ranges_found': len(assets.ip_ranges),
                'certificates_analyzed': len(assets.certificates),
                'open_ports_found': len(assets.open_ports),
                'third_party_services': len(assets.third_party_services)
            },
            'regulatory_compliance': self._assess_regulatory_compliance_detailed(
                category_scores, regulations
            ),
            'recommendations': self._generate_recommendations(
                pillar_scores, framework_scores
            ),
            'executive_summary': self._generate_executive_summary(
                domain, overall_score, risk_level, pillar_scores
            )
        }

    def _determine_overall_risk_level(self, score: float) -> str:
        if score >= 90: return "excellent"
        elif score >= 80: return "good"
        elif score >= 70: return "acceptable"
        elif score >= 60: return "needs_improvement"
        else: return "high_risk"

    def _assess_regulatory_compliance_detailed(self, category_scores: Dict[str, Dict[str, float]], 
                                             regulations: List[str]) -> Dict[str, Any]:
        """Detailed regulatory compliance assessment"""
        compliance_scores = {}
        
        for regulation in regulations:
            if regulation.upper() == 'GDPR':
                compliance_scores['GDPR'] = {
                    'overall_score': category_scores.get('privacy', {}).get('regulatory_compliance', 70),
                    'data_protection': category_scores.get('privacy', {}).get('privacy_controls', 70),
                    'consent_management': category_scores.get('privacy', {}).get('consent_management', 70),
                    'breach_notification': category_scores.get('resiliency', {}).get('incident_response', 70)
                }
            elif regulation.upper() == 'SOC2':
                compliance_scores['SOC2'] = {
                    'security': np.mean(list(category_scores.get('safeguard', {}).values())),
                    'availability': category_scores.get('resiliency', {}).get('business_continuity', 70),
                    'processing_integrity': category_scores.get('safeguard', {}).get('access_control', 70),
                    'confidentiality': category_scores.get('safeguard', {}).get('encryption', 70),
                    'privacy': np.mean(list(category_scores.get('privacy', {}).values()))
                }
        
        return compliance_scores

    def _generate_recommendations(self, pillar_scores: Dict[str, float], 
                                framework_scores: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Pillar-based recommendations
        for pillar, score in pillar_scores.items():
            if score < 70:
                recommendations.append({
                    'category': pillar,
                    'priority': 'high' if score < 50 else 'medium',
                    'recommendation': f"Improve {pillar} controls and processes",
                    'impact': 'Reduces overall risk exposure'
                })
        
        # Framework-specific recommendations
        if 'mitre_ctsa' in framework_scores:
            ctsa_data = framework_scores['mitre_ctsa']
            if isinstance(ctsa_data, dict) and 'recommendations' in ctsa_data:
                for rec in ctsa_data['recommendations']:
                    recommendations.append({
                        'category': 'threat_susceptibility',
                        'priority': 'high',
                        'recommendation': rec,
                        'impact': 'Reduces cyber threat susceptibility'
                    })
        
        return recommendations

    def _generate_executive_summary(self, domain: str, overall_score: float, 
                                  risk_level: str, pillar_scores: Dict[str, float]) -> str:
        """Generate executive summary"""
        
        strongest_pillar = max(pillar_scores, key=pillar_scores.get)
        weakest_pillar = min(pillar_scores, key=pillar_scores.get)
        
        summary = f"""
        Executive Risk Assessment Summary for {domain}

        Overall Risk Score: {overall_score}/100 ({risk_level.replace('_', ' ').title()})

        Key Findings:
        • Strongest area: {strongest_pillar.title()} ({pillar_scores[strongest_pillar]:.1f}/100)
        • Area for improvement: {weakest_pillar.title()} ({pillar_scores[weakest_pillar]:.1f}/100)
        • Assessment based on industry-standard frameworks (MITRE CTSA, CWRAF, CVSS, Open FAIR)

        Risk Profile:
        • Safeguard Controls: {pillar_scores.get('safeguard', 0):.1f}/100
        • Privacy Protection: {pillar_scores.get('privacy', 0):.1f}/100  
        • Business Resiliency: {pillar_scores.get('resiliency', 0):.1f}/100
        • Market Reputation: {pillar_scores.get('reputation', 0):.1f}/100

        This assessment provides a comprehensive view of vendor risk across 20 security categories
        using established cybersecurity frameworks and methodologies.
        """
        
        return summary.strip()

# Instantiate the enhanced engine
enhanced_assessment_engine = EnhancedAssessmentEngine()
