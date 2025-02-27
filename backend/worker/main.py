import json

import pika
from pdf_utils import process_pdf_task

# REPLY_EXCHANGE = "replies"

# rabbitmq_url = settings.RABBITMQ_URL
# request_exchange = settings.REQUEST_EXCHANGE
# queue_name = settings.REQUEST_QUEUE

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
parameters = pika.URLParameters(RABBITMQ_URL)
request_exchange = "request_exchange"
request_queue = "request_queue"


def callback(channel, method, header, body):
    result_data = json.loads(body)

    process_pdf_task(result_data)

    # then reply
    # correlation_id = header.correlation_id

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # check if exist
    channel.queue_declare(queue=request_queue)
    channel.queue_bind(
        exchange=request_exchange,
        queue=request_queue,
        routing_key="process",
    )

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=request_queue, on_message_callback=callback, auto_ack=False
    )

    print("Result processor started. Waiting for results...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
