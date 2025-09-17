#!/usr/bin/env python3
"""
Test AI detection specifically for Mixpanel to debug why it's not detecting AI features correctly.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.web_app import analyze_content_with_ai, scan_ai_services

async def test_mixpanel_ai_detection():
    """Test Mixpanel AI detection to see what the system is returning"""
    
    vendor_domain = "mixpanel.com"
    vendor_name = "Mixpanel"
    
    print(f"🧪 Testing AI detection for {vendor_name} ({vendor_domain})")
    print("=" * 60)
    
    # Test the analyze_content_with_ai function directly
    print("1. Testing analyze_content_with_ai function:")
    try:
        ai_analysis = await analyze_content_with_ai(vendor_domain, vendor_name)
        print(f"   Result: {ai_analysis}")
        
        if ai_analysis:
            print(f"   Offers AI Services: {ai_analysis.get('offers_ai_services', False)}")
            print(f"   AI Maturity: {ai_analysis.get('ai_maturity_level', 'Unknown')}")
            print(f"   Confidence: {ai_analysis.get('confidence', 'Unknown')}")
            print(f"   Categories: {ai_analysis.get('ai_service_categories', [])}")
            print(f"   Services Detail: {ai_analysis.get('ai_services_detail', [])}")
        else:
            print("   ❌ No results returned from AI analysis")
    except Exception as e:
        print(f"   ❌ Error in AI analysis: {str(e)}")
    
    print("\n2. Testing scan_ai_services function (full workflow):")
    try:
        ai_services = await scan_ai_services(vendor_domain, vendor_name)
        print(f"   Result: {ai_services}")
        
        if ai_services:
            print(f"   Offers AI Services: {ai_services.get('offers_ai_services', False)}")
            print(f"   AI Maturity: {ai_services.get('ai_maturity_level', 'Unknown')}")
            print(f"   Categories: {ai_services.get('ai_service_categories', [])}")
        else:
            print("   ❌ No results returned from full scan")
    except Exception as e:
        print(f"   ❌ Error in full scan: {str(e)}")
    
    print("\n3. Manual prompt test (what should work in GPT-4 browser):")
    print("   Expected prompt: 'Does Mixpanel use AI or machine learning in their platform?'")
    print("   Expected answer: Yes - Mixpanel uses AI/ML for:")
    print("   - Predictive analytics and forecasting")
    print("   - User behavior analysis and insights")
    print("   - Automated anomaly detection")
    print("   - Intelligent segmentation")
    print("   - Recommendation systems for product optimization")
    
    print("\n🔍 Analysis complete!")

if __name__ == "__main__":
    asyncio.run(test_mixpanel_ai_detection())