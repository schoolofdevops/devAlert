# Generated by Django 5.0.1 on 2024-12-22 03:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('github', 'GitHub'), ('gitlab', 'GitLab'), ('jira', 'Jira'), ('custom', 'Custom Webhook')], max_length=20)),
                ('config', models.JSONField(help_text='Integration-specific configuration')),
                ('webhook_url', models.URLField(blank=True, null=True)),
                ('api_key', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('severity', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], max_length=20)),
                ('status', models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('conditions', models.JSONField(help_text='Alert trigger conditions')),
                ('notification_channels', models.JSONField(help_text='List of notification channels')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_triggered', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_alerts', to=settings.AUTH_USER_MODEL)),
                ('notify_users', models.ManyToManyField(related_name='alert_subscriptions', to=settings.AUTH_USER_MODEL)),
                ('integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alerts.integration')),
            ],
        ),
        migrations.CreateModel(
            name='AlertHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('triggered', 'Triggered'), ('acknowledged', 'Acknowledged'), ('resolved', 'Resolved')], max_length=20)),
                ('triggered_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('trigger_data', models.JSONField()),
                ('notes', models.TextField(blank=True)),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='alerts.alert')),
                ('handled_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='handled_alerts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Alert histories',
                'ordering': ['-triggered_at'],
            },
        ),
    ]