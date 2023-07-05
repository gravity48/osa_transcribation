from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tasks.models import PLAY_STATUS_TASK, STOP_STATUS_TASK, Tasks


class TaskListSerializer(serializers.ModelSerializer):
    db = serializers.SlugRelatedField(slug_field='alias', read_only=True)

    class Meta:
        model = Tasks
        fields = (
            'id',
            'alias',
            'status',
            'db'
        )


class TaskRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    db = serializers.SlugRelatedField(slug_field='alias', read_only=True)

    class Meta:
        model = Tasks
        fields = (
            'id',
            'alias',
            'status',
            'db'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'read_only': True},
        }


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'


class TaskPlaySerializer(serializers.Serializer):
    def validate(self, attrs):
        task = self.context['task']
        if task.status_id != STOP_STATUS_TASK:
            raise ValidationError(_('task not stopped'))
        return attrs


class TaskStopSerializer(serializers.Serializer):
    def validate(self, attrs):
        task = self.context['task']
        if task.status_id != PLAY_STATUS_TASK:
            raise ValidationError(_('task not played'))
        return attrs
