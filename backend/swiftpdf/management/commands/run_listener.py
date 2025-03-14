import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run the listener"

    def handle(self, *args, **options):
        if os.environ.get("RUN_MAIN") != "true":
            from swiftpdf.external.listener import ResultListener

            rl = ResultListener()
            rl.run()
