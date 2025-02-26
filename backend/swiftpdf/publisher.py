import json

import pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
# queue_name = "response-queue"  # khong duoc ai dung, dung de delcare cai queue phan hoi
parameters = pika.URLParameters(RABBITMQ_URL)
request_exchange = "request_exchange"


class Publisher:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def publish(self, body: str) -> None:
        print(body)
        properties = pika.BasicProperties(
            content_type="text/plain", delivery_mode=pika.DeliveryMode.Transient
        )
        self.channel.basic_publish(
            exchange=request_exchange,
            routing_key="process",
            body=json.dumps(body),
            properties=properties,
        )
