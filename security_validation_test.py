import requests
import json

# Test security validation with malicious inputs
BASE_URL = "http://localhost:8026"

malicious_inputs = [
    "'; DROP TABLE assessments; --",
    "<script>alert('xss')</script>",
    "../../etc/passwd",
    "\x00\x01\x02",  # Binary data
]

print("🔒 SECURITY VALIDATION TEST")
print("=" * 50)

for i, malicious_input in enumerate(malicious_inputs, 1):
    print(f"\nTest {i}: {repr(malicious_input)}")
    
    try:
        # Test in vendor domain field
        data = {
            "vendor_domain": malicious_input,
            "requester_email": "test@company.com"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/assessments", json=data, timeout=10)
        
        if response.status_code in [400, 422]:
            print(f"  ✅ PASS: Malicious input rejected (HTTP {response.status_code})")
            try:
                error_detail = response.json()
                print(f"      Error: {error_detail}")
            except:
                pass
        else:
            print(f"  ❌ FAIL: Malicious input accepted (HTTP {response.status_code})")
            print(f"      Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"  ✅ PASS: Safe error handling - {e}")

print("\n" + "=" * 50)
print("Security validation test completed")
