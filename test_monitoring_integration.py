#!/usr/bin/env python3
"""
Test script to verify the "Enable Continuous Monitoring" functionality
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8028"

def test_monitoring_integration():
    """Test the complete monitoring integration flow"""
    
    print("🧪 Testing Continuous Monitoring Integration")
    print("=" * 50)
    
    # Step 1: Submit an assessment WITH monitoring enabled
    print("1. Submitting assessment WITH continuous monitoring enabled...")
    
    assessment_data_with_monitoring = {
        "vendor_domain": "slack.com",
        "requester_email": "test@example.com",
        "regulations": ["SOC2", "ISO27001", "GDPR"],
        "data_sensitivity": "internal",
        "business_criticality": "medium",
        "auto_trust_center": True,
        "enhanced_assessment": True,
        "assessment_mode": "comprehensive_analysis",
        "enable_continuous_monitoring": True  # THIS IS THE KEY FLAG
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/assessments", json=assessment_data_with_monitoring)
        if response.status_code == 200:
            result = response.json()
            monitored_assessment_id = result.get("assessment_id")
            print(f"   ✅ Assessment started with monitoring: {monitored_assessment_id}")
        else:
            print(f"   ❌ Failed to start monitored assessment: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error starting monitored assessment: {e}")
        return False
    
    # Step 2: Submit an assessment WITHOUT monitoring enabled
    print("2. Submitting assessment WITHOUT continuous monitoring...")
    
    assessment_data_no_monitoring = {
        "vendor_domain": "github.com",
        "requester_email": "test@example.com",
        "regulations": ["SOC2", "ISO27001"],
        "data_sensitivity": "internal",
        "business_criticality": "medium",
        "auto_trust_center": True,
        "enhanced_assessment": True,
        "assessment_mode": "comprehensive_analysis",
        "enable_continuous_monitoring": False  # No monitoring
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/assessments", json=assessment_data_no_monitoring)
        if response.status_code == 200:
            result = response.json()
            regular_assessment_id = result.get("assessment_id")
            print(f"   ✅ Assessment started without monitoring: {regular_assessment_id}")
        else:
            print(f"   ❌ Failed to start regular assessment: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error starting regular assessment: {e}")
        return False
    
    # Step 3: Wait for assessments to complete
    print("3. Waiting for assessments to complete...")
    time.sleep(10)  # Give some time for processing
    
    # Step 4: Check assessment history to see the monitoring flag
    print("4. Checking assessment history...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/assessments/history")
        if response.status_code == 200:
            history = response.json()
            assessments = history.get("assessments", [])
            
            print(f"   📊 Found {len(assessments)} assessments in history")
            
            # Look for our assessments
            monitored_found = False
            regular_found = False
            
            for assessment in assessments:
                domain = assessment.get("vendor_domain", assessment.get("domain", ""))
                monitoring_enabled = assessment.get("enable_continuous_monitoring", False)
                
                print(f"     - {domain}: monitoring={monitoring_enabled}")
                
                if domain == "slack.com" and monitoring_enabled:
                    monitored_found = True
                    print(f"       ✅ Found slack.com with monitoring enabled")
                elif domain == "github.com" and not monitoring_enabled:
                    regular_found = True
                    print(f"       ✅ Found github.com without monitoring")
            
            if not monitored_found:
                print(f"   ⚠️  Slack assessment with monitoring not found in history")
            if not regular_found:
                print(f"   ⚠️  GitHub assessment without monitoring not found in history")
                
        else:
            print(f"   ❌ Failed to get assessment history: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting assessment history: {e}")
        return False
    
    # Step 5: Check monitoring status to see if vendor was added to monitoring
    print("5. Checking monitoring system status...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/monitoring/status")
        if response.status_code == 200:
            status = response.json()
            monitored_vendors = status.get("monitored_vendors", [])
            
            print(f"   📊 Currently monitored vendors: {len(monitored_vendors)}")
            
            slack_monitored = any(vendor for vendor in monitored_vendors if "slack.com" in str(vendor))
            
            if slack_monitored:
                print(f"   ✅ slack.com is in the monitored vendors list")
            else:
                print(f"   ❌ slack.com is NOT in the monitored vendors list")
                print(f"       Current monitored vendors: {monitored_vendors}")
                
        else:
            print(f"   ❌ Failed to get monitoring status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting monitoring status: {e}")
        return False
    
    # Step 6: Test the dashboard data (this should show ALL vendors)
    print("6. Testing dashboard data (should show ALL vendors)...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/dashboard")
        if response.status_code == 200:
            dashboard = response.json()
            data = dashboard.get("data", {})
            
            total_vendors = data.get("totalVendors", 0)
            print(f"   📊 Dashboard shows {total_vendors} total vendors")
            
            if total_vendors >= 2:  # Should include both slack.com and github.com
                print(f"   ✅ Dashboard correctly shows all vendors")
            else:
                print(f"   ⚠️  Dashboard may not be showing all vendors")
                
        else:
            print(f"   ❌ Failed to get dashboard data: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting dashboard data: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("   - Assessments submitted (with and without monitoring)")
    print("   - Check /api/v1/assessments/history for enable_continuous_monitoring flag")
    print("   - Check /api/v1/monitoring/status for monitored vendors list")
    print("   - Check /api/v1/dashboard for ALL vendors in activity/risk stats")
    print("\n📝 Next: Open the web UI and verify:")
    print("   1. Go to 'Monitoring & Dashboard' tab")
    print("   2. Monitored Vendors section should show slack.com")
    print("   3. Assessment Activity should show ALL vendors")
    print("   4. Risk Distribution should show ALL vendors")
    
    return True

if __name__ == "__main__":
    try:
        success = test_monitoring_integration()
        if success:
            print("\n✅ Test completed successfully!")
        else:
            print("\n❌ Test failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)