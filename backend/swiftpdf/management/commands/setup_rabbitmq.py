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
            channel.exchange_declare(
                exchange=config["REQUEST_EXCHANGE"],
                exchange_type="direct",
            )
            channel.exchange_declare(
                exchange=config["REPLY_EXCHANGE"],
                exchange_type="direct",
            )

            channel.queue_declare(queue=config["REQUEST_QUEUE"])
            channel.queue_declare(queue=config["REPLY_QUEUE"])

            channel.queue_bind(
                queue=config["REQUEST_QUEUE"],
                exchange=config["REQUEST_EXCHANGE"],
                routing_key="process",
            )
            channel.queue_bind(
                queue=config["REPLY_QUEUE"],
                exchange=config["REPLY_EXCHANGE"],
                routing_key="reply",
            )

            print("RabbitMQ setup completed successfully")
