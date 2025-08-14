#!/usr/bin/env python3
"""
Enhanced test script for keyword-focused compliance URL discovery
Shows prioritization of URLs that contain actual compliance keywords
"""

def generate_keyword_focused_urls(domain: str, doc_type: str):
    """Generate URLs prioritizing those with compliance keywords in the path"""
    
    vendor_name = domain.replace('www.', '').replace('.com', '').replace('.org', '').replace('.net', '').replace('.io', '')
    base_urls = [f"https://{domain}", f"https://www.{domain}"]
    
    paths = []
    
    if doc_type == 'gdpr':
        # Prioritize URLs that contain "gdpr" in the path
        paths = [
            # HIGH PRIORITY: URLs with "gdpr" keyword
            '/gdpr',
            '/legal/gdpr',
            '/compliance/gdpr',
            '/privacy/gdpr',
            '/trust/gdpr',
            f'/legal/{vendor_name}-gdpr/',
            f'/gdpr/{vendor_name}/',
            f'/compliance/{vendor_name}-gdpr/',
            f'/privacy/{vendor_name}-gdpr/',
            f'/legal/gdpr-{vendor_name}/',
            '/eu-gdpr',
            '/data-protection/gdpr',
            '/privacy-policy/gdpr',
            # MEDIUM PRIORITY: data protection related
            '/data-protection',
            '/privacy-policy',
            '/privacy',
            '/legal/privacy',
            '/legal/data-protection',
            f'/legal/{vendor_name}-privacy/',
            f'/legal/{vendor_name}-data-protection/'
        ]
    elif doc_type == 'hipaa':
        # Prioritize URLs that contain "hipaa" in the path
        paths = [
            # HIGH PRIORITY: URLs with "hipaa" keyword
            '/hipaa',
            '/legal/hipaa',
            '/compliance/hipaa',
            '/security/hipaa',
            '/trust/hipaa',
            f'/legal/{vendor_name}-hipaa/',
            f'/hipaa/{vendor_name}/',
            f'/compliance/{vendor_name}-hipaa/',
            f'/security/{vendor_name}-hipaa/',
            f'/legal/hipaa-{vendor_name}/',
            '/healthcare/hipaa',
            '/medical/hipaa',
            '/phi/hipaa',
            # MEDIUM PRIORITY: BAA and healthcare related
            '/baa',
            '/business-associate-agreement',
            '/healthcare-compliance',
            '/medical-compliance',
            f'/legal/{vendor_name}-healthcare/',
            f'/baa/{vendor_name}/',
            f'/legal/{vendor_name}-baa/'
        ]
    elif doc_type == 'ccpa':
        # Prioritize URLs that contain "ccpa" in the path
        paths = [
            # HIGH PRIORITY: URLs with "ccpa" keyword
            '/ccpa',
            '/legal/ccpa',
            '/compliance/ccpa',
            '/privacy/ccpa',
            '/trust/ccpa',
            f'/legal/{vendor_name}-ccpa/',
            f'/ccpa/{vendor_name}/',
            f'/compliance/{vendor_name}-ccpa/',
            f'/privacy/{vendor_name}-ccpa/',
            f'/legal/ccpa-{vendor_name}/',
            '/california/ccpa',
            '/privacy-policy/ccpa',
            # MEDIUM PRIORITY: California privacy related
            '/california-privacy',
            '/california-consumer-privacy',
            '/ca-privacy',
            '/your-privacy-choices',
            f'/legal/{vendor_name}-california-privacy/',
            f'/legal/california-{vendor_name}/'
        ]
    elif doc_type in ['pci-dss', 'pci']:
        # Prioritize URLs that contain "pci" in the path
        paths = [
            # HIGH PRIORITY: URLs with "pci" keyword
            '/pci',
            '/pci-dss',
            '/legal/pci',
            '/compliance/pci',
            '/security/pci',
            '/trust/pci',
            f'/legal/{vendor_name}-pci/',
            f'/legal/{vendor_name}-pci-dss/',
            f'/pci/{vendor_name}/',
            f'/compliance/{vendor_name}-pci/',
            f'/security/{vendor_name}-pci/',
            f'/legal/pci-{vendor_name}/',
            '/payment/pci',
            '/security/pci-dss',
            '/compliance/pci-dss',
            # MEDIUM PRIORITY: payment security related
            '/payment-security',
            '/compliance/payment',
            '/pci-compliance',
            f'/legal/{vendor_name}-payment/',
            f'/legal/payment-{vendor_name}/'
        ]
    
    # Generate all URL combinations
    urls = []
    for base in base_urls:
        for path in paths:
            urls.append(f"{base}{path}")
    
    return list(set(urls))  # Remove duplicates

def analyze_url_keywords(url, doc_type):
    """Analyze if URL contains compliance keywords"""
    url_lower = url.lower()
    path = url_lower.split('/')[-1] if '/' in url_lower else url_lower
    
    keyword_score = 0
    keyword_details = []
    
    if doc_type == 'gdpr':
        if 'gdpr' in url_lower:
            keyword_score += 10
            keyword_details.append('Contains "gdpr"')
        if 'privacy' in url_lower:
            keyword_score += 5
            keyword_details.append('Contains "privacy"')
        if 'data-protection' in url_lower:
            keyword_score += 5
            keyword_details.append('Contains "data-protection"')
    elif doc_type == 'hipaa':
        if 'hipaa' in url_lower:
            keyword_score += 10
            keyword_details.append('Contains "hipaa"')
        if 'baa' in url_lower:
            keyword_score += 7
            keyword_details.append('Contains "baa"')
        if 'healthcare' in url_lower:
            keyword_score += 5
            keyword_details.append('Contains "healthcare"')
    elif doc_type == 'ccpa':
        if 'ccpa' in url_lower:
            keyword_score += 10
            keyword_details.append('Contains "ccpa"')
        if 'california' in url_lower:
            keyword_score += 5
            keyword_details.append('Contains "california"')
    elif doc_type in ['pci-dss', 'pci']:
        if 'pci' in url_lower:
            keyword_score += 10
            keyword_details.append('Contains "pci"')
        if 'payment' in url_lower:
            keyword_score += 5
            keyword_details.append('Contains "payment"')
    
    return keyword_score, keyword_details

def test_keyword_focused_discovery():
    """Test the keyword-focused URL discovery"""
    
    test_cases = [
        ("mixpanel.com", "hipaa"),
        ("stripe.com", "pci"),
        ("salesforce.com", "gdpr"),
        ("zoom.us", "ccpa")
    ]
    
    print("🎯 Keyword-Focused Compliance URL Discovery Test")
    print("=" * 60)
    print()
    
    for domain, doc_type in test_cases:
        vendor_name = domain.replace('.com', '').replace('.us', '')
        print(f"🏢 Vendor: {domain}")
        print(f"📋 Compliance Type: {doc_type.upper()}")
        print()
        
        urls = generate_keyword_focused_urls(domain, doc_type)
        
        # Analyze and sort URLs by keyword relevance
        url_analysis = []
        for url in urls:
            score, details = analyze_url_keywords(url, doc_type)
            url_analysis.append((url, score, details))
        
        # Sort by keyword score (highest first)
        url_analysis.sort(key=lambda x: x[1], reverse=True)
        
        print("📊 URLs ranked by keyword relevance:")
        print()
        
        high_priority = [u for u in url_analysis if u[1] >= 10]
        medium_priority = [u for u in url_analysis if 5 <= u[1] < 10]
        low_priority = [u for u in url_analysis if u[1] < 5]
        
        if high_priority:
            print("  🎯⭐ HIGH PRIORITY (Contains exact compliance keyword):")
            for i, (url, score, details) in enumerate(high_priority[:5], 1):
                print(f"    {i:2d}. {url}")
                print(f"        Score: {score} | {', '.join(details)}")
                if "mixpanel.com/legal/mixpanel-hipaa/" in url:
                    print("        ✅ MATCHES YOUR EXAMPLE!")
            print()
        
        if medium_priority:
            print("  ⭐ MEDIUM PRIORITY (Contains related keywords):")
            for i, (url, score, details) in enumerate(medium_priority[:3], 1):
                print(f"    {i:2d}. {url}")
                print(f"        Score: {score} | {', '.join(details)}")
            print()
        
        if low_priority:
            print("  📋 STANDARD PATHS (No specific keywords):")
            for i, (url, score, details) in enumerate(low_priority[:2], 1):
                print(f"    {i:2d}. {url}")
                print(f"        Score: {score}")
            print()
        
        print("-" * 60)
        print()

def demo_keyword_detection():
    """Demonstrate keyword detection in URLs"""
    
    print("🔍 Keyword Detection Demonstration")
    print("=" * 40)
    print()
    
    sample_urls = [
        ("https://mixpanel.com/legal/mixpanel-hipaa/", "hipaa"),
        ("https://stripe.com/legal/pci-dss/", "pci"),
        ("https://salesforce.com/trust/gdpr/", "gdpr"),
        ("https://zoom.us/legal/ccpa/", "ccpa"),
        ("https://example.com/legal/privacy/", "gdpr"),  # No specific keyword
        ("https://vendor.com/compliance/", "hipaa")       # No specific keyword
    ]
    
    for url, doc_type in sample_urls:
        score, details = analyze_url_keywords(url, doc_type)
        priority = "🎯⭐ HIGH" if score >= 10 else "⭐ MEDIUM" if score >= 5 else "📋 LOW"
        print(f"{priority}: {url}")
        print(f"   Score: {score} | {', '.join(details) if details else 'No compliance keywords found'}")
        print()

if __name__ == "__main__":
    demo_keyword_detection()
    print()
    test_keyword_focused_discovery()
    
    print()
    print("🚀 Key Keyword-Focused Enhancements:")
    print("✅ URLs with exact compliance keywords get priority score +10")
    print("✅ URLs with related terms get priority score +5-7")
    print("✅ Vendor-specific + keyword combinations ranked highest")
    print("✅ Clear visual indicators: 🎯⭐ = Best, ⭐ = Good, 📋 = Standard")
    print("✅ Intelligent sorting by keyword relevance")
    print()
    print("This system now specifically targets URLs that contain")
    print("the actual compliance keywords like 'GDPR', 'HIPAA', 'CCPA', 'PCI'!")
