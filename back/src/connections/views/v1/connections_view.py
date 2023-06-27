from base.mixins import PartialUpdateMixin
from connections.filters import ConnectionsFilter
from connections.models import Connections
from connections.serializers.v1.connections_serializers import (
    CheckConnectionSerializer,
    ConnectionCreateSerializer,
    ConnectionListSerializer,
    ConnectionRetrieveSerializer,
    ConnectionUpdateSerializer,
)
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        description=_('get connections'),
        tags=[
            _('connection'),
        ],
    ),
    create=extend_schema(
        description=_('create connection'),
        tags=[
            _('connection'),
        ],
    ),
    retrieve=extend_schema(
        description=_('get connection detail'),
        tags=[
            _('connection'),
        ],
    ),
    update=extend_schema(
        description=_('update connection'),
        tags=[
            _('connection'),
        ],
    ),
    destroy=extend_schema(
        description=_('delete connection'),
        tags=[
            _('connection'),
        ],
    ),
)
class ConnectionsViewSet(PartialUpdateMixin, viewsets.ModelViewSet):
    queryset = Connections.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = ConnectionsFilter
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return ConnectionListSerializer
        elif self.action == 'create':
            return ConnectionCreateSerializer
        elif self.action == 'retrieve':
            return ConnectionRetrieveSerializer
        elif self.action == 'update':
            return ConnectionUpdateSerializer
        elif self.action == 'refresh':
            return CheckConnectionSerializer

    @extend_schema(description=_('check connection'), tags=[_('connection')])
    @action(
        detail=True,
        methods=[
            'get',
        ],
    )
    def refresh(self, request, pk=None):
        # serializer = self.get_serializer(self.get_object())
        # TranscriptionServer().check_connection(serializer.data)
        return Response(status=status.HTTP_200_OK)
