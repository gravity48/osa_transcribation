from connections.models import DatabaseSystems
from rest_framework import serializers


class DatabaseSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseSystems
        fields = '__all__'
