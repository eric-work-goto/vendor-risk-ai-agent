#!/usr/bin/env python3
"""
Full end-to-end test of Business Risk Assessment with Mixpanel to validate AI detection fix.
"""

import asyncio
import requests
import time
import json

def test_full_assessment():
    """Test the full Business Risk Assessment with Mixpanel"""
    
    print("🧪 Testing Full Business Risk Assessment for Mixpanel")
    print("=" * 60)
    
    # Assessment request payload
    payload = {
        "vendor_domain": "mixpanel.com",
        "vendor_name": "Mixpanel", 
        "requester_email": "test@example.com",
        "data_sensitivity": "medium",
        "business_criticality": "medium",
        "assessment_mode": "standard"
    }
    
    try:
        # Submit assessment
        print("1. Submitting assessment request...")
        response = requests.post(
            "http://localhost:8028/api/v1/assessments",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            assessment_id = result.get("assessment_id")
            print(f"   ✅ Assessment submitted: {assessment_id}")
            
            # Wait for completion
            print("2. Waiting for assessment completion...")
            time.sleep(15)  # Allow time for assessment
            
            # Get results
            print("3. Retrieving assessment results...")
            result_response = requests.get(
                f"http://localhost:8028/api/v1/assessments/{assessment_id}",
                timeout=30
            )
            
            if result_response.status_code == 200:
                assessment_data = result_response.json()
                ai_services = assessment_data.get('ai_services', {})
                
                print("\n🤖 AI DETECTION RESULTS:")
                print(f"   Offers AI Services: {ai_services.get('offers_ai_services', False)}")
                print(f"   AI Maturity Level: {ai_services.get('ai_maturity_level', 'Unknown')}")
                print(f"   AI Categories: {ai_services.get('ai_service_categories', [])}")
                print(f"   AI Services Detail: {len(ai_services.get('ai_services_detail', []))} services found")
                
                if ai_services.get('offers_ai_services', False):
                    print("\n✅ SUCCESS: AI services correctly detected!")
                    print("🎯 Expected behavior confirmed - Mixpanel AI features now detected")
                else:
                    print("\n❌ FAILURE: AI services still not detected")
                    print("🚨 Issue persists in full assessment workflow")
                
                return ai_services.get('offers_ai_services', False)
            else:
                print(f"   ❌ Failed to retrieve results: {result_response.status_code}")
                return False
        else:
            print(f"   ❌ Assessment submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_full_assessment()
    if success:
        print("\n🎉 AI DETECTION FIX VALIDATED!")
        print("✅ Mixpanel AI features are now correctly detected in Business Risk Assessments")
    else:
        print("\n🚨 AI DETECTION ISSUE REMAINS")
        print("❌ Further investigation needed")