# backend/alerts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IntegrationViewSet, AlertViewSet, AlertHistoryViewSet

router = DefaultRouter()
router.register(r'integrations', IntegrationViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'history', AlertHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
