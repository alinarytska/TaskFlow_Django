from django.contrib import admin
from django.urls import path
from test_app.views import (
    greetings,
    task_statistics,
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),

    path('api/tasks/statistics/', task_statistics),
    path('api/tasks/', TaskListCreateView.as_view()),
    path('api/tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view()),

    path('api/subtasks/', SubTaskListCreateView.as_view()),
    path('api/subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),
]
