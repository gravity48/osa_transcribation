from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from tasks.models import TaskType
from tasks.serializers.v1.task_type_serializers import TasksTypeSerializer


@extend_schema_view(
    get=extend_schema(
        description=_('task type list'),
        tags=[_('task')],
    ),
)
class TaskTypeView(generics.ListAPIView):
    queryset = TaskType.objects.all()
    serializer_class = TasksTypeSerializer
