import json

import pika
import pika.exceptions
from django.conf import settings

parameters = pika.URLParameters(settings.RABBITMQ_URL)
pdf_exchange = settings.RABBITMQ_CONFIG["PDF_EXCHANGE"]
pdf_rk = settings.RABBITMQ_CONFIG["PDF_RK"]
reply_rk = settings.RABBITMQ_CONFIG["REPLY_RK"]


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
        self.channel.confirm_delivery()

    def publish(self, task_id: str, body: dict) -> bool:
        properties = pika.BasicProperties(
            content_type="application/json",
            delivery_mode=pika.DeliveryMode.Persistent,
            correlation_id=task_id,
            reply_to=reply_rk,
        )
        try:
            self.channel.basic_publish(
                exchange=pdf_exchange,
                routing_key=pdf_rk,
                body=json.dumps(body),
                properties=properties,
                mandatory=True,
            )
            print("Message was published")
            return True
        except pika.exceptions.UnroutableError:
            print("Message was returned! Make sure the queues are declared.")
            return False

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
