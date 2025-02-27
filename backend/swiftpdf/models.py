import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Status(models.TextChoices):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Tool(models.TextChoices):
    MERGE = "merge"
    SPLIT = "split"


class User(AbstractUser):
    pass


class Task(models.Model):
    task_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    tool = models.CharField(max_length=20, choices=Tool.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    input_files = models.JSONField(default=list)
    output_files = models.JSONField(default=list)
    error = models.CharField(max_length=200, null=True, blank=True)
    ranges = models.JSONField(default=list)

    def __str__(self):
        return f"Task {self.task_id} - {self.status}"
