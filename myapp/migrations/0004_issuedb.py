# Generated by Django 5.1.3 on 2024-11-10 07:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_delete_maintenancedept'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueDB',
            fields=[
                ('issue_id', models.AutoField(primary_key=True, serialize=False)),
                ('issue_category', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('issue_description', models.TextField()),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=20)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], default='Pending', max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='issues/')),
                ('reported_date', models.DateTimeField(auto_now_add=True)),
                ('reported_dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='myapp.department')),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reported_issues', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-reported_date'],
            },
        ),
    ]
