from connections.models import ConnectionsStatus
from rest_framework import serializers


class ConnectionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionsStatus
        fields = '__all__'
