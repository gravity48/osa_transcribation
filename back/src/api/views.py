from django.conf import settings
from api.transcribation_server import TranscriptionServer
from connections.models import ConnectionsStatus
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from . import serializers, filters
from connections.models import DB_STATUS_ONLINE, DB_STATUS_OFFLINE
from tasks.models import StatusTasks, TASK_IN_PROGRESS, TASK_STOPPED


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
    queryset = Connections.objects.all().order_by('-date')
    serializer_class = serializers.ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = filters.ConnectionsFilter

    @staticmethod
    def check_connection(connection):
        return True

    @action(detail=True, methods=['get', ])
    def refresh(self, request, pk=None, *args, **kwargs):
        instanse = self.get_object()
        serializer = self.serializer_class(instanse)
        custom_serializer = serializers.ConnectionRunSerializer(data=serializer.data)
        if custom_serializer.is_valid():
            server_status, context = TranscriptionServer().check_connection(serializer.data)
            if server_status:
                instanse.db_status = ConnectionsStatus.objects.get(pk=DB_STATUS_ONLINE)
                instanse.save()
                return Response(data=context, status=status.HTTP_200_OK)
            else:
                instanse.db_status = ConnectionsStatus.objects.get(pk=DB_STATUS_OFFLINE)
                instanse.save()
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        else:
            instanse.db_status = ConnectionsStatus.objects.get(pk=DB_STATUS_OFFLINE)
            instanse.save()
            return Response(data=custom_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        new_connection = self.queryset.create(**request.data)
        return Response(self.serializer_class(new_connection).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            self.queryset.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Connections.DoesNotExist:
            return Response('Not Exist', status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            context = {
                'data': self.serializer_class(self.get_object(), many=False).data,
                'errors': serializer.errors
            }
            return Response(data=context, status=status.HTTP_404_NOT_FOUND)


class DbSystemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DatabaseSystems.objects.all()
    serializer_class = DatabaseSystemSerializer
    permission_classes = [permissions.IsAuthenticated]


class TasksTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer


class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ModelListSerializer
    queryset = ModelsList.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all().order_by('-date')
    serializer_class = serializers.TasksSerializer

    @action(detail=True, methods=['get', ])
    def play_task(self, request, pk=None, *args, **kwargs):
        task = self.get_object()
        serializer = self.serializer_class(task, many=False)
        run_serializer = serializers.TaskSerializerRun(data=serializer.data)
        if run_serializer.is_valid():
            data = serializer.data
            connection_data = data.pop('db')
            connection_model = ConnectionSerializer(instance=Connections.objects.get(pk=connection_data['id']))
            data['db'] = connection_model.data
            server_status, response = TranscriptionServer().start_task(data)
            if server_status:
                task.status = StatusTasks.objects.get(pk=TASK_IN_PROGRESS)
                task.save()
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                task.status = StatusTasks.objects.get(pk=TASK_STOPPED)
                task.save()
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=run_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', ])
    def stop_task(self, request, pk=None, *args, **kwargs):
        task = self.get_object()
        server_status, response = TranscriptionServer().stop_task({'id': task.id})
        if server_status:
            task.status = StatusTasks.objects.get(pk=TASK_STOPPED)
            task.save()
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post', ])
    def status(self, request, *args, **kwargs):
        context = request.data
        response = {'task_run': []}
        for task in context['task_run']:
            response['task_run'].append(task['id'])
        server_status, response = TranscriptionServer().status_task(response)
        if server_status:
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

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

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            context = {
                'errors': serializer.errors,
                'data': self.serializer_class(self.get_object(), many=False).data
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)





