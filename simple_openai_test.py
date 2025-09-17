#!/usr/bin/env python3
"""
Simple OpenAI API Test
Quick test to verify OpenAI API key is working
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def simple_openai_test():
    """Simple test for OpenAI API"""
    
    print("🔑 Simple OpenAI API Test")
    print("=" * 30)
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key found")
        return False
        
    print(f"✅ API Key: {api_key[:8]}...{api_key[-8:]}")
    
    try:
        import openai
        
        # Test with corporate ExpertCity server
        corporate_base_url = "https://chat.expertcity.com/api/v1"
        corporate_api_key = "sk-2ea30b318c514c9f874dcd2aa56aa090"
        
        client = openai.OpenAI(base_url=corporate_base_url, api_key=corporate_api_key)
        
        print("🧪 Making test API call...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello World'"}],
            max_tokens=10
        )
        
        if response.choices:
            result = response.choices[0].message.content
            print(f"✅ Response: {result}")
            print("🎉 OpenAI API is working!")
            return True
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(simple_openai_test())
    if result:
        print("\n✅ Your OpenAI API key is working correctly!")
    else:
        print("\n❌ There's an issue with your OpenAI API key or connection")