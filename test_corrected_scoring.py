#!/usr/bin/env python3
"""Quick test of the corrected scoring system"""

import sys
import os
sys.path.insert(0, '.')

try:
    from user_friendly_scoring import convert_to_user_friendly, grading_system
    
    print("🧪 TESTING CORRECTED SCORING SYSTEM")
    print("=" * 50)
    print("Logic: Lower risk scores = Better letter grades")
    print()
    
    # Test individual scoring thresholds
    test_scores = [5, 15, 25, 35, 45, 55, 65, 75, 85]
    
    print("📊 Individual Score Tests:")
    for score in test_scores:
        grade, desc, emoji, explanation = grading_system.calculate_letter_grade(score)
        print(f"  Risk Score {score:2d}/100 → Grade: {grade:2s} ({desc})")
    
    print("\n🎯 Complete Assessment Test:")
    
    # Test the example case: 27/100 should be a good grade (low risk)
    test_data = {
        'vendor_name': 'Test Vendor',
        'overall_score': 27,  # Should be a good grade (low risk)
        'scores': {
            'compliance': 30,     # Should be D+ (higher risk)
            'security': 15,       # Should be B+ (lower risk) 
            'data_protection': 80  # Should be F (very high risk)
        }
    }
    
    result = convert_to_user_friendly(test_data)
    
    print(f"Overall: {result.get('letter_grades', {}).get('overall', 'N/A')} (Risk: {result.get('overall_score', 'N/A')}/100)")
    
    for category in ['compliance', 'security', 'data_protection']:
        grade = result.get('letter_grades', {}).get(category, 'N/A')
        score = result.get('scores', {}).get(category, 'N/A')
        print(f"{category.title()}: {grade} (Risk: {score}/100)")
    
    print(f"\n💼 Business Recommendation: {result.get('business_recommendation', 'N/A')}")
    print(f"📋 Risk Description: {result.get('risk_description', 'N/A')}")
    
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
