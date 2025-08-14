#!/usr/bin/env python3
"""
Simple test to verify dynamic discovery with fetch_webpage tool
"""

async def test_simple_discovery():
    """Test using fetch_webpage tool directly"""
    
    print("🔍 Testing Direct Webpage Fetch for Mixpanel HIPAA")
    print("=" * 60)
    
    # Test the specific Mixpanel HIPAA URL that we know exists
    mixpanel_hipaa_url = "https://mixpanel.com/legal/mixpanel-hipaa"
    
    print(f"🎯 Testing URL: {mixpanel_hipaa_url}")
    
    # Use a simple requests approach instead of aiohttp
    try:
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; compliance-scanner/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        response = requests.get(mixpanel_hipaa_url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            content = response.text
            print(f"✅ Successfully fetched page!")
            print(f"   Status: {response.status_code}")
            print(f"   Content Length: {len(content)} characters")
            
            # Check for HIPAA keywords
            hipaa_keywords = ["hipaa", "health insurance portability", "protected health information", "business associate", "phi"]
            content_lower = content.lower()
            
            found_keywords = []
            for keyword in hipaa_keywords:
                if keyword in content_lower:
                    found_keywords.append(keyword)
                    print(f"   ✅ Found keyword: '{keyword}'")
            
            if found_keywords:
                print(f"\n🎉 SUCCESS: Found {len(found_keywords)} HIPAA-related keywords!")
                print("   This confirms Mixpanel has HIPAA compliance information available.")
            else:
                print("\n❌ No HIPAA keywords found")
                
            # Show a snippet of the content
            if "hipaa" in content_lower:
                start_idx = content_lower.find("hipaa") - 100
                end_idx = content_lower.find("hipaa") + 200
                start_idx = max(0, start_idx)
                end_idx = min(len(content), end_idx)
                snippet = content[start_idx:end_idx]
                print(f"\n📝 Content snippet around 'HIPAA':")
                print(f"   ...{snippet}...")
                
        else:
            print(f"❌ Failed to fetch page: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_simple_discovery())
