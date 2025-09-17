#!/usr/bin/env python3
"""
Fresh OpenAI API Test - Corporate Key Validation
"""

import os
import requests
import urllib3
from pathlib import Path

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_env_manually():
    """Manually load .env file to ensure we get the latest values"""
    env_file = Path('.env')
    if not env_file.exists():
        return None
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('OPENAI_API_KEY='):
                return line.split('=', 1)[1]
    return None

def test_corporate_api_key():
    """Test the corporate OpenAI API key"""
    print("🏢 Testing Corporate OpenAI API Key")
    print("=" * 40)
    
    # Load API key directly from file
    api_key = load_env_manually()
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"🔑 API Key: {api_key[:12]}...{api_key[-8:]}")
    print(f"📏 Length: {len(api_key)} characters")
    
    # Check format
    if not api_key.startswith('sk-'):
        print("❌ API key should start with 'sk-'")
        return False
    
    if len(api_key) < 30:
        print("❌ API key seems too short")
        return False
    
    print("✅ API key format looks good")
    
    # Test the API
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Respond with: Corporate API working'}],
        'max_tokens': 20
    }
    
    print("\n🧪 Testing API call...")
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30,
            verify=False  # Bypass SSL for corporate network
        )
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and result['choices']:
                message = result['choices'][0]['message']['content']
                print(f"✅ SUCCESS! Response: '{message}'")
                
                # Show usage info
                if 'usage' in result:
                    usage = result['usage']
                    print(f"📊 Tokens used: {usage.get('total_tokens', 0)}")
                
                print("\n🎉 Your corporate OpenAI API key is working perfectly!")
                return True
            else:
                print(f"⚠️  Unexpected response: {result}")
                return False
                
        elif response.status_code == 401:
            print("❌ Authentication failed")
            error_detail = response.json() if response.content else {}
            print(f"   Error: {error_detail.get('error', {}).get('message', 'Invalid API key')}")
            return False
            
        elif response.status_code == 429:
            print("❌ Rate limit exceeded")
            return False
            
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_corporate_api_key()
    
    if success:
        print("\n🌟 EXCELLENT! Your corporate OpenAI API is ready to use!")
        print("   The compliance discovery system will work perfectly.")
    else:
        print("\n⚠️  API key needs attention. Please verify:")
        print("   • Key is correctly copied")
        print("   • Account has available credits")
        print("   • Key is active and not expired")