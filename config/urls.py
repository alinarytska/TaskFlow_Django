from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
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

    path('api/tasks/statistics/', task_statistics),
    path('api/tasks/', TaskListCreateView.as_view()),
    path('api/tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view()),

    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),

    path('api/', include(router.urls)),
]
