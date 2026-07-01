from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from test_app.views import (
    greetings,
    task_statistics,
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView,
    CategoryViewSet,
    UserTaskListView,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="API documentation for Task Manager project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/tasks/statistics/', task_statistics),
    path('api/tasks/', TaskListCreateView.as_view()),
    path('api/tasks/my/', UserTaskListView.as_view()),
    path('api/tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view()),

    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),

    path('api/', include(router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
