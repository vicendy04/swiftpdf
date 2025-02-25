from django.shortcuts import get_object_or_404
from nanoid import generate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .minio import get_put_url
from .models import Task
from .serializers import TaskCreateSerializer, TaskSerializer, UploadInitSerializer


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


@api_view(["GET"])
def init_upload(request):
    pub_filename = generate(size=10) + ".pdf"
    url = get_put_url(pub_filename, 5)
    serializer = UploadInitSerializer(data={"pub_filename": pub_filename, "url": url})
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
