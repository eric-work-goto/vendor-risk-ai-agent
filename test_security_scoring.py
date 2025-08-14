#!/usr/bin/env python3
"""Test the corrected security scoring system"""

import sys
sys.path.insert(0, '.')

from user_friendly_scoring import convert_to_user_friendly, grading_system

print("🧪 TESTING CORRECTED SECURITY SCORING SYSTEM")
print("=" * 55)
print("Logic: Higher security scores = Better letter grades")
print()

# Test specific examples from user request
test_cases = [
    {"score": 100, "expected": "A+", "description": "Perfect security"},
    {"score": 83, "expected": "B", "description": "Good security (user example)"},
    {"score": 27, "expected": "F", "description": "Poor security (user example)"},
    {"score": 0, "expected": "F", "description": "Worst security"},
]

print("📊 Individual Score Tests:")
for case in test_cases:
    grade, desc, emoji, explanation = grading_system.calculate_letter_grade(case["score"])
    status = "✅" if grade == case["expected"] else "❌"
    print(f"  {case['score']:3d}/100 → {grade:2s} {status} ({case['description']})")

print("\n🎯 Complete Assessment Test:")

# Test realistic security assessment data
test_data = {
    'vendor_name': 'Test Vendor',
    'overall_score': 83,  # Should be B grade (good security)
    'scores': {
        'compliance': 85,     # Should be B (good)
        'security': 83,       # Should be B (good) 
        'data_protection': 27  # Should be F (poor)
    }
}

result = convert_to_user_friendly(test_data)

print(f"Overall: {result.get('letter_grades', {}).get('overall', 'N/A')} (Score: {result.get('overall_score', 'N/A')}/100)")

for category in ['compliance', 'security', 'data_protection']:
    grade = result.get('letter_grades', {}).get(category, 'N/A')
    score = result.get('scores', {}).get(category, 'N/A')
    print(f"{category.title()}: {grade} (Score: {score}/100)")

print(f"\n💼 Business Recommendation: {result.get('business_recommendation', 'N/A')}")
print(f"📋 Risk Description: {result.get('risk_description', 'N/A')}")

print("\n✅ Testing completed!")
print("\nExpected Results:")
print("- 100/100 = A+ (Perfect)")  
print("- 83/100 = B (Good)")
print("- 27/100 = F (Poor)")
print("- 0/100 = F (Worst)")
