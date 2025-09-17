#!/usr/bin/env python3
"""
Test the fixed compliance framework URL assignment to verify each framework gets a unique URL.
"""

import asyncio
import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.web_app import DynamicComplianceDiscovery

async def test_compliance_url_fix():
    """Test the compliance URL assignment fix"""
    
    print("🧪 Testing Fixed Compliance Framework URL Assignment")
    print("=" * 60)
    
    try:
        # Initialize the compliance discovery
        discovery = DynamicComplianceDiscovery()
        
        vendor_domain = "mixpanel.com"
        frameworks = ["gdpr", "ccpa", "hipaa", "soc2"]
        
        print(f"1. Testing compliance discovery for {vendor_domain}")
        print(f"   Frameworks: {frameworks}")
        
        # Discover compliance documents
        result = await discovery.discover_vendor_compliance(vendor_domain, frameworks)
        
        compliance_docs = result.get("compliance_documents", [])
        
        print(f"\n📋 Found {len(compliance_docs)} compliance documents:")
        print("-" * 50)
        
        framework_url_map = {}
        url_count = {}
        
        for doc in compliance_docs:
            framework = doc.get("framework", "unknown")
            url = doc.get("source_url", "no_url")
            name = doc.get("document_name", "unknown")
            confidence = doc.get("confidence", 0)
            
            # Track framework to URL mapping
            framework_url_map[framework] = url
            
            # Count URL usage
            if url not in url_count:
                url_count[url] = 0
            url_count[url] += 1
            
            print(f"Framework: {framework.upper()}")
            print(f"  Document: {name}")
            print(f"  URL: {url}")
            print(f"  Confidence: {confidence:.2f}")
            print()
        
        print("\n🔍 URL Usage Analysis:")
        print("-" * 50)
        
        duplicate_urls = []
        unique_urls = []
        
        for url, count in url_count.items():
            if count > 1:
                duplicate_urls.append((url, count))
                print(f"⚠️ DUPLICATE: {url} (used {count} times)")
            else:
                unique_urls.append(url)
                print(f"✅ UNIQUE: {url}")
        
        print(f"\n📊 Summary:")
        print(f"  Total Documents: {len(compliance_docs)}")
        print(f"  Unique URLs: {len(unique_urls)}")
        print(f"  Duplicate URLs: {len(duplicate_urls)}")
        
        if duplicate_urls:
            print(f"\n🚨 ISSUE: Found {len(duplicate_urls)} duplicate URLs")
            for url, count in duplicate_urls:
                print(f"  ❌ {url} -> {count} frameworks")
            return False
        else:
            print(f"\n✅ SUCCESS: All {len(compliance_docs)} documents have unique URLs!")
            
            print("\n🎯 Framework → URL Mapping:")
            for framework, url in framework_url_map.items():
                print(f"  {framework.upper()} → {url}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_compliance_url_fix())
    if success:
        print("\n🎉 COMPLIANCE URL FIX WORKING CORRECTLY!")
        print("✅ Each framework now has a unique URL")
    else:
        print("\n🚨 COMPLIANCE URL FIX NEEDS MORE WORK")
        print("❌ Still finding duplicate URLs")