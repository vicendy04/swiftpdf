import os

from django.core.management.base import BaseCommand

from worker.worker import main


class Command(BaseCommand):
    help = "Run the worker"

    def handle(self, *args, **options):
        if os.environ.get("RUN_MAIN") != "true":
            main()
