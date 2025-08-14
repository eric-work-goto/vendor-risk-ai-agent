#!/usr/bin/env python3
"""
Test the new dynamic compliance discovery system
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_dynamic_discovery():
    """Test the dynamic compliance discovery with Mixpanel"""
    
    # Import after adding to path
    from api.web_app import DynamicComplianceDiscovery
    
    print("🔍 Testing Dynamic Compliance Discovery System")
    print("=" * 60)
    
    # Initialize the discovery engine
    discovery = DynamicComplianceDiscovery()
    
    # Test with Mixpanel (the vendor that had the HIPAA issue)
    test_vendor = "mixpanel.com"
    test_frameworks = ["hipaa", "gdpr", "ccpa", "pci-dss"]
    
    print(f"🎯 Testing vendor: {test_vendor}")
    print(f"🎯 Requested frameworks: {', '.join(test_frameworks)}")
    print()
    
    try:
        # Run the discovery
        result = await discovery.discover_vendor_compliance(test_vendor, test_frameworks)
        
        print("📊 DISCOVERY RESULTS:")
        print(f"   Trust Centers Found: {len(result['trust_centers'])}")
        print(f"   Frameworks Detected: {', '.join(result['frameworks_found'])}")
        print(f"   Total Documents: {len(result['compliance_documents'])}")
        print()
        
        # Show trust centers
        if result['trust_centers']:
            print("🏢 TRUST CENTERS:")
            for i, tc in enumerate(result['trust_centers'][:3], 1):  # Show top 3
                print(f"   {i}. {tc['url']} (score: {tc['trust_score']:.2f})")
                print(f"      Title: {tc.get('page_title', 'Unknown')}")
        print()
        
        # Show compliance documents
        if result['compliance_documents']:
            print("📄 COMPLIANCE DOCUMENTS:")
            for i, doc in enumerate(result['compliance_documents'][:5], 1):  # Show top 5
                framework = doc['compliance_info']['detected_frameworks'][0] if doc['compliance_info']['detected_frameworks'] else 'general'
                confidence = max(doc['compliance_info']['confidence_scores'].values()) if doc['compliance_info']['confidence_scores'] else 0.0
                print(f"   {i}. {framework.upper()}: {doc['url']}")
                print(f"      Confidence: {confidence:.2f}")
                print(f"      Content: {doc['compliance_info'].get('content_summary', 'No summary')}")
        
        # Specific HIPAA check
        hipaa_docs = [doc for doc in result['compliance_documents'] 
                     if 'hipaa' in doc['compliance_info']['detected_frameworks']]
        
        print()
        print("🏥 HIPAA-SPECIFIC RESULTS:")
        if hipaa_docs:
            print(f"   ✅ Found {len(hipaa_docs)} HIPAA-related documents!")
            for doc in hipaa_docs:
                confidence = doc['compliance_info']['confidence_scores'].get('hipaa', 0.0)
                print(f"   📋 {doc['url']} (confidence: {confidence:.2f})")
        else:
            print("   ❌ No HIPAA documents detected")
        
        print()
        print("🎉 Test completed successfully!")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_mixpanel_hipaa():
    """Specific test for Mixpanel HIPAA discovery"""
    
    from api.web_app import DynamicComplianceDiscovery
    
    print("\n🏥 SPECIFIC MIXPANEL HIPAA TEST")
    print("=" * 40)
    
    discovery = DynamicComplianceDiscovery()
    
    # Test the exact URL we know has HIPAA info
    test_url = "https://mixpanel.com/legal/mixpanel-hipaa"
    
    print(f"🎯 Testing known HIPAA URL: {test_url}")
    
    import aiohttp
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'identity',
            'Connection': 'keep-alive'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(test_url, timeout=10, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Test our content analysis
                    analysis = discovery._analyze_page_content(content, ["hipaa"])
                    
                    print(f"📊 Page Analysis Results:")
                    print(f"   Status Code: {response.status}")
                    print(f"   Content Length: {len(content)} characters")
                    print(f"   Relevance Score: {analysis['relevance_score']:.2f}")
                    print(f"   Detected Frameworks: {analysis['detected_frameworks']}")
                    print(f"   Confidence Scores: {analysis['confidence_scores']}")
                    print(f"   Document Type: {analysis['document_type']}")
                    
                    # Check if HIPAA keywords are found
                    hipaa_keywords = ["hipaa", "health insurance portability", "protected health information", "phi", "healthcare compliance"]
                    found_keywords = [kw for kw in hipaa_keywords if kw.lower() in content.lower()]
                    
                    print(f"   HIPAA Keywords Found: {found_keywords}")
                    
                    if analysis['relevance_score'] > 0.4:
                        print("   ✅ Page correctly identified as HIPAA-relevant!")
                    else:
                        print("   ❌ Page not identified as HIPAA-relevant (needs tuning)")
                
                else:
                    print(f"   ❌ Failed to fetch page: HTTP {response.status}")
                    
    except Exception as e:
        print(f"   ❌ Error fetching page: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Dynamic Compliance Discovery Tests")
    print()
    
    # Run the main test
    result = asyncio.run(test_dynamic_discovery())
    
    # Run the specific HIPAA test
    asyncio.run(test_mixpanel_hipaa())
    
    print("\n✨ All tests completed!")
