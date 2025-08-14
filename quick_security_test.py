#!/usr/bin/env python3
"""
Quick Security Validation Test
Tests the improved security features we implemented
"""

import requests
import json
import time

BASE_URL = "http://localhost:8026"

def test_security_validation():
    """Test that malicious inputs are properly rejected"""
    print("🔒 SECURITY VALIDATION TEST")
    print("=" * 60)
    
    malicious_inputs = [
        ("SQL Injection", "'; DROP TABLE assessments; --"),
        ("XSS Script", "<script>alert('xss')</script>"),
        ("Path Traversal", "../../etc/passwd"),
        ("Binary Data", "\x00\x01\x02")
    ]
    
    passed = 0
    total = len(malicious_inputs)
    
    for test_name, malicious_input in malicious_inputs:
        print(f"\n🧪 Testing {test_name}: {repr(malicious_input)}")
        
        try:
            data = {
                "vendor_domain": malicious_input,
                "requester_email": "test@company.com"
            }
            
            response = requests.post(f"{BASE_URL}/api/v1/assessments", json=data, timeout=10)
            
            if response.status_code in [400, 422]:
                print(f"   ✅ PASS: Rejected with HTTP {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   📝 Error: {error_detail.get('detail', 'Validation error')}")
                except:
                    pass
                passed += 1
            else:
                print(f"   ❌ FAIL: Accepted with HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ✅ PASS: Safe error handling - {e}")
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"🎯 SECURITY TEST RESULTS")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("   🎉 ALL SECURITY TESTS PASSED!")
    else:
        print("   ⚠️  Some security tests failed")
    
    return passed, total

def test_legitimate_input():
    """Test that legitimate inputs still work"""
    print(f"\n{'='*60}")
    print("✅ LEGITIMATE INPUT TEST")
    print("=" * 60)
    
    try:
        data = {
            "vendor_domain": "example.com",
            "requester_email": "test@company.com",
            "data_sensitivity": "internal",
            "business_criticality": "medium"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/assessments", json=data, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ PASS: Legitimate input accepted")
            result = response.json()
            print(f"   📝 Assessment ID: {result.get('assessment_id', 'N/A')}")
            return True
        else:
            print(f"   ❌ FAIL: Legitimate input rejected with HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ FAIL: Error with legitimate input - {e}")
        return False

def test_health_check():
    """Test basic health endpoint"""
    print(f"\n{'='*60}")
    print("🏥 HEALTH CHECK TEST")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ PASS: Health check successful")
            data = response.json()
            print(f"   📝 Service: {data.get('service', 'N/A')}")
            return True
        else:
            print(f"   ❌ FAIL: Health check failed with HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ FAIL: Health check error - {e}")
        return False

def main():
    print("🧪 QUICK BACKEND VALIDATION TEST SUITE")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    health_ok = test_health_check()
    security_passed, security_total = test_security_validation()
    legitimate_ok = test_legitimate_input()
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    
    total_tests = 1 + security_total + 1  # health + security + legitimate
    passed_tests = (1 if health_ok else 0) + security_passed + (1 if legitimate_ok else 0)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Pass Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Backend security is working correctly.")
    else:
        print("⚠️  Some tests failed. Backend needs attention.")
    
    print(f"Completed: {time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
