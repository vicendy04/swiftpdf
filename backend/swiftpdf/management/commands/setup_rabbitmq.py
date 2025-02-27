import os

from django.core.management.base import BaseCommand

from swiftpdf.services.rabbitmq import setup_rabbitmq


class Command(BaseCommand):
    help = "Setup RabbitMQ exchanges and queues"

    def handle(self, *args, **kwargs):
        if os.environ.get("RUN_MAIN") != "true":
            setup_rabbitmq()
            self.stdout.write(
                self.style.SUCCESS("RabbitMQ setup completed successfully")
            )
