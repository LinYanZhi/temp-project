from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogViewSet, AlertViewSet

router = DefaultRouter()
router.register(r'logs', LogViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]