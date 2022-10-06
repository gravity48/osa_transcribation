import binascii
from abc import ABC
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from connections.models import Connections, DatabaseSystems
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from tasks.models import Tasks, TaskType, ModelsList, StatusTasks


def generate_hash():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time_hash = binascii.crc32(date_time.encode('utf8'))
    date_time_hash = hex(date_time_hash)
    return str(date_time_hash)


def cnnct_alias_validator(value):
    if Connections.objects.filter(alias=value).exists():
        raise serializers.ValidationError("Alias is exists")


def tsl_alias_validator(value):
    if Tasks.objects.filter(alias=value).exists():
        raise serializers.ValidationError("Alias is exists")


def stopped_task(value):
    if value != 'stopped':
        raise serializers.ValidationError('Задание должно быть остановлено')


ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'


class DatabaseSystemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = DatabaseSystems
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {
                'validators': [],
            }
        }


class ConnectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    db_system = DatabaseSystemSerializer(many=False, allow_null=True)
    db_status = serializers.SlugRelatedField(slug_field='status_name', read_only=True)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value is not None and attr == 'db_system':
                value = DatabaseSystems.objects.get(pk=value['id'])
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Connections
        fields = '__all__'
        extra_kwargs = {
            'alias': {
                'validators': [UniqueValidator(queryset=Connections.objects.all(),
                                               message='Подключение с таким именем уже существует'), ],
                'required': False,
            },
        }


class ConnectionRunSerializer(serializers.Serializer):
    alias = serializers.CharField(max_length=100, error_messages=settings.DEF_ERROR_MESSAGES)
    db_system = DatabaseSystemSerializer(error_messages=settings.DEF_ERROR_MESSAGES)
    ip = serializers.CharField(max_length=100,
                               validators=[RegexValidator(ip_regex, message='Неверный формат IP адреса')],
                               error_messages=settings.DEF_ERROR_MESSAGES)
    port = serializers.IntegerField(error_messages=settings.DEF_ERROR_MESSAGES)
    db_login = serializers.CharField(max_length=100, error_messages=settings.DEF_ERROR_MESSAGES)
    db_password = serializers.CharField(max_length=100, error_messages=settings.DEF_ERROR_MESSAGES)
    db_name = serializers.CharField(max_length=500, error_messages=settings.DEF_ERROR_MESSAGES)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class TaskTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TaskType
        fields = "__all__"


class ModelListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ModelsList
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTasks
        fields = "__all__"


class ConnectionOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Connections
        fields = ['id', 'alias']
        extra_kwargs = {
            'alias': {
                'validators': [],
                'required': False,
            }
        }


class TasksSerializer(serializers.ModelSerializer):
    db = ConnectionOptionSerializer(many=False, allow_null=True)
    model = ModelListSerializer(many=False, allow_null=True)
    task_type = TaskTypeSerializer(many=False, allow_null=True)
    status = serializers.SlugRelatedField(slug_field='status', read_only=True)

    def validate(self, attrs):
        if not attrs['alias']:
            attrs['alias'] = generate_hash()
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value is not None and attr == 'db':
                value = Connections.objects.get(pk=value['id'])
            if value is not None and attr == 'model':
                value = ModelsList.objects.get(pk=value['id'])
            if value is not None and attr == 'task_type':
                value = TaskType.objects.get(pk=value['id'])
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Tasks
        fields = "__all__"
        extra_kwargs = {
            'thread_count': {
                'error_messages': settings.DEF_ERROR_MESSAGES,
            },
            'alias': {
                'error_messages': settings.DEF_ERROR_MESSAGES,
                'validators': [UniqueValidator(queryset=Tasks.objects.all(), message='Поле должно быть уникальным')]
            },
        }


class TaskSerializerRun(serializers.Serializer):
    db = ConnectionOptionSerializer(many=False, error_messages=settings.DEF_ERROR_MESSAGES)
    model = ModelListSerializer(many=False, error_messages=settings.DEF_ERROR_MESSAGES)
    task_type = TaskTypeSerializer(many=False, error_messages=settings.DEF_ERROR_MESSAGES)
    status = serializers.CharField(error_messages=settings.DEF_ERROR_MESSAGES, validators=[stopped_task, ])
    celery_id = serializers.CharField(max_length=50, allow_null=True, error_messages=settings.DEF_ERROR_MESSAGES)
    alias = serializers.CharField(max_length=100, error_messages=settings.DEF_ERROR_MESSAGES)
    period_from = serializers.DateTimeField(error_messages=settings.DEF_ERROR_MESSAGES)
    period_to = serializers.DateTimeField(error_messages=settings.DEF_ERROR_MESSAGES)
    limit = serializers.IntegerField(error_messages=settings.DEF_ERROR_MESSAGES)
    processed_record_id = serializers.IntegerField(error_messages=settings.DEF_ERROR_MESSAGES)
    thread_count = serializers.IntegerField(error_messages=settings.DEF_ERROR_MESSAGES)
    time_processing = serializers.IntegerField(error_messages=settings.DEF_ERROR_MESSAGES)
    force_stop = serializers.BooleanField(error_messages=settings.DEF_ERROR_MESSAGES)
    options = serializers.JSONField(error_messages=settings.DEF_ERROR_MESSAGES)
    date = serializers.DateTimeField(error_messages=settings.DEF_ERROR_MESSAGES)
