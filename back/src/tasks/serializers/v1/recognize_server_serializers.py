from rest_framework import serializers
from tasks.models import RecognizeServers


class RecognizeServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognizeServers
        fields = '__all__'
