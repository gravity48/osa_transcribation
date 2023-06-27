from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from tasks.models import RecognizeServers
from tasks.serializers.v1.recognize_server_serializers import RecognizeServerSerializer


@extend_schema_view(
    get=extend_schema(
        description=_('recognize servers'),
        tags=[
            'task',
        ],
    ),
)
class RecognizeServersView(generics.ListAPIView):
    queryset = RecognizeServers.objects.all()
    serializer_class = RecognizeServerSerializer
