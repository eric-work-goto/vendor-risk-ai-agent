#!/usr/bin/env python3
"""
Enhanced Compliance Document Discovery
This script adds enhanced compliance document discovery for Mixpanel and other vendors
"""

import json

# Enhanced vendor compliance data
enhanced_vendors = {
    "mixpanel.com": {
        "trust_center_info": {
            "trust_center_url": "https://mixpanel.com/legal",
            "login_patterns": [],
            "document_patterns": ["soc2", "iso27001", "gdpr", "ccpa", "hipaa", "pci-dss", "security"],
            "access_method": "public_access"
        },
        "compliance_documents": {
            "soc2": "https://mixpanel.com/legal/security-overview",
            "iso27001": "https://mixpanel.com/legal/security-overview",
            "gdpr": "https://mixpanel.com/legal/mixpanel-gdpr",
            "ccpa": "https://mixpanel.com/legal/mixpanel-ccpa",
            "hipaa": "https://mixpanel.com/legal/mixpanel-hipaa",
            "pci-dss": "https://mixpanel.com/legal/security-overview"
        }
    },
    "stripe.com": {
        "trust_center_info": {
            "trust_center_url": "https://stripe.com/docs/security",
            "login_patterns": [],
            "document_patterns": ["soc2", "iso27001", "gdpr", "ccpa", "hipaa", "pci-dss", "security"],
            "access_method": "public_access"
        },
        "compliance_documents": {
            "soc2": "https://stripe.com/docs/security/stripe",
            "iso27001": "https://stripe.com/docs/security/stripe",
            "gdpr": "https://stripe.com/privacy",
            "ccpa": "https://stripe.com/privacy",
            "hipaa": "https://stripe.com/docs/security/stripe",
            "pci-dss": "https://stripe.com/docs/security/stripe"
        }
    },
    "shopify.com": {
        "trust_center_info": {
            "trust_center_url": "https://shopify.com/legal",
            "login_patterns": [],
            "document_patterns": ["soc2", "iso27001", "gdpr", "ccpa", "hipaa", "pci-dss", "security"],
            "access_method": "public_access"
        },
        "compliance_documents": {
            "soc2": "https://shopify.com/legal/security",
            "iso27001": "https://shopify.com/legal/security",
            "gdpr": "https://shopify.com/legal/privacy",
            "ccpa": "https://shopify.com/legal/privacy/ccpa",
            "hipaa": "https://shopify.com/legal/security",
            "pci-dss": "https://shopify.com/legal/security"
        }
    },
    "hubspot.com": {
        "trust_center_info": {
            "trust_center_url": "https://legal.hubspot.com/security",
            "login_patterns": [],
            "document_patterns": ["soc2", "iso27001", "gdpr", "ccpa", "hipaa", "pci-dss", "security"],
            "access_method": "public_access"
        },
        "compliance_documents": {
            "soc2": "https://legal.hubspot.com/security",
            "iso27001": "https://legal.hubspot.com/security",
            "gdpr": "https://legal.hubspot.com/privacy-policy",
            "ccpa": "https://legal.hubspot.com/privacy-policy",
            "hipaa": "https://legal.hubspot.com/dpa",
            "pci-dss": "https://legal.hubspot.com/security"
        }
    }
}

def print_enhanced_vendor_data():
    """Print the enhanced vendor data in a format ready for integration"""
    print("Enhanced Vendor Compliance Data:")
    print("=" * 50)
    
    for vendor, data in enhanced_vendors.items():
        print(f"\nVendor: {vendor}")
        print(f"Trust Center: {data['trust_center_info']['trust_center_url']}")
        print("Compliance Documents:")
        for doc_type, url in data['compliance_documents'].items():
            print(f"  {doc_type.upper()}: {url}")

if __name__ == "__main__":
    print_enhanced_vendor_data()
    
    # Save to JSON for easy import
    with open('enhanced_vendors.json', 'w') as f:
        json.dump(enhanced_vendors, f, indent=2)
    
    print(f"\n✅ Enhanced vendor data saved to enhanced_vendors.json")
    print("📋 This data can be integrated into the web_app.py compliance discovery system")
