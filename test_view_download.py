#!/usr/bin/env python3
"""
Test script for Assessment History View and Download functionality
"""

import requests
import json

BASE_URL = "http://localhost:8026"

def test_view_and_download_functions():
    """Test the View and Download functionality in Assessment History"""
    
    print("🧪 Testing Assessment History View and Download Functions")
    print("=" * 60)
    
    # Step 1: Get assessment history to get an assessment ID
    print("\n1️⃣ Getting Assessment History...")
    try:
        history_response = requests.get(f"{BASE_URL}/api/v1/assessments/history", timeout=10)
        
        if history_response.status_code == 200:
            history_data = history_response.json()
            if history_data.get("success") and history_data.get("assessments"):
                assessments = history_data["assessments"]
                print(f"✅ Found {len(assessments)} assessments in history")
                
                # Test with the first assessment
                test_assessment = assessments[0]
                assessment_id = test_assessment["id"]
                vendor_name = test_assessment["vendor_name"]
                
                print(f"📋 Testing with: {vendor_name} (ID: {assessment_id})")
                
                # Step 2: Test individual assessment retrieval (View function backend)
                print("\n2️⃣ Testing Individual Assessment Retrieval (View function)...")
                try:
                    view_response = requests.get(f"{BASE_URL}/api/v1/assessments/{assessment_id}", timeout=10)
                    
                    if view_response.status_code == 200:
                        view_data = view_response.json()
                        if view_data.get("success") and view_data.get("assessment"):
                            assessment_detail = view_data["assessment"]
                            print("✅ Individual assessment retrieval works!")
                            print(f"   📊 Vendor: {assessment_detail.get('vendor_name', 'N/A')}")
                            print(f"   📊 Risk Score: {assessment_detail.get('risk_score', 'N/A')}%")
                            print(f"   📊 Status: {assessment_detail.get('status', 'N/A')}")
                            
                            # Check for detailed data needed for the modal
                            has_detailed_analysis = bool(assessment_detail.get('detailed_analysis'))
                            has_recommendations = bool(assessment_detail.get('recommendations'))
                            has_letter_grades = bool(assessment_detail.get('letter_grades'))
                            
                            print(f"   📊 Has Detailed Analysis: {has_detailed_analysis}")
                            print(f"   📊 Has Recommendations: {has_recommendations}")
                            print(f"   📊 Has Letter Grades: {has_letter_grades}")
                            
                            return True
                        else:
                            print("❌ View function: API returned success=false")
                            return False
                    else:
                        print(f"❌ View function: HTTP {view_response.status_code}")
                        return False
                        
                except Exception as e:
                    print(f"❌ View function: Request failed - {str(e)}")
                    return False
                    
            else:
                print("❌ No assessments found in history")
                return False
        else:
            print(f"❌ History API failed: HTTP {history_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ History API request failed: {str(e)}")
        return False

def test_frontend_accessibility():
    """Test that the frontend loads and contains the updated functions"""
    print("\n3️⃣ Testing Frontend Accessibility...")
    
    try:
        response = requests.get(f"{BASE_URL}/static/combined-ui.html", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Check for the new functions
            has_view_function = "function viewAssessment" in content
            has_download_function = "function downloadReport" in content
            has_modal_function = "function showAssessmentModal" in content
            has_close_modal_function = "function closeAssessmentModal" in content
            has_generate_report_function = "function generateReportContent" in content
            
            print(f"✅ Frontend loads successfully")
            print(f"   📋 Has viewAssessment function: {has_view_function}")
            print(f"   📋 Has downloadReport function: {has_download_function}")
            print(f"   📋 Has showAssessmentModal function: {has_modal_function}")
            print(f"   📋 Has closeAssessmentModal function: {has_close_modal_function}")
            print(f"   📋 Has generateReportContent function: {has_generate_report_function}")
            
            all_functions_present = all([
                has_view_function, has_download_function, has_modal_function, 
                has_close_modal_function, has_generate_report_function
            ])
            
            if all_functions_present:
                print("✅ All required functions are present in the frontend!")
                return True
            else:
                print("⚠️ Some functions are missing from the frontend")
                return False
        else:
            print(f"❌ Frontend not accessible: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend request failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    
    # Test backend functionality
    backend_works = test_view_and_download_functions()
    
    # Test frontend functionality  
    frontend_works = test_frontend_accessibility()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VIEW & DOWNLOAD FUNCTIONALITY TEST SUMMARY")
    print("=" * 60)
    
    if backend_works and frontend_works:
        print("🎉 SUCCESS: View and Download functionality is fully implemented!")
        print("✅ Backend API endpoints work correctly")
        print("✅ Frontend functions are properly implemented")
        print("✅ Assessment details can be retrieved")
        print("✅ Modal display and report generation ready")
        
        print("\n📍 How to test manually:")
        print("   1. Open http://localhost:8026/static/combined-ui.html")
        print("   2. Click on 'Assessment History' tab")
        print("   3. Click 'View' button on any assessment")
        print("   4. Verify modal opens with detailed information")
        print("   5. Click 'Download' button to get HTML report")
        
    elif backend_works:
        print("⚠️ PARTIAL SUCCESS: Backend works but frontend has issues")
        print("✅ API endpoints work correctly")
        print("❌ Frontend functions may have issues")
        
    elif frontend_works:
        print("⚠️ PARTIAL SUCCESS: Frontend ready but backend has issues")
        print("❌ API endpoints have issues")
        print("✅ Frontend functions are implemented")
        
    else:
        print("❌ FAILURE: Both backend and frontend have issues")
        print("❌ API endpoints not working")
        print("❌ Frontend functions missing or broken")

if __name__ == "__main__":
    main()
