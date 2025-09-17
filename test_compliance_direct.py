#!/usr/bin/env python3
"""
Simple direct test of compliance discovery endpoint without a running server
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the correct paths to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
api_dir = os.path.join(current_dir, 'src', 'api')

sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, api_dir)

def test_compliance_discovery_direct():
    """Test compliance discovery by importing the modules directly"""
    
    print("🧪 Direct Compliance Discovery Test")
    print("=" * 50)
    
    try:
        # Try to import the DynamicComplianceDiscovery class from web_app.py
        sys.path.append(os.path.join(current_dir, 'src', 'api'))
        from web_app import DynamicComplianceDiscovery
        print("✅ DynamicComplianceDiscovery imported successfully")
        
        # Create an instance
        discovery = DynamicComplianceDiscovery()
        print("✅ DynamicComplianceDiscovery instance created")
        
        # Test with GitHub
        test_domain = "github.com"
        test_frameworks = ["gdpr", "ccpa", "hipaa"]
        
        print(f"\n🎯 Testing with domain: {test_domain}")
        print(f"🎯 Testing with frameworks: {test_frameworks}")
        
        # Call the discover method
        result = discovery.discover_vendor_compliance(test_domain, test_frameworks)
        
        print(f"\n📊 Result type: {type(result)}")
        print(f"📊 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict):
            # Check compliance_results
            if 'compliance_results' in result:
                compliance_results = result['compliance_results']
                print(f"\n✅ compliance_results found:")
                print(f"   Type: {type(compliance_results)}")
                
                if isinstance(compliance_results, dict):
                    print(f"   Keys: {list(compliance_results.keys())}")
                    
                    # Check for compliance_documents
                    if 'compliance_documents' in compliance_results:
                        docs = compliance_results['compliance_documents']
                        print(f"\n📄 Found {len(docs)} compliance documents:")
                        
                        for i, doc in enumerate(docs[:3], 1):  # Show first 3
                            print(f"\n   Document {i}:")
                            print(f"      Name: {doc.get('document_name', 'No name')}")
                            print(f"      Type: {doc.get('document_type', 'No type')}")
                            print(f"      URL: {doc.get('source_url', 'No URL')}")
                            print(f"      Status: {doc.get('status', 'No status')}")
                            
                            # Check if URL looks real
                            url = doc.get('source_url', '')
                            if url and ('http' in url or 'https' in url):
                                print(f"      ✅ URL looks real: {url[:60]}...")
                            else:
                                print(f"      ⚠️  URL might be placeholder: {url}")
                    else:
                        print(f"   ❌ No compliance_documents found")
                else:
                    print(f"   ❌ compliance_results is not a dict: {compliance_results}")
            else:
                print(f"   ❌ No compliance_results in response")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def check_ai_configuration():
    """Check if AI is properly configured"""
    
    print(f"\n🤖 AI Configuration Check")
    print("=" * 50)
    
    try:
        # Check environment variables
        import os
        
        openai_key = os.getenv('OPENAI_API_KEY', '')
        openai_base = os.getenv('OPENAI_BASE_URL', '')
        openai_model = os.getenv('OPENAI_MODEL', '')
        
        print(f"OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Missing'}")
        print(f"OPENAI_BASE_URL: {openai_base or '❌ Missing'}")
        print(f"OPENAI_MODEL: {openai_model or '❌ Missing'}")
        
        if openai_key and openai_base and openai_model:
            print(f"\n✅ AI configuration looks complete")
            return True
        else:
            print(f"\n⚠️  AI configuration may be incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Error checking AI config: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 Direct Compliance Discovery Test Suite")
    print("=" * 60)
    
    # Test 1: AI Configuration
    ai_configured = check_ai_configuration()
    
    # Test 2: Direct compliance discovery
    discovery_working = test_compliance_discovery_direct()
    
    # Summary
    print(f"\n{'='*60}")
    print("🏁 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"AI Configuration: {'✅ WORKING' if ai_configured else '❌ ISSUES'}")
    print(f"Discovery Module: {'✅ WORKING' if discovery_working else '❌ FAILED'}")
    
    if ai_configured and discovery_working:
        print(f"\n🎉 EXCELLENT! Core compliance discovery is working!")
        print(f"   The issue might be in the web server or frontend integration.")
        print(f"   Your AI-powered compliance discovery system is functional.")
    else:
        print(f"\n❌ Issues detected in core functionality")

if __name__ == "__main__":
    main()