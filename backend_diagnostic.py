#!/usr/bin/env python3
"""
Backend Fixes for Comprehensive Test Issues
"""

import requests
import json

BASE_URL = "http://localhost:8026"

def fix_data_validation():
    """Test the current data validation and provide recommendations"""
    print("🔧 Testing Current Data Validation Issues")
    print("-" * 50)
    
    # Test cases that should fail validation
    test_cases = [
        {
            "data": {"vendor_domain": "", "requester_email": "invalid-email"},
            "description": "Invalid email format"
        },
        {
            "data": {"vendor_domain": "test.com", "requester_email": "test@test.com", "urgency": "invalid"},
            "description": "Invalid urgency level"
        },
        {
            "data": {"vendor_domain": "'; DROP TABLE assessments; --", "requester_email": "test@test.com"},
            "description": "SQL injection attempt"
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(f"{BASE_URL}/api/v1/assessments", 
                                   json=test_case["data"], timeout=10)
            print(f"❌ {test_case['description']}: HTTP {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
            elif response.status_code == 500:
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ {test_case['description']}: Error - {str(e)}")

def check_assessment_history():
    """Check assessment history for data corruption"""
    print("\n📊 Checking Assessment History")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/assessments/history", timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if "assessments" in result:
                assessments = result["assessments"]
                print(f"✅ Found {len(assessments)} assessments")
                
                # Check for data corruption
                for i, assessment in enumerate(assessments):
                    vendor_name = assessment.get("vendor_name", "")
                    vendor_domain = assessment.get("vendor_domain", "")
                    
                    # Check for binary data or corruption
                    if any(ord(c) < 32 or ord(c) > 126 for c in str(vendor_name) if c not in '\n\r\t'):
                        print(f"⚠️  Assessment {i+1}: Corrupted vendor_name detected")
                    
                    if any(ord(c) < 32 or ord(c) > 126 for c in str(vendor_domain) if c not in '\n\r\t'):
                        print(f"⚠️  Assessment {i+1}: Corrupted vendor_domain detected")
                
            else:
                print("❌ Invalid response format - missing 'assessments' key")
                print(f"Response keys: {list(result.keys())}")
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_trust_center_timeout():
    """Test trust center request with shorter timeout"""
    print("\n🛡️ Testing Trust Center Request")
    print("-" * 50)
    
    request_data = {
        "vendor_domain": "testvendor.com",
        "requester_email": "test@company.com",
        "document_types": ["SOC2"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/trust-center/request-access", 
                               json=request_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Trust Center Request: {result.get('message', 'Success')}")
            print(f"   Access Method: {result.get('access_method', 'unknown')}")
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - this indicates a performance issue")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_bulk_assessment_debug():
    """Debug bulk assessment start issues"""
    print("\n📋 Debugging Bulk Assessment Start")
    print("-" * 50)
    
    try:
        # First check if we have uploaded vendors
        print("Checking vendor upload status...")
        
        # Try to start bulk assessments
        response = requests.post(f"{BASE_URL}/api/v1/bulk/start-assessments", timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 500:
            print("❌ Server error detected - this needs backend fixes")
        elif response.status_code == 404:
            print("ℹ️  No vendor list found - this is expected if no vendors uploaded recently")
        elif response.status_code == 200:
            result = response.json()
            print(f"✅ Bulk assessment started: {result}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Run diagnostic tests"""
    print("🔬 BACKEND DIAGNOSTIC TESTS")
    print("=" * 60)
    
    fix_data_validation()
    check_assessment_history()
    test_trust_center_timeout()
    test_bulk_assessment_debug()
    
    print("\n" + "=" * 60)
    print("📋 RECOMMENDATIONS FOR FIXES")
    print("=" * 60)
    print("1. Add Pydantic validation models for all endpoints")
    print("2. Add input sanitization for string fields")
    print("3. Add email validation using regex or email-validator library")
    print("4. Add enumeration validation for fields like 'urgency'")
    print("5. Clean up corrupted data in assessment storage")
    print("6. Add timeout handling for Trust Center requests")
    print("7. Fix bulk assessment parameter handling")
    print("8. Add comprehensive error handling and logging")

if __name__ == "__main__":
    main()
