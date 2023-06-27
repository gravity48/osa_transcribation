from connections.models import ConnectionsStatus
from connections.serializers.v1.connection_status_serializers import (
    ConnectionStatusSerializer,
)
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics


@extend_schema_view(
    get=extend_schema(
        description=_('connection status list'),
        tags=[
            'connection',
        ],
    ),
)
class ConnectionStatusView(generics.ListAPIView):
    queryset = ConnectionsStatus.objects.all()
    serializer_class = ConnectionStatusSerializer
