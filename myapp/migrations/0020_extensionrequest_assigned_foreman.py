# Generated by Django 5.1.3 on 2024-12-08 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_issuestatuschange'),
    ]

    operations = [
        migrations.AddField(
            model_name='extensionrequest',
            name='assigned_foreman',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_foreman', to=settings.AUTH_USER_MODEL),
        ),
    ]