#!/usr/bin/env python3
"""
Test script to verify the compliance document discovery system is working
"""

import json
import requests
import sys
import os
import time
from datetime import datetime

def test_compliance_discovery(vendor_domain="github.com"):
    """Test the compliance document discovery functionality"""
    
    print(f"🧪 Testing Compliance Discovery System for {vendor_domain}")
    print("=" * 60)
    
    # Test data
    test_payload = {
        "vendor_domain": vendor_domain,
        "frameworks": ["gdpr", "hipaa", "pci-dss", "ccpa"]
    }
    
    # Test if server is running
    try:
        health_response = requests.get("http://127.0.0.1:8026/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Server is running and healthy")
        else:
            print("❌ Server health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not running: {e}")
        print("Please start the server first with: python src/api/web_app.py")
        return False
    
    # Test compliance discovery endpoint
    try:
        print(f"\n🔍 Testing compliance discovery for {vendor_domain}...")
        
        response = requests.post(
            "http://127.0.0.1:8026/find-compliance-documents",
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Compliance discovery API responded successfully")
            
            # Analyze results
            if result.get("success"):
                compliance_results = result.get("compliance_results", {})
                trust_centers = compliance_results.get("trust_centers", [])
                compliance_docs = compliance_results.get("compliance_documents", [])
                frameworks_found = compliance_results.get("frameworks_found", [])
                
                print(f"\n📊 Discovery Results:")
                print(f"   Trust Centers Found: {len(trust_centers)}")
                print(f"   Compliance Documents: {len(compliance_docs)}")
                print(f"   Frameworks Detected: {frameworks_found}")
                
                # Show trust centers
                if trust_centers:
                    print(f"\n🏢 Trust Centers:")
                    for tc in trust_centers[:3]:  # Show top 3
                        print(f"   - {tc['url']} (score: {tc.get('trust_score', 0):.2f})")
                
                # Show compliance documents
                if compliance_docs:
                    print(f"\n📄 Compliance Documents:")
                    for doc in compliance_docs[:5]:  # Show top 5
                        framework = doc.get('framework', 'unknown')
                        confidence = doc.get('confidence', 0)
                        url = doc.get('source_url', 'N/A')
                        print(f"   - {framework.upper()}: {url} (confidence: {confidence:.2f})")
                
                # Test if View button URLs are accessible
                print(f"\n🔗 Testing URL Accessibility:")
                accessible_count = 0
                for doc in compliance_docs[:3]:  # Test top 3
                    url = doc.get('source_url')
                    if url:
                        try:
                            test_response = requests.head(url, timeout=5, allow_redirects=True)
                            if test_response.status_code < 400:
                                print(f"   ✅ {url} - Accessible")
                                accessible_count += 1
                            else:
                                print(f"   ⚠️  {url} - Status {test_response.status_code}")
                        except:
                            print(f"   ❌ {url} - Not accessible")
                
                print(f"\n📈 Summary:")
                print(f"   - Total documents found: {len(compliance_docs)}")
                print(f"   - Accessible URLs: {accessible_count}/{min(len(compliance_docs), 3)}")
                print(f"   - Frameworks covered: {len(frameworks_found)}/{len(test_payload['frameworks'])}")
                
                return True
            else:
                print(f"❌ Discovery failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_ui_labels():
    """Test that UI labels are correct (no AI prefixes)"""
    
    print(f"\n🎨 Testing UI Labels")
    print("=" * 40)
    
    try:
        # Read the combined UI file
        ui_file_path = "src/api/static/combined-ui.html"
        if os.path.exists(ui_file_path):
            with open(ui_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for incorrect AI prefixes
            ai_data_flow = "AI Data Flow Documentation Discovery" in content
            ai_compliance = "AI Compliance Documentation Discovery" in content
            
            # Check for correct labels
            correct_data_flow = "Data Flow Documentation Discovery" in content
            correct_compliance = "Compliance Documentation Discovery" in content
            
            print(f"❌ Found 'AI Data Flow Documentation Discovery': {ai_data_flow}")
            print(f"❌ Found 'AI Compliance Documentation Discovery': {ai_compliance}")
            print(f"✅ Found 'Data Flow Documentation Discovery': {correct_data_flow}")
            print(f"✅ Found 'Compliance Documentation Discovery': {correct_compliance}")
            
            if not ai_data_flow and not ai_compliance and correct_data_flow and correct_compliance:
                print("\n✅ All UI labels are correct!")
                return True
            else:
                print("\n⚠️  Some UI labels need attention")
                return False
        else:
            print(f"❌ UI file not found: {ui_file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking UI labels: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🚀 Vendor Risk Assessment - Compliance System Test")
    print("=" * 60)
    print(f"Started at: {datetime.now().isoformat()}")
    
    # Test UI labels
    ui_test_passed = test_ui_labels()
    
    # Test compliance system with a well-known vendor
    compliance_test_passed = test_compliance_discovery("github.com")
    
    print(f"\n🏁 Test Results Summary")
    print("=" * 40)
    print(f"UI Labels Test: {'✅ PASSED' if ui_test_passed else '❌ FAILED'}")
    print(f"Compliance Discovery Test: {'✅ PASSED' if compliance_test_passed else '❌ FAILED'}")
    
    if ui_test_passed and compliance_test_passed:
        print(f"\n🎉 All tests passed! The system is working correctly.")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)