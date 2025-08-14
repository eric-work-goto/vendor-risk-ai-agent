#!/usr/bin/env python3
"""
Comprehensive test script for the Vendor Risk Assessment Combined UI
"""

import requests
import json
import time
import sys

API_BASE = "http://localhost:8026"

def test_api_endpoint(endpoint, method="GET", data=None, description=""):
    """Test an API endpoint and return results"""
    try:
        url = f"{API_BASE}{endpoint}"
        print(f"🔄 Testing {description or endpoint}...")
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        if response.status_code == 200:
            print(f"✅ {description or endpoint} - SUCCESS")
            return True, response.json()
        else:
            print(f"❌ {description or endpoint} - FAILED (HTTP {response.status_code})")
            print(f"   Response: {response.text}")
            return False, response.text
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {description or endpoint} - CONNECTION FAILED")
        return False, "Connection failed"
    except Exception as e:
        print(f"❌ {description or endpoint} - ERROR: {str(e)}")
        return False, str(e)

def test_health_check():
    """Test the health check endpoint"""
    return test_api_endpoint("/health", description="Health Check")

def test_dashboard():
    """Test the dashboard API"""
    return test_api_endpoint("/api/v1/dashboard", description="Dashboard API")

def test_assessment_history():
    """Test the assessment history API"""
    return test_api_endpoint("/api/v1/assessments/history", description="Assessment History")

def test_create_assessment():
    """Test creating a new assessment"""
    test_data = {
        "vendor_domain": "test-vendor.com",
        "requester_email": "test@example.com",
        "regulations": ["SOC2", "GDPR"],
        "data_sensitivity": "confidential",
        "business_criticality": "high",
        "auto_trust_center": True
    }
    
    success, result = test_api_endpoint(
        "/api/v1/assessments", 
        method="POST", 
        data=test_data,
        description="Create Assessment"
    )
    
    if success and isinstance(result, dict) and "assessment_id" in result:
        assessment_id = result["assessment_id"]
        print(f"   📝 Assessment ID: {assessment_id}")
        
        # Test retrieving the assessment
        print(f"🔄 Testing assessment retrieval...")
        time.sleep(2)  # Wait a moment for processing
        
        get_success, get_result = test_api_endpoint(
            f"/api/v1/assessments/{assessment_id}",
            description="Get Assessment Status"
        )
        
        if get_success:
            print(f"   📊 Assessment Status: {get_result.get('assessment', {}).get('status', 'unknown')}")
            print(f"   📈 Progress: {get_result.get('assessment', {}).get('progress', 0)}%")
        
        return True, assessment_id
    
    return success, result

def test_bulk_template():
    """Test bulk template download"""
    try:
        print(f"🔄 Testing bulk template download...")
        response = requests.get(f"{API_BASE}/api/v1/bulk/sample-template")
        
        if response.status_code == 200 and "vendor_domain" in response.text:
            print(f"✅ Bulk Template Download - SUCCESS")
            print(f"   📄 Template size: {len(response.text)} bytes")
            return True, response.text
        else:
            print(f"❌ Bulk Template Download - FAILED (HTTP {response.status_code})")
            return False, response.text
            
    except Exception as e:
        print(f"❌ Bulk Template Download - ERROR: {str(e)}")
        return False, str(e)

def test_trust_center():
    """Test trust center functionality"""
    test_data = {
        "vendor_domain": "trust-test.com",
        "requester_email": "test@example.com",
        "document_types": ["SOC2", "ISO27001"]
    }
    
    return test_api_endpoint(
        "/api/v1/trust-center/request-access",
        method="POST",
        data=test_data,
        description="Trust Center Request"
    )

def run_comprehensive_tests():
    """Run all tests"""
    print("🚀 Starting Comprehensive Test Suite for Combined UI")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Dashboard API", test_dashboard),
        ("Assessment History", test_assessment_history),
        ("Bulk Template", test_bulk_template),
        ("Create Assessment", test_create_assessment),
        ("Trust Center", test_trust_center),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 40)
        
        try:
            success, result = test_func()
            results.append((test_name, success, result))
            
            if success:
                passed += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ {test_name} - EXCEPTION: {str(e)}")
            results.append((test_name, False, str(e)))
            failed += 1
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, success, result in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    print(f"🎭 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if passed == len(tests):
        print("\n🎉 ALL TESTS PASSED! The combined UI is working perfectly!")
    elif passed >= len(tests) * 0.8:
        print("\n⚠️  Most tests passed. Minor issues detected.")
    else:
        print("\n🚨 Several tests failed. Please check the system.")
    
    return passed, failed

if __name__ == "__main__":
    print("Combined UI Test Suite")
    print("Connecting to:", API_BASE)
    print()
    
    # Quick connectivity test
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        print(f"✅ Server is reachable (HTTP {response.status_code})")
    except:
        print(f"❌ Cannot connect to {API_BASE}")
        print("Please ensure the server is running on port 8005")
        sys.exit(1)
    
    print()
    passed, failed = run_comprehensive_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)
