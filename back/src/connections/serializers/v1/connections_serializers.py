from connections.models import Connections
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ConnectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connections
        fields = '__all__'


class ConnectionRetrieveSerializer(serializers.ModelSerializer):
    db_system = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    db_status = serializers.SlugRelatedField(
        slug_field='status_name',
        read_only=True,
    )

    class Meta:
        model = Connections
        fields = '__all__'


class ConnectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connections
        fields = '__all__'


class ConnectionCreateSerializer(serializers.ModelSerializer):
    alias = serializers.CharField(
        required=False,
        validators=[
            UniqueValidator(queryset=Connections.objects.all()),
        ],
    )

    def create(self, validated_data):
        return Connections.objects.create(**validated_data)

    class Meta:
        model = Connections
        fields = ('id', 'alias')
        extra_kwargs = {'id': {'read_only': True}}


class CheckConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connections
        exclude = ('created_at', 'options')
