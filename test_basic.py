"""
Test vendor risk assessment with multiple scenarios
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import VendorRiskApp


async def quick_test():
    """Quick test of the system"""
    
    print("🔧 Quick Test - Vendor Risk Assessment System")
    print("=" * 50)
    
    # Create app
    app = VendorRiskApp()
    await app.start()
    
    # Test with a well-known vendor
    test_domain = "github.com"
    
    print(f"🔍 Testing assessment for: {test_domain}")
    print("📋 Assessment criteria:")
    print("   • Data Sensitivity: High")
    print("   • Regulations: GDPR, SOC2") 
    print("   • Business Criticality: High")
    print()
    
    try:
        result = await app.assess_vendor(
            vendor_domain=test_domain,
            vendor_name="GitHub Inc",
            custom_criteria={
                'data_sensitivity': 'high',
                'regulatory_exposure': ['GDPR', 'SOC2'],
                'business_criticality': 'high'
            }
        )
        
        # Print results
        s = result.summary
        print("✅ Assessment Results:")
        print(f"   🎯 Overall Risk Score: {s['overall_risk_score']:.1f}/100")
        print(f"   📊 Risk Category: {s['risk_category'].upper()}")
        print(f"   📄 Documents Found: {s['total_documents_analyzed']}")
        print(f"   🔍 Total Findings: {s['total_findings']}")
        print(f"   ⚠️  Critical Issues: {s['critical_findings']}")
        print(f"   👥 Human Review Needed: {s['requires_human_review']}")
        print(f"   📧 Follow-up Actions: {s['follow_up_actions_generated']}")
        
        if s.get('key_risk_factors'):
            print(f"\n🚨 Key Risk Factors:")
            for factor in s['key_risk_factors'][:3]:
                print(f"   • {factor}")
        
        if s.get('recommendations'):
            print(f"\n💡 Recommendations:")
            for rec in s['recommendations'][:3]:
                print(f"   • {rec}")
        
        print(f"\n🎉 Test completed successfully!")
        
        # Determine if this is a good result
        risk_score = s['overall_risk_score']
        if risk_score < 40:
            print("✅ LOW RISK - Vendor appears to have strong security posture")
        elif risk_score < 65:
            print("⚠️  MEDIUM RISK - Some areas need attention")
        elif risk_score < 80:
            print("🔴 HIGH RISK - Significant concerns identified")
        else:
            print("🚨 CRITICAL RISK - Immediate action required")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("💡 This might be because:")
        print("   • Dependencies not installed (run: pip install -r requirements.txt)")
        print("   • OpenAI API key not set in .env file")
        print("   • Network connectivity issues")


if __name__ == "__main__":
    asyncio.run(quick_test())
