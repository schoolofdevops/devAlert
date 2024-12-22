# backend/alerts/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Integration, Alert, AlertHistory
from .serializers import IntegrationSerializer, AlertSerializer, AlertHistorySerializer

class IntegrationViewSet(viewsets.ModelViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter integrations based on query parameters"""
        queryset = Integration.objects.all()
        integration_type = self.request.query_params.get('type', None)
        if integration_type:
            queryset = queryset.filter(type=integration_type)
        return queryset.order_by('-created_at')

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter alerts based on query parameters"""
        queryset = Alert.objects.all()
        severity = self.request.query_params.get('severity', None)
        status = self.request.query_params.get('status', None)
        integration_id = self.request.query_params.get('integration', None)

        if severity:
            queryset = queryset.filter(severity=severity)
        if status:
            queryset = queryset.filter(status=status)
        if integration_id:
            queryset = queryset.filter(integration_id=integration_id)

        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        AlertHistory.objects.create(
            alert=alert,
            status='acknowledged',
            handled_by=request.user,
            trigger_data={},
            notes=request.data.get('notes', '')
        )
        return Response({'status': 'alert acknowledged'})

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an alert"""
        alert = self.get_object()
        AlertHistory.objects.create(
            alert=alert,
            status='resolved',
            handled_by=request.user,
            trigger_data={},
            notes=request.data.get('notes', '')
        )
        return Response({'status': 'alert resolved'})

class AlertHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertHistory.objects.all()
    serializer_class = AlertHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter history based on query parameters"""
        queryset = AlertHistory.objects.all()
        alert_id = self.request.query_params.get('alert', None)
        status = self.request.query_params.get('status', None)

        if alert_id:
            queryset = queryset.filter(alert_id=alert_id)
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-triggered_at')
