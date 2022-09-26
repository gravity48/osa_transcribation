import binascii
from datetime import datetime
from django.db import models
DB_STATUS_OFFLINE = 2


def generate_hash():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time_hash = binascii.crc32(date_time.encode('utf8'))
    date_time_hash = hex(date_time_hash)
    return str(date_time_hash)


class DatabaseSystems(models.Model):
    name = models.CharField(unique=True, max_length=100)


class ConnectionsStatus(models.Model):
    status_name = models.CharField(unique=True, max_length=100)


class Connections(models.Model):
    alias = models.CharField(unique=True, max_length=100, default=generate_hash)
    db_system = models.ForeignKey(DatabaseSystems, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    db_login = models.CharField(max_length=100, null=True, blank=True)
    db_password = models.CharField(max_length=100, null=True, blank=True)
    db_name = models.CharField(max_length=500, null=True, blank=True)
    db_status = models.ForeignKey(ConnectionsStatus, default=DB_STATUS_OFFLINE, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    options = models.JSONField(default=dict)

