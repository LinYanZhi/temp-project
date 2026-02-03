import requests
import time
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:8000/api'

class LogMonitorSystemTest:
    def __init__(self):
        self.app_id = None
    
    def create_test_app(self):
        """Create a test app using Django shell"""
        import os
        import django
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log_monitor_system.settings')
        django.setup()
        
        from log_monitor_system.apps.core.models import App
        
        app, created = App.objects.get_or_create(
            name='Test App',
            owner='Test Owner'
        )
        self.app_id = app.id
        print(f"Created test app with ID: {self.app_id}")
    
    def test_log_creation(self):
        """Test creating logs"""
        print("\n=== Testing log creation ===")
        
        # Test different log levels
        log_levels = ['INFO', 'WARN', 'ERROR']
        for level in log_levels:
            payload = {
                'app': self.app_id,
                'level': level,
                'message': f'Test {level} log'
            }
            
            response = requests.post(f'{BASE_URL}/logs/', json=payload)
            print(f"Created {level} log: {response.status_code}")
            print(f"Response: {response.json()}")
    
    def test_log_query(self):
        """Test querying logs"""
        print("\n=== Testing log query ===")
        
        # Test querying all logs
        response = requests.get(f'{BASE_URL}/logs/')
        print(f"All logs count: {len(response.json())}")
        
        # Test querying by level
        response = requests.get(f'{BASE_URL}/logs/?level=ERROR')
        print(f"ERROR logs count: {len(response.json())}")
        
        # Test querying by app and level
        response = requests.get(f'{BASE_URL}/logs/?level=ERROR&app={self.app_id}')
        print(f"ERROR logs for app {self.app_id}: {len(response.json())}")
    
    def test_alert_creation(self):
        """Test alert creation by pushing many error logs"""
        print("\n=== Testing alert creation ===")
        
        # Push 101 error logs to trigger alert
        print("Pushing 101 error logs...")
        for i in range(101):
            payload = {
                'app': self.app_id,
                'level': 'ERROR',
                'message': f'Test error log {i+1}'
            }
            requests.post(f'{BASE_URL}/logs/', json=payload)
        
        print("101 error logs pushed")
        
        # Wait for Celery task to process
        print("Waiting for Celery to process...")
        time.sleep(15)  # Wait 15 seconds for task to run
        
        # Check if alert was created
        response = requests.get(f'{BASE_URL}/alerts/')
        alerts = response.json()
        print(f"Unresolved alerts count: {len(alerts)}")
        
        if alerts:
            print(f"Alert details: {json.dumps(alerts[0], indent=2)}")
            return alerts[0]['id']
        return None
    
    def test_alert_resolution(self, alert_id):
        """Test alert resolution"""
        if not alert_id:
            print("\n=== No alert to resolve ===")
            return
        
        print("\n=== Testing alert resolution ===")
        
        response = requests.patch(f'{BASE_URL}/alerts/{alert_id}/resolve/')
        print(f"Alert resolution status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Verify alert is resolved
        response = requests.get(f'{BASE_URL}/alerts/')
        alerts = response.json()
        print(f"Unresolved alerts count after resolution: {len(alerts)}")
    
    def test_daily_summary(self):
        """Test daily summary generation"""
        print("\n=== Testing daily summary ===")
        
        # Trigger the daily summary task manually
        import os
        import django
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log_monitor_system.settings')
        django.setup()
        
        from log_monitor_system.apps.core.tasks import generate_daily_summary
        from log_monitor_system.apps.core.models import LogSummary
        
        # Run the task
        print("Running daily summary task...")
        generate_daily_summary.delay()
        
        # Wait for task to complete
        time.sleep(10)
        
        # Check if summary was created
        yesterday = datetime.now().date() - timedelta(days=1)
        from log_monitor_system.apps.core.models import App
        app = App.objects.get(id=self.app_id)
        
        try:
            summary = LogSummary.objects.get(app=app, date=yesterday)
            print(f"Daily summary created:")
            print(f"  Date: {summary.date}")
            print(f"  INFO count: {summary.info_count}")
            print(f"  WARN count: {summary.warn_count}")
            print(f"  ERROR count: {summary.error_count}")
        except LogSummary.DoesNotExist:
            print("No daily summary found")

def run_tests():
    print("Starting Log Monitor System tests...")
    
    test = LogMonitorSystemTest()
    
    # Create test app
    test.create_test_app()
    
    # Test log creation
    test.test_log_creation()
    
    # Test log querying
    test.test_log_query()
    
    # Test alert creation
    alert_id = test.test_alert_creation()
    
    # Test alert resolution
    test.test_alert_resolution(alert_id)
    
    # Test daily summary
    test.test_daily_summary()
    
    print("\n=== All tests completed ===")

if __name__ == '__main__':
    run_tests()
