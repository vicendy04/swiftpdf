from rest_framework import serializers

from .models import Task, Tool


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "task_id",
            "created_at",
            "completed_at",
            "status",
            "output_files",
            "error",
        )

    def validate(self, data):
        tool = data.get("tool")
        input_files = data.get("input_files")
        if tool == Tool.MERGE and len(input_files) < 2:
            raise serializers.ValidationError(
                {"input_files": "Requires at least 2 files."}
            )
        elif tool == Tool.SPLIT and len(input_files) < 1:
            raise serializers.ValidationError(
                {"input_files": "Requires at least 1 files."}
            )
        return data


class UploadInitSerializer(serializers.Serializer):
    pub_filename = serializers.CharField(max_length=14)
    url = serializers.URLField(allow_blank=True)
