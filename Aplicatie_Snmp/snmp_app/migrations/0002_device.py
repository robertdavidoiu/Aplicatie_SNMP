# Generated by Django 3.0.3 on 2020-03-06 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snmp_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ip_address', models.GenericIPAddressField()),
                ('subnet_mask', models.GenericIPAddressField()),
                ('Authentication_Protocol', models.CharField(choices=[('usmHMACMD5AuthProtocol', 'md5'), ('usmHMACSHAAuthProtocol', 'sha'), ('usmHMAC128SHA224AuthProtocol', 'sha 224'), ('usmHMAC192SHA256AuthProtocol', 'sha 256'), ('usmHMAC256SHA384AuthProtocol', 'sha 384'), ('usmHMAC384SHA512AuthProtocol', 'sha 512')], default='usmHMACSHAAuthProtocol', max_length=28)),
                ('Authentication_password', models.CharField(max_length=50)),
                ('Private_Protocol', models.CharField(choices=[('usmDESPrivProtocol', 'des'), ('usm3DESEDEPrivProtocol', '3des'), ('usmAesCfb128Protocol', 'aes 128'), ('usmAesCfb192Protocol', 'aes 192'), ('usmAesCfb256Protocol', 'aes 256'), ('usmNoPrivProtocol', 'no protocol')], default='usm3DESEDEPrivProtocol', max_length=22)),
                ('Private_password', models.CharField(max_length=50)),
                ('Details', models.CharField(max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
