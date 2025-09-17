#!/usr/bin/env python3
"""
Test AI Features Detection Prompt Directly
==========================================
This script tests the AI detection functionality to verify that the prompt 
"Does (vendor domain) use AI in their services or platform?" is working correctly.
"""

import asyncio
import os
import sys
import json
from datetime import datetime

# Add src/api to path so we can import from web_app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'api'))

async def test_ai_detection_direct():
    """Test AI detection using the direct OpenAI prompt"""
    
    try:
        from openai import OpenAI
        
        # Test with a known AI company
        test_cases = [
            {"domain": "anthropic.com", "name": "Anthropic", "expected": True},
            {"domain": "openai.com", "name": "OpenAI", "expected": True}, 
            {"domain": "microsoft.com", "name": "Microsoft", "expected": True},
            {"domain": "shopify.com", "name": "Shopify", "expected": False},
            {"domain": "stripe.com", "name": "Stripe", "expected": False}
        ]
        
        # Use ExpertCity corporate server configuration
        corporate_base_url = "https://chat.expertcity.com/api/v1"
        corporate_api_key = "sk-2ea30b318c514c9f874dcd2aa56aa090"
        
        client = OpenAI(base_url=corporate_base_url, api_key=corporate_api_key)
        
        print("🔍 Testing AI Detection Prompt Directly")
        print("=" * 50)
        
        for test_case in test_cases:
            vendor_domain = test_case["domain"]
            vendor_name = test_case["name"]
            expected = test_case["expected"]
            
            print(f"\n🤖 Testing: {vendor_name} ({vendor_domain})")
            print(f"Expected AI Services: {expected}")
            
            # Create the exact prompt used in the system
            prompt = f"""
Analyze the company "{vendor_name}" (website: {vendor_domain}) and determine if they offer AI functionality in their products or platform.

Please provide a JSON response with the following structure:
{{
    "offers_ai_services": boolean,
    "ai_maturity_level": "Advanced" | "Intermediate" | "Basic" | "No AI Services",
    "ai_service_categories": ["category1", "category2", ...],
    "ai_services_detail": [
        {{
            "category": "category_name",
            "services": ["service1", "service2"],
            "use_cases": ["use_case1", "use_case2"],
            "data_types": ["data_type1", "data_type2"]
        }}
    ],
    "governance_score": number_between_60_and_100,
    "confidence": "High" | "Medium" | "Low"
}}

Consider AI functionality including but not limited to:
- Machine Learning and predictive analytics
- Natural Language Processing (NLP)
- Computer Vision and image recognition
- Conversational AI and chatbots
- Automated decision making
- Intelligent automation
- Recommendation systems
- Speech recognition and processing
- Generative AI capabilities

Base your analysis on your knowledge of {vendor_name} and common AI implementations in their industry sector.
"""

            try:
                response = client.chat.completions.create(
                    model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                    messages=[
                        {"role": "system", "content": "You are an AI expert analyst specializing in identifying AI capabilities in enterprise software and services. Provide accurate, detailed assessments."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.3,
                    timeout=30
                )
                
                result_text = response.choices[0].message.content.strip()
                
                # Parse JSON response
                ai_analysis = json.loads(result_text)
                
                offers_ai = ai_analysis.get('offers_ai_services', False)
                ai_maturity = ai_analysis.get('ai_maturity_level', 'Unknown')
                categories = ai_analysis.get('ai_service_categories', [])
                confidence = ai_analysis.get('confidence', 'Unknown')
                
                print(f"✅ Result: Offers AI = {offers_ai}")
                print(f"   Maturity Level: {ai_maturity}")
                print(f"   Categories: {categories}")
                print(f"   Confidence: {confidence}")
                
                # Check if result matches expectation
                if offers_ai == expected:
                    print(f"✅ PASS - Detection matches expectation")
                else:
                    print(f"❌ FAIL - Expected {expected}, got {offers_ai}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {str(e)}")
                print(f"Raw response: {result_text}")
            except Exception as e:
                print(f"❌ OpenAI API error: {str(e)}")
        
        print(f"\n🎯 AI Detection Prompt Test Complete")
        
    except ImportError:
        print("❌ OpenAI package not available")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_ai_detection_direct())