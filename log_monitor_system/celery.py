import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log_monitor_system.settings')

app = Celery('log_monitor_system')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Define the task schedule
app.conf.beat_schedule = {
    'check-error-logs-every-10-minutes': {
        'task': 'log_monitor_system.apps.core.tasks.check_error_logs',
        'schedule': 600,  # 10 minutes in seconds
    },
    'generate-daily-summary': {
        'task': 'log_monitor_system.apps.core.tasks.generate_daily_summary',
        'schedule': crontab(hour=0, minute=0),  # Every day at midnight
    },
}

app.conf.timezone = 'UTC'