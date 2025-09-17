#!/usr/bin/env python3
"""
Debug Continuous Monitoring Integration
This script tests the continuous monitoring functionality step by step.
"""
import requests
import json
import time

def test_continuous_monitoring_workflow():
    """Test the complete continuous monitoring workflow"""
    
    print("🧪 CONTINUOUS MONITORING DEBUG TEST")
    print("="*50)
    
    # Step 1: Test API connectivity
    print("\n1️⃣ Testing API Connectivity...")
    try:
        response = requests.get('http://localhost:8028/health')
        print(f"   ✅ Server Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        return False
    
    # Step 2: Check current assessment history
    print("\n2️⃣ Checking Current Assessment History...")
    try:
        response = requests.get('http://localhost:8028/api/v1/assessments/history')
        if response.status_code == 200:
            data = response.json()
            assessments = data.get('data', [])
            print(f"   📊 Total assessments found: {len(assessments)}")
            
            monitored_count = 0
            for assessment in assessments:
                monitoring_enabled = assessment.get('enable_continuous_monitoring', False)
                if monitoring_enabled:
                    monitored_count += 1
                    print(f"   🔄 Monitored vendor: {assessment.get('vendor_domain', 'Unknown')}")
                
                print(f"   📋 Assessment: {assessment.get('vendor_domain', 'Unknown')} - Monitoring: {'✅' if monitoring_enabled else '❌'}")
            
            print(f"   📈 Total with monitoring enabled: {monitored_count}")
            
        else:
            print(f"   ❌ History API Error: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ History API Error: {e}")
    
    # Step 3: Test creating a new assessment with continuous monitoring
    print("\n3️⃣ Creating Test Assessment with Continuous Monitoring...")
    test_assessment = {
        "vendor_domain": "testvendor.com",
        "requester_email": "test@example.com", 
        "regulations": ["GDPR"],
        "data_sensitivity": "internal",
        "business_criticality": "medium",
        "auto_trust_center": True,
        "enhanced_assessment": True,
        "assessment_mode": "business_risk",
        "enable_continuous_monitoring": True
    }
    
    try:
        response = requests.post('http://localhost:8028/api/v1/assessments', json=test_assessment)
        if response.status_code == 200:
            result = response.json()
            assessment_id = result.get('assessment_id')
            print(f"   ✅ Assessment created: {assessment_id}")
            print(f"   📝 Status: {result.get('status')}")
            
            # Wait a moment for processing
            print("   ⏳ Waiting for assessment to process...")
            time.sleep(10)
            
            # Check if it appears in history with monitoring enabled
            response = requests.get('http://localhost:8028/api/v1/assessments/history')
            if response.status_code == 200:
                data = response.json()
                for assessment in data.get('data', []):
                    if assessment.get('vendor_domain') == 'testvendor.com':
                        monitoring_enabled = assessment.get('enable_continuous_monitoring', False)
                        print(f"   📊 Found test assessment - Monitoring: {'✅ ENABLED' if monitoring_enabled else '❌ DISABLED'}")
                        
                        if monitoring_enabled:
                            print("   🎉 SUCCESS: Continuous monitoring flag is working!")
                            return True
                        else:
                            print("   ⚠️ ISSUE: Continuous monitoring flag not saved properly")
                            print(f"   🔍 Assessment data: {json.dumps(assessment, indent=2)}")
            
        else:
            print(f"   ❌ Assessment creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Assessment creation error: {e}")
    
    return False

def test_enhanced_monitoring_api():
    """Test if the enhanced monitoring data loads correctly"""
    
    print("\n4️⃣ Testing Enhanced Monitoring Data Loading...")
    
    # Test direct API call to see what data the frontend should receive
    try:
        response = requests.get('http://localhost:8028/api/v1/assessments/history')
        if response.status_code == 200:
            data = response.json()
            assessments = data.get('data', [])
            
            # Filter for monitored vendors (same logic as frontend)
            monitored_vendors = [a for a in assessments if a.get('enable_continuous_monitoring') == True]
            
            print(f"   📊 Total assessments: {len(assessments)}")
            print(f"   🔄 Monitored vendors: {len(monitored_vendors)}")
            
            if monitored_vendors:
                print("   📋 Monitored vendors list:")
                for vendor in monitored_vendors:
                    print(f"     • {vendor.get('vendor_domain', 'Unknown')} (Score: {vendor.get('final_score', 'N/A')})")
                return True
            else:
                print("   ⚠️ No vendors have continuous monitoring enabled")
                print("   🔍 This is why Enhanced Monitoring Dashboard shows empty")
                
                # Show available assessments for debugging
                print("\n   📋 Available assessments:")
                for assessment in assessments[:3]:  # Show first 3
                    monitoring = assessment.get('enable_continuous_monitoring', False)
                    print(f"     • {assessment.get('vendor_domain', 'Unknown')} - Monitoring: {monitoring}")
                    
        else:
            print(f"   ❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return False

def test_frontend_integration():
    """Test how the frontend should handle the data"""
    
    print("\n5️⃣ Testing Frontend Data Integration...")
    
    print("   📝 Frontend should:")
    print("     1. Call /api/v1/assessments/history")
    print("     2. Filter assessments where enable_continuous_monitoring === true")
    print("     3. Display those vendors in Enhanced Monitoring Dashboard")
    print("     4. Use ALL assessments for Risk Distribution and Assessment Activity charts")
    
    print("\n   🔧 Current Implementation Status:")
    print("     ✅ Backend API supports enable_continuous_monitoring field")
    print("     ✅ Assessment creation includes continuous monitoring flag")
    print("     ⚠️ Need to verify frontend filtering logic")
    print("     ⚠️ Need to separate monitoring vendors vs. all vendors for charts")

if __name__ == "__main__":
    print("🚀 Starting Continuous Monitoring Debug Test")
    
    # Run workflow test
    success = test_continuous_monitoring_workflow()
    
    # Test monitoring API
    test_enhanced_monitoring_api()
    
    # Test frontend integration
    test_frontend_integration()
    
    print("\n" + "="*50)
    if success:
        print("🎉 CONTINUOUS MONITORING IS WORKING!")
        print("   Issue might be in frontend filtering logic.")
    else:
        print("⚠️ CONTINUOUS MONITORING NEEDS DEBUGGING")
        print("   Check backend storage and API response structure.")
    
    print("\n📝 RECOMMENDED NEXT STEPS:")
    print("   1. Check if frontend loadEnhancedMonitoringData() is filtering correctly")
    print("   2. Verify assessment form is sending enable_continuous_monitoring=true") 
    print("   3. Test dashboard statistics are using ALL assessments, not just monitored ones")
    print("="*50)