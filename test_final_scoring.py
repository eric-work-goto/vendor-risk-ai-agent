#!/usr/bin/env python3
"""
Test script to validate the corrected security scoring system.
This tests that higher scores = better grades (security-based) instead of higher scores = worse grades (risk-based).
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'api'))

from user_friendly_scoring import convert_to_user_friendly

def test_security_scoring():
    """Test that the scoring system correctly implements security-based scoring where higher scores = better grades"""
    
    print("🧪 Testing Security-Based Scoring System")
    print("=" * 50)
    
    test_cases = [
        {"score": 100, "expected_grade": "A+", "description": "Perfect security"},
        {"score": 95, "expected_grade": "A+", "description": "Excellent security"},  
        {"score": 90, "expected_grade": "A-", "description": "Very good security"},
        {"score": 85, "expected_grade": "B+", "description": "Good security"},
        {"score": 83, "expected_grade": "B", "description": "Good security"},  # This was the user's example
        {"score": 78, "expected_grade": "B-", "description": "Decent security"},
        {"score": 70, "expected_grade": "C-", "description": "Adequate security"},
        {"score": 60, "expected_grade": "D-", "description": "Poor security"},
        {"score": 50, "expected_grade": "F", "description": "Critical security issues"},
        {"score": 27, "expected_grade": "F", "description": "Critical security issues"},  # This was the user's example
        {"score": 0, "expected_grade": "F", "description": "Critical security issues"},
    ]
    
    print("Testing user's specific examples:")
    print("-" * 30)
    
    # Test user's specific case: 83/100 should be B (good), not D (bad)
    result_83 = convert_to_user_friendly({"overall_score": 83, "vendor_name": "Test Vendor", "vendor_domain": "test.com"})
    print(f"📊 Score 83/100: Grade = {result_83['letter_grade']} ({result_83['description']})")
    print(f"   Business Recommendation: {result_83['business_recommendation']}")
    
    # Test user's specific case: 27/100 should be F (bad), not B (good)  
    result_27 = convert_to_user_friendly({"overall_score": 27, "vendor_name": "Test Vendor", "vendor_domain": "test.com"})
    print(f"📊 Score 27/100: Grade = {result_27['letter_grade']} ({result_27['description']})")
    print(f"   Business Recommendation: {result_27['business_recommendation']}")
    
    print("\nTesting full grade spectrum:")
    print("-" * 30)
    
    all_passed = True
    for test_case in test_cases:
        score = test_case["score"]
        expected_grade = test_case["expected_grade"]
        
        result = convert_to_user_friendly({
            "overall_score": score, 
            "vendor_name": "Test Vendor", 
            "vendor_domain": "test.com"
        })
        
        actual_grade = result["letter_grade"]
        passed = actual_grade == expected_grade
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"{status} Score {score:3d}/100 → Grade {actual_grade:2s} (Expected: {expected_grade:2s}) - {test_case['description']}")
        
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 SUCCESS: All tests passed! Security scoring system is working correctly.")
        print("   Higher scores (100/100) = Better grades (A+)")
        print("   Lower scores (0/100) = Worse grades (F)")
        print("   This matches user's requirement for security-based scoring!")
    else:
        print("❌ FAILURE: Some tests failed. Scoring system needs correction.")
    
    print("=" * 50)
    return all_passed

if __name__ == "__main__":
    test_security_scoring()
