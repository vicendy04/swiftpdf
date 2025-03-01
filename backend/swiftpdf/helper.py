from .models import Task


def create_task_message(task: Task) -> tuple[str, dict]:
    message = {
        "tool": task.tool,
        "input_files": task.input_files,
    }

    if hasattr(task, "ranges") and task.ranges:
        message["ranges"] = task.ranges

    return str(task.task_id), message
