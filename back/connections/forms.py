import re
import binascii
from datetime import datetime
from django import forms
from django.forms.fields import CharField, EmailField, IntegerField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from . import models

ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'


class ConnectionForm(forms.Form):
    alias = CharField(max_length=100, required=False)
    db_system = IntegerField()
    ip = CharField(max_length=50, validators=[RegexValidator(ip_regex), ])
    port = IntegerField()
    db_login = CharField(max_length=100)
    db_password = CharField(max_length=100)
    db_name = CharField(max_length=500)

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
        elif models.Connections.objects.filter(alias=self.cleaned_data['alias']).exists():
            self.add_error('alias', 'Alias is exists')
        return self.cleaned_data


class DelConnectionForm(forms.Form):
    con_id = IntegerField()

    def clean(self):
        try:
            models.Connections.objects.get(pk=self.cleaned_data['con_id'])
        except models.Connections.DoesNotExist:
            self.add_error('con_id', 'No have error')
        return self.cleaned_data
