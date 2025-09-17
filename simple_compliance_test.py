#!/usr/bin/env python3
"""
Simple test to inspect the compliance framework URLs being returned by checking the actual assessment data.
"""

import requests
import json
import time

def check_assessment_compliance_urls():
    """Check what URLs are actually being returned in assessment data"""
    
    print("🔍 Checking Assessment Compliance Framework URLs")
    print("=" * 60)
    
    try:
        # Start the server first
        print("Starting server and submitting assessment...")
        
        # Submit assessment  
        payload = {
            "vendor_domain": "mixpanel.com",
            "vendor_name": "Mixpanel",
            "requester_email": "test@example.com",
            "data_sensitivity": "medium",
            "business_criticality": "medium",
            "assessment_mode": "standard"
        }
        
        response = requests.post(
            "http://localhost:8028/api/v1/assessments",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            assessment_id = result.get("assessment_id")
            print(f"✅ Assessment ID: {assessment_id}")
            
            # Wait for completion
            time.sleep(10)
            
            # Get results  
            result_response = requests.get(
                f"http://localhost:8028/api/v1/assessments/{assessment_id}",
                timeout=30
            )
            
            if result_response.status_code == 200:
                data = result_response.json()
                compliance_docs = data.get("compliance_documents", [])
                
                print(f"\n📋 Found {len(compliance_docs)} compliance documents:")
                print("-" * 50)
                
                framework_urls = {}
                for doc in compliance_docs:
                    framework = doc.get("framework", "unknown")
                    url = doc.get("source_url", "no_url")
                    name = doc.get("document_name", "unknown")
                    
                    if framework not in framework_urls:
                        framework_urls[framework] = []
                    framework_urls[framework].append(url)
                    
                    print(f"Framework: {framework}")
                    print(f"  Name: {name}")  
                    print(f"  URL: {url}")
                    print()
                
                print("\n🎯 URL Summary by Framework:")
                for framework, urls in framework_urls.items():
                    unique_urls = set(urls)
                    print(f"{framework}: {len(unique_urls)} unique URL(s)")
                    for url in unique_urls:
                        print(f"  → {url}")
                
                # Check if there are duplicate URLs
                all_urls = [doc.get("source_url") for doc in compliance_docs]
                unique_all = set(all_urls)
                
                if len(unique_all) < len(all_urls):
                    print(f"\n⚠️ ISSUE: {len(all_urls)} total docs but only {len(unique_all)} unique URLs")
                    print("This means some frameworks are pointing to the same URL")
                    return False
                else:
                    print(f"\n✅ GOOD: All {len(all_urls)} documents have unique URLs")
                    return True
                    
            else:
                print(f"❌ Failed to get assessment: {result_response.status_code}")
                return False
        else:
            print(f"❌ Failed to submit: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = check_assessment_compliance_urls()
    if success:
        print("\n🎉 ALL COMPLIANCE FRAMEWORKS HAVE UNIQUE URLS!")
    else:
        print("\n🚨 DUPLICATE URL ISSUE DETECTED")