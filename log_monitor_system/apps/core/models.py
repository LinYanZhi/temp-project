from django.db import models
from django.utils import timezone

class App(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Log(models.Model):
    class LogLevel(models.TextChoices):
        INFO = 'INFO', 'Info'
        WARN = 'WARN', 'Warn'
        ERROR = 'ERROR', 'Error'
    
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=LogLevel.choices)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    content = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class LogSummary(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    info_count = models.IntegerField(default=0)
    warn_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    date = models.DateField()
    
    class Meta:
        unique_together = ['app', 'date']