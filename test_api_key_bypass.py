#!/usr/bin/env python3
"""
OpenAI API Test with SSL Bypass (for testing purposes only)
"""

import os
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings for testing (NOT for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

def test_api_with_ssl_bypass():
    """Test API with SSL verification disabled (testing only)"""
    print("🔓 Testing OpenAI API with SSL verification disabled...")
    print("⚠️  WARNING: This is for testing only, not secure for production!")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return False
    
    print(f"🔑 Using API key: {api_key[:8]}...{api_key[-8:]}")
    print(f"📏 Key length: {len(api_key)} characters")
    
    if len(api_key) < 40:
        print("⚠️  Warning: API key seems shorter than expected")
        print("   Normal OpenAI keys are around 51 characters")
        print("   Please verify your key at https://platform.openai.com/api-keys")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Test message - respond with OK'}],
        'max_tokens': 10
    }
    
    try:
        # Test with SSL verification disabled
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30,
            verify=False  # Disable SSL verification for testing
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and result['choices']:
                message = result['choices'][0]['message']['content']
                print(f"✅ Success! OpenAI responded: '{message}'")
                print("🎉 Your API key is working!")
                return True
            else:
                print(f"⚠️  Unexpected response format: {result}")
                return False
                
        elif response.status_code == 401:
            print("❌ Authentication Error (401)")
            print("   This means your API key is invalid or expired")
            print("   Please check your key at: https://platform.openai.com/api-keys")
            print(f"   Response: {response.text}")
            return False
            
        elif response.status_code == 429:
            print("❌ Rate Limit Error (429)")
            print("   You've exceeded the API rate limit")
            print("   Please wait a moment and try again")
            return False
            
        elif response.status_code == 400:
            print("❌ Bad Request (400)")
            print("   There's an issue with the request format")
            print(f"   Response: {response.text}")
            return False
            
        else:
            print(f"❌ API Error: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    print("🚀 OpenAI API Key Test (SSL Bypass Mode)")
    print("=" * 50)
    
    # Check if running in secure environment
    print("⚠️  SECURITY NOTICE:")
    print("   This test disables SSL verification to bypass corporate firewalls")
    print("   This is ONLY for testing API key validity")
    print("   Do NOT use this in production code!")
    print()
    
    result = test_api_with_ssl_bypass()
    
    print("\n" + "=" * 50)
    if result:
        print("✅ RESULT: Your OpenAI API key is valid and working!")
        print("   The connection issue is likely due to corporate network/SSL settings")
        print("   Your compliance discovery system should work in production")
    else:
        print("❌ RESULT: There are issues with your OpenAI API key")
        print("   Please verify your API key at: https://platform.openai.com/api-keys")
        print("   Make sure it's:")
        print("   • Active and not expired")  
        print("   • Has sufficient credits/usage allowance")
        print("   • Properly copied (around 51 characters starting with 'sk-')")

if __name__ == "__main__":
    main()