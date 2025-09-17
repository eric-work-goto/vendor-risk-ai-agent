#!/usr/bin/env python3
"""
Enhanced Document Discovery Test
Test the improved document and webpage discovery system with URL validation and content analysis.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api.web_app import (
    scan_data_flows,
    discover_vendor_compliance_pages, 
    validate_and_analyze_urls,
    enhance_data_flow_discovery_with_ai
)

async def test_enhanced_discovery():
    """Test the enhanced document discovery system"""
    
    print("🚀 Enhanced Document Discovery Test")
    print("=" * 50)
    
    # Test vendors with different characteristics
    test_vendors = [
        {
            'domain': 'slack.com',
            'name': 'Slack Technologies',
            'description': 'Well-documented SaaS company'
        },
        {
            'domain': 'zoom.us', 
            'name': 'Zoom Video Communications',
            'description': 'Popular video conferencing platform'
        },
        {
            'domain': 'salesforce.com',
            'name': 'Salesforce',
            'description': 'Large enterprise CRM platform'
        }
    ]
    
    for vendor in test_vendors:
        print(f"\n🔍 Testing Enhanced Discovery for {vendor['name']}")
        print(f"Domain: {vendor['domain']}")
        print(f"Description: {vendor['description']}")
        print("-" * 40)
        
        try:
            # Test enhanced data flow discovery
            print("\n📊 Data Flow Documentation Discovery:")
            data_flow_results = await scan_data_flows(vendor['domain'], vendor['name'])
            
            if data_flow_results and 'source_information' in data_flow_results:
                source_info = data_flow_results['source_information']
                
                print(f"✅ Scan Method: {source_info.get('scan_method', 'Standard')}")
                
                # Display AI-discovered URLs
                ai_urls = source_info.get('ai_discovered_urls', [])
                if ai_urls:
                    print(f"🤖 AI Discovered URLs: {len(ai_urls)}")
                    for i, url_data in enumerate(ai_urls[:3], 1):  # Show top 3
                        print(f"   {i}. {url_data.get('url', 'Unknown URL')}")
                        print(f"      Status: {url_data.get('status_code', 'Unknown')}")
                        print(f"      Relevance: {url_data.get('relevance_score', 0):.2f}/1.0")
                        print(f"      Content: {url_data.get('content_summary', 'No summary')}")
                
                # Display validation summary
                validation_summary = source_info.get('url_validation_summary', {})
                if validation_summary:
                    print(f"📈 URL Validation Summary:")
                    print(f"   Total Discovered: {validation_summary.get('total_discovered', 0)}")
                    print(f"   Valid URLs: {validation_summary.get('valid_urls', 0)}")
                    print(f"   High Relevance: {validation_summary.get('high_relevance_urls', 0)}")
            
            # Test compliance framework discovery
            print(f"\n⚖️ Compliance Framework Discovery:")
            compliance_types = ['gdpr', 'soc2', 'iso27001', 'ccpa']
            
            for doc_type in compliance_types:
                print(f"\n   Testing {doc_type.upper()} discovery...")
                compliance_docs = await discover_vendor_compliance_pages(vendor['domain'], doc_type)
                
                if compliance_docs:
                    print(f"   ✅ Found {len(compliance_docs)} {doc_type.upper()} document(s)")
                    
                    for doc in compliance_docs[:2]:  # Show top 2 results
                        confidence = doc.get('confidence_level', 'Unknown')
                        relevance = doc.get('relevance_score', 0)
                        print(f"      • URL: {doc.get('url', 'Unknown')}")
                        print(f"        Confidence: {confidence} (Relevance: {relevance:.2f})")
                        print(f"        Content: {doc.get('content_summary', 'No summary')}")
                else:
                    print(f"   ❌ No valid {doc_type.upper()} documents found")
            
            # Test manual URL validation
            print(f"\n🔧 Manual URL Validation Test:")
            test_urls = [
                f"https://{vendor['domain']}/privacy-policy",
                f"https://{vendor['domain']}/security", 
                f"https://{vendor['domain']}/trust",
                f"https://{vendor['domain']}/legal/dpa"
            ]
            
            validated_urls = await validate_and_analyze_urls(test_urls, vendor['domain'])
            
            valid_count = len([u for u in validated_urls if u['is_valid']])
            relevant_count = len([u for u in validated_urls if u.get('relevance_score', 0) > 0.3])
            
            print(f"   📊 Results: {valid_count}/{len(test_urls)} valid, {relevant_count} relevant")
            
            if validated_urls:
                best_url = max(validated_urls, key=lambda x: (x['is_valid'], x.get('relevance_score', 0)))
                print(f"   🏆 Best Result: {best_url.get('url', 'Unknown')}")
                print(f"      Relevance Score: {best_url.get('relevance_score', 0):.2f}")
                print(f"      Content Summary: {best_url.get('content_summary', 'No summary')}")
            
        except Exception as e:
            print(f"❌ Error testing {vendor['name']}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("✅ Enhanced Document Discovery Test Complete!")
    print("\n📋 Key Improvements Demonstrated:")
    print("• AI-powered URL generation with corporate API")
    print("• Real-time URL validation and status checking") 
    print("• Content relevance scoring and analysis")
    print("• Enhanced compliance framework discovery")
    print("• Comprehensive error handling and fallbacks")
    print("• Progressive result filtering and prioritization")

if __name__ == "__main__":
    print("Starting Enhanced Document Discovery Test...")
    asyncio.run(test_enhanced_discovery())