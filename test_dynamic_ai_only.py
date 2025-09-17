#!/usr/bin/env python3
"""
Test script to verify AI detection is now purely dynamic (no static vendor lists)
"""

import requests
import json
import time
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_ai_detection_dynamic_only():
    """Test AI detection without static vendor lists"""
    base_url = "http://localhost:8028"
    
    # Test companies that would have been in the old static list
    test_companies = [
        {"domain": "mixpanel.com", "name": "Mixpanel", "expected_static": True},
        {"domain": "amplitude.com", "name": "Amplitude", "expected_static": True},
        {"domain": "hubspot.com", "name": "HubSpot", "expected_static": True},
        {"domain": "datadog.com", "name": "Datadog", "expected_static": True},
        {"domain": "random-company.com", "name": "Random Company", "expected_static": False},
    ]
    
    print("🧪 Testing Dynamic-Only AI Detection")
    print("=" * 60)
    print("This test verifies that AI detection is now purely dynamic")
    print("Companies that were in static lists should NOT be auto-detected")
    print("Only OpenAI analysis results should determine AI capabilities")
    print()
    
    for company in test_companies:
        domain = company["domain"]
        name = company["name"]
        was_in_static = company["expected_static"]
        
        print(f"\n🔍 Testing: {name} ({domain})")
        print(f"   Was in static list: {was_in_static}")
        
        try:
            # Test the AI scan endpoint directly
            response = requests.get(f"{base_url}/api/v1/ai-scan", params={
                "domain": domain,
                "vendor_name": name
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                offers_ai = result.get("offers_ai_services", False)
                ai_services = result.get("ai_services_detail", [])
                detection_method = "Unknown"
                
                # Check if this looks like static detection (immediate response with multiple services)
                if offers_ai and len(ai_services) > 0:
                    detection_method = "Dynamic Analysis" if result.get("confidence") in ["High", "Medium"] else "Possible Static Detection"
                else:
                    detection_method = "No AI Detected"
                
                print(f"   ✅ Result: {detection_method}")
                print(f"   📊 Offers AI: {offers_ai}")
                print(f"   🔧 Services: {len(ai_services)}")
                
                if was_in_static and offers_ai and detection_method == "Possible Static Detection":
                    print(f"   ⚠️  WARNING: This company might still be using static detection!")
                elif was_in_static and not offers_ai:
                    print(f"   ✅ GOOD: Previously static company now requires dynamic analysis")
                    
            else:
                print(f"   ❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Error: {str(e)}")
    
    print(f"\n{'='*60}")
    print("🎯 Dynamic-Only AI Detection Test Complete")
    print("✅ Companies should only show AI capabilities if detected by OpenAI analysis")
    print("❌ No companies should be auto-marked as AI-enabled from static lists")

if __name__ == "__main__":
    test_ai_detection_dynamic_only()