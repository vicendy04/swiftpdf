from django.shortcuts import get_object_or_404
from nanoid import generate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .external.minio import get_get_url, get_put_url
from .external.publisher import get_publisher
from .helper import create_task_message
from .models import Task
from .serializers import FileSerializer, TaskCreateSerializer, TaskSerializer


@api_view(["GET"])
def get_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(["POST"])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        task_id, body = create_task_message(instance)
        publisher = get_publisher()
        is_success = publisher.publish(task_id, body)
        if is_success:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def init_upload(request):
    filename = f"{generate(size=10)}.pdf"
    url = get_put_url(filename, 5)
    serializer = FileSerializer(data={"filename": filename, "url": url})
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def download_result(request, output_id):
    filename = f"{output_id}.pdf"
    url = get_get_url(filename, 5)
    serializer = FileSerializer(data={"filename": filename, "url": url})
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
