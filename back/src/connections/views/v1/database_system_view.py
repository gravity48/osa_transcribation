from connections.models import DatabaseSystems
from connections.serializers.v1.db_systems_serializers import DatabaseSystemSerializer
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics


@extend_schema_view(
    get=extend_schema(description=_('get database system list'), tags=[_('connection')]),
)
class DatabaseSystemView(generics.ListAPIView):
    queryset = DatabaseSystems.objects.all()
    serializer_class = DatabaseSystemSerializer
