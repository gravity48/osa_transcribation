from datetime import datetime, timedelta

from connections.models import Connections
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from utils.services import generate_hash, default_period_date

PLAY_STATUS_TASK = 1
STOP_STATUS_TASK = 2


class RecognizeServers(models.Model):
    name = models.CharField(_('recognize server name'), max_length=100)
    short_name = models.CharField(_('recognize server short name'), max_length=10)
    ip = models.CharField(_('recognize server ip'), max_length=100)
    port = models.IntegerField(_('recognize server port'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'recognize_servers'
        verbose_name = _('recognize servers')
        verbose_name_plural = _('recognize server')


class StatusTasks(models.Model):
    status = models.TextField(_('task status'), max_length=100)

    def __str__(self):
        return self.status

    class Meta:
        db_table = 'task_status'
        verbose_name = _('task status')
        verbose_name_plural = _('task status')


class TaskType(models.Model):
    name = models.TextField(_('task type name'), max_length=100)

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'task_type'
        verbose_name = _('task type')
        verbose_name_plural = _('task type')


class Tasks(models.Model):
    db = models.ForeignKey(
        Connections,
        verbose_name=_('databases'),
        related_name='task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    model = models.ManyToManyField(
        RecognizeServers,
        verbose_name=_('tasks models'),
        related_name='tasks',
        blank=True,
    )
    task_type = models.ForeignKey(
        TaskType,
        verbose_name=_('task type'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        StatusTasks,
        verbose_name=_('task status'),
        default=STOP_STATUS_TASK,
        on_delete=models.RESTRICT,
        blank=True,
    )
    alias = models.CharField(_('task alias'), max_length=100, unique=True, default=generate_hash)
    period_from = models.DateTimeField(
        _('task period from'),
        default=datetime.now,
    )
    period_to = models.DateTimeField(
        _('task period to'),
        default=default_period_date
    )
    thread_count = models.IntegerField(_('process count'), default=1)
    options = models.JSONField(_('task options'), default=dict, blank=True)
    created_at = models.DateTimeField(_('task created at'), auto_now_add=True, blank=True)

    def __str__(self):
        return self.alias

    def clean(self):
        if self.period_from >= self.period_to:
            raise ValidationError(_('period_from greater than or equal period_to'))

    class Meta:
        db_table = 'tasks'
        ordering = [
            '-created_at',
        ]
        verbose_name = _('tasks')
        verbose_name_plural = _('task')
