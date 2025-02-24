from django.urls import path

from .views import create_task, get_task

urlpatterns = [
    path("tasks/", create_task, name="task-create"),
    path("tasks/<uuid:task_id>/", get_task, name="task-get"),
]
