# Generated by Django 5.1.3 on 2025-02-02 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_alter_assetstock_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetstock',
            name='prev_maintenance_date',
            field=models.DateField(blank=True),
        ),
    ]
