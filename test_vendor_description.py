#!/usr/bin/env python3
"""
Test script to verify the vendor description API endpoint
"""
import requests
import json
import time

def test_vendor_description_api():
    """Test the vendor description API endpoint"""
    
    # Wait for server to be ready
    print("🚀 Testing vendor description API endpoint...")
    
    # Test endpoint
    url = "http://localhost:8026/api/v1/generate-vendor-description"
    
    # Test with a known domain
    test_data = {
        "domain": "microsoft.com"
    }
    
    try:
        print(f"📡 Making request to: {url}")
        print(f"📋 Request data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            url, 
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response received!")
            print(f"📋 Response data:")
            print(json.dumps(result, indent=2))
            
            # Check if the response has the expected structure
            if result.get("success"):
                print("\n🎉 SUCCESS: Vendor description API is working correctly!")
                print(f"🏢 Company: {result.get('company_name', 'N/A')}")
                print(f"📝 Description: {result.get('description', 'N/A')[:100]}...")
                return True
            else:
                print(f"\n❌ API returned error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    success = test_vendor_description_api()
    
    if success:
        print("\n🎯 Test completed successfully!")
    else:
        print("\n💥 Test failed - check the server logs for more details")