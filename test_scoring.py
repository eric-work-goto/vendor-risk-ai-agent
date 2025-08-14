#!/usr/bin/env python3
"""
Test script for user-friendly scoring system
"""

import sys
import os
sys.path.append('.')

from user_friendly_scoring import convert_to_user_friendly

def test_scoring():
    """Test the user-friendly scoring conversion"""
    
    print("🧪 Testing User-Friendly Scoring System")
    print("=" * 50)
    
    # Test data mimicking assessment results
    test_data = {
        'vendor_name': 'Test Vendor Inc.',
        'vendor_domain': 'testvendor.com',
        'overall_score': 75,
        'risk_level': 'medium',
        'scores': {
            'compliance': 80,
            'security': 70,
            'data_protection': 75
        },
        'findings': [],
        'recommendations': []
    }
    
    try:
        result = convert_to_user_friendly(test_data)
        
        print(f"✅ Conversion successful!")
        print(f"📊 Letter Grades: {result.get('letter_grades', {})}")
        print(f"📋 Risk Description: {result.get('risk_description', 'N/A')}")
        print(f"💼 Business Recommendation: {result.get('business_recommendation', 'N/A')}")
        
        # Check the structure
        if 'letter_grades' in result:
            grades = result['letter_grades']
            print(f"\n🎯 Individual Grades:")
            print(f"   Overall: {grades.get('overall', 'N/A')}")
            print(f"   Compliance: {grades.get('compliance', 'N/A')}")
            print(f"   Security: {grades.get('security', 'N/A')}")
            print(f"   Data Protection: {grades.get('data_protection', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in scoring conversion: {e}")
        return False

if __name__ == "__main__":
    success = test_scoring()
    if success:
        print("\n🎉 User-friendly scoring system is working correctly!")
    else:
        print("\n💥 User-friendly scoring system has issues!")
