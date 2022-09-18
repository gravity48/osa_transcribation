from django.db import models
DB_STATUS_OFFLINE = 2


class DatabaseSystems(models.Model):
    name = models.CharField(unique=True, max_length=100)


class ConnectionsStatus(models.Model):
    status_name = models.CharField(unique=True, max_length=100)


class Connections(models.Model):

    def __init__(self, *args, **kwargs):
        if 'db_system' in kwargs:
            kwargs['db_system'] = DatabaseSystems.objects.get(pk=kwargs['db_system'])
        super().__init__(*args, **kwargs)

    alias = models.CharField(unique=True, max_length=100)
    db_system = models.ForeignKey(DatabaseSystems, on_delete=models.CASCADE)
    ip = models.CharField(max_length=100)
    port = models.IntegerField()
    db_login = models.CharField(max_length=100)
    db_password = models.CharField(max_length=100)
    db_name = models.CharField(max_length=500)
    db_status = models.ForeignKey(ConnectionsStatus, default=DB_STATUS_OFFLINE, on_delete=models.CASCADE)

