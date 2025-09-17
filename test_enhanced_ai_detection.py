#!/usr/bin/env python3
"""
Quick test script for AI detection with improved keyword fallback.
"""

import requests
import json
import time

def test_ai_detection_direct():
    """Test the /api/v1/ai-scan endpoint directly with companies that should detect AI."""
    
    url = "http://localhost:8028/api/v1/ai-scan"
    
    # Test cases with enhanced keyword detection
    test_cases = [
        {"domain": "mixpanel.com", "expected": True, "description": "Analytics platform with AI features"},
        {"domain": "anthropic.com", "expected": True, "description": "Core AI company"},
        {"domain": "amplitude.com", "expected": True, "description": "Product analytics with AI"},
        {"domain": "hubspot.com", "expected": True, "description": "CRM with AI features"},
        {"domain": "datadog.com", "expected": True, "description": "Monitoring with AI/ML"},
        {"domain": "example.com", "expected": False, "description": "Generic domain - no AI expected"}
    ]
    
    print("🧪 Testing Enhanced AI Detection")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        domain = test_case["domain"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        print(f"\n🔍 Testing: {domain}")
        print(f"Description: {description}")
        print(f"Expected AI: {expected}")
        
        try:
            response = requests.post(
                url, 
                json={"domain": domain},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_detected = result.get("offers_ai_services", False)
                ai_categories = result.get("ai_service_categories", [])
                
                print(f"✅ Response received")
                print(f"AI Detected: {ai_detected}")
                print(f"Categories: {ai_categories}")
                
                if ai_detected == expected:
                    print(f"✅ PASS")
                    passed += 1
                else:
                    print(f"❌ FAIL: Expected {expected}, got {ai_detected}")
                    failed += 1
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed += 1
        
        time.sleep(0.5)  # Brief pause between tests
    
    print(f"\n" + "=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! AI detection is working correctly.")
    else:
        print(f"⚠️  {failed} tests failed. AI detection needs improvement.")

if __name__ == "__main__":
    print("🚀 Testing Enhanced AI Detection System")
    print("Make sure the server is running on http://localhost:8028")
    
    test_ai_detection_direct()