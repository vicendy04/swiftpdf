from django.urls import path

from swiftpdf import views

urlpatterns = [
    path("tasks/", views.create_task, name="task-create"),
    path("tasks/<uuid:task_id>/", views.get_task, name="task-get"),
    path("files/", views.init_upload, name="init-upload"),
    path("files/<str:output_id>/", views.download_result, name="download-result"),
]
