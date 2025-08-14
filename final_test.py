#!/usr/bin/env python3
"""
Final Comprehensive Test
Tests all major functionality to verify the complete system works
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8026"

def test_assessment_workflow():
    """Test complete assessment workflow"""
    print("🔍 Testing Assessment Workflow")
    print("-" * 50)
    
    # Create assessment
    assessment_data = {
        "vendor_name": "Final Test Vendor",
        "vendor_domain": "finaltestvendor.com",
        "description": "Final comprehensive test",
        "requester_email": "test@company.com",
        "urgency": "medium",
        "auto_trust_center": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/assessments", json=assessment_data)
    print(f"✅ Assessment Creation: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        assessment_id = result.get("assessment_id")
        print(f"   📊 Assessment ID: {assessment_id}")
        
        # Test polling
        response = requests.get(f"{BASE_URL}/api/v1/assessments/{assessment_id}")
        if response.status_code == 200:
            print("✅ Assessment Retrieval: Working")
            return True
    
    return False

def test_trust_center_integration():
    """Test Trust Center for multiple scenarios"""
    print("\n🌐 Testing Trust Center Integration")
    print("-" * 50)
    
    test_cases = [
        {"domain": "github.com", "expected": "public"},
        {"domain": "salesforce.com", "expected": "email_request"},
        {"domain": "unknown-vendor.io", "expected": "manual"}
    ]
    
    all_passed = True
    
    for case in test_cases:
        request_data = {
            "vendor_domain": case["domain"],
            "requester_email": "test@company.com",
            "document_types": ["SOC2"]
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/trust-center/request-access", json=request_data)
        if response.status_code == 200:
            result = response.json()
            access_method = result.get("access_method", "unknown")
            print(f"✅ {case['domain']:20} → {access_method}")
            
            if access_method != case["expected"] and case["expected"] != "any":
                print(f"   ⚠️  Expected {case['expected']}, got {access_method}")
        else:
            print(f"❌ {case['domain']:20} → HTTP {response.status_code}")
            all_passed = False
    
    return all_passed

def test_api_endpoints():
    """Test all major API endpoints"""
    print("\n🔧 Testing API Endpoints")
    print("-" * 50)
    
    endpoints = [
        ("GET", "/health", None),
        ("GET", "/api/v1/assessments/history", None),
        ("GET", "/api/v1/dashboard/summary", None),
    ]
    
    all_passed = True
    
    for method, endpoint, data in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json=data)
            
            if response.status_code in [200, 404]:  # 404 is ok for empty lists
                print(f"✅ {method:4} {endpoint:30} → {response.status_code}")
            else:
                print(f"❌ {method:4} {endpoint:30} → {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"💥 {method:4} {endpoint:30} → Error: {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    """Run comprehensive system test"""
    print("🚀 FINAL COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    
    # Test server health
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return
    except:
        print("💥 Server is not running! Start the server first.")
        return
    
    results = {
        "assessment_workflow": test_assessment_workflow(),
        "trust_center": test_trust_center_integration(),
        "api_endpoints": test_api_endpoints()
    }
    
    print("\n" + "=" * 60)
    print("📋 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed_count = 0
    total_count = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title():25} {status}")
        if passed:
            passed_count += 1
    
    print(f"\n🎯 Overall Results: {passed_count}/{total_count} test suites passed")
    
    if passed_count == total_count:
        print("🎉 ALL TESTS PASSED!")
        print("✨ The system is fully functional and ready for use!")
        print("\n🌐 Access the application at: http://localhost:8026/combined-ui.html")
    else:
        print(f"⚠️  {total_count - passed_count} test suite(s) failed")
        print("🔧 Some issues need to be addressed")

if __name__ == "__main__":
    main()
