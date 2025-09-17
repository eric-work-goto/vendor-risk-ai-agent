#!/usr/bin/env python3
"""
Test the live compliance discovery endpoint
"""

import requests
import json

def test_compliance_endpoint():
    """Test the /find-compliance-documents endpoint with the live server"""
    
    print("🧪 Testing Live Compliance Discovery Endpoint")
    print("=" * 50)
    
    # Test data
    test_data = {
        "vendor_domain": "github.com",
        "frameworks": ["gdpr", "ccpa", "hipaa", "pci-dss"]
    }
    
    print(f"🎯 Testing with: {test_data}")
    
    try:
        # Call the endpoint
        response = requests.post(
            "http://localhost:8028/find-compliance-documents",
            json=test_data,
            timeout=60  # Give it time for AI processing
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Endpoint returned data:")
            
            # Pretty print the structure
            print(f"   Success: {result.get('success')}")
            print(f"   Vendor: {result.get('vendor_domain')}")
            print(f"   Frameworks Requested: {result.get('frameworks_requested')}")
            
            # Check compliance results
            compliance_results = result.get('compliance_results', {})
            print(f"\n📊 Compliance Results:")
            print(f"   Type: {type(compliance_results)}")
            print(f"   Keys: {list(compliance_results.keys()) if isinstance(compliance_results, dict) else 'Not a dict'}")
            
            # Check for compliance documents
            if 'compliance_documents' in compliance_results:
                docs = compliance_results['compliance_documents']
                print(f"   Documents found: {len(docs)}")
                
                for i, doc in enumerate(docs[:3], 1):  # Show first 3
                    print(f"\n   📄 Document {i}:")
                    print(f"      Name: {doc.get('document_name', 'No name')}")
                    print(f"      Type: {doc.get('document_type', 'No type')}")  
                    print(f"      URL: {doc.get('source_url', 'No URL')}")
                    print(f"      Status: {doc.get('status', 'No status')}")
            
            # Check for frameworks found
            if 'frameworks_found' in compliance_results:
                frameworks = compliance_results['frameworks_found']
                print(f"\n   🏷️  Frameworks found: {frameworks}")
            
            # Check if AI enhancement was used
            if 'ai_enhanced_urls' in compliance_results:
                print(f"\n   🤖 AI Enhancement: YES")
            else:
                print(f"\n   🤖 AI Enhancement: Not visible in response")
            
            return True, result
            
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False, None

def test_frontend_integration():
    """Test if the frontend can access the endpoint"""
    
    print(f"\n🌐 Testing Frontend Integration")
    print("=" * 50)
    
    try:
        # Test the main UI page
        response = requests.get("http://localhost:8028/static/combined-ui.html", timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend UI is accessible")
            
            # Check if the compliance JavaScript function exists
            if "fetchRealComplianceDocuments" in response.text:
                print("✅ Frontend compliance function found")
                return True
            else:
                print("⚠️  Frontend compliance function not found")
                return False
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend test error: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 Live Compliance Discovery Test Suite")
    print("=" * 60)
    
    # Test 1: Backend API endpoint
    backend_working, result = test_compliance_endpoint()
    
    # Test 2: Frontend accessibility  
    frontend_working = test_frontend_integration()
    
    # Summary
    print(f"\n{'='*60}")
    print("🏁 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Backend API: {'✅ WORKING' if backend_working else '❌ FAILED'}")
    print(f"Frontend UI: {'✅ WORKING' if frontend_working else '❌ FAILED'}")
    
    if backend_working and frontend_working:
        print(f"\n🎉 EXCELLENT! Both backend and frontend are working!")
        print(f"   Your compliance discovery system should now show real AI-generated links")
        print(f"   in the 'Compliance Documentation Discovery' tab.")
        
        print(f"\n🔗 Next Steps:")
        print(f"   1. Open: http://localhost:8028/static/combined-ui.html")
        print(f"   2. Run a vendor assessment")
        print(f"   3. Check the 'Compliance Documentation Discovery' tab")
        print(f"   4. Verify it shows real AI-discovered links")
        
    elif backend_working:
        print(f"\n✅ Backend is working but frontend needs attention")
    else:
        print(f"\n❌ Issues detected - check server logs")

if __name__ == "__main__":
    main()