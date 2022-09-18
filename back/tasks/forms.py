import re
import binascii
from datetime import datetime
from django import forms
from django.forms.fields import CharField, EmailField, IntegerField, DateTimeField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from . import models


class TasksForm(forms.Form):
    period_from = DateTimeField()
    period_to = DateTimeField()
    alias = CharField(required=False)
    connection_id = IntegerField()
    language_id = IntegerField()
    log = CharField(required=False)
    thread_count = IntegerField()
    time_processing = IntegerField()

    @staticmethod
    def generate_hash():
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        date_time_hash = binascii.crc32(date_time.encode('utf8'))
        date_time_hash = hex(date_time_hash)
        return str(date_time_hash)

    def clean(self):
        if not self.cleaned_data['alias']:
            self.cleaned_data['alias'] = self.generate_hash()
        elif models.Tasks.objects.filter(alias=self.cleaned_data['alias']).exists():
            self.add_error('alias', 'Alias is exists')
        if self.cleaned_data['period_from'] >= self.cleaned_data['period_to']:
            raise ValidationError('Неверный период')
        try:
            models.LanguageList.objects.get(pk=self.cleaned_data['language_id'])
        except models.LanguageList.DoesNotExist:
            self.add_error('language_id', 'No have language')
        try:
            models.Connections.objects.get(pk=self.cleaned_data['connection_id'])
        except models.Connections.DoesNotExist:
            self.add_error('connection_id', 'No have connections')
        self.cleaned_data['log'] = self.cleaned_data['alias'] + '.txt'
        return self.cleaned_data


class DelTaskForm(forms.Form):
    task_id = IntegerField()

    def clean(self):
        try:
            task_id = self.cleaned_data['task_id']
            models.Tasks.objects.get(pk=task_id)
        except models.Tasks.DoesNotExist:
            self.add_error('task_id', 'No have error')
        return self.cleaned_data
