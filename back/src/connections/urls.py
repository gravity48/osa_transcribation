from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = 'connections'

urlpatterns = [
    path('', views.ConnectionsView.as_view(), name='connections_post'),
]
