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
                'validators': [],
                'required': False,
            },
        }


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


class TasksSerializer(serializers.ModelSerializer):
    db = ConnectionSerializer(many=False, allow_null=True)
    model = ModelListSerializer(many=False, allow_null=True)
    task_type = TaskTypeSerializer(many=False, allow_null=True)

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



