#!/usr/bin/env python3
"""
Async test of compliance discovery with proper await
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add API path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'api'))

async def test_compliance_discovery_async():
    """Test compliance discovery with proper async/await"""
    
    print("🧪 Async Compliance Discovery Test")
    print("=" * 50)
    
    try:
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
        print("\n⏳ Running async compliance discovery... (this may take 30-60 seconds)")
        
        # Call the discover method with proper await
        result = await discovery.discover_vendor_compliance(test_domain, test_frameworks)
        
        print(f"\n📊 Result type: {type(result)}")
        print(f"📊 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict):
            print(f"\n✅ SUCCESS! Got compliance results:")
            
            # Check basic structure
            vendor = result.get('vendor_domain', 'N/A')
            frameworks_found = result.get('frameworks_found', [])
            compliance_docs = result.get('compliance_documents', [])
            trust_centers = result.get('trust_centers', [])
            
            print(f"   Vendor: {vendor}")
            print(f"   Frameworks Found: {frameworks_found}")
            print(f"   Trust Centers: {len(trust_centers)}")
            print(f"   Compliance Documents: {len(compliance_docs)}")
            
            # Show trust centers
            if trust_centers:
                print(f"\n🏛️  Trust Centers found:")
                for i, tc in enumerate(trust_centers[:3], 1):
                    print(f"   {i}. {tc.get('url', 'No URL')}")
                    print(f"      Score: {tc.get('trust_score', 0):.2f}")
                    print(f"      Title: {tc.get('page_title', 'No title')}")
            
            # Show compliance documents  
            if compliance_docs:
                print(f"\n📄 Compliance Documents found:")
                for i, doc in enumerate(compliance_docs[:5], 1):
                    print(f"   {i}. {doc.get('document_name', 'No name')}")
                    print(f"      Type: {doc.get('document_type', 'No type')}")
                    print(f"      Framework: {doc.get('framework', 'No framework')}")
                    print(f"      URL: {doc.get('source_url', 'No URL')}")
                    print(f"      Status: {doc.get('status', 'No status')}")
                    
                    # Check if URL looks real
                    url = doc.get('source_url', '')
                    if url and ('github.com' in url or 'https://' in url):
                        print(f"      ✅ URL looks real")
                    else:
                        print(f"      ⚠️  URL might be placeholder")
                    print()
            else:
                print(f"\n⚠️  No compliance documents found")
            
            return True, result
        else:
            print(f"\n❌ Unexpected result type: {type(result)}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error during async testing: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def main():
    """Run the async test"""
    
    print("🚀 Async Compliance Discovery Test Suite")
    print("=" * 60)
    
    # Check AI configuration
    api_key = os.getenv('OPENAI_API_KEY', '')
    base_url = os.getenv('OPENAI_BASE_URL', '')
    model = os.getenv('OPENAI_MODEL', '')
    
    print(f"🤖 AI Configuration:")
    print(f"   API Key: {'✅ Set' if api_key else '❌ Missing'}")
    print(f"   Base URL: {base_url or '❌ Missing'}")
    print(f"   Model: {model or '❌ Missing'}")
    
    if not (api_key and base_url and model):
        print(f"⚠️  AI configuration incomplete - may affect results")
    
    # Run the async test
    success, result = await test_compliance_discovery_async()
    
    # Summary
    print(f"\n{'='*60}")
    print("🏁 ASYNC TEST RESULTS")
    print(f"{'='*60}")
    
    if success:
        print(f"✅ EXCELLENT! Async compliance discovery is working!")
        print(f"   Your AI system is successfully finding compliance documents.")
        print(f"   If the web interface isn't showing results, the issue is likely in:")
        print(f"   - Frontend JavaScript (fetchRealComplianceDocuments function)")
        print(f"   - API endpoint response handling")
        print(f"   - UI rendering of the results")
    else:
        print(f"❌ Issues with async compliance discovery")

if __name__ == "__main__":
    asyncio.run(main())