#!/usr/bin/env python3
"""
Test script to verify the assessment endpoint fix
"""

import requests
import json
import time
import sys

def test_assessment_endpoint():
    """Test the assessment creation and retrieval"""
    API_BASE = "http://localhost:8026"
    
    print("🔄 Testing Assessment Endpoint Fix...")
    
    try:
        # Test health first
        print("1. Testing health endpoint...")
        health_response = requests.get(f"{API_BASE}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        return False
    
    try:
        # Create a test assessment
        print("2. Creating test assessment...")
        assessment_data = {
            "vendor_domain": "test-fix.com",
            "requester_email": "test@example.com",
            "regulations": ["SOC2"],
            "data_sensitivity": "internal",
            "business_criticality": "medium",
            "auto_trust_center": False
        }
        
        create_response = requests.post(
            f"{API_BASE}/api/v1/assessments",
            json=assessment_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if create_response.status_code == 200:
            result = create_response.json()
            assessment_id = result.get("assessment_id")
            print(f"✅ Assessment created: {assessment_id}")
        else:
            print(f"❌ Assessment creation failed: {create_response.status_code}")
            print(f"   Response: {create_response.text}")
            return False
    except Exception as e:
        print(f"❌ Assessment creation error: {str(e)}")
        return False
    
    try:
        # Wait a moment for the assessment to start
        print("3. Waiting for assessment to start...")
        time.sleep(2)
        
        # Test the fixed endpoint
        print("4. Testing assessment retrieval...")
        get_response = requests.get(f"{API_BASE}/api/v1/assessments/{assessment_id}", timeout=10)
        
        if get_response.status_code == 200:
            result = get_response.json()
            print("✅ Assessment retrieval successful!")
            print(f"   Response format: {result.keys()}")
            
            if "success" in result and "assessment" in result:
                assessment = result["assessment"]
                print(f"   Assessment ID: {assessment.get('assessment_id')}")
                print(f"   Status: {assessment.get('status')}")
                print(f"   Progress: {assessment.get('progress', 0)}%")
                print(f"   Vendor: {assessment.get('vendor_domain')}")
                print("🎉 Fix is working correctly!")
                return True
            else:
                print(f"❌ Unexpected response format: {result}")
                return False
        else:
            print(f"❌ Assessment retrieval failed: {get_response.status_code}")
            print(f"   Response: {get_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Assessment retrieval error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Assessment Endpoint Fix Test")
    print("=" * 40)
    
    success = test_assessment_endpoint()
    
    if success:
        print("\n🎯 ALL TESTS PASSED! The assessment endpoint fix is working!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed. Please check the server and endpoint.")
        sys.exit(1)
