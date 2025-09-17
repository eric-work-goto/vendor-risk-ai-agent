#!/usr/bin/env python3
"""
Test script to verify AI features detection is working with ExpertCity server configuration.
"""

import requests
import json
import time

def test_ai_detection():
    """Test the AI detection endpoint directly."""
    
    # Test the direct AI scan endpoint
    url = "http://localhost:8028/api/v1/ai-scan"
    
    # Test cases
    test_vendors = [
        {"domain": "anthropic.com", "expected": True, "description": "AI company - should detect AI"},
        {"domain": "openai.com", "expected": True, "description": "AI company - should detect AI"},
        {"domain": "huggingface.co", "expected": True, "description": "AI/ML platform - should detect AI"},
        {"domain": "microsoft.com", "expected": True, "description": "Uses AI in many services"},
        {"domain": "example.com", "expected": False, "description": "Generic domain - should not detect AI"}
    ]
    
    print("🧪 Testing AI Features Detection with ExpertCity Configuration")
    print("=" * 60)
    
    for test_case in test_vendors:
        domain = test_case["domain"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        print(f"\n📡 Testing: {domain}")
        print(f"Description: {description}")
        print(f"Expected AI detection: {expected}")
        
        try:
            # Make request to AI scan endpoint
            response = requests.post(
                url, 
                json={"domain": domain},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_detected = result.get("uses_ai", False)
                confidence = result.get("confidence", 0)
                
                print(f"✅ Response received")
                print(f"AI Detected: {ai_detected}")
                print(f"Confidence: {confidence}")
                print(f"Analysis: {result.get('analysis', 'No analysis provided')}")
                
                # Check if result matches expectation
                if ai_detected == expected:
                    print(f"✅ PASS: Detection matches expectation")
                else:
                    print(f"❌ FAIL: Expected {expected}, got {ai_detected}")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🔬 Test completed!")

def test_comprehensive_assessment():
    """Test AI detection within a full vendor assessment."""
    
    print("\n🔄 Testing AI detection in comprehensive assessment...")
    
    url = "http://localhost:8028/api/v1/assess"
    
    # Test with a known AI company
    test_data = {
        "vendor_domain": "anthropic.com",
        "vendor_name": "Anthropic",
        "categories": ["ai_features", "security", "privacy"]
    }
    
    try:
        print(f"📊 Running assessment for {test_data['vendor_domain']}...")
        
        response = requests.post(
            url,
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if AI features are detected
            ai_features = result.get("ai_features", {})
            
            print(f"✅ Assessment completed")
            print(f"AI Features detected: {ai_features}")
            
            if ai_features.get("uses_ai"):
                print(f"✅ SUCCESS: AI features detected in comprehensive assessment")
            else:
                print(f"❌ FAILURE: AI features not detected in comprehensive assessment")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting AI Features Detection Test")
    print("Make sure the server is running on http://localhost:8028")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Test direct AI detection endpoint
    test_ai_detection()
    
    # Test AI detection in comprehensive assessment
    test_comprehensive_assessment()
    
    print("\n✨ All tests completed!")