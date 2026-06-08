from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from test_app.models import Task
from test_app.serializers import TaskSerializer


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, user!")


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)

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
