#!/usr/bin/env python3
"""
Simple test to check monitoring status and troubleshoot the issue
"""

import requests
import json

BASE_URL = "http://localhost:8028"

def test_monitoring_status():
    """Test the monitoring status endpoint"""
    
    print("🧪 Testing Monitoring System Status")
    print("=" * 40)
    
    # Test monitoring status endpoint
    print("1. Checking monitoring system status...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/monitoring/status")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ Monitoring Available: {status.get('monitoring_available')}")
            print(f"   📊 System Health: {status.get('system_health')}")
            print(f"   🔢 Active Monitors: {status.get('active_monitors')}")
            print(f"   📋 Monitored Vendors: {status.get('monitored_vendors')}")
            
            if not status.get('monitoring_available'):
                print(f"   ❌ ISSUE: Monitoring service is not available!")
                print(f"   📝 Error: {status.get('error')}")
        else:
            print(f"   ❌ Failed to get monitoring status: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception getting monitoring status: {e}")
    
    # Test assessment history to see if monitoring flags are stored
    print("\n2. Checking assessment history for monitoring flags...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/assessments/history")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            history = response.json()
            assessments = history.get("assessments", [])
            
            print(f"   📊 Total assessments: {len(assessments)}")
            
            monitoring_enabled_count = 0
            for assessment in assessments:
                monitoring_enabled = assessment.get("enable_continuous_monitoring", False)
                domain = assessment.get("vendor_domain", assessment.get("domain", "Unknown"))
                
                if monitoring_enabled:
                    monitoring_enabled_count += 1
                    print(f"   🟢 {domain}: monitoring=TRUE")
                else:
                    print(f"   ⚪ {domain}: monitoring=FALSE")
            
            print(f"   ✅ Assessments with monitoring enabled: {monitoring_enabled_count}")
            
        else:
            print(f"   ❌ Failed to get assessment history: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception getting assessment history: {e}")
    
    # Test direct monitoring enable endpoint
    print("\n3. Testing direct monitoring enable...")
    test_domain = "example.com"
    try:
        response = requests.post(f"{BASE_URL}/api/v1/monitoring/enable", json={
            "vendor_domain": test_domain,
            "vendor_name": "Example Corp",
            "assessment_id": "test-123"
        })
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Monitoring enable result: {result}")
        else:
            print(f"   ❌ Failed to enable monitoring: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception enabling monitoring: {e}")
    
    # Check status again after enable attempt
    print("\n4. Checking monitoring status after enable attempt...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/monitoring/status")
        if response.status_code == 200:
            status = response.json()
            print(f"   🔢 Active Monitors: {status.get('active_monitors')}")
            print(f"   📋 Monitored Vendors: {status.get('monitored_vendors')}")
        else:
            print(f"   ❌ Failed to get updated status: {response.status_code}")
            
    except Exception as e:
        print(f"   💥 Exception getting updated status: {e}")

if __name__ == "__main__":
    test_monitoring_status()