#!/usr/bin/env python3
"""
Test the actual web server API endpoint while it's running
"""

import requests
import json

def test_live_server_endpoint():
    """Test the live /find-compliance-documents endpoint"""
    
    print("🌐 Testing Live Server Endpoint")
    print("=" * 50)
    
    # Test data
    test_data = {
        "vendor_domain": "github.com",
        "frameworks": ["gdpr", "ccpa", "hipaa"]
    }
    
    print(f"🎯 Sending request to: http://localhost:8028/find-compliance-documents")
    print(f"📤 Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Send POST request to the live server
        response = requests.post(
            "http://localhost:8028/find-compliance-documents",
            json=test_data,
            timeout=120  # Give it 2 minutes for AI processing
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"📡 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"\n✅ SUCCESS! Server returned JSON response")
                
                # Check the response structure
                print(f"\n📋 Response Structure:")
                print(f"   Keys: {list(result.keys())}")
                
                # Check each key
                for key, value in result.items():
                    print(f"\n   {key}: {type(value)}")
                    if isinstance(value, dict):
                        print(f"      Dict keys: {list(value.keys())}")
                    elif isinstance(value, list):
                        print(f"      List length: {len(value)}")
                        if value:
                            print(f"      First item: {type(value[0])}")
                    else:
                        print(f"      Value: {str(value)[:100]}...")
                
                # Check compliance_results specifically
                if 'compliance_results' in result:
                    compliance_results = result['compliance_results']
                    print(f"\n📊 Compliance Results Analysis:")
                    print(f"   Type: {type(compliance_results)}")
                    
                    if isinstance(compliance_results, dict):
                        print(f"   Keys: {list(compliance_results.keys())}")
                        
                        # Look for compliance_documents
                        if 'compliance_documents' in compliance_results:
                            docs = compliance_results['compliance_documents']
                            print(f"\n   📄 Found {len(docs)} compliance documents:")
                            
                            for i, doc in enumerate(docs[:3], 1):
                                print(f"\n      Document {i}:")
                                for key, value in doc.items():
                                    print(f"         {key}: {value}")
                        else:
                            print(f"   ❌ No 'compliance_documents' found in compliance_results")
                    else:
                        print(f"   ❌ compliance_results is not a dict: {compliance_results}")
                
                # Pretty print the entire response for debugging
                print(f"\n🔍 Full Response (formatted):")
                print(json.dumps(result, indent=2))
                
                return True, result
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                print(f"Raw response: {response.text[:500]}...")
                return False, None
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response text: {response.text}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error - is the server running on localhost:8028?")
        return False, None
    except requests.exceptions.Timeout:
        print(f"❌ Request timeout - server took too long to respond")
        return False, None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False, None

def main():
    """Run the live server test"""
    
    print("🚀 Live Server API Endpoint Test")
    print("=" * 60)
    
    success, result = test_live_server_endpoint()
    
    print(f"\n{'='*60}")
    print("🏁 LIVE SERVER TEST RESULTS")
    print(f"{'='*60}")
    
    if success:
        print(f"✅ EXCELLENT! Live server endpoint is working!")
        print(f"   The backend API is properly returning compliance data.")
        print(f"   If the frontend isn't showing results, check:")
        print(f"   1. JavaScript fetchRealComplianceDocuments() function")
        print(f"   2. How the frontend parses the response")
        print(f"   3. UI rendering of the compliance tab")
    else:
        print(f"❌ Issues with live server endpoint")
        print(f"   Make sure the server is running: cd src/api && python web_app.py")

if __name__ == "__main__":
    main()