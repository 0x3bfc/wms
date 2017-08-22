from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Service(models.Model):
    name = models.CharField(max_length=50, null=True)
    apikey=models.CharField(max_length=100, null=True)
    cbroker = models.CharField(max_length=50, null=True)
    entity_type = models.CharField(max_length=50, null=True)
    resource = models.CharField(max_length=50, null=True)

    class Meta():
        db_table="service"


class WorkSpace(models.Model):
    service = models.ForeignKey(Service, null=True)
    entity_name = models.CharField(max_length=50, null=True)
    ws_id = models.CharField(max_length=50, null=True)
    protocol = models.CharField(max_length=50, null=True)
    timezone = models.CharField(max_length=50, null=True)
    maxsize = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    location_long = models.CharField(max_length=100, null=True)
    location_lat = models.CharField(max_length=100, null=True)

    class Meta():
        db_table="workspace"

