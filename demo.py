"""
Example usage and testing script for the Vendor Risk Assessment system
"""

import asyncio
import json
from datetime import datetime
from src.main import VendorRiskApp
from src.models.schemas import AssessmentRequest


async def demo_assessment():
    """Run a demonstration assessment"""
    
    print("=" * 60)
    print("VENDOR RISK ASSESSMENT DEMO")
    print("=" * 60)
    
    # Create app instance
    app = VendorRiskApp()
    await app.start()
    
    # Test vendors with different risk profiles
    test_vendors = [
        {
            "domain": "github.com",
            "name": "GitHub",
            "criteria": {
                "data_sensitivity": "medium",
                "regulatory_exposure": ["SOC2"],
                "business_criticality": "high"
            }
        },
        {
            "domain": "slack.com", 
            "name": "Slack Technologies",
            "criteria": {
                "data_sensitivity": "high",
                "regulatory_exposure": ["GDPR", "SOC2"],
                "business_criticality": "critical"
            }
        },
        {
            "domain": "zoom.us",
            "name": "Zoom Video Communications",
            "criteria": {
                "data_sensitivity": "high",
                "regulatory_exposure": ["HIPAA", "GDPR"],
                "business_criticality": "high"
            }
        }
    ]
    
    results = []
    
    for vendor in test_vendors:
        print(f"\n🔍 Assessing {vendor['name']} ({vendor['domain']})...")
        print("-" * 40)
        
        try:
            # Run assessment
            result = await app.assess_vendor(
                vendor_domain=vendor["domain"],
                vendor_name=vendor["name"],
                custom_criteria=vendor["criteria"]
            )
            
            # Display results
            summary = result.summary
            print(f"✅ Assessment completed!")
            print(f"   Risk Score: {summary['overall_risk_score']:.1f}/100")
            print(f"   Risk Level: {summary['risk_category'].upper()}")
            print(f"   Documents: {summary['total_documents_analyzed']}")
            print(f"   Findings: {summary['total_findings']}")
            print(f"   Critical: {summary['critical_findings']}")
            print(f"   Review Required: {summary['requires_human_review']}")
            print(f"   Follow-ups: {summary['follow_up_actions_generated']}")
            
            if summary.get('key_risk_factors'):
                print(f"   Key Risks: {', '.join(summary['key_risk_factors'][:2])}")
            
            results.append({
                "vendor": vendor["name"],
                "domain": vendor["domain"],
                "risk_score": summary['overall_risk_score'],
                "risk_category": summary['risk_category'],
                "summary": summary
            })
            
        except Exception as e:
            print(f"❌ Error assessing {vendor['name']}: {str(e)}")
    
    # Summary report
    print("\n" + "=" * 60)
    print("ASSESSMENT SUMMARY REPORT")
    print("=" * 60)
    
    if results:
        print(f"📊 Assessed {len(results)} vendors")
        
        # Risk distribution
        risk_counts = {}
        for result in results:
            category = result["risk_category"]
            risk_counts[category] = risk_counts.get(category, 0) + 1
        
        print(f"📈 Risk Distribution:")
        for category, count in risk_counts.items():
            print(f"   {category.upper()}: {count} vendor(s)")
        
        # Average risk score
        avg_score = sum(r["risk_score"] for r in results) / len(results)
        print(f"📉 Average Risk Score: {avg_score:.1f}")
        
        # Highest risk vendor
        highest_risk = max(results, key=lambda x: x["risk_score"])
        print(f"⚠️  Highest Risk: {highest_risk['vendor']} ({highest_risk['risk_score']:.1f})")
        
        # Recommendations
        print(f"\n💡 Key Recommendations:")
        high_risk_vendors = [r for r in results if r["risk_score"] >= 70]
        if high_risk_vendors:
            print(f"   • {len(high_risk_vendors)} vendor(s) require immediate attention")
        
        review_required = [r for r in results if r["summary"].get("requires_human_review")]
        if review_required:
            print(f"   • {len(review_required)} assessment(s) need human review")
        
        print(f"   • Consider regular re-assessment cycles")
        print(f"   • Implement continuous monitoring for critical vendors")
    
    print("\n" + "=" * 60)
    return results


async def demo_api_simulation():
    """Simulate API usage patterns"""
    
    print("\n🔧 API SIMULATION")
    print("-" * 30)
    
    # Simulate various API calls
    scenarios = [
        "Bulk vendor assessment",
        "Real-time risk monitoring", 
        "Compliance dashboard updates",
        "Automated follow-up processing"
    ]
    
    for scenario in scenarios:
        print(f"📡 Simulating: {scenario}")
        await asyncio.sleep(0.5)  # Simulate processing time
        print(f"   ✅ Completed in 0.5s")
    
    print(f"🎯 All API scenarios completed successfully")


async def demo_compliance_analysis():
    """Demonstrate compliance analysis capabilities"""
    
    print("\n🔍 COMPLIANCE ANALYSIS DEMO")
    print("-" * 35)
    
    # Sample document content for analysis
    sample_documents = {
        "SOC 2 Report": """
        This report describes the suitability of the design and operating effectiveness 
        of controls relevant to security, availability, and confidentiality for the 
        period January 1, 2024 to December 31, 2024. The service organization uses 
        AES-256 encryption for data at rest and TLS 1.3 for data in transit. 
        Multi-factor authentication is required for all user accounts.
        """,
        
        "Privacy Policy": """
        We collect personal information including names, email addresses, and usage data.
        Data is processed based on legitimate business interests and user consent.
        Users have the right to access, rectify, and delete their personal information.
        We implement appropriate technical and organizational measures to protect data.
        Data retention periods vary by data type, typically 2-7 years.
        """,
        
        "Security Policy": """
        Our security framework includes regular vulnerability assessments,
        incident response procedures, and employee security training.
        Access controls are implemented using role-based permissions.
        All systems are monitored 24/7 for security threats.
        We maintain ISO 27001 certification and undergo annual audits.
        """
    }
    
    from src.agents.compliance_analysis import ComplianceAnalysisAgent
    from src.models.schemas import DocumentType
    
    analyzer = ComplianceAnalysisAgent()
    
    doc_types = {
        "SOC 2 Report": DocumentType.SOC2,
        "Privacy Policy": DocumentType.PRIVACY_POLICY,
        "Security Policy": DocumentType.SECURITY_POLICY
    }
    
    for doc_name, content in sample_documents.items():
        print(f"\n📄 Analyzing: {doc_name}")
        
        try:
            findings = await analyzer.analyze_document(
                content=content,
                document_type=doc_types[doc_name],
                document_id=1,
                assessment_id=1
            )
            
            print(f"   📊 Generated {len(findings)} findings")
            
            # Show sample findings
            for i, finding in enumerate(findings[:3]):  # Show first 3
                print(f"   {i+1}. {finding.category}: {finding.finding_type.value}")
                print(f"      Risk: {finding.risk_level.value}, Confidence: {finding.confidence_score:.2f}")
            
            if len(findings) > 3:
                print(f"   ... and {len(findings) - 3} more findings")
                
        except Exception as e:
            print(f"   ❌ Analysis error: {str(e)}")


async def main():
    """Main demo function"""
    
    print("🚀 Starting Vendor Risk Assessment System Demo")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run main assessment demo
        results = await demo_assessment()
        
        # Show compliance analysis capabilities
        await demo_compliance_analysis()
        
        # Simulate API usage
        await demo_api_simulation()
        
        print("\n🎉 Demo completed successfully!")
        print("💡 To get started:")
        print("   1. Set up your .env file with API keys")
        print("   2. Run: python src/main.py your-vendor-domain.com")
        print("   3. Or start the API: python src/api/app.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("💡 Make sure to install dependencies: pip install -r requirements.txt")


if __name__ == "__main__":
    asyncio.run(main())
