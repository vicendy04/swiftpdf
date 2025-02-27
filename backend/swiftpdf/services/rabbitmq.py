import pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
REQUEST_EXCHANGE = "request_exchange"
REPLY_EXCHANGE = "reply_exchange"
REQUEST_QUEUE = "request_queue"
REPLY_QUEUE = "reply_queue"


def setup_rabbitmq():
    parameters = pika.URLParameters(RABBITMQ_URL)

    with pika.BlockingConnection(parameters) as connection:
        with connection.channel() as channel:
            channel.exchange_declare(exchange=REQUEST_EXCHANGE, exchange_type="direct")
            channel.exchange_declare(exchange=REPLY_EXCHANGE, exchange_type="direct")

            channel.queue_declare(queue=REQUEST_QUEUE)
            channel.queue_declare(queue=REPLY_QUEUE)

            channel.queue_bind(
                exchange=REQUEST_EXCHANGE,
                queue=REQUEST_QUEUE,
                routing_key="process",
            )
            channel.queue_bind(
                exchange=REPLY_EXCHANGE,
                queue=REPLY_QUEUE,
                routing_key="reply",
            )

            print("RabbitMQ setup completed successfully")
