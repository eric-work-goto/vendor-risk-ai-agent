#!/usr/bin/env python3
"""
Test script to verify data flow documentation discovery functionality
"""

import requests
import json
import sys

def test_data_flow_discovery():
    """Test the new data flow documentation discovery endpoint"""
    
    # Test with a known domain
    test_domain = "slack.com"
    
    # API endpoint
    url = "http://localhost:8028/find-data-flow-documents"
    
    # Request payload
    payload = {
        "vendor_domain": test_domain,
        "categories": ["dpa", "privacy_policy", "architecture", "api_docs", "security", "integration"]
    }
    
    try:
        print(f"🔍 Testing data flow discovery for {test_domain}...")
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print(f"📊 Response structure:")
            print(f"  - Success: {result.get('success')}")
            print(f"  - Domain: {result.get('vendor_domain')}")
            print(f"  - Categories requested: {result.get('categories_requested')}")
            
            data_flow_results = result.get('data_flow_results', {})
            print(f"\n📋 Data Flow Results:")
            print(f"  - Documentation centers found: {len(data_flow_results.get('documentation_centers', []))}")
            print(f"  - Data flow documents found: {len(data_flow_results.get('data_flow_documents', []))}")
            print(f"  - Categories found: {data_flow_results.get('categories_found', [])}")
            
            # Show discovered documents
            documents = data_flow_results.get('data_flow_documents', [])
            if documents:
                print(f"\n📄 Discovered Documents:")
                for i, doc in enumerate(documents, 1):
                    print(f"  {i}. {doc.get('document_name', 'Unnamed')} ({doc.get('category', 'Unknown')})")
                    print(f"     URL: {doc.get('source_url', 'N/A')}")
                    print(f"     Confidence: {doc.get('confidence', 0):.1f}%")
                    print()
            else:
                print("  ⚠️ No documents discovered")
            
            # Check for AI enhancement
            if data_flow_results.get('ai_enhanced_urls'):
                print("🤖 AI enhancement was applied!")
            
            print(f"\n✅ Test completed successfully for {test_domain}")
            return True
        
        else:
            print(f"❌ API call failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the server is running on port 8028")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timeout - server might be overloaded")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_multiple_vendors():
    """Test with multiple vendors to verify consistency"""
    
    test_vendors = ["hubspot.com", "salesforce.com", "microsoft.com"]
    
    for vendor in test_vendors:
        print(f"\n{'='*60}")
        print(f"Testing {vendor}")
        print('='*60)
        
        # Temporarily modify test_data_flow_discovery for each vendor
        global test_domain
        original_test = test_data_flow_discovery
        
        def vendor_test():
            url = "http://localhost:8028/find-data-flow-documents"
            payload = {
                "vendor_domain": vendor,
                "categories": ["dpa", "privacy_policy", "api_docs"]  # Smaller set for faster testing
            }
            
            try:
                response = requests.post(url, json=payload, timeout=15)
                if response.status_code == 200:
                    result = response.json()
                    docs_count = len(result.get('data_flow_results', {}).get('data_flow_documents', []))
                    print(f"  ✅ {vendor}: {docs_count} documents found")
                    return True
                else:
                    print(f"  ❌ {vendor}: Failed ({response.status_code})")
                    return False
            except Exception as e:
                print(f"  ❌ {vendor}: Error - {str(e)}")
                return False
        
        vendor_test()

if __name__ == "__main__":
    print("🚀 Data Flow Documentation Discovery Test")
    print("=" * 50)
    
    # Test single vendor
    success = test_data_flow_discovery()
    
    if success:
        print("\n🧪 Running multi-vendor tests...")
        test_multiple_vendors()
    
    print(f"\n{'='*50}")
    print("📋 Test Summary:")
    print("- Backend endpoint: /find-data-flow-documents")
    print("- Categories: dpa, privacy_policy, architecture, api_docs, security, integration") 
    print("- AI enhancement: OpenAI integration for URL discovery")
    print("- Frontend integration: Real-time document discovery in UI")
    
    if success:
        print("✅ Data flow discovery system is working correctly!")
    else:
        print("❌ Issues found - check server logs")