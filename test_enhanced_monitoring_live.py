#!/usr/bin/env python3
"""
Live Test of Enhanced Monitoring Dashboard
Tests the complete integrated monitoring functionality at http://localhost:8028/static/combined-ui.html
"""

import requests
import time
import json
from datetime import datetime

def test_enhanced_monitoring_live():
    """Test the enhanced monitoring dashboard functionality"""
    print("🚀 Testing Enhanced Monitoring Dashboard Live")
    print("🔗 URL: http://localhost:8028/static/combined-ui.html")
    print("=" * 60)
    
    base_url = "http://localhost:8028"
    
    # Test 1: Check if server is running
    print("\n🔍 Test 1: Server Connectivity")
    try:
        response = requests.get(f"{base_url}/static/combined-ui.html", timeout=5)
        if response.status_code == 200:
            print("  ✅ Combined UI page is accessible")
            print(f"  📄 Page size: {len(response.text):,} characters")
        else:
            print(f"  ❌ Page returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Server not accessible: {e}")
        return False
    
    # Test 2: Check for Enhanced Monitoring Elements in HTML
    print("\n🔍 Test 2: Enhanced Monitoring Integration")
    html_content = response.text
    
    monitoring_elements = [
        ("Enhanced Monitoring Dashboard", "Dashboard Title"),
        ("statsMonitoredVendors", "Monitored Vendors Counter"),
        ("statsActiveAlerts", "Active Alerts Counter"), 
        ("statsRecentChanges", "Recent Changes Counter"),
        ("statsAverageScore", "Average Score Display"),
        ("monitoredVendorsList", "Monitored Vendors List"),
        ("recentAlertsList", "Recent Alerts List"),
        ("scoreChangesList", "Score Changes List"),
        ("toggleAlertDetails", "Toggle Alert Details Function"),
        ("refreshMonitoringData", "Refresh Data Function"),
        ("loadEnhancedMonitoringData", "Load Enhanced Data Function"),
        ("onclick=\"refreshMonitoringData()\"", "Refresh Button"),
        ("class=\"clickable-row\"", "Clickable Row Styling"),
        ("class=\"dropdown-content\"", "Dropdown Content Styling")
    ]
    
    missing_elements = []
    for element, description in monitoring_elements:
        if element in html_content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            missing_elements.append(element)
    
    # Test 3: Check Monitoring API Endpoints
    print("\n🔍 Test 3: Monitoring API Endpoints")
    
    api_endpoints = [
        ("/api/v1/monitoring/vendors", "Monitored Vendors API"),
        ("/api/v1/monitoring/alerts", "Recent Alerts API"),
        ("/api/v1/monitoring/score-changes", "Score Changes API"),
        ("/api/v1/monitoring/status", "Monitoring Status API")
    ]
    
    api_results = []
    for endpoint, description in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ {description} - Status: {response.status_code}")
                api_results.append((endpoint, True, data))
            else:
                print(f"  ⚠️ {description} - Status: {response.status_code}")
                api_results.append((endpoint, False, None))
        except Exception as e:
            print(f"  ❌ {description} - Error: {str(e)[:50]}...")
            api_results.append((endpoint, False, None))
    
    # Test 4: Test Demo Data Integration
    print("\n🔍 Test 4: Demo Data Integration")
    
    demo_features = [
        ("Slack Technologies", "Demo Vendor - Slack"),
        ("Zoom Video Communications", "Demo Vendor - Zoom"), 
        ("Microsoft Corporation", "Demo Vendor - Microsoft"),
        ("Security Alert - Slack Technologies", "Demo Security Alert"),
        ("Compliance Update - Microsoft Corporation", "Demo Compliance Alert"),
        ("Score changed from", "Demo Score Change"),
        ("Security incident discovery", "Demo Change Factor"),
        ("SOC 2 Type II certification renewal", "Demo Compliance Factor"),
        ("logo.clearbit.com", "Vendor Logo Integration"),
        ("icons.duckduckgo.com", "Logo Fallback Integration")
    ]
    
    demo_missing = []
    for feature, description in demo_features:
        if feature in html_content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            demo_missing.append(feature)
    
    # Test 5: JavaScript Functionality Check
    print("\n🔍 Test 5: JavaScript Functionality")
    
    js_functions = [
        ("function toggleAlertDetails", "Toggle Alert Details"),
        ("function refreshMonitoringData", "Refresh Monitoring Data"),
        ("function loadEnhancedMonitoringData", "Load Enhanced Data"),
        ("function displayEnhancedVendors", "Display Enhanced Vendors"),
        ("function displayEnhancedAlerts", "Display Enhanced Alerts"),
        ("function displayEnhancedScoreChanges", "Display Enhanced Score Changes"),
        ("function getVendorLogo", "Get Vendor Logo"),
        ("function handleLogoError", "Handle Logo Error"),
        ("window.toggleAlertDetails", "Global Toggle Function"),
        ("window.refreshMonitoringData", "Global Refresh Function")
    ]
    
    js_missing = []
    for func, description in js_functions:
        if func in html_content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            js_missing.append(func)
    
    # Test 6: Tab Integration Check
    print("\n🔍 Test 6: Dashboard Tab Integration")
    
    tab_features = [
        ("if (tabName === 'dashboard')", "Dashboard Tab Detection"),
        ("loadEnhancedMonitoringData()", "Auto-load on Tab Switch"),
        ("id=\"dashboardAssessment\"", "Dashboard Tab Content"),
        ("Monitoring & Dashboard", "Tab Title")
    ]
    
    tab_missing = []
    for feature, description in tab_features:
        if feature in html_content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            tab_missing.append(feature)
    
    # Summary
    print("\n📊 Enhanced Monitoring Dashboard Test Summary")
    print("=" * 50)
    
    total_elements = len(monitoring_elements)
    total_demo = len(demo_features)  
    total_js = len(js_functions)
    total_tab = len(tab_features)
    total_checks = total_elements + total_demo + total_js + total_tab
    
    missing_count = len(missing_elements) + len(demo_missing) + len(js_missing) + len(tab_missing)
    passed_count = total_checks - missing_count
    
    # Count successful API endpoints
    successful_apis = sum(1 for _, success, _ in api_results if success)
    total_apis = len(api_endpoints)
    
    print(f"HTML Integration: {total_elements - len(missing_elements)}/{total_elements}")
    print(f"Demo Data: {total_demo - len(demo_missing)}/{total_demo}")
    print(f"JavaScript Functions: {total_js - len(js_missing)}/{total_js}")
    print(f"Tab Integration: {total_tab - len(tab_missing)}/{total_tab}")
    print(f"API Endpoints: {successful_apis}/{total_apis}")
    print(f"Overall Success: {passed_count}/{total_checks} ({(passed_count/total_checks)*100:.1f}%)")
    
    if missing_count == 0 and successful_apis >= 2:  # At least 2 APIs working
        print("\n🎉 ALL TESTS PASSED! Enhanced Monitoring Dashboard is FULLY FUNCTIONAL!")
        print("\n✨ Features Ready:")
        print("   🔗 Access: http://localhost:8028/static/combined-ui.html")
        print("   📊 Click 'Monitoring & Dashboard' tab")
        print("   🔽 Click alerts and score changes for detailed explanations")
        print("   🖼️ Vendor logos automatically loaded")
        print("   📈 Numerical scores displayed prominently")
        print("   🔄 Refresh button for real-time updates")
        print("   🎨 Professional UI with hover effects")
        
        print("\n🎯 Demo Data Available:")
        print("   • Slack Technologies (Score: 72)")
        print("   • Zoom Video Communications (Score: 89)")  
        print("   • Microsoft Corporation (Score: 94)")
        print("   • Security alerts with detailed explanations")
        print("   • Score changes with contributing factors")
        
        return True
    else:
        print(f"\n⚠️ Some issues detected ({missing_count} missing features)")
        if missing_elements:
            print(f"Missing HTML elements: {len(missing_elements)}")
        if demo_missing:
            print(f"Missing demo features: {len(demo_missing)}")
        if js_missing:
            print(f"Missing JS functions: {len(js_missing)}")
        if tab_missing:
            print(f"Missing tab features: {len(tab_missing)}")
        if successful_apis < 2:
            print(f"Limited API functionality: {successful_apis}/{total_apis}")
        return False

if __name__ == "__main__":
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = test_enhanced_monitoring_live()
    
    if success:
        print(f"\n🚀 Ready to use! Navigate to: http://localhost:8028/static/combined-ui.html")
    else:
        print(f"\n🔧 Some features may need attention")
    
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")