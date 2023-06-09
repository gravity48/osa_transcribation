from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TasksView.as_view(), name='tasks_post'),
]
