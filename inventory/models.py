from django.db import models

class Device(models.Model):
    mac = models.CharField(max_length=12)
    hostname = models.CharField(max_length=50)
    last_ip = models.GenericIPAddressField()
    firmware = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.hostname



