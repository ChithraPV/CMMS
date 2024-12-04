# Generated by Django 5.1.3 on 2024-12-02 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_issuedb_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedb',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(3, 'High'), (2, 'Medium'), (1, 'Low')], default=2, null=True),
        ),
    ]