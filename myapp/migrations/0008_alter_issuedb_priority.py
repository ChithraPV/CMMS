# Generated by Django 5.1.3 on 2024-12-02 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_issuedb_issue_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedb',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(3, 'High'), (2, 'Medium'), (1, 'Low')], null=True),
        ),
    ]
