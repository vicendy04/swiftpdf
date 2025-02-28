import json

import pika
from django.conf import settings

parameters = pika.URLParameters(settings.RABBITMQ_URL)
request_exchange = settings.RABBITMQ_CONFIG["REQUEST_EXCHANGE"]


_publisher = None


def get_publisher():
    global _publisher
    if _publisher is None:
        _publisher = Publisher()
    return _publisher


class Publisher:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        # declare something if need

    def publish(self, task_id: str, body: dict) -> None:
        properties = pika.BasicProperties(
            content_type="application/json",
            delivery_mode=pika.DeliveryMode.Persistent,
            correlation_id=task_id,
            reply_to="reply",
        )
        self.channel.basic_publish(
            exchange=request_exchange,
            routing_key="process",
            body=json.dumps(body),
            properties=properties,
        )

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
