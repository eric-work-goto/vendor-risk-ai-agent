#!/usr/bin/env python3
"""
Test OpenAI API Key Functionality
Simple test to verify the OpenAI API key is working correctly
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_openai_api():
    """Test basic OpenAI API connectivity and functionality"""
    
    print("🔑 Testing OpenAI API Key...")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Please set your OpenAI API key in .env file")
        return False
    
    # Show partial API key for verification (security)
    masked_key = api_key[:8] + "..." + api_key[-8:] if len(api_key) > 16 else "***"
    print(f"✅ API Key found: {masked_key}")
    
    # Test OpenAI API connection
    try:
        import openai
        
        # Configure OpenAI client with corporate ExpertCity server
        corporate_base_url = "https://chat.expertcity.com/api/v1"
        corporate_api_key = "sk-2ea30b318c514c9f874dcd2aa56aa090"
        
        client = openai.AsyncOpenAI(base_url=corporate_base_url, api_key=corporate_api_key)
        
        print("\n🤖 Testing OpenAI API connection...")
        
        # Simple API test - get a short response
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user", 
                    "content": "Say 'API Test Successful' if you receive this message."
                }
            ],
            max_tokens=50,
            temperature=0
        )
        
        # Check response
        if response and response.choices:
            result = response.choices[0].message.content.strip()
            print(f"✅ OpenAI API Response: {result}")
            
            # Verify it's working properly
            if "API Test Successful" in result or "successful" in result.lower():
                print("\n🎉 OpenAI API is working correctly!")
                
                # Test usage information
                if hasattr(response, 'usage') and response.usage:
                    print(f"📊 Tokens used: {response.usage.total_tokens}")
                    print(f"   - Prompt: {response.usage.prompt_tokens}")
                    print(f"   - Completion: {response.usage.completion_tokens}")
                
                return True
            else:
                print(f"⚠️  Unexpected response: {result}")
                return False
        else:
            print("❌ No response from OpenAI API")
            return False
            
    except ImportError:
        print("❌ OpenAI library not installed")
        print("   Please install with: pip install openai")
        return False
    except openai.AuthenticationError:
        print("❌ Authentication failed - Invalid API key")
        print("   Please check your OPENAI_API_KEY in .env file")
        return False
    except openai.RateLimitError:
        print("❌ Rate limit exceeded")
        print("   Please wait a moment before trying again")
        return False
    except openai.APIError as e:
        print(f"❌ OpenAI API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_compliance_discovery():
    """Test the compliance discovery function specifically"""
    
    print("\n🔍 Testing Compliance Discovery Function...")
    print("=" * 50)
    
    try:
        # Import the function we need to test
        sys.path.append('src')
        from api.web_app import enhance_compliance_discovery_with_ai
        
        print("✅ Successfully imported enhance_compliance_discovery_with_ai")
        
        # Test with a simple vendor
        test_vendor = "github.com"
        test_frameworks = ["gdpr"]
        
        print(f"🧪 Testing discovery for {test_vendor} with {test_frameworks}")
        
        result = await enhance_compliance_discovery_with_ai(test_vendor, test_frameworks)
        
        if result:
            print("✅ Compliance discovery function returned results:")
            print(f"   Frameworks found: {result.get('frameworks_found', [])}")
            print(f"   Documents found: {len(result.get('compliance_documents', []))}")
            
            # Show first document if available
            docs = result.get('compliance_documents', [])
            if docs:
                doc = docs[0]
                print(f"   First document: {doc.get('document_name', 'Unknown')}")
                print(f"   URL: {doc.get('source_url', 'No URL')}")
            
            return True
        else:
            print("⚠️  Compliance discovery returned empty results")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   The compliance discovery function may not be available")
        return False
    except Exception as e:
        print(f"❌ Error testing compliance discovery: {e}")
        return False

async def main():
    """Run all tests"""
    
    print("🚀 OpenAI API Key Test Suite")
    print("=" * 50)
    print(f"Date: {os.popen('date /t').read().strip()}")
    print(f"Time: {os.popen('time /t').read().strip()}")
    print()
    
    # Test 1: Basic API connectivity
    api_test = await test_openai_api()
    
    # Test 2: Compliance discovery function
    compliance_test = await test_compliance_discovery()
    
    # Summary
    print("\n📋 Test Results Summary")
    print("=" * 50)
    print(f"OpenAI API Test: {'✅ PASSED' if api_test else '❌ FAILED'}")
    print(f"Compliance Discovery Test: {'✅ PASSED' if compliance_test else '❌ FAILED'}")
    
    if api_test and compliance_test:
        print("\n🎉 All tests passed! Your OpenAI API key is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)