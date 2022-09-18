import json
from connections.models import Connections, DatabaseSystems
from connections.models import DatabaseSystems
from django.contrib.auth.models import User, Group
from django.conf import settings
from tasks.models import Tasks, TaskType, ModelsList, StatusTasks
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from . import serializers


# Create your views here.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = User.objects.get(pk=self.request.user.id)
        return User.objects.filter(pk=self.request.user.id).all()


class ConnectionsViewSet(viewsets.ModelViewSet):
    queryset = Connections.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        new_connection = self.queryset.get_or_create(**request.data)
        return Response(self.serializer_class(new_connection).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            self.queryset.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Connections.DoesNotExist:
            return Response('Not Exist', status=status.HTTP_400_BAD_REQUEST)


class DbSystemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DatabaseSystems.objects.all()
    serializer_class = DatabaseSystemSerializer
    permission_classes = [permissions.IsAuthenticated]


class TasksTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskType.objects.all()
    serializer_class = serializers.TaskTypeSerializer


class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ModelListSerializer
    queryset = ModelsList.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = serializers.TasksSerializer

    def create(self, request, *args, **kwargs):
        alias = generate_hash()
        new_task = Tasks.objects.create(alias=alias)
        return Response(self.serializer_class(new_task).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            self.queryset.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tasks.DoesNotExist:
            return Response('No exists', status=status.HTTP_400_BAD_REQUEST)


class TasksView(APIView):
    @staticmethod
    def _add_task(data):
        ts = serializers.TasksSerializer(data=data)
        if ts.is_valid():
            ts.save()
            return {'success': True}, settings.DEFAULT_SUCCESS_STATUS
        else:
            return ts.errors, settings.DEFAULT_ERROR_STATUS

    @staticmethod
    def _del_task(data):
        try:
            id = data['id']
        except KeyError:
            return {'error': 'no task id'}, settings.DEFAULT_ERROR_STATUS
        Tasks.objects.get(pk=id).delete()
        return {'success': True}, settings.DEFAULT_SUCCESS_STATUS

    def get(self, request):
        queryset = Tasks.objects.all()
        serializer = serializers.TasksSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            event = request.data['event']
        except KeyError:
            return Response(status=settings.DEFAULT_ERROR_STATUS)
        if event == 'add_task':
            response, status = self._add_task(request.data)
            return Response(response, status=status)
        if event == 'del_task':
            response, status = self._del_task(request.data)
            return Response(response, status=status)
        return Response({'error': 'no event'}, status=settings.DEFAULT_ERROR_STATUS)




