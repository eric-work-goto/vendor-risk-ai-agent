#!/usr/bin/env python3
"""
Comprehensive Test Suite for Assessment History Functionality
Tests the Assessment History tab, API endpoints, and data persistence
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8026"

class AssessmentHistoryTester:
    """Test suite for Assessment History functionality"""
    
    def __init__(self):
        self.session = None
        self.test_results = []
        
    async def setup_session(self):
        """Setup HTTP session for testing"""
        self.session = aiohttp.ClientSession()
        print("🔧 Test session initialized")
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
        print("🧹 Test session cleaned up")
        
    def log_test(self, test_name, success, message, details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
    async def test_server_health(self):
        """Test if server is running and responsive"""
        try:
            async with self.session.get(f"{BASE_URL}/health") as response:
                if response.status == 200:
                    self.log_test("Server Health", True, "Server is running and responsive")
                    return True
                else:
                    self.log_test("Server Health", False, f"Server returned status {response.status}")
                    return False
        except Exception as e:
            self.log_test("Server Health", False, f"Server not accessible: {str(e)}")
            return False
            
    async def test_assessment_creation(self):
        """Test creating sample assessments for history testing"""
        test_vendors = [
            {"domain": "github.com", "name": "GitHub", "sensitivity": "high"},
            {"domain": "slack.com", "name": "Slack", "sensitivity": "medium"},
            {"domain": "google.com", "name": "Google", "sensitivity": "high"},
            {"domain": "microsoft.com", "name": "Microsoft", "sensitivity": "medium"},
            {"domain": "salesforce.com", "name": "Salesforce", "sensitivity": "high"}
        ]
        
        created_assessments = []
        
        for vendor in test_vendors:
            try:
                payload = {
                    "vendorDomain": vendor["domain"],
                    "vendorName": vendor["name"],
                    "dataSensitivity": vendor["sensitivity"],
                    "businessCriticality": "high",
                    "regulations": ["gdpr", "soc2"]
                }
                
                async with self.session.post(f"{BASE_URL}/api/v1/assessments", 
                                           json=payload) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        assessment_id = result.get("assessment_id")
                        if assessment_id:
                            created_assessments.append({
                                "id": assessment_id,
                                "vendor": vendor["name"]
                            })
                            print(f"   📝 Created assessment for {vendor['name']}: {assessment_id}")
                        else:
                            print(f"   ⚠️ No assessment ID returned for {vendor['name']}")
                    else:
                        print(f"   ❌ Failed to create assessment for {vendor['name']}: {response.status}")
                        
                # Small delay between requests
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Error creating assessment for {vendor['name']}: {str(e)}")
        
        if len(created_assessments) > 0:
            self.log_test("Assessment Creation", True, 
                         f"Created {len(created_assessments)} test assessments", 
                         created_assessments)
            return created_assessments
        else:
            self.log_test("Assessment Creation", False, "Failed to create any test assessments")
            return []
            
    async def test_history_api_endpoint(self):
        """Test the assessment history API endpoint"""
        try:
            async with self.session.get(f"{BASE_URL}/api/v1/assessments/history") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("success"):
                        assessments = data.get("assessments", [])
                        self.log_test("History API Endpoint", True, 
                                     f"Retrieved {len(assessments)} assessments", 
                                     {"count": len(assessments), "data": assessments[:3]})  # Show first 3
                        return assessments
                    else:
                        self.log_test("History API Endpoint", False, 
                                     f"API returned success=false: {data.get('error', 'Unknown error')}")
                        return []
                else:
                    self.log_test("History API Endpoint", False, 
                                 f"HTTP {response.status}: {await response.text()}")
                    return []
                    
        except Exception as e:
            self.log_test("History API Endpoint", False, f"Request failed: {str(e)}")
            return []
            
    async def test_individual_assessment_retrieval(self, assessment_ids):
        """Test retrieving individual assessments"""
        if not assessment_ids:
            self.log_test("Individual Assessment Retrieval", False, "No assessment IDs to test")
            return
            
        successful_retrievals = 0
        
        for assessment_data in assessment_ids[:3]:  # Test first 3
            assessment_id = assessment_data["id"]
            vendor_name = assessment_data["vendor"]
            
            try:
                async with self.session.get(f"{BASE_URL}/api/v1/assessments/{assessment_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            successful_retrievals += 1
                            print(f"   ✅ Retrieved assessment for {vendor_name}")
                        else:
                            print(f"   ❌ Failed to retrieve {vendor_name}: {data.get('error', 'Unknown error')}")
                    else:
                        print(f"   ❌ HTTP {response.status} for {vendor_name}")
                        
            except Exception as e:
                print(f"   ❌ Error retrieving {vendor_name}: {str(e)}")
        
        if successful_retrievals > 0:
            self.log_test("Individual Assessment Retrieval", True, 
                         f"Successfully retrieved {successful_retrievals}/{len(assessment_ids[:3])} assessments")
        else:
            self.log_test("Individual Assessment Retrieval", False, "Failed to retrieve any individual assessments")
            
    async def test_history_data_structure(self, assessments):
        """Test the structure and quality of history data"""
        if not assessments:
            self.log_test("History Data Structure", False, "No assessments to validate")
            return
            
        required_fields = ["id", "vendor_name", "vendor_domain", "status", "created_at"]
        issues = []
        
        for i, assessment in enumerate(assessments[:5]):  # Check first 5
            for field in required_fields:
                if field not in assessment:
                    issues.append(f"Assessment {i+1} missing field: {field}")
                elif assessment[field] is None:
                    issues.append(f"Assessment {i+1} has null {field}")
                    
            # Check vendor name isn't corrupted
            vendor_name = assessment.get("vendor_name", "")
            if any(ord(char) > 127 for char in vendor_name):
                issues.append(f"Assessment {i+1} has non-ASCII characters in vendor_name")
                
        if issues:
            self.log_test("History Data Structure", False, 
                         f"Found {len(issues)} data issues", issues)
        else:
            self.log_test("History Data Structure", True, 
                         f"All {min(5, len(assessments))} assessments have valid structure")
            
    async def test_frontend_accessibility(self):
        """Test that the frontend pages load correctly"""
        pages_to_test = [
            "/",
            "/combined-ui",
            "/index.html"
        ]
        
        accessible_pages = 0
        
        for page in pages_to_test:
            try:
                async with self.session.get(f"{BASE_URL}{page}") as response:
                    if response.status == 200:
                        content = await response.text()
                        if "Assessment History" in content:
                            accessible_pages += 1
                            print(f"   ✅ {page} loads and contains Assessment History")
                        else:
                            print(f"   ⚠️ {page} loads but missing Assessment History content")
                    else:
                        print(f"   ❌ {page} returned status {response.status}")
                        
            except Exception as e:
                print(f"   ❌ Error loading {page}: {str(e)}")
        
        if accessible_pages > 0:
            self.log_test("Frontend Accessibility", True, 
                         f"{accessible_pages}/{len(pages_to_test)} pages accessible with History content")
        else:
            self.log_test("Frontend Accessibility", False, "No pages with Assessment History content found")
            
    async def test_api_performance(self):
        """Test API response times"""
        start_time = time.time()
        
        try:
            async with self.session.get(f"{BASE_URL}/api/v1/assessments/history") as response:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response.status == 200:
                    if response_time < 1000:  # Less than 1 second
                        self.log_test("API Performance", True, 
                                     f"History API responded in {response_time:.2f}ms")
                    else:
                        self.log_test("API Performance", False, 
                                     f"History API slow response: {response_time:.2f}ms")
                else:
                    self.log_test("API Performance", False, 
                                 f"API returned status {response.status}")
                    
        except Exception as e:
            self.log_test("API Performance", False, f"Performance test failed: {str(e)}")
            
    async def run_all_tests(self):
        """Run all Assessment History tests"""
        print("🚀 Starting Assessment History Test Suite")
        print("=" * 60)
        
        await self.setup_session()
        
        try:
            # Test 1: Server Health
            if not await self.test_server_health():
                print("❌ Server not accessible. Stopping tests.")
                return
                
            # Test 2: Create sample assessments
            print("\n📝 Testing Assessment Creation...")
            created_assessments = await self.test_assessment_creation()
            
            # Wait for assessments to process
            if created_assessments:
                print("⏳ Waiting for assessments to process...")
                await asyncio.sleep(10)
            
            # Test 3: History API endpoint
            print("\n📊 Testing History API Endpoint...")
            assessments = await self.test_history_api_endpoint()
            
            # Test 4: Individual assessment retrieval
            print("\n🔍 Testing Individual Assessment Retrieval...")
            await self.test_individual_assessment_retrieval(created_assessments)
            
            # Test 5: Data structure validation
            print("\n🔧 Testing History Data Structure...")
            await self.test_history_data_structure(assessments)
            
            # Test 6: Frontend accessibility
            print("\n🌐 Testing Frontend Accessibility...")
            await self.test_frontend_accessibility()
            
            # Test 7: API performance
            print("\n⚡ Testing API Performance...")
            await self.test_api_performance()
            
        finally:
            await self.cleanup_session()
            
        # Print summary
        self.print_test_summary()
        
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 ASSESSMENT HISTORY TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   • {result['test']}: {result['message']}")
                    
        print("\n🎯 RECOMMENDATIONS:")
        if passed_tests == total_tests:
            print("   🎉 All tests passed! Assessment History is working perfectly.")
        elif passed_tests >= total_tests * 0.8:
            print("   ✅ Assessment History is mostly working. Minor issues to address.")
        else:
            print("   ⚠️ Assessment History needs attention. Multiple issues found.")
            
        print("\n📍 Next Steps:")
        print("   1. Fix any failed tests")
        print("   2. Test Assessment History tab manually in browser")
        print("   3. Verify search and filter functionality")
        print("   4. Test download and view actions")

async def main():
    """Main test execution"""
    tester = AssessmentHistoryTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
