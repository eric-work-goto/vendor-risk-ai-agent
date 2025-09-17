import requests
import json

def test_monitoring_api():
    try:
        print("🧪 Testing Continuous Monitoring API...")
        
        # Check assessment history
        response = requests.get('http://localhost:8028/api/v1/assessments/history')
        if response.status_code == 200:
            data = response.json()
            assessments = data.get('data', [])
            print(f'📊 Total assessments: {len(assessments)}')
            
            # Check for continuous monitoring
            monitored = [a for a in assessments if a.get('enable_continuous_monitoring') == True]
            print(f'🔄 Vendors with continuous monitoring: {len(monitored)}')
            
            if monitored:
                print("📋 Monitored vendors:")
                for vendor in monitored:
                    domain = vendor.get('vendor_domain', 'Unknown')
                    score = vendor.get('final_score', vendor.get('risk_score', 'N/A'))
                    print(f'  • {domain} (Score: {score})')
            else:
                print('⚠️ No vendors currently have continuous monitoring enabled')
                
            # Show all assessments for context
            print(f"\n📋 All assessments:")
            for assessment in assessments:
                domain = assessment.get('vendor_domain', 'Unknown')
                monitoring = assessment.get('enable_continuous_monitoring', False)
                score = assessment.get('final_score', assessment.get('risk_score', 'N/A'))
                status = '✅ MONITORED' if monitoring else '❌ Not monitored'
                print(f'  • {domain} - {status} (Score: {score})')
                
        else:
            print(f'❌ API Error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    test_monitoring_api()