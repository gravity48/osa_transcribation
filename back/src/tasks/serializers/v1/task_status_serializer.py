from rest_framework import serializers
from tasks.models import StatusTasks


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTasks
        fields = '__all__'
