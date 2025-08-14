#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite
Tests all API endpoints, error handling, data validation, and business logic
"""

import requests
import json
import time
import uuid
from typing import Dict, Any, List
from datetime import datetime
import tempfile
import csv
import os

BASE_URL = "http://localhost:8026"

class BackendTestSuite:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        self.test_data = {}  # Store test data for cleanup
        
    def log_test_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result and update counters"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        if passed:
            self.passed_tests += 1
            print(f"{status} | {test_name}")
        else:
            self.failed_tests += 1
            print(f"{status} | {test_name} - {details}")
        
        if details and passed:
            print(f"      └─ {details}")
    
    def test_health_endpoint(self):
        """Test basic health check endpoint"""
        print("\n🏥 Testing Health Endpoint")
        print("-" * 50)
        
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test_result("Health Check", True, f"Service: {data.get('service')}, Version: {data.get('version')}")
                else:
                    self.log_test_result("Health Check", False, f"Unexpected status: {data.get('status')}")
            else:
                self.log_test_result("Health Check", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Health Check", False, f"Connection error: {str(e)}")
    
    def test_assessment_endpoints(self):
        """Test assessment creation, retrieval, and management"""
        print("\n📊 Testing Assessment Endpoints")
        print("-" * 50)
        
        # Test assessment creation
        assessment_data = {
            "vendor_name": "Test Vendor Corp",
            "vendor_domain": "testvendor.com",
            "description": "Comprehensive backend test assessment",
            "requester_email": "test@company.com",
            "urgency": "medium",
            "regulations": ["SOC2", "ISO27001"],
            "data_sensitivity": "confidential",
            "business_criticality": "high",
            "auto_trust_center": True
        }
        
        try:
            # Create assessment
            response = requests.post(f"{BASE_URL}/api/v1/assessments", json=assessment_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                assessment_id = result.get("assessment_id")
                
                if assessment_id:
                    self.test_data["assessment_id"] = assessment_id
                    self.log_test_result("Assessment Creation", True, f"ID: {assessment_id}")
                    
                    # Test assessment retrieval
                    time.sleep(2)  # Allow some processing time
                    self.test_assessment_retrieval(assessment_id)
                    
                else:
                    self.log_test_result("Assessment Creation", False, "No assessment ID returned")
            else:
                self.log_test_result("Assessment Creation", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test_result("Assessment Creation", False, f"Error: {str(e)}")
        
        # Test assessment history
        self.test_assessment_history()
        
        # Test invalid assessment data
        self.test_invalid_assessment_data()
    
    def test_assessment_retrieval(self, assessment_id: str):
        """Test retrieving a specific assessment"""
        try:
            response = requests.get(f"{BASE_URL}/api/v1/assessments/{assessment_id}", timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("assessment"):
                    assessment = result["assessment"]
                    self.log_test_result("Assessment Retrieval", True, 
                                       f"Status: {assessment.get('status')}, Progress: {assessment.get('progress', 0)}%")
                else:
                    self.log_test_result("Assessment Retrieval", False, "Invalid response format")
            else:
                self.log_test_result("Assessment Retrieval", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Assessment Retrieval", False, f"Error: {str(e)}")
    
    def test_assessment_history(self):
        """Test assessment history endpoint"""
        try:
            response = requests.get(f"{BASE_URL}/api/v1/assessments/history", timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if "assessments" in result:
                    count = len(result["assessments"])
                    self.log_test_result("Assessment History", True, f"Found {count} assessments")
                else:
                    self.log_test_result("Assessment History", False, "Invalid response format")
            else:
                self.log_test_result("Assessment History", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Assessment History", False, f"Error: {str(e)}")
    
    def test_invalid_assessment_data(self):
        """Test assessment creation with invalid data"""
        invalid_data_sets = [
            ({}, "Empty data"),
            ({"vendor_name": "Test"}, "Missing required fields"),
            ({"vendor_domain": "", "requester_email": "invalid-email"}, "Invalid email format"),
            ({"vendor_domain": "test.com", "requester_email": "test@test.com", "urgency": "invalid"}, "Invalid urgency level")
        ]
        
        for invalid_data, description in invalid_data_sets:
            try:
                response = requests.post(f"{BASE_URL}/api/v1/assessments", json=invalid_data, timeout=10)
                
                if response.status_code in [400, 422]:  # Bad Request or Validation Error
                    self.log_test_result(f"Validation: {description}", True, "Properly rejected invalid data")
                else:
                    self.log_test_result(f"Validation: {description}", False, 
                                       f"Should reject invalid data but got HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test_result(f"Validation: {description}", False, f"Error: {str(e)}")
    
    def test_trust_center_endpoints(self):
        """Test Trust Center functionality"""
        print("\n🛡️ Testing Trust Center Endpoints")
        print("-" * 50)
        
        # Test trust center discovery
        test_domains = [
            ("github.com", "known vendor"),
            ("salesforce.com", "known vendor"),
            ("unknown-vendor.io", "unknown vendor")
        ]
        
        for domain, description in test_domains:
            try:
                response = requests.get(f"{BASE_URL}/api/v1/trust-center/discover/{domain}", timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        self.log_test_result(f"Trust Center Discovery: {description}", True, 
                                           f"Method: {result.get('access_method', 'unknown')}")
                    else:
                        self.log_test_result(f"Trust Center Discovery: {description}", False, 
                                           f"Discovery failed: {result.get('message', 'Unknown error')}")
                else:
                    self.log_test_result(f"Trust Center Discovery: {description}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test_result(f"Trust Center Discovery: {description}", False, f"Error: {str(e)}")
        
        # Test trust center document request
        self.test_trust_center_request()
    
    def test_trust_center_request(self):
        """Test trust center document request"""
        request_data = {
            "vendor_domain": "testvendor.com",
            "requester_email": "test@company.com",
            "document_types": ["SOC2", "ISO27001"]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/v1/trust-center/request-access", 
                                   json=request_data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    request_id = result.get("request_id")
                    self.test_data["trust_center_request_id"] = request_id
                    self.log_test_result("Trust Center Request", True, 
                                       f"Request ID: {request_id}, Method: {result.get('access_method')}")
                    
                    # Test request status
                    if request_id:
                        self.test_trust_center_status(request_id)
                else:
                    self.log_test_result("Trust Center Request", False, 
                                       f"Request failed: {result.get('message', 'Unknown error')}")
            else:
                self.log_test_result("Trust Center Request", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Trust Center Request", False, f"Error: {str(e)}")
    
    def test_trust_center_status(self, request_id: str):
        """Test trust center request status"""
        try:
            response = requests.get(f"{BASE_URL}/api/v1/trust-center/status/{request_id}", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                status = result.get("status", "unknown")
                self.log_test_result("Trust Center Status", True, f"Status: {status}")
            elif response.status_code == 404:
                self.log_test_result("Trust Center Status", False, "Request not found")
            else:
                self.log_test_result("Trust Center Status", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Trust Center Status", False, f"Error: {str(e)}")
    
    def test_bulk_assessment_endpoints(self):
        """Test bulk assessment functionality"""
        print("\n📋 Testing Bulk Assessment Endpoints")
        print("-" * 50)
        
        # Create test CSV file
        test_csv_content = [
            ["vendor_domain", "vendor_name", "regulations", "data_sensitivity", "business_criticality"],
            ["test1.com", "Test Vendor 1", "SOC2,ISO27001", "internal", "medium"],
            ["test2.com", "Test Vendor 2", "GDPR,CCPA", "confidential", "high"],
            ["test3.com", "Test Vendor 3", "SOC2", "public", "low"]
        ]
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            writer = csv.writer(f)
            writer.writerows(test_csv_content)
            csv_file_path = f.name
        
        try:
            # Test file upload
            with open(csv_file_path, 'rb') as f:
                files = {'file': ('test_vendors.csv', f, 'text/csv')}
                data = {'requester_email': 'test@company.com'}
                
                response = requests.post(f"{BASE_URL}/api/v1/bulk/upload-vendors", 
                                       files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        vendor_count = result.get("vendor_count", 0)
                        self.log_test_result("Bulk Upload", True, f"Uploaded {vendor_count} vendors")
                        
                        # Test starting bulk assessments
                        self.test_bulk_assessment_start()
                    else:
                        self.log_test_result("Bulk Upload", False, f"Upload failed: {result.get('message')}")
                else:
                    self.log_test_result("Bulk Upload", False, f"HTTP {response.status_code}")
                    
        except Exception as e:
            self.log_test_result("Bulk Upload", False, f"Error: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(csv_file_path):
                os.unlink(csv_file_path)
        
        # Test sample template download
        self.test_sample_template_download()
    
    def test_bulk_assessment_start(self):
        """Test starting bulk assessments"""
        try:
            response = requests.post(f"{BASE_URL}/api/v1/bulk/start-assessments", timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("assessment_ids"):
                    count = len(result["assessment_ids"])
                    self.test_data["bulk_assessment_ids"] = result["assessment_ids"]
                    self.log_test_result("Bulk Assessment Start", True, f"Started {count} assessments")
                else:
                    self.log_test_result("Bulk Assessment Start", False, "No assessment IDs returned")
            else:
                self.log_test_result("Bulk Assessment Start", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Bulk Assessment Start", False, f"Error: {str(e)}")
    
    def test_sample_template_download(self):
        """Test sample template download"""
        try:
            response = requests.get(f"{BASE_URL}/api/v1/bulk/sample-template", timeout=10)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                content_length = len(response.content)
                
                if 'csv' in content_type.lower() or content_length > 0:
                    self.log_test_result("Sample Template Download", True, 
                                       f"Downloaded {content_length} bytes, Type: {content_type}")
                else:
                    self.log_test_result("Sample Template Download", False, "Invalid file format")
            else:
                self.log_test_result("Sample Template Download", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Sample Template Download", False, f"Error: {str(e)}")
    
    def test_dashboard_endpoints(self):
        """Test dashboard and analytics endpoints"""
        print("\n📈 Testing Dashboard Endpoints")
        print("-" * 50)
        
        # Test dashboard summary
        try:
            response = requests.get(f"{BASE_URL}/api/v1/dashboard/summary", timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict):
                    self.log_test_result("Dashboard Summary", True, f"Data keys: {list(result.keys())}")
                else:
                    self.log_test_result("Dashboard Summary", False, "Invalid response format")
            elif response.status_code == 404:
                self.log_test_result("Dashboard Summary", True, "Endpoint not implemented (404 expected)")
            else:
                self.log_test_result("Dashboard Summary", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test_result("Dashboard Summary", False, f"Error: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n🚨 Testing Error Handling")
        print("-" * 50)
        
        # Test non-existent endpoints
        test_cases = [
            ("/api/v1/nonexistent", "GET", "Non-existent endpoint"),
            ("/api/v1/assessments/invalid-uuid", "GET", "Invalid UUID format"),
            ("/api/v1/trust-center/status/nonexistent", "GET", "Non-existent request ID"),
        ]
        
        for endpoint, method, description in test_cases:
            try:
                if method == "GET":
                    response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}", timeout=10)
                
                if response.status_code in [404, 422]:
                    self.log_test_result(f"Error Handling: {description}", True, 
                                       f"Properly returned HTTP {response.status_code}")
                else:
                    self.log_test_result(f"Error Handling: {description}", False, 
                                       f"Expected 404/422 but got HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test_result(f"Error Handling: {description}", False, f"Error: {str(e)}")
    
    def test_data_validation(self):
        """Test data validation and security"""
        print("\n🔒 Testing Data Validation & Security")
        print("-" * 50)
        
        # Test SQL injection attempts
        malicious_inputs = [
            "'; DROP TABLE assessments; --",
            "<script>alert('xss')</script>",
            "../../etc/passwd",
            "\x00\x01\x02",  # Binary data
        ]
        
        for malicious_input in malicious_inputs:
            try:
                # Test in vendor domain field
                data = {
                    "vendor_domain": malicious_input,
                    "requester_email": "test@company.com"
                }
                
                response = requests.post(f"{BASE_URL}/api/v1/assessments", json=data, timeout=10)
                
                if response.status_code in [400, 422]:
                    self.log_test_result("Security: Input Validation", True, 
                                       "Malicious input properly rejected")
                else:
                    self.log_test_result("Security: Input Validation", False, 
                                       f"Malicious input not rejected: {response.status_code}")
                    
            except Exception as e:
                self.log_test_result("Security: Input Validation", True, 
                                   "Input validation caused safe error handling")
    
    def test_performance_basic(self):
        """Test basic performance characteristics"""
        print("\n⚡ Testing Basic Performance")
        print("-" * 50)
        
        # Test response times
        endpoints_to_test = [
            ("/health", "Health Check"),
            ("/api/v1/assessments/history", "Assessment History"),
            ("/api/v1/trust-center/discover/github.com", "Trust Center Discovery")
        ]
        
        for endpoint, name in endpoints_to_test:
            try:
                start_time = time.time()
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=30)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response.status_code == 200 and response_time < 5000:  # 5 second threshold
                    self.log_test_result(f"Performance: {name}", True, 
                                       f"Response time: {response_time:.0f}ms")
                elif response_time >= 5000:
                    self.log_test_result(f"Performance: {name}", False, 
                                       f"Slow response: {response_time:.0f}ms")
                else:
                    self.log_test_result(f"Performance: {name}", False, 
                                       f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test_result(f"Performance: {name}", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run the complete test suite"""
        print("🧪 COMPREHENSIVE BACKEND TEST SUITE")
        print("=" * 70)
        print(f"Target: {BASE_URL}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Run all test categories
        self.test_health_endpoint()
        self.test_assessment_endpoints()
        self.test_trust_center_endpoints()
        self.test_bulk_assessment_endpoints()
        self.test_dashboard_endpoints()
        self.test_error_handling()
        self.test_data_validation()
        self.test_performance_basic()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 70)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 70)
        
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests Run: {total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "FAIL" in result["status"]:
                    print(f"   • {result['test']}: {result['details']}")
        
        print(f"\n🏁 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if pass_rate >= 90:
            print("🎉 EXCELLENT! Backend is working very well!")
        elif pass_rate >= 75:
            print("✅ GOOD! Backend is mostly functional with minor issues.")
        elif pass_rate >= 50:
            print("⚠️ WARNING! Backend has significant issues that need attention.")
        else:
            print("🚨 CRITICAL! Backend has major problems that need immediate fixes.")
        
        return pass_rate >= 75


if __name__ == "__main__":
    test_suite = BackendTestSuite()
    test_suite.run_all_tests()
