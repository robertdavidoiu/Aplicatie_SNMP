# Generated by Django 3.0.3 on 2020-03-06 13:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('snmp_app', '0002_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
