from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Task
from core.serializers import TaskCreateSerializer, TaskSerializer


@api_view(["GET"])
def get_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(["POST"])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
