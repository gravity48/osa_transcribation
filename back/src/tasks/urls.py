from django.urls import path
from rest_framework.routers import DefaultRouter
from tasks.views.v1.recognize_servers_view import RecognizeServersView
from tasks.views.v1.task_status_view import TaskStatusView
from tasks.views.v1.task_type_view import TaskTypeView
from tasks.views.v1.task_view import TaskViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('servers/', RecognizeServersView.as_view(), name='recognize_servers'),
    path('types/', TaskTypeView.as_view(), name='task_type'),
    path('status/', TaskStatusView.as_view(), name='task_status'),
]

urlpatterns += router.urls
