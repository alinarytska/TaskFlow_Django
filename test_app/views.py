from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from test_app.models import Task, SubTask
from test_app.serializers import TaskSerializer, TaskCreateSerializer, TaskDetailSerializer, SubTaskSerializer, SubTaskCreateSerializer


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, user!")


@api_view(['POST'])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_list(request):
    weekday = request.query_params.get('weekday')
    tasks = Task.objects.all()

    if weekday:
        tasks = tasks.annotate(week_day=ExtractWeekDay('deadline')).filter(week_day=int(weekday))

    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)

    return Response(serializer.data)


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


class SubTaskListCreateView(APIView, PageNumberPagination):
    page_size = 5

    def get(self, request):
        subtasks = SubTask.objects.all()

        task_title = request.query_params.get('task_title')
        status_filter = request.query_params.get('status')

        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)

        if status_filter:
            subtasks = subtasks.filter(status=status_filter)

        subtasks = subtasks.order_by('-created_at')

        result_page = self.paginate_queryset(subtasks, request, view=self)
        serializer = SubTaskSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)

        if subtask is None:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskSerializer(subtask)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = self.get_object(pk)

        if subtask is None:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskCreateSerializer(subtask, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)

        if subtask is None:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        subtask.delete()

        return Response({"message": "SubTask deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
