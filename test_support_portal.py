#!/usr/bin/env python3
"""
Test script to verify the support portal API endpoint
"""

import requests
import json

def test_support_portal_api(domain):
    """Test the support portal API for a specific domain"""
    url = "http://localhost:8028/api/v1/find-vendor-support-portal"
    
    payload = {
        "domain": domain
    }
    
    print(f"🔍 Testing support portal API for: {domain}")
    print(f"📤 Request URL: {url}")
    print(f"📤 Request payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📥 Response data: {json.dumps(result, indent=2)}")
            
            if result.get('success'):
                support_portal = result.get('support_portal')
                if support_portal and support_portal.get('url'):
                    print(f"✅ SUCCESS: Found support portal URL: {support_portal['url']}")
                else:
                    print("❌ SUCCESS but no URL found")
            else:
                print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the web server running on localhost:8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test with some common domains that should have support portals
    test_domains = [
        "github.com",
        "slack.com", 
        "microsoft.com",
        "google.com",
        "atlassian.com"
    ]
    
    print("🚀 Starting Support Portal API Tests")
    print("=" * 50)
    
    for domain in test_domains:
        test_support_portal_api(domain)
        print("-" * 50)