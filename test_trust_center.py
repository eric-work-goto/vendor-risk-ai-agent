#!/usr/bin/env python3
"""
Test Trust Center Integration
Tests the Trust Center functionality with various vendor domains
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8026"

def test_trust_center_endpoint(vendor_domain: str) -> Dict[str, Any]:
    """Test trust center functionality for a specific vendor domain"""
    
    print(f"\n🔍 Testing Trust Center for: {vendor_domain}")
    
    # Test trust center request
    request_data = {
        "vendor_domain": vendor_domain,
        "requester_email": "test@company.com",
        "document_types": ["SOC2", "Privacy Policy", "Security Documentation"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/trust-center/request-access",
            json=request_data,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message', 'No message')}")
            print(f"🔧 Access Method: {result.get('access_method', 'Unknown')}")
            print(f"⏱️  Response Time: {result.get('estimated_response_time', 'Unknown')}")
            
            if result.get('guidance'):
                print(f"💡 Guidance: {result['guidance']}")
                
            if result.get('trust_center_url'):
                print(f"🌐 Trust Center URL: {result['trust_center_url']}")
                
            return {
                "status": "success",
                "vendor": vendor_domain,
                "method": result.get('access_method'),
                "details": result
            }
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return {
                "status": "error",
                "vendor": vendor_domain,
                "error": f"HTTP {response.status_code}"
            }
            
    except Exception as e:
        print(f"💥 Exception occurred: {str(e)}")
        return {
            "status": "exception",
            "vendor": vendor_domain,
            "error": str(e)
        }

def main():
    """Test Trust Center with various vendor domains"""
    
    print("🚀 Starting Trust Center Integration Tests")
    print("=" * 60)
    
    # Test various vendor domains
    test_domains = [
        "github.com",           # Unknown vendor (should use manual method)
        "salesforce.com",       # Known vendor (should use discovered method)
        "microsoft.com",        # Unknown vendor
        "aws.amazon.com",       # Unknown vendor
        "google.com",           # Unknown vendor
        "slack.com",            # Known vendor
        "random-vendor.io",     # Unknown vendor
        "example-saas.com"      # Unknown vendor
    ]
    
    results = []
    
    for domain in test_domains:
        result = test_trust_center_endpoint(domain)
        results.append(result)
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    success_count = 0
    for result in results:
        vendor = result['vendor']
        status = result['status']
        method = result.get('method', 'N/A')
        
        if status == "success":
            print(f"✅ {vendor:20} | {method:15} | SUCCESS")
            success_count += 1
        else:
            error = result.get('error', 'Unknown error')
            print(f"❌ {vendor:20} | {method:15} | {error}")
    
    print(f"\n🎯 Results: {success_count}/{len(results)} tests passed")
    
    if success_count == len(results):
        print("🎉 ALL TRUST CENTER TESTS PASSED!")
        print("✨ Trust Center can handle any vendor domain gracefully")
    else:
        print(f"⚠️  {len(results) - success_count} tests failed")
        print("🔧 Trust Center needs additional fixes")

if __name__ == "__main__":
    main()
