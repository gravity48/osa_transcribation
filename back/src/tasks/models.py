from datetime import datetime
from django.db import models
from django.conf import settings
from connections.models import Connections

TASK_IN_PROGRESS = 1
TASK_STOPPED = 2


class ModelsList(models.Model):
    name = models.TextField(max_length=100)
    path = models.TextField(max_length=100)
    short_name = models.TextField(max_length=10)
    ip = models.TextField(max_length=100)
    port = models.IntegerField()


class StatusTasks(models.Model):
    status = models.TextField(max_length=100)


class TaskType(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Tasks(models.Model):
    db = models.ForeignKey(Connections, related_name='task', on_delete=models.CASCADE, null=True, blank=True)
    model = models.ManyToManyField(ModelsList, null=True, blank=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(StatusTasks, default=TASK_STOPPED, on_delete=models.CASCADE)
    celery_id = models.CharField(max_length=50, blank=True, null=True)
    alias = models.CharField(max_length=100, unique=True)
    period_from = models.DateTimeField(blank=True, null=True)
    period_to = models.DateTimeField(blank=True, null=True)
    limit = models.IntegerField(default=1000)
    processed_record_id = models.IntegerField(default=0)
    thread_count = models.IntegerField(default=1)
    time_processing = models.IntegerField(default=200)
    force_stop = models.BooleanField(default=False)
    options = models.JSONField(default=dict)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = datetime.now()
        return super().save(*args, **kwargs)

