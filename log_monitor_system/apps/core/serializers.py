from rest_framework import serializers
from .models import Log, Alert, App

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'owner', 'created_at']

class LogSerializer(serializers.ModelSerializer):
    app = serializers.PrimaryKeyRelatedField(queryset=App.objects.all())
    
    class Meta:
        model = Log
        fields = ['id', 'app', 'level', 'message', 'created_at']

class AlertSerializer(serializers.ModelSerializer):
    app = serializers.PrimaryKeyRelatedField(queryset=App.objects.all())
    
    class Meta:
        model = Alert
        fields = ['id', 'app', 'content', 'is_resolved', 'created_at']