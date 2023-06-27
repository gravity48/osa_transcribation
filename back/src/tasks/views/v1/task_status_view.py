from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from tasks.models import StatusTasks
from tasks.serializers.v1.task_status_serializer import TaskStatusSerializer


@extend_schema_view(
    get=extend_schema(
        description=_('status task list'),
        tags=[
            'task',
        ],
    ),
)
class TaskStatusView(generics.ListAPIView):
    queryset = StatusTasks.objects.all()
    serializer_class = TaskStatusSerializer
