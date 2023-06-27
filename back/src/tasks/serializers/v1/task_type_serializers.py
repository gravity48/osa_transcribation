from rest_framework import serializers
from tasks.models import TaskType


class TasksTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = '__all__'
