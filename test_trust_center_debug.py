#!/usr/bin/env python3

"""Debug script to test trust center discovery"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from api.web_app import DynamicComplianceDiscovery
    print("✅ Successfully imported DynamicComplianceDiscovery")
    
    # Test creating an instance
    scanner = DynamicComplianceDiscovery()
    print("✅ Successfully created DynamicComplianceDiscovery instance")
    print(f"Trust center indicators: {scanner.trust_center_indicators[:3]}")
    
except Exception as e:
    print(f"❌ Error importing or using DynamicComplianceDiscovery: {e}")
    import traceback
    traceback.print_exc()

# Test the discovery function
try:
    import asyncio
    
    async def test_discovery():
        scanner = DynamicComplianceDiscovery()
        result = await scanner._discover_trust_centers("atlassian.com")
        print(f"✅ Trust center discovery result: {result}")
    
    print("\n🔍 Testing trust center discovery...")
    asyncio.run(test_discovery())
    
except Exception as e:
    print(f"❌ Error during discovery test: {e}")
    import traceback
    traceback.print_exc()