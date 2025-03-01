import os

import pika
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Setup RabbitMQ exchanges and queues"

    def handle(self, *args, **kwargs):
        if os.environ.get("RUN_MAIN") != "true":
            setup_rabbitmq()


def get_rabbitmq_config():
    return {"url": settings.RABBITMQ_URL, **settings.RABBITMQ_CONFIG}


def setup_rabbitmq():
    config = get_rabbitmq_config()
    parameters = pika.URLParameters(config["url"])

    with pika.BlockingConnection(parameters) as connection:
        with connection.channel() as channel:
            for exchange_name in [config["PDF_EXCHANGE"], config["DLX_EXCHANGE"]]:
                channel.exchange_declare(
                    exchange=exchange_name,
                    exchange_type="direct",
                )

            print("RabbitMQ setup completed successfully")
