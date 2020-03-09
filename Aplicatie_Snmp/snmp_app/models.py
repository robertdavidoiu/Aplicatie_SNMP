from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


authentication_protocol_choices = (('usmHMACMD5AuthProtocol', 'md5'),
                                   ('usmHMACSHAAuthProtocol', 'sha'),
                                   ('usmHMAC128SHA224AuthProtocol','sha 224'),
                                   ('usmHMAC192SHA256AuthProtocol', 'sha 256'),
                                   ('usmHMAC256SHA384AuthProtocol', 'sha 384'),
                                   ('usmHMAC384SHA512AuthProtocol', 'sha 512'),
                                   )

private_protocol_choces = (('usmDESPrivProtocol', 'des'),
                           ('usm3DESEDEPrivProtocol', '3des'),
                           ('usmAesCfb128Protocol', 'aes 128'),
                           ('usmAesCfb192Protocol', 'aes 192'),
                           ('usmAesCfb256Protocol', 'aes 256'),
                           ('usmNoPrivProtocol', 'no protocol'),
                           )

class Device(models.Model):
    name = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    subnet_mask = models.GenericIPAddressField()
    # Snmp_Version = models.CharField(choices=['v1', 'v2c', 'v3'])
    Authentication_Protocol = models.CharField(max_length=28, choices=authentication_protocol_choices, default='usmHMACSHAAuthProtocol')
    Authentication_password = models.CharField(max_length=50)
    Private_Protocol = models.CharField(max_length=22, choices=private_protocol_choces, default='usm3DESEDEPrivProtocol')
    Private_password = models.CharField(max_length=50)
    Details = models.CharField(max_length=50)
    date_added = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('device_detail', kwargs={'pk': self.pk})
