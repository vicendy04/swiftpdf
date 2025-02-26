import pika
from django.conf import settings
from minio import Minio

from .constants import RabbitMQConfig

minio_client = Minio(
    endpoint=settings.MINIO_HOST,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.USE_MINIO_HTTPS,
)


def init_queue():
    import rabbitpy

    with rabbitpy.Connection() as connection:
        with connection.channel() as channel:
            for exchange_name in ["requests", "replies"]:
                exchange = rabbitpy.Exchange(
                    channel, exchange_name, exchange_type="direct"
                )
                exchange.declare()


# reply_queue = settings.REPLY_QUEUE


def setup_rabbitmq():
    parameters = pika.URLParameters(RabbitMQConfig.RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(
        exchange=RabbitMQConfig.REQUEST_EXCHANGE, exchange_type="direct"
    )
    channel.exchange_declare(
        exchange=RabbitMQConfig.REPLY_EXCHANGE, exchange_type="direct"
    )

    channel.queue_declare(queue=RabbitMQConfig.REQUEST_QUEUE)
    # channel.queue_declare(queue=reply_queue)

    channel.queue_bind(
        exchange=RabbitMQConfig.REQUEST_EXCHANGE,
        queue=RabbitMQConfig.REQUEST_QUEUE,
        routing_key="process",
    )
    # channel.queue_bind(exchange=reply_exchange, queue=reply_queue, routing_key="reply")

    connection.close()
    print("RabbitMQ setup completed successfully")
