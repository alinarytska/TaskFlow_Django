from django.contrib import admin
from django.urls import path
from test_app.views import (create_task, greetings, task_detail, task_list, task_statistics)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home-page/', greetings),

    path('api/tasks/create/', create_task),
    path('api/tasks/', task_list),
    path('api/tasks/<int:pk>/', task_detail),
    path('api/tasks/statistics/', task_statistics),
]
