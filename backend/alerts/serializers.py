from rest_framework import serializers
from .models import Integration, Alert, AlertHistory

class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'last_triggered', 'created_by')

    def create(self, validated_data):
        # Set the created_by field to the current user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class AlertHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertHistory
        fields = '__all__'
        read_only_fields = ('triggered_at',)
