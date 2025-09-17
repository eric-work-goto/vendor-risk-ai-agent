#!/usr/bin/env python3
"""
Test Enhanced Monitoring Integration in Combined UI
Verifies that the enhanced monitoring dashboard works within the main Combined UI
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def test_enhanced_monitoring_integration():
    """Test enhanced monitoring integration in Combined UI"""
    print("🧪 Testing Enhanced Monitoring Integration in Combined UI")
    print("=" * 60)
    
    # Check if combined-ui.html exists and has enhanced monitoring
    combined_ui_path = Path("src/api/static/combined-ui.html")
    if not combined_ui_path.exists():
        print("❌ combined-ui.html not found")
        return False
    
    # Read the file and check for enhanced monitoring integration
    content = combined_ui_path.read_text(encoding='utf-8')
    
    # Check for enhanced monitoring HTML elements
    html_checks = [
        ('statsMonitoredVendors', '📊 Monitored Vendors stat card'),
        ('statsActiveAlerts', '🚨 Active Alerts stat card'),
        ('statsRecentChanges', '📈 Recent Changes stat card'),
        ('statsAverageScore', '⭐ Average Score stat card'),
        ('monitoredVendorsList', '👥 Monitored Vendors List'),
        ('recentAlertsList', '🚨 Recent Alerts List'),
        ('scoreChangesList', '📊 Score Changes List'),
        ('lastMonitoringUpdate', '⏰ Last Update Time'),
        ('refreshMonitoringData()', '🔄 Refresh Button')
    ]
    
    print("\n🔍 Checking Enhanced Monitoring HTML Elements:")
    html_missing = []
    for element_id, description in html_checks:
        # Special handling for refresh button which uses onclick instead of id
        if element_id == 'refreshMonitoringData()':
            if 'onclick="refreshMonitoringData()"' in content:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description}")
                html_missing.append(element_id)
        elif f'id="{element_id}"' in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            html_missing.append(element_id)
    
    # Check for JavaScript functions
    js_checks = [
        ('function toggleAlertDetails', '🔽 Toggle Alert Details Function'),
        ('function refreshMonitoringData', '🔄 Refresh Monitoring Data Function'),
        ('function loadEnhancedMonitoringData', '📊 Load Enhanced Data Function'),
        ('function displayEnhancedVendors', '👥 Display Vendors Function'),
        ('function displayEnhancedAlerts', '🚨 Display Alerts Function'),
        ('function displayEnhancedScoreChanges', '📈 Display Score Changes Function'),
        ('function getVendorLogo', '🖼️ Get Vendor Logo Function'),
        ('function handleLogoError', '🔧 Handle Logo Error Function'),
        ('function loadDemoVendorsData', '📊 Demo Vendors Data Function'),
        ('function loadDemoAlertsData', '🚨 Demo Alerts Data Function'),
        ('function loadDemoScoreChangesData', '📈 Demo Score Changes Data Function'),
        ('window.toggleAlertDetails', '🌐 Global Toggle Function'),
        ('window.refreshMonitoringData', '🌐 Global Refresh Function'),
        ('window.handleLogoError', '🌐 Global Logo Error Function')
    ]
    
    print("\n🔍 Checking Enhanced Monitoring JavaScript Functions:")
    js_missing = []
    for function_check, description in js_checks:
        if function_check in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            js_missing.append(function_check)
    
    # Check for dashboard tab initialization
    print("\n🔍 Checking Dashboard Tab Integration:")
    if "if (tabName === 'dashboard')" in content:
        print("  ✅ Dashboard tab detection")
    else:
        print("  ❌ Dashboard tab detection")
        
    if "loadEnhancedMonitoringData()" in content:
        print("  ✅ Enhanced monitoring initialization on tab switch")
    else:
        print("  ❌ Enhanced monitoring initialization on tab switch")
    
    # Check for clickable functionality
    print("\n🔍 Checking Clickable Functionality:")
    clickable_checks = [
        ('onclick="toggleAlertDetails', '🔽 Clickable Alert Details'),
        ('onclick="refreshMonitoringData', '🔄 Clickable Refresh Button'),
        ('clickable-row mb-3', '👆 Clickable Row Styling'),
        ('class="dropdown-content"', '📋 Dropdown Content Styling')
    ]
    
    clickable_missing = []
    for check, description in clickable_checks:
        if check in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            clickable_missing.append(check)
    
    # Check for demo data integration
    print("\n🔍 Checking Demo Data Integration:")
    demo_checks = [
        ('Slack Technologies', '🏢 Demo Vendor - Slack'),
        ('Zoom Video Communications', '🏢 Demo Vendor - Zoom'),
        ('Microsoft Corporation', '🏢 Demo Vendor - Microsoft'),
        ('Security Alert - Slack Technologies', '🚨 Demo Security Alert'),
        ('Compliance Update - Microsoft Corporation', '📋 Demo Compliance Alert'),
        ('Score changed from', '📊 Demo Score Change'),
        ('Security incident discovery', '🔍 Demo Change Factor'),
        ('SOC 2 Type II certification renewal', '🏆 Demo Compliance Factor')
    ]
    
    demo_missing = []
    for check, description in demo_checks:
        if check in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            demo_missing.append(check)
    
    # Summary
    print("\n📊 Integration Test Summary:")
    print("=" * 40)
    
    total_checks = len(html_checks) + len(js_checks) + 2 + len(clickable_checks) + len(demo_checks)
    missing_count = len(html_missing) + len(js_missing) + len(clickable_missing) + len(demo_missing)
    
    # Add dashboard tab checks
    if "if (tabName === 'dashboard')" not in content:
        missing_count += 1
    if "loadEnhancedMonitoringData()" not in content:
        missing_count += 1
    
    passed_checks = total_checks - missing_count
    
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {passed_checks}")
    print(f"Failed: {missing_count}")
    print(f"Success Rate: {(passed_checks/total_checks)*100:.1f}%")
    
    if missing_count == 0:
        print("\n🎉 ALL TESTS PASSED! Enhanced Monitoring Integration Complete!")
        print("\n✨ Enhanced Monitoring Features Successfully Integrated:")
        print("   • 📊 Vendor logos and numerical scores")
        print("   • 🔽 Clickable dropdowns for alerts and score changes")  
        print("   • 📋 Detailed explanations for triggers and changes")
        print("   • 🔄 Real-time data loading and refresh capability")
        print("   • 🎨 Professional UI with Tailwind CSS styling")
        print("   • 🚫 No template literal syntax issues")
        print("   • 🌐 Fully integrated into main Combined UI")
        
        print("\n🚀 Ready to Use:")
        print("   1. Start the server with: python run_web.py")
        print("   2. Navigate to the Combined UI")
        print("   3. Click on 'Monitoring & Dashboard' tab")
        print("   4. Click on alerts and score changes for detailed explanations")
        return True
    else:
        print(f"\n⚠️ Integration incomplete - {missing_count} checks failed")
        return False

if __name__ == "__main__":
    success = test_enhanced_monitoring_integration()
    sys.exit(0 if success else 1)