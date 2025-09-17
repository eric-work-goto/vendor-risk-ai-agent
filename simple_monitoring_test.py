"""
Simple test for monitoring endpoints
"""

import requests
import time

def test_with_delay():
    print("🚀 Testing monitoring endpoints...")
    base_url = "http://localhost:8028"
    
    try:
        # Test monitoring status
        print("Testing monitoring status...")
        response = requests.get(f"{base_url}/api/v1/monitoring/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Monitoring available: {data.get('monitoring_available')}")
        else:
            print(f"❌ Status check failed: {response.status_code}")
        
        # Test enable monitoring
        print("Testing enable monitoring...")
        response = requests.post(
            f"{base_url}/api/v1/monitoring/enable",
            params={"vendor_domain": "test.com", "vendor_name": "Test Corp"}
        )
        if response.status_code == 200:
            print("✅ Monitoring enabled successfully")
        else:
            print(f"❌ Enable failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_with_delay()