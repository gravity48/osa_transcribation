from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.v1.connections_status import ConnectionStatusView
from .views.v1.connections_view import ConnectionsViewSet
from .views.v1.database_system_view import DatabaseSystemView

router = DefaultRouter()
router.register('connections', ConnectionsViewSet, basename='connections')

urlpatterns = [
    path('status/', ConnectionStatusView.as_view(), name='connection_status'),
    path('systems/', DatabaseSystemView.as_view(), name='database_systems'),
]

urlpatterns += router.urls
