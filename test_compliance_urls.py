#!/usr/bin/env python3
"""
Test compliance document discovery to see what URLs are being generated for different frameworks.
"""

import asyncio
import requests
import json
import time

def test_compliance_framework_urls():
    """Test compliance framework URL generation for a vendor"""
    
    print("🧪 Testing Compliance Framework URL Generation")
    print("=" * 60)
    
    # Test with Mixpanel to see what framework-specific URLs are found
    vendor_domain = "mixpanel.com"
    
    try:
        print(f"1. Testing compliance discovery for {vendor_domain}...")
        
        # Submit a request to find compliance documents
        response = requests.post(
            "http://localhost:8028/find-compliance-documents",
            json={
                "vendor_domain": vendor_domain,
                "frameworks": ["gdpr", "ccpa", "soc2", "iso27001", "hipaa"]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            compliance_docs = result.get("compliance_results", [])
            
            print(f"\n📋 Found {len(compliance_docs)} compliance documents:")
            print("-" * 50)
            
            framework_urls = {}
            
            for doc in compliance_docs:
                framework = doc.get("framework", "unknown")
                source_url = doc.get("source_url", "no_url")
                document_name = doc.get("document_name", "unknown")
                
                if framework not in framework_urls:
                    framework_urls[framework] = []
                framework_urls[framework].append(source_url)
                
                print(f"Framework: {framework.upper()}")
                print(f"  Document: {document_name}")
                print(f"  URL: {source_url}")
                print(f"  Confidence: {doc.get('confidence', 0)}")
                print()
            
            print("\n🔍 URL Analysis by Framework:")
            print("-" * 50)
            
            issues_found = []
            
            for framework, urls in framework_urls.items():
                unique_urls = set(urls)
                print(f"{framework.upper()}: {len(urls)} docs, {len(unique_urls)} unique URLs")
                
                if len(unique_urls) < len(urls):
                    issues_found.append(f"{framework}: Duplicate URLs found")
                
                for url in unique_urls:
                    print(f"  → {url}")
                print()
            
            if issues_found:
                print("🚨 ISSUES DETECTED:")
                for issue in issues_found:
                    print(f"  ⚠️ {issue}")
                return False
            else:
                print("✅ All frameworks have unique URLs!")
                return True
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_compliance_framework_urls()
    if success:
        print("\n🎉 COMPLIANCE URL GENERATION WORKING CORRECTLY!")
    else:
        print("\n🚨 COMPLIANCE URL ISSUES DETECTED - NEEDS FIXING")