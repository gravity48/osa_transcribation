from base.mixins import PartialUpdateMixin
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from tasks.models import PLAY_STATUS_TASK, STOP_STATUS_TASK, Tasks
from tasks.serializers.v1.task_serializer import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskPlaySerializer,
    TaskRetrieveSerializer,
    TaskStopSerializer,
    TaskUpdateSerializer,
)


@extend_schema_view(
    list=extend_schema(
        description=_('get tasks'),
        tags=[
            _('task'),
        ],
    ),
    create=extend_schema(
        description=_('create task'),
        tags=[
            _('task'),
        ],
    ),
    retrieve=extend_schema(
        description=_('get task detail'),
        tags=[
            _('task'),
        ],
    ),
    update=extend_schema(
        description=_('update task'),
        tags=[
            _('task'),
        ],
    ),
    destroy=extend_schema(
        description=_('delete task'),
        tags=[
            _('task'),
        ],
    ),
)
class TaskViewSet(PartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        if self.action == 'retrieve':
            return TaskRetrieveSerializer
        if self.action == 'create':
            return TaskCreateSerializer
        if self.action == 'update':
            return TaskUpdateSerializer
        if self.action == 'play':
            return TaskPlaySerializer
        if self.action == 'stop':
            return TaskStopSerializer

    @extend_schema(description=_('play task'), tags=[_('task')])
    @action(detail=True, methods=['post'])
    def play(self, request, pk):
        instance: Tasks = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'task': instance})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(description=_('stop task'), tags=[_('task')])
    @action(detail=True, methods=['post'])
    def stop(self, request, pk):
        instance: Tasks = self.get_object()
        if instance.status_id != PLAY_STATUS_TASK:
            raise ValidationError(_('task is not stopped'))
        instance.status_id = STOP_STATUS_TASK
        instance.save()
        return Response(status=status.HTTP_200_OK)
