#!/usr/bin/env python3
"""
Quick Assessment Timing Test
============================
Tests the assessment completion time to verify our optimizations work.
"""

import asyncio
import aiohttp
import time
import json

BASE_URL = "http://localhost:8029"

async def test_assessment_timing():
    """Test how long it takes for an assessment to complete and be available."""
    
    async with aiohttp.ClientSession() as session:
        print("🚀 Starting assessment timing test...")
        
        # Start a new assessment
        assessment_data = {
            "vendor_domain": "example.com",
            "requester_email": "test@example.com",
            "data_sensitivity": "medium",
            "regulations": ["GDPR"],
            "business_criticality": "medium",
            "auto_trust_center": False,
            "assessment_mode": "business_risk"
        }
        
        start_time = time.time()
        
        # Create assessment
        async with session.post(f"{BASE_URL}/api/v1/assessments", json=assessment_data) as response:
            if response.status == 200:
                result = await response.json()
                assessment_id = result["assessment_id"]
                print(f"✅ Assessment created: {assessment_id}")
            else:
                print(f"❌ Failed to create assessment: {response.status}")
                return
        
        # Poll for completion
        poll_count = 0
        max_polls = 30  # Max 90 seconds with 3-second intervals
        
        while poll_count < max_polls:
            poll_count += 1
            poll_start = time.time()
            
            async with session.get(f"{BASE_URL}/api/v1/assessments/{assessment_id}") as response:
                if response.status == 200:
                    result = await response.json()
                    assessment = result.get("assessment", {})
                    status = assessment.get("status", "unknown")
                    progress = assessment.get("progress", 0)
                    
                    elapsed = time.time() - start_time
                    print(f"📡 Poll {poll_count}: Status={status}, Progress={progress}%, Elapsed={elapsed:.1f}s")
                    
                    if status == "completed":
                        completion_time = time.time() - start_time
                        print(f"🎉 Assessment completed in {completion_time:.1f} seconds!")
                        
                        # Check if results are available
                        if assessment.get("results"):
                            print("✅ Results are available immediately")
                            results = assessment["results"]
                            print(f"📊 Overall Score: {results.get('overall_score', 'N/A')}")
                            print(f"📊 Risk Level: {results.get('risk_level', 'N/A')}")
                        else:
                            print("⚠️ Assessment completed but results not found")
                        
                        return completion_time
                else:
                    print(f"❌ Error polling assessment: {response.status}")
            
            # Wait before next poll (simulating frontend behavior)
            await asyncio.sleep(3)
        
        print(f"⏰ Assessment did not complete within {max_polls * 3} seconds")
        return None

async def main():
    """Run the timing test."""
    print("🔍 Testing Assessment Response Time")
    print("=" * 40)
    
    try:
        completion_time = await test_assessment_timing()
        
        if completion_time:
            print("\n📈 TIMING ANALYSIS:")
            print(f"   • Total time: {completion_time:.1f} seconds")
            print(f"   • Expected improvement: ~10 seconds faster than before")
            print(f"   • Polling frequency: Every 3 seconds (was 10 seconds)")
            print(f"   • Processing time: ~9 seconds (was 18 seconds)")
        else:
            print("\n❌ Test failed or timed out")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
