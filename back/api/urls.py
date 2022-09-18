from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, "User")
router.register(r'database_system', views.DbSystemViewSet)
router.register(r'connections', views.ConnectionsViewSet)
router.register(r'tasks_type', views.TasksTypeViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'models', views.ModelViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]