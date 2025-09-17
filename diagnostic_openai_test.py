#!/usr/bin/env python3
"""
Detailed OpenAI API Test with Error Diagnostics
"""

import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_internet_connection():
    """Test basic internet connectivity"""
    print("🌐 Testing internet connection...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("✅ Internet connection is working")
            return True
        else:
            print(f"⚠️  Internet connection issue: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No internet connection: {e}")
        return False

def test_openai_endpoint():
    """Test direct connection to OpenAI API endpoint"""
    print("\n🔌 Testing OpenAI API endpoint accessibility...")
    try:
        response = requests.get("https://api.openai.com/v1/models", timeout=10)
        print(f"✅ OpenAI endpoint accessible: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Cannot reach OpenAI endpoint: {e}")
        return False

def test_api_key_format():
    """Test API key format"""
    print("\n🔑 Testing API key format...")
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return False
        
    if not api_key.startswith('sk-'):
        print("❌ API key should start with 'sk-'")
        return False
        
    if len(api_key) < 40:
        print("❌ API key seems too short")
        return False
        
    print("✅ API key format looks correct")
    return True

def test_openai_with_requests():
    """Test OpenAI API using requests library directly"""
    print("\n🧪 Testing OpenAI API with direct HTTP request...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key")
        return False
        
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Say hello'}],
        'max_tokens': 5
    }
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and result['choices']:
                message = result['choices'][0]['message']['content']
                print(f"✅ OpenAI API working! Response: {message}")
                return True
            else:
                print(f"⚠️  Unexpected response format: {result}")
                return False
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid API key")
            return False
        elif response.status_code == 429:
            print("❌ Rate limit exceeded - Please wait")
            return False
        else:
            print(f"❌ API error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    
    print("🚀 OpenAI API Diagnostic Test")
    print("=" * 40)
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Internet connection
    internet_ok = test_internet_connection()
    
    # Test 2: OpenAI endpoint accessibility  
    endpoint_ok = test_openai_endpoint()
    
    # Test 3: API key format
    key_format_ok = test_api_key_format()
    
    # Test 4: Direct API test
    api_ok = test_openai_with_requests()
    
    # Summary
    print("\n📋 Diagnostic Results")
    print("=" * 40)
    print(f"Internet Connection: {'✅' if internet_ok else '❌'}")
    print(f"OpenAI Endpoint: {'✅' if endpoint_ok else '❌'}")
    print(f"API Key Format: {'✅' if key_format_ok else '❌'}")
    print(f"OpenAI API Test: {'✅' if api_ok else '❌'}")
    
    if all([internet_ok, endpoint_ok, key_format_ok, api_ok]):
        print("\n🎉 All tests passed! Your OpenAI API is fully functional.")
    else:
        print("\n⚠️  Some issues detected. Please address the failed tests above.")
        
        if not internet_ok:
            print("   • Check your internet connection")
        if not endpoint_ok:
            print("   • Check firewall/proxy settings")
        if not key_format_ok:
            print("   • Verify your API key in .env file")
        if not api_ok:
            print("   • Check API key validity at https://platform.openai.com/")

if __name__ == "__main__":
    main()