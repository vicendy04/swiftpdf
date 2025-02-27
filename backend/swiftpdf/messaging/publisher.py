import json

import pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
parameters = pika.URLParameters(RABBITMQ_URL)
request_exchange = "request_exchange"


class Publisher:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

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
