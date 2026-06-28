from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.db.models import Count
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend


from test_app.models import Task, SubTask, Category
from test_app.serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
)


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, user!")


@api_view(['GET'])
@permission_classes([AllowAny])
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


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer

        return TaskCreateSerializer


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer

        return SubTaskCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        tasks_count = category.task_set.count()

        return Response(
            {
                'category': category.name,
                'tasks_count': tasks_count
            }
        )
