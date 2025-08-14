#!/usr/bin/env python3
"""
Quick Assessment History Test
Tests basic functionality of the Assessment History tab
"""

import requests
import json
import time

BASE_URL = "http://localhost:8026"

def test_server_health():
    """Test if server is responsive"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server Health: Server is running and responsive")
            return True
        else:
            print(f"❌ Server Health: Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server Health: Server not accessible - {str(e)}")
        return False

def test_history_api():
    """Test the assessment history API endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/assessments/history", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                assessments = data.get("assessments", [])
                print(f"✅ History API: Retrieved {len(assessments)} assessments successfully")
                
                # Show sample data if available
                if assessments:
                    print("   📊 Sample assessment data:")
                    sample = assessments[0]
                    print(f"      Vendor: {sample.get('vendor_name', 'N/A')}")
                    print(f"      Domain: {sample.get('vendor_domain', 'N/A')}")
                    print(f"      Status: {sample.get('status', 'N/A')}")
                    print(f"      Risk Score: {sample.get('risk_score', 'N/A')}")
                else:
                    print("   ℹ️ No assessment history found (this is normal for new installations)")
                
                return True
            else:
                print(f"❌ History API: API returned success=false - {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ History API: HTTP {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ History API: Request failed - {str(e)}")
        return False

def test_frontend_pages():
    """Test that frontend pages contain Assessment History"""
    pages_to_test = [
        "/",
        "/static/combined-ui.html"
    ]
    
    successful_pages = 0
    
    for page in pages_to_test:
        try:
            response = requests.get(f"{BASE_URL}{page}", timeout=10)
            if response.status_code == 200:
                content = response.text
                if "Assessment History" in content:
                    print(f"✅ Frontend: {page} loads and contains Assessment History tab")
                    successful_pages += 1
                else:
                    print(f"⚠️ Frontend: {page} loads but missing Assessment History content")
            else:
                print(f"❌ Frontend: {page} returned status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Frontend: Error loading {page} - {str(e)}")
    
    return successful_pages > 0

def test_create_sample_assessment():
    """Test creating a sample assessment for history"""
    try:
        payload = {
            "vendorDomain": "github.com",
            "vendorName": "GitHub",
            "dataSensitivity": "high",
            "businessCriticality": "high",
            "regulations": ["gdpr", "soc2"]
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/assessments", 
                               json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            assessment_id = result.get("assessment_id")
            if assessment_id:
                print(f"✅ Assessment Creation: Created test assessment {assessment_id}")
                return assessment_id
            else:
                print("⚠️ Assessment Creation: No assessment ID returned")
                return None
        else:
            print(f"❌ Assessment Creation: HTTP {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Assessment Creation: Request failed - {str(e)}")
        return None

def main():
    """Run quick Assessment History tests"""
    print("🚀 Quick Assessment History Test Suite")
    print("=" * 50)
    
    # Test 1: Server Health
    print("\n1️⃣ Testing Server Health...")
    if not test_server_health():
        print("❌ Cannot continue - server not accessible")
        return
    
    # Test 2: History API
    print("\n2️⃣ Testing Assessment History API...")
    history_works = test_history_api()
    
    # Test 3: Frontend Pages
    print("\n3️⃣ Testing Frontend Pages...")
    frontend_works = test_frontend_pages()
    
    # Test 4: Create Sample Assessment
    print("\n4️⃣ Testing Assessment Creation...")
    assessment_id = test_create_sample_assessment()
    
    # Wait a moment for processing
    if assessment_id:
        print("⏳ Waiting for assessment to process...")
        time.sleep(5)
        
        # Retest history API
        print("\n5️⃣ Re-testing History API after creation...")
        history_works_after = test_history_api()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 QUICK TEST SUMMARY")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    if history_works:
        tests_passed += 1
        print("✅ Assessment History API is working")
    else:
        print("❌ Assessment History API has issues")
    
    if frontend_works:
        tests_passed += 1
        print("✅ Frontend pages contain Assessment History")
    else:
        print("❌ Frontend pages missing Assessment History")
    
    if assessment_id:
        tests_passed += 1
        total_tests += 1
        print("✅ Assessment creation is working")
    else:
        print("❌ Assessment creation has issues")
    
    print(f"\n🎯 SUCCESS RATE: {tests_passed}/{total_tests} tests passed ({(tests_passed/total_tests)*100:.1f}%)")
    
    if tests_passed == total_tests:
        print("🎉 Assessment History is working perfectly!")
    elif tests_passed >= 2:
        print("✅ Assessment History is mostly working - minor issues to address")
    else:
        print("⚠️ Assessment History needs attention - multiple issues found")
    
    print("\n📍 Next Steps:")
    print("   1. Open browser and navigate to http://localhost:8026/static/combined-ui.html")
    print("   2. Click on 'Assessment History' tab")
    print("   3. Test search and filter functionality manually")
    print("   4. Verify assessment data displays correctly")

if __name__ == "__main__":
    main()
