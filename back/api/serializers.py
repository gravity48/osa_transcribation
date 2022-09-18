import binascii
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.core.exceptions import ValidationError
from connections.models import Connections, DatabaseSystems
from rest_framework import serializers
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


class DatabaseSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseSystems
        fields = "__all__"


class ConnectionSerializer(serializers.ModelSerializer):
    db_system = serializers.SlugRelatedField(slug_field='name', read_only=True)
    db_status = serializers.SlugRelatedField(slug_field='status_name', read_only=True)

    class Meta:
        model = Connections
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = "__all__"


class ModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelsList
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTasks
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    db = serializers.SlugRelatedField(slug_field='id', read_only=True)
    model = serializers.SlugRelatedField(slug_field='id', read_only=True)
    task_type = serializers.SlugRelatedField(slug_field='id', read_only=True)
    status = serializers.SlugRelatedField(slug_field='id', read_only=True)

    def validate(self, attrs):
        if not attrs['alias']:
            attrs['alias'] = generate_hash()
        return attrs

    class Meta:
        model = Tasks
        fields = "__all__"
