from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend


from test_app.models import Task, SubTask
from test_app.serializers import TaskSerializer, TaskCreateSerializer, TaskDetailSerializer, SubTaskSerializer, SubTaskCreateSerializer


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, user!")


@api_view(['GET'])
def task_statistics(request):
    total_tasks = Task.objects.count()

    tasks_by_status = Task.objects.values('status').annotate(count=Count('id'))

    overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()

    return Response(
        {
            'total_tasks': total_tasks,
            'tasks_by_status': list(tasks_by_status),
            'overdue_tasks': overdue_tasks
        }
    )


class CustomPagination(PageNumberPagination):
    page_size = 5


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all().order_by('-created_at')
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer

        return TaskSerializer


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer

        return TaskCreateSerializer


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer

        return SubTaskSerializer


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer

        return SubTaskCreateSerializer
