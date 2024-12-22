from django.contrib import admin
from .models import Integration, Alert, AlertHistory

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('name', 'integration', 'severity', 'status', 'created_at', 'last_triggered')
    list_filter = ('severity', 'status', 'integration')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'last_triggered')
    filter_horizontal = ('notify_users',)

@admin.register(AlertHistory)
class AlertHistoryAdmin(admin.ModelAdmin):
    list_display = ('alert', 'status', 'triggered_at', 'resolved_at', 'handled_by')
    list_filter = ('status', 'alert', 'handled_by')
    search_fields = ('alert__name', 'notes')
    readonly_fields = ('triggered_at',)
