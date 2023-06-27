from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.services import generate_hash

DB_STATUS_OFFLINE = 2
DB_STATUS_ONLINE = 1


class DatabaseSystems(models.Model):
    name = models.CharField(_('database system name'), unique=True, max_length=100)

    class Meta:
        db_table = 'database_system'
        verbose_name = _('database systems')
        verbose_name_plural = _('database system')


class ConnectionsStatus(models.Model):
    status_name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'connection_status'
        verbose_name = _('connection status')
        verbose_name_plural = _('connection status')


class Connections(models.Model):
    alias = models.CharField(
        _('connection alias'),
        unique=True,
        max_length=100,
        default=generate_hash,
    )
    db_system = models.ForeignKey(
        DatabaseSystems,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('database system'),
    )
    db_status = models.ForeignKey(
        ConnectionsStatus,
        verbose_name=_('database status'),
        default=DB_STATUS_OFFLINE,
        on_delete=models.CASCADE,
    )
    ip = models.CharField(_('ip address database server'), max_length=100, default='')
    port = models.IntegerField(_('database server port'), null=True, blank=True)
    db_login = models.CharField(_('database login'), max_length=100, default='')
    db_password = models.CharField(_('database password'), max_length=100, default='')
    db_name = models.CharField(_('database name'), max_length=500, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    options = models.JSONField(default=dict)

    class Meta:
        db_table = 'connections'
        ordering = ["-created_at"]
        verbose_name = _('connections')
        verbose_name_plural = _('connection')
