from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from test_app.views import (
    greetings,
    task_statistics,
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView,
    CategoryViewSet,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/tasks/statistics/', task_statistics),
    path('api/tasks/', TaskListCreateView.as_view()),
    path('api/tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view()),

    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),

    path('api/', include(router.urls)),
]
