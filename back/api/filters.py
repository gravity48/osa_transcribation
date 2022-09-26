from django_filters import rest_framework as filters
from connections.models import Connections


class ConnectionsFilter(filters.FilterSet):

    db_status = filters.NumberFilter(field_name='db_status', lookup_expr='exact')

    class Meta:
        model = Connections
        fields = ['db_status', ]
