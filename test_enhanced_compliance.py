#!/usr/bin/env python3
"""
Test Enhanced Compliance Resource Discovery
Tests the new functionality to find general compliance resources when no dedicated trust center exists.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_compliance_discovery():
    """Test the enhanced compliance resource discovery"""
    try:
        from api.web_app import DynamicComplianceDiscovery
        print("✅ Successfully imported DynamicComplianceDiscovery")
        
        # Create discovery instance
        scanner = DynamicComplianceDiscovery()
        print("✅ Successfully created DynamicComplianceDiscovery instance")
        
        # Test with a domain that likely has privacy policy but no dedicated trust center
        test_domains = [
            "github.com",  # Has privacy policy, security docs, but no traditional trust center
            "stripe.com",  # Has dedicated trust center (for comparison)
            "example.org"  # Minimal site (for fallback testing)
        ]
        
        for domain in test_domains:
            print(f"\n🔍 Testing compliance discovery for {domain}")
            
            # Test trust center discovery first
            print(f"  📋 Step 1: Looking for dedicated trust centers...")
            trust_centers = await scanner._discover_trust_centers(domain)
            print(f"  ✅ Found {len(trust_centers)} trust center(s)")
            
            # Test general compliance resource discovery
            print(f"  📋 Step 2: Looking for general compliance resources...")
            compliance_resources = await scanner._discover_general_compliance_resources(domain)
            print(f"  ✅ Found {len(compliance_resources)} compliance resource(s)")
            
            # Display results
            print(f"  📊 Results for {domain}:")
            if trust_centers:
                for tc in trust_centers[:2]:  # Show top 2
                    print(f"    🔒 Trust Center: {tc['url']} (Score: {tc['trust_score']:.2f})")
            
            if compliance_resources:
                for cr in compliance_resources[:3]:  # Show top 3
                    print(f"    📄 {cr['resource_type']}: {cr['url']} (Score: {cr['resource_score']:.2f})")
            
            if not trust_centers and not compliance_resources:
                print(f"    ❌ No compliance resources found for {domain}")
            
            print(f"  📈 Total resources found: {len(trust_centers) + len(compliance_resources)}")
    
    except Exception as e:
        print(f"❌ Error during compliance discovery test: {e}")
        import traceback
        traceback.print_exc()

async def test_api_endpoint():
    """Test the API endpoint directly"""
    try:
        import requests
        
        test_domains = ["github.com", "stripe.com"]
        
        for domain in test_domains:
            print(f"\n🌐 Testing API endpoint for {domain}")
            response = requests.get(f"http://localhost:8028/api/v1/trust-center/discover/{domain}", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ API call successful")
                print(f"  🔒 Trust centers found: {data.get('trust_centers_found', 0)}")
                print(f"  📄 Compliance resources found: {data.get('compliance_resources_found', 0)}")
                
                if data.get('trust_centers'):
                    print(f"  🎯 Top trust center: {data['trust_centers'][0]['url']}")
                
                if data.get('compliance_resources'):
                    print(f"  📋 Top compliance resource: {data['compliance_resources'][0]['url']} ({data['compliance_resources'][0]['resource_type']})")
            else:
                print(f"  ❌ API call failed: {response.status_code}")
                print(f"  📄 Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during API endpoint test: {e}")

if __name__ == "__main__":
    print("🧪 Enhanced Compliance Resource Discovery Test")
    print("=" * 60)
    
    # Test discovery methods directly
    print("\n🔬 Testing discovery methods directly...")
    asyncio.run(test_compliance_discovery())
    
    # Test API endpoint
    print("\n🌐 Testing API endpoint...")
    asyncio.run(test_api_endpoint())
    
    print("\n✅ Test complete!")