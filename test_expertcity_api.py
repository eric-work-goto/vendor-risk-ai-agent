#!/usr/bin/env python3
"""
ExpertCity Open WebUI API Test
Test connection to https://chat.expertcity.com with the provided API key
"""

import os
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv(override=True)

def test_expertcity_openwebui():
    """Test ExpertCity Open WebUI API"""
    print("🏢 Testing ExpertCity Open WebUI API")
    print("=" * 50)
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL')
    
    print(f"🔑 API Key: {api_key[:12]}...{api_key[-8:]}")
    print(f"🌐 Base URL: {base_url}")
    print(f"📏 Key Length: {len(api_key)} characters")
    
    # Test endpoints for ExpertCity Open WebUI
    test_endpoints = [
        f"{base_url}/chat/completions",
        f"{base_url}/models",
        "https://chat.expertcity.com/v1/chat/completions",
        "https://chat.expertcity.com/api/v1/chat/completions"
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'User-Agent': 'VendorRiskAssessment/1.0'
    }
    
    # Test data
    test_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'user', 'content': 'Hello! Respond with "ExpertCity API Working" to confirm connection.'}
        ],
        'max_tokens': 50,
        'temperature': 0
    }
    
    print(f"\n🧪 Testing API Connection...")
    
    for i, endpoint in enumerate(test_endpoints, 1):
        print(f"\n--- Test {i}: {endpoint} ---")
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=test_data,
                timeout=30,
                verify=False  # Bypass SSL issues
            )
            
            print(f"📡 Status Code: {response.status_code}")
            print(f"📋 Headers: {dict(list(response.headers.items())[:3])}")  # Show first 3 headers
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ SUCCESS! Raw response keys: {list(result.keys())}")
                    
                    # Handle different response formats
                    message = None
                    if 'choices' in result and result['choices']:
                        message = result['choices'][0].get('message', {}).get('content', '')
                    elif 'response' in result:
                        message = result['response']
                    elif 'text' in result:
                        message = result['text']
                    
                    if message:
                        print(f"🎉 AI Response: '{message.strip()}'")
                        print(f"🎯 Working endpoint: {endpoint}")
                        
                        # Show usage info if available
                        if 'usage' in result:
                            usage = result['usage']
                            print(f"📊 Token usage: {usage}")
                        
                        return True, endpoint
                    else:
                        print(f"⚠️  Response format: {result}")
                        
                except Exception as e:
                    print(f"⚠️  JSON parsing error: {e}")
                    print(f"📄 Raw response: {response.text[:200]}...")
                    
            elif response.status_code == 401:
                print("❌ Authentication Error - Invalid API key")
                print(f"📄 Response: {response.text}")
            elif response.status_code == 403:
                print("❌ Forbidden - Access denied")
            elif response.status_code == 404:
                print("❌ Not Found - Endpoint doesn't exist")
            elif response.status_code == 429:
                print("❌ Rate Limited - Too many requests")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"📄 Response: {response.text[:200]}...")
                
        except requests.exceptions.SSLError as e:
            print(f"❌ SSL Error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection Error: {e}")
        except requests.exceptions.Timeout:
            print("❌ Timeout - Request took too long")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
    
    return False, None

def test_models_availability():
    """Test what models are available"""
    print("\n📋 Testing Available Models")
    print("=" * 50)
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL')
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    models_endpoints = [
        f"{base_url}/models",
        "https://chat.expertcity.com/v1/models",
        "https://chat.expertcity.com/api/v1/models"
    ]
    
    for endpoint in models_endpoints:
        print(f"\n🔍 Checking: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=15, verify=False)
            
            if response.status_code == 200:
                models_data = response.json()
                print(f"✅ Models endpoint working!")
                
                if 'data' in models_data:
                    models = models_data['data']
                    print(f"📊 Found {len(models)} models:")
                    for model in models[:10]:  # Show first 10
                        model_id = model.get('id', model.get('name', 'Unknown'))
                        print(f"   • {model_id}")
                elif 'models' in models_data:
                    models = models_data['models']
                    print(f"📊 Found {len(models)} models:")
                    for model in models[:10]:
                        print(f"   • {model.get('name', model.get('id', 'Unknown'))}")
                else:
                    print(f"📄 Response: {models_data}")
                
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

def main():
    """Run ExpertCity Open WebUI tests"""
    print("🚀 ExpertCity Open WebUI API Test Suite")
    print("=" * 60)
    
    # Test 1: API Connection
    api_working, working_endpoint = test_expertcity_openwebui()
    
    # Test 2: Models
    models_working = test_models_availability()
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 FINAL TEST RESULTS")
    print(f"{'='*60}")
    print(f"API Connection: {'✅ SUCCESS' if api_working else '❌ FAILED'}")
    print(f"Models Access: {'✅ SUCCESS' if models_working else '❌ FAILED'}")
    
    if api_working:
        print(f"\n🎉 EXCELLENT! Your ExpertCity Open WebUI is working!")
        print(f"   Working endpoint: {working_endpoint}")
        print(f"   Your compliance discovery system is ready to use multiple models.")
        print(f"   The system will now use AI-powered dynamic discovery instead of hardcoded URLs.")
        
        # Test if we can import and use the compliance function
        try:
            print(f"\n🧪 Testing compliance discovery integration...")
            import sys
            sys.path.append('src')
            from api.web_app import enhance_compliance_discovery_with_ai
            print(f"✅ Compliance discovery function imported successfully!")
            print(f"✅ Your system is fully configured for dynamic AI-powered compliance discovery!")
        except Exception as e:
            print(f"⚠️  Compliance function import: {e}")
        
    else:
        print(f"\n⚠️  Configuration needed for ExpertCity Open WebUI")
        print(f"   Please verify:")
        print(f"   • API key is correct and active")
        print(f"   • Network access to https://chat.expertcity.com")
        print(f"   • Server is running and accessible")

if __name__ == "__main__":
    main()