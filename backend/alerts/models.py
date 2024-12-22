# backend/alerts/models.py
from django.db import models
from django.conf import settings

class Integration(models.Model):
    TYPE_CHOICES = [
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('jira', 'Jira'),
        ('custom', 'Custom Webhook'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    config = models.JSONField(help_text="Integration-specific configuration")
    webhook_url = models.URLField(blank=True, null=True)
    api_key = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.type})"

class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Alert conditions stored as JSON
    conditions = models.JSONField(help_text="Alert trigger conditions")
    
    # Notification settings
    notification_channels = models.JSONField(help_text="List of notification channels")
    notify_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='alert_subscriptions'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_alerts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class AlertHistory(models.Model):
    STATUS_CHOICES = [
        ('triggered', 'Triggered'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]

    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    triggered_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Store the actual data that triggered the alert
    trigger_data = models.JSONField()
    
    # Who acknowledged/resolved the alert
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='handled_alerts'
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-triggered_at']
        verbose_name_plural = "Alert histories"
    
    def __str__(self):
        return f"{self.alert.name} - {self.status} at {self.triggered_at}"
