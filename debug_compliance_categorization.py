#!/usr/bin/env python3
"""
Debug the compliance framework categorization issue
"""

import requests
import json

def test_compliance_framework_categorization():
    """Test to debug why all frameworks are showing up in GDPR section"""
    
    print("🔍 Debugging Compliance Framework Categorization")
    print("=" * 60)
    
    try:
        # Test with a known vendor
        response = requests.post(
            "http://localhost:8028/find-compliance-documents",
            json={
                "vendor_domain": "github.com",
                "frameworks": ["gdpr", "ccpa", "hipaa", "pci-dss"]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ API Response received successfully")
            print(f"📊 Success: {result.get('success')}")
            
            compliance_results = result.get('compliance_results', {})
            compliance_docs = compliance_results.get('compliance_documents', [])
            
            print(f"\n📄 Found {len(compliance_docs)} compliance documents:")
            
            # Analyze each document
            for i, doc in enumerate(compliance_docs, 1):
                print(f"\n   Document {i}:")
                print(f"      📝 Name: {doc.get('document_name', 'N/A')}")
                print(f"      🏷️  Framework: {doc.get('framework', 'N/A')}")
                print(f"      🔗 URL: {doc.get('source_url', 'N/A')}")
                print(f"      📊 Confidence: {doc.get('confidence', 0)}")
                print(f"      📋 All Frameworks: {doc.get('all_frameworks', [])}")
                
                # Check if document has multiple frameworks
                all_frameworks = doc.get('all_frameworks', [])
                if len(all_frameworks) > 1:
                    print(f"      ⚠️  ISSUE: Document has multiple frameworks: {all_frameworks}")
                    print(f"         This could cause categorization issues!")
                elif not doc.get('framework'):
                    print(f"      ❌ ISSUE: Document missing primary framework field!")
                else:
                    print(f"      ✅ Properly categorized as: {doc.get('framework')}")
            
            # Simulate frontend processing
            print(f"\n🖥️  Frontend Processing Simulation:")
            framework_map = {
                'gdpr': 'General Data Protection Regulation',
                'hipaa': 'Health Insurance Portability and Accountability Act', 
                'pci-dss': 'Payment Card Industry Data Security Standard',
                'ccpa': 'California Consumer Privacy Act'
            }
            
            for framework, name in framework_map.items():
                matching_docs = [doc for doc in compliance_docs if doc.get('framework') == framework]
                print(f"\n   {framework.upper()} ({name}):")
                print(f"      Documents found: {len(matching_docs)}")
                
                if matching_docs:
                    for doc in matching_docs:
                        print(f"         • {doc.get('document_name', 'Unnamed')}")
                        print(f"           URL: {doc.get('source_url', 'No URL')}")
                else:
                    print(f"      ❌ No documents found for {framework}")
            
            # Check for potential issues
            print(f"\n🔍 Potential Issues Analysis:")
            
            # Issue 1: Documents with wrong framework assignment
            for doc in compliance_docs:
                doc_url = doc.get('source_url', '').lower()
                doc_framework = doc.get('framework', '')
                
                if 'gdpr' in doc_url and doc_framework != 'gdpr':
                    print(f"   ⚠️  URL contains 'gdpr' but framework is '{doc_framework}': {doc_url}")
                elif 'ccpa' in doc_url and doc_framework != 'ccpa':
                    print(f"   ⚠️  URL contains 'ccpa' but framework is '{doc_framework}': {doc_url}")
                elif 'hipaa' in doc_url and doc_framework != 'hipaa':
                    print(f"   ⚠️  URL contains 'hipaa' but framework is '{doc_framework}': {doc_url}")
                elif 'pci' in doc_url and doc_framework != 'pci-dss':
                    print(f"   ⚠️  URL contains 'pci' but framework is '{doc_framework}': {doc_url}")
            
            # Issue 2: Check if all documents are being assigned to the same framework
            frameworks_found = [doc.get('framework') for doc in compliance_docs if doc.get('framework')]
            unique_frameworks = set(frameworks_found)
            
            if len(unique_frameworks) == 1 and len(compliance_docs) > 1:
                print(f"   ❌ MAJOR ISSUE: All {len(compliance_docs)} documents assigned to same framework: {list(unique_frameworks)[0]}")
                print(f"      This is likely causing the UI grouping issue!")
            else:
                print(f"   ✅ Documents properly distributed across {len(unique_frameworks)} frameworks")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run the debug test"""
    
    print("🚀 Compliance Framework Categorization Debug")
    print("=" * 60)
    
    success = test_compliance_framework_categorization()
    
    if success:
        print(f"\n💡 If all documents are showing in GDPR section, likely causes:")
        print(f"   1. Backend assigning wrong 'framework' field to documents")
        print(f"   2. Frontend not properly reading the 'framework' field") 
        print(f"   3. All documents detected as GDPR-related even when they're not")
        print(f"   4. URL pattern matching incorrectly categorizing all docs as GDPR")
    else:
        print(f"\n❌ Could not connect to server. Make sure it's running:")
        print(f"   cd src/api && python web_app.py")

if __name__ == "__main__":
    main()