#!/usr/bin/env python3
"""
Test compliance framework URL assignment with multiple vendors to ensure consistent unique URL behavior.
"""

import asyncio
import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.web_app import DynamicComplianceDiscovery

async def test_vendor_compliance_urls(vendor_domain: str, frameworks: list):
    """Test compliance URL uniqueness for a specific vendor"""
    
    print(f"\n🏢 Testing {vendor_domain}")
    print("-" * 40)
    
    try:
        discovery = DynamicComplianceDiscovery()
        result = await discovery.discover_vendor_compliance(vendor_domain, frameworks)
        
        compliance_docs = result.get("compliance_documents", [])
        print(f"Found {len(compliance_docs)} compliance documents")
        
        # Track URLs and frameworks
        urls_seen = set()
        framework_counts = {}
        duplicate_urls = []
        
        for doc in compliance_docs:
            framework = doc.get("framework", "unknown")
            url = doc.get("source_url", "no_url")
            
            # Count frameworks
            framework_counts[framework] = framework_counts.get(framework, 0) + 1
            
            # Check for duplicates
            if url in urls_seen:
                duplicate_urls.append(url)
            else:
                urls_seen.add(url)
                
            print(f"  📄 {framework.upper()}: {url}")
        
        # Summary
        unique_urls = len(urls_seen)
        total_docs = len(compliance_docs)
        
        if duplicate_urls:
            print(f"  ❌ Found {len(duplicate_urls)} duplicate URLs: {duplicate_urls}")
            return False
        else:
            print(f"  ✅ All {unique_urls} URLs are unique ({total_docs} documents)")
            return True
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

async def main():
    """Test multiple vendors for compliance URL uniqueness"""
    
    print("🧪 Testing Compliance Framework URL Uniqueness Across Multiple Vendors")
    print("=" * 70)
    
    test_cases = [
        ("mixpanel.com", ["gdpr", "ccpa", "soc2"]),
        ("salesforce.com", ["gdpr", "soc2", "iso27001"]),
        ("slack.com", ["gdpr", "ccpa", "hipaa"]),
        ("zoom.us", ["gdpr", "soc2", "hipaa"])
    ]
    
    all_passed = True
    
    for vendor_domain, frameworks in test_cases:
        success = await test_vendor_compliance_urls(vendor_domain, frameworks)
        if not success:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Compliance framework URL assignment is working correctly")
        print("✅ No duplicate URLs found across all vendors")
    else:
        print("🚨 SOME TESTS FAILED!")
        print("❌ Compliance framework URL assignment needs attention")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)