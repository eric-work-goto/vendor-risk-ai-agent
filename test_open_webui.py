#!/usr/bin/env python3
"""
Open WebUI API Test
Test API key for Open WebUI which provides access to multiple models
"""

import os
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

def test_open_webui_api():
    """Test Open WebUI API connection"""
    print("🌐 Testing Open WebUI API")
    print("=" * 40)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return False
    
    print(f"🔑 API Key: {api_key[:12]}...{api_key[-8:]}")
    print(f"📏 Length: {len(api_key)} characters")
    
    # Check if we have a base URL configured for Open WebUI
    base_url = os.getenv('OPENAI_BASE_URL', 'http://localhost:11434')  # Default Ollama/Open WebUI port
    print(f"🌐 Base URL: {base_url}")
    
    # Test different possible endpoints
    test_endpoints = [
        f"{base_url}/v1/chat/completions",  # OpenAI-compatible endpoint
        f"{base_url}/api/chat",             # Open WebUI direct endpoint
        f"{base_url}/v1/models",            # Models endpoint
        "https://api.openai.com/v1/chat/completions"  # Fallback to OpenAI direct
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    test_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Test message - respond with OK'}],
        'max_tokens': 10
    }
    
    for i, endpoint in enumerate(test_endpoints, 1):
        print(f"\n🧪 Test {i}: {endpoint}")
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=test_data,
                timeout=30,
                verify=False  # Bypass SSL for corporate/local networks
            )
            
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'choices' in result and result['choices']:
                        message = result['choices'][0]['message']['content']
                        print(f"✅ SUCCESS! Response: '{message}'")
                        print(f"🎯 Working endpoint: {endpoint}")
                        return True, endpoint
                    elif 'response' in result:  # Some APIs return different format
                        message = result['response']
                        print(f"✅ SUCCESS! Response: '{message}'")
                        print(f"🎯 Working endpoint: {endpoint}")
                        return True, endpoint
                    else:
                        print(f"⚠️  Unexpected response format: {result}")
                except Exception as e:
                    print(f"⚠️  Response parsing error: {e}")
                    
            elif response.status_code == 401:
                print("❌ Authentication failed")
            elif response.status_code == 404:
                print("❌ Endpoint not found")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - server may not be running")
        except Exception as e:
            print(f"❌ Request error: {e}")
    
    return False, None

def test_models_endpoint():
    """Test available models"""
    print("\n📋 Testing Available Models")
    print("=" * 40)
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL', 'http://localhost:11434')
    
    headers = {'Authorization': f'Bearer {api_key}'}
    
    model_endpoints = [
        f"{base_url}/v1/models",
        f"{base_url}/api/tags",
        "https://api.openai.com/v1/models"
    ]
    
    for endpoint in model_endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10, verify=False)
            if response.status_code == 200:
                models = response.json()
                print(f"✅ Models from {endpoint}:")
                
                if 'data' in models:  # OpenAI format
                    for model in models['data'][:5]:  # Show first 5
                        print(f"   • {model.get('id', 'Unknown')}")
                elif 'models' in models:  # Ollama format
                    for model in models['models'][:5]:
                        print(f"   • {model.get('name', 'Unknown')}")
                else:
                    print(f"   Raw response: {str(models)[:200]}...")
                return True
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    return False

def update_config_for_open_webui():
    """Suggest configuration updates for Open WebUI"""
    print("\n⚙️  Configuration Recommendations")
    print("=" * 40)
    
    print("For Open WebUI integration, add these to your .env file:")
    print()
    print("# Open WebUI Configuration")
    print("OPENAI_BASE_URL=http://localhost:11434/v1")
    print("# or your Open WebUI server URL, e.g.:")
    print("# OPENAI_BASE_URL=https://your-openwebui-server.com/v1")
    print()
    print("This will make the OpenAI client library use your Open WebUI endpoint")
    print("instead of OpenAI's direct API.")

def main():
    """Run Open WebUI API tests"""
    print("🚀 Open WebUI API Key Test Suite")
    print("=" * 50)
    
    # Test 1: API connection
    api_working, working_endpoint = test_open_webui_api()
    
    # Test 2: Available models
    models_working = test_models_endpoint()
    
    # Test 3: Configuration suggestions
    update_config_for_open_webui()
    
    # Summary
    print("\n📋 Test Results Summary")
    print("=" * 50)
    print(f"API Connection: {'✅ PASSED' if api_working else '❌ FAILED'}")
    print(f"Models Access: {'✅ PASSED' if models_working else '❌ FAILED'}")
    
    if api_working:
        print(f"\n🎉 Open WebUI API is working!")
        print(f"   Working endpoint: {working_endpoint}")
        print("   Your compliance discovery system will work with multiple models.")
    else:
        print("\n⚠️  Open WebUI API needs configuration.")
        print("   Please check:")
        print("   • Open WebUI server is running")
        print("   • Correct API key and base URL")
        print("   • Network connectivity to the server")

if __name__ == "__main__":
    main()