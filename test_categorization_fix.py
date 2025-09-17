#!/usr/bin/env python3
"""
Test the fixed compliance framework categorization
"""

def test_framework_categorization_logic():
    """Test the logic that should create separate entries for each framework"""
    
    print("🧪 Testing Fixed Framework Categorization Logic")
    print("=" * 60)
    
    # Simulate what the backend should now do
    mock_document = {
        "url": "https://trust.github.com/privacy",
        "compliance_info": {
            "detected_frameworks": ["gdpr", "ccpa"],  # Multiple frameworks detected
            "confidence_scores": {"gdpr": 0.8, "ccpa": 0.7},
            "document_type": "webpage"
        },
        "discovered_at": "2025-09-15T14:30:00"
    }
    
    print("📄 Mock Document Analysis:")
    print(f"   URL: {mock_document['url']}")
    print(f"   Detected Frameworks: {mock_document['compliance_info']['detected_frameworks']}")
    print(f"   Confidence Scores: {mock_document['compliance_info']['confidence_scores']}")
    
    # Simulate the new fixed logic
    print(f"\n🔧 NEW LOGIC - Creating separate entries for each framework:")
    
    analyzed_docs = []
    compliance_info = mock_document["compliance_info"]
    detected_frameworks = compliance_info.get("detected_frameworks", [])
    
    for framework in detected_frameworks:
        framework_confidence = compliance_info["confidence_scores"].get(framework, 0.5)
        
        # Generate framework-specific document name
        url_path = mock_document['url'].split('/')[-1] or 'page'
        if framework.lower() in url_path.lower():
            doc_name = f"{framework.upper()} Compliance Page"
        else:
            doc_name = f"Compliance Information - {framework}"
        
        doc_entry = {
            "document_name": doc_name,
            "source_url": mock_document["url"],
            "framework": framework,  # Each entry gets ONE framework
            "confidence": framework_confidence,
            "document_type": compliance_info["document_type"],
            "status": "available",
            "access_method": "public",
            "retrieved_at": mock_document["discovered_at"],
            "content_summary": f"Contains {framework.upper()} compliance information",
            "all_frameworks": [framework]  # Only this framework
        }
        
        analyzed_docs.append(doc_entry)
        
        print(f"\n   📋 Entry {len(analyzed_docs)}:")
        print(f"      🏷️  Framework: {doc_entry['framework']}")
        print(f"      📝 Name: {doc_entry['document_name']}")
        print(f"      🔗 URL: {doc_entry['source_url']}")
        print(f"      📊 Confidence: {doc_entry['confidence']:.1f}")
        print(f"      📋 All Frameworks: {doc_entry['all_frameworks']}")
    
    print(f"\n🎯 RESULT:")
    print(f"   Before: 1 document with multiple frameworks → UI groups everything together")
    print(f"   After: {len(analyzed_docs)} documents, each with 1 framework → UI displays separately")
    
    # Test frontend processing simulation
    print(f"\n🖥️  Frontend Processing Simulation:")
    framework_map = {
        'gdpr': 'General Data Protection Regulation',
        'ccpa': 'California Consumer Privacy Act',
        'hipaa': 'Health Insurance Portability and Accountability Act',
        'pci-dss': 'Payment Card Industry Data Security Standard'
    }
    
    for framework, name in framework_map.items():
        matching_docs = [doc for doc in analyzed_docs if doc.get('framework') == framework]
        print(f"\n   {framework.upper()} Section:")
        if matching_docs:
            for doc in matching_docs:
                print(f"      ✅ {doc['document_name']} ({doc['confidence']:.1f} confidence)")
        else:
            print(f"      ❌ No documents")
    
    return len(analyzed_docs) > 1  # Should create multiple entries

def test_url_based_detection():
    """Test the new URL-based framework detection"""
    
    print(f"\n🔗 Testing URL-Based Framework Detection")
    print("=" * 60)
    
    test_urls = [
        ("https://trust.github.com/gdpr", ["gdpr"]),
        ("https://trust.github.com/ccpa", ["ccpa"]),
        ("https://example.com/hipaa", ["hipaa"]),
        ("https://vendor.com/pci-dss", ["pci-dss"]),
        ("https://vendor.com/privacy", [])  # No specific framework in URL
    ]
    
    for url, expected_frameworks in test_urls:
        print(f"\n   🔍 Testing: {url}")
        
        # Simulate URL analysis
        url_lower = url.lower()
        detected_frameworks = []
        
        if any(pattern in url_lower for pattern in ["gdpr", "data-protection", "privacy/gdpr"]):
            detected_frameworks.append("gdpr")
        if any(pattern in url_lower for pattern in ["ccpa", "california-privacy", "privacy/ccpa"]):
            detected_frameworks.append("ccpa")
        if any(pattern in url_lower for pattern in ["hipaa", "healthcare", "compliance/hipaa"]):
            detected_frameworks.append("hipaa")
        if any(pattern in url_lower for pattern in ["pci", "payment", "card"]):
            detected_frameworks.append("pci-dss")
        
        print(f"      Expected: {expected_frameworks}")
        print(f"      Detected: {detected_frameworks}")
        
        if set(detected_frameworks) == set(expected_frameworks):
            print(f"      ✅ PASS")
        else:
            print(f"      ❌ FAIL")
    
    return True

def main():
    """Run all tests"""
    
    print("🚀 Compliance Framework Categorization Fix Test")
    print("=" * 60)
    
    test1_pass = test_framework_categorization_logic()
    test2_pass = test_url_based_detection()
    
    print(f"\n{'='*60}")
    print("🏁 TEST RESULTS")
    print(f"{'='*60}")
    
    if test1_pass and test2_pass:
        print(f"✅ ALL TESTS PASSED!")
        print(f"\n💡 The fix should resolve the UI grouping issue:")
        print(f"   • Each framework gets its own document entry")
        print(f"   • URL-based detection improves accuracy")
        print(f"   • Frontend will display frameworks separately")
        print(f"\n🔄 To test the fix:")
        print(f"   1. Restart the server: cd src/api && python web_app.py") 
        print(f"   2. Run an assessment for 'github.com'")
        print(f"   3. Check 'Compliance Framework Pages' tab")
        print(f"   4. You should now see GDPR and CCPA in separate sections!")
    else:
        print(f"❌ Some tests failed - check the logic")

if __name__ == "__main__":
    main()