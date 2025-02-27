import os

from django.core.management.base import BaseCommand

from swiftpdf.messaging.listener import ResultListener


class Command(BaseCommand):
    help = "Run the listener"

    def handle(self, *args, **options):
        if os.environ.get("RUN_MAIN") != "true":
            rl = ResultListener()
            rl.start()
            self.stdout.write("Triggered the listener")
