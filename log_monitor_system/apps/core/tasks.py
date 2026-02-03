from celery import shared_task
from datetime import datetime, timedelta
from .models import Log, Alert, App, LogSummary

@shared_task
def check_error_logs():
    """Check error logs every 10 minutes and create alerts if needed"""
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=10)
    
    apps = App.objects.all()
    for app in apps:
        error_count = Log.objects.filter(
            app=app,
            level='ERROR',
            created_at__gte=start_time,
            created_at__lte=end_time
        ).count()
        
        if error_count > 100:
            Alert.objects.create(
                app=app,
                content=f'Error log count exceeded threshold: {error_count} errors in the last 10 minutes'
            )

@shared_task
def generate_daily_summary():
    """Generate daily log summary"""
    yesterday = datetime.now().date() - timedelta(days=1)
    start_time = datetime.combine(yesterday, datetime.min.time())
    end_time = datetime.combine(yesterday, datetime.max.time())
    
    apps = App.objects.all()
    for app in apps:
        info_count = Log.objects.filter(
            app=app,
            level='INFO',
            created_at__gte=start_time,
            created_at__lte=end_time
        ).count()
        
        warn_count = Log.objects.filter(
            app=app,
            level='WARN',
            created_at__gte=start_time,
            created_at__lte=end_time
        ).count()
        
        error_count = Log.objects.filter(
            app=app,
            level='ERROR',
            created_at__gte=start_time,
            created_at__lte=end_time
        ).count()
        
        LogSummary.objects.update_or_create(
            app=app,
            date=yesterday,
            defaults={
                'info_count': info_count,
                'warn_count': warn_count,
                'error_count': error_count
            }
        )