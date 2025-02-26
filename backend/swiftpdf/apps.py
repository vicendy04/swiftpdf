import os

from django.apps import AppConfig

from .setup import setup_rabbitmq


class SwiftpdfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "swiftpdf"

    def ready(self):
        # or python manage.py runserver --noreload
        if os.environ.get("RUN_MAIN") != "true":
            setup_rabbitmq()
