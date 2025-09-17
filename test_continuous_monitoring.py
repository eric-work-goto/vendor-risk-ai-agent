#!/usr/bin/env python3
"""
Test script to verify continuous monitoring integration functionality
"""
import requests
import json
import time

def test_assessment_with_monitoring():
    """Test assessment API with continuous monitoring enabled"""
    
    print("🧪 Testing Continuous Monitoring Assessment Integration...")
    
    # Test assessment with continuous monitoring enabled
    assessment_data = {
        "vendor_domain": "slack.com", 
        "requester_email": "test@example.com",
        "regulations": ["GDPR"],
        "data_sensitivity": "internal",
        "business_criticality": "medium", 
        "auto_trust_center": True,
        "enhanced_assessment": True,
        "assessment_mode": "comprehensive_assessment",
        "enable_continuous_monitoring": True
    }
    
    try:
        # Perform assessment
        print(f"📊 Performing assessment for {assessment_data['vendor_domain']} with continuous monitoring enabled...")
        response = requests.post('http://localhost:8028/api/v1/assessments', json=assessment_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Assessment successful: {result.get('message', 'No message')}")
            print(f"📈 Risk Score: {result.get('final_score', 'N/A')}")
            
            # Wait a moment then check history
            time.sleep(2)
            
            # Check assessment history 
            print("\n🔍 Checking assessment history...")
            history_response = requests.get('http://localhost:8028/api/v1/assessments/history')
            
            if history_response.status_code == 200:
                history_data = history_response.json()
                print(f"✅ History retrieved: {len(history_data.get('data', []))} assessments found")
                
                # Look for our assessment with continuous monitoring
                for assessment in history_data.get('data', []):
                    if assessment.get('vendor_domain') == 'slack.com':
                        has_monitoring = assessment.get('enable_continuous_monitoring', False)
                        print(f"📋 Found Slack assessment - Continuous Monitoring: {'✅ Enabled' if has_monitoring else '❌ Disabled'}")
                        
                        if has_monitoring:
                            print("🎯 SUCCESS: Assessment correctly stored with continuous monitoring enabled!")
                            return True
                        else:
                            print("⚠️ WARNING: Continuous monitoring flag not found in assessment data")
                            print(f"Assessment data: {json.dumps(assessment, indent=2)}")
            else:
                print(f"❌ Failed to retrieve history: {history_response.status_code}")
                print(history_response.text)
        else:
            print(f"❌ Assessment failed: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on http://localhost:8028")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

def test_enhanced_monitoring_api():
    """Test the enhanced monitoring data endpoint"""
    
    print("\n🧪 Testing Enhanced Monitoring Data Retrieval...")
    
    try:
        response = requests.get('http://localhost:8028/api/v1/assessments/history')
        
        if response.status_code == 200:
            data = response.json()
            assessments = data.get('data', [])
            
            # Filter for continuous monitoring enabled
            monitored_vendors = [a for a in assessments if a.get('enable_continuous_monitoring') == True]
            
            print(f"📊 Total assessments: {len(assessments)}")
            print(f"🔄 Vendors with continuous monitoring: {len(monitored_vendors)}")
            
            if monitored_vendors:
                print("\n📋 Vendors under continuous monitoring:")
                for vendor in monitored_vendors:
                    print(f"  • {vendor.get('vendor_domain', 'Unknown')} (Score: {vendor.get('final_score', 'N/A')})")
                return True
            else:
                print("⚠️ No vendors currently have continuous monitoring enabled")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 Starting Continuous Monitoring Integration Tests\n")
    
    # Test 1: Assessment with monitoring
    success1 = test_assessment_with_monitoring()
    
    # Test 2: Enhanced monitoring data
    success2 = test_enhanced_monitoring_api()
    
    print("\n" + "="*60)
    if success1 and success2:
        print("🎉 All tests passed! Continuous monitoring integration working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    print("="*60)