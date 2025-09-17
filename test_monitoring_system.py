"""
Test AI-Powered Continuous Monitoring
Tests the complete monitoring workflow
"""

import asyncio
import requests
import json
from datetime import datetime

def test_monitoring_endpoints():
    """Test the monitoring API endpoints"""
    base_url = "http://localhost:8028"
    
    print("🚀 Testing AI-Powered Continuous Monitoring")
    print("=" * 60)
    
    # Test data
    test_vendor = "example.com"
    test_name = "Example Corp"
    
    try:
        # Test 1: Check monitoring status
        print("\n1️⃣ Testing monitoring status endpoint...")
        response = requests.get(f"{base_url}/api/v1/monitoring/status")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Monitoring Available: {status.get('monitoring_available')}")
            print(f"📊 Active Monitors: {status.get('active_monitors')}")
        else:
            print(f"❌ Error: {response.text}")
        
        # Test 2: Enable monitoring for a vendor
        print(f"\n2️⃣ Testing enable monitoring for {test_vendor}...")
        response = requests.post(
            f"{base_url}/api/v1/monitoring/enable",
            params={
                "vendor_domain": test_vendor,
                "vendor_name": test_name,
                "assessment_id": "test-123"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result.get('message')}")
        else:
            print(f"❌ Error: {response.text}")
        
        # Test 3: Check vendor for alerts
        print(f"\n3️⃣ Testing check monitoring for {test_vendor}...")
        response = requests.get(f"{base_url}/api/v1/monitoring/check/{test_vendor}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result.get('total_alerts', 0)} alerts")
            print(f"📅 Checked at: {result.get('checked_at')}")
        else:
            print(f"❌ Error: {response.text}")
        
        # Test 4: Get all monitoring alerts
        print(f"\n4️⃣ Testing get all monitoring alerts...")
        response = requests.get(f"{base_url}/api/v1/monitoring/alerts")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result.get('total_count', 0)} total alerts")
        else:
            print(f"❌ Error: {response.text}")
        
        # Test 5: Check updated monitoring status
        print(f"\n5️⃣ Testing updated monitoring status...")
        response = requests.get(f"{base_url}/api/v1/monitoring/status")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Active Monitors: {status.get('active_monitors')}")
            monitored = status.get('monitored_vendors', [])
            if monitored:
                print(f"📋 Monitored Vendors: {', '.join(monitored)}")
        else:
            print(f"❌ Error: {response.text}")
        
        print("\n" + "=" * 60)
        print("✅ Monitoring tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Please start the web app first.")
        print("Run: cd src/api && python web_app.py")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

async def test_ai_monitoring_directly():
    """Test the AI monitoring service directly"""
    print("\n🤖 Testing AI Monitoring Service Directly")
    print("=" * 60)
    
    try:
        # Import the monitoring service
        from src.services.ai_monitoring import monitor_vendor_ai
        
        test_vendor = "microsoft.com"
        test_name = "Microsoft Corporation"
        
        print(f"\n🔍 Running AI monitoring check for {test_vendor}...")
        
        # Perform monitoring
        alerts = await monitor_vendor_ai(test_vendor, test_name)
        
        print(f"✅ AI monitoring completed!")
        print(f"📊 Found {len(alerts)} alerts")
        
        if alerts:
            print("\n🚨 ALERTS FOUND:")
            for i, alert in enumerate(alerts, 1):
                print(f"\n{i}. {alert['title']}")
                print(f"   Severity: {alert['severity']}")
                print(f"   Type: {alert['alert_type']}")
                print(f"   Confidence: {alert['confidence']}%")
                print(f"   Description: {alert['description'][:100]}...")
        else:
            print("✅ No alerts found - vendor appears secure")
        
    except ImportError as e:
        print(f"❌ Cannot import monitoring service: {e}")
    except Exception as e:
        print(f"❌ AI monitoring test failed: {str(e)}")

async def test_monitoring_scheduler():
    """Test the background monitoring scheduler"""
    print("\n⏰ Testing Monitoring Scheduler")
    print("=" * 60)
    
    try:
        from src.services.monitoring_scheduler import (
            add_vendor_to_monitoring,
            get_monitoring_status,
            get_all_monitoring_alerts
        )
        
        test_vendor = "github.com"
        test_name = "GitHub Inc"
        
        print(f"\n➕ Adding {test_vendor} to monitoring...")
        success = await add_vendor_to_monitoring(test_vendor, test_name)
        print(f"✅ Added to monitoring: {success}")
        
        print(f"\n📊 Getting monitoring status...")
        status = await get_monitoring_status()
        print(f"✅ Running: {status.get('running')}")
        print(f"📋 Monitored vendors: {status.get('monitored_vendors')}")
        
        print(f"\n📄 Getting all alerts...")
        alerts = await get_all_monitoring_alerts(limit=5)
        print(f"✅ Found {len(alerts)} stored alerts")
        
    except ImportError as e:
        print(f"❌ Cannot import scheduler: {e}")
    except Exception as e:
        print(f"❌ Scheduler test failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE MONITORING TESTS")
    print("=" * 70)
    
    # Test API endpoints (requires server running)
    test_monitoring_endpoints()
    
    # Test AI monitoring directly
    asyncio.run(test_ai_monitoring_directly())
    
    # Test monitoring scheduler
    asyncio.run(test_monitoring_scheduler())
    
    print("\n🎯 ALL TESTS COMPLETED!")
    print("\nNext Steps:")
    print("1. Start the web server: cd src/api && python web_app.py")
    print("2. Open the UI: http://localhost:8028/combined-ui")
    print("3. Run an assessment and enable continuous monitoring")
    print("4. Check the 'Monitoring & Dashboard' tab for real-time updates")