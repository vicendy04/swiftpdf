from django.urls import path

from core import views

urlpatterns = [
    path("tasks/", views.create_task, name="task-create"),
    path("tasks/<uuid:task_id>/", views.get_task, name="task-get"),
    path("upload/", views.init_upload, name="init-upload"),
]
