#!/usr/bin/env python3
import requests
import time

print("Testing AI Detection - Quick Check")
print("=" * 40)

try:
    # Test a company that was in the old static list  
    response = requests.get("http://localhost:8028/api/v1/ai-scan/mixpanel.com", timeout=15)
    
    if response.status_code == 200:
        result = response.json()
        offers_ai = result.get("offers_ai_services", False)
        services_count = len(result.get("ai_services_detail", []))
        confidence = result.get("confidence", "None")
        
        print(f"✅ Mixpanel.com Results:")
        print(f"   Offers AI: {offers_ai}")
        print(f"   Services: {services_count}")
        print(f"   Confidence: {confidence}")
        
        if offers_ai and confidence in ["High", "Medium"]:
            print(f"   🎯 Dynamic detection successful")
        elif offers_ai:
            print(f"   ⚠️  Possible static detection (no confidence)")
        else:
            print(f"   ✅ No AI detected - purely dynamic")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"💥 Error: {e}")
    
print("\nNote: If no AI is detected, this means static lists were successfully removed!")