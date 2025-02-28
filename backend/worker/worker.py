import json
from datetime import datetime

import pika
from django.conf import settings

from .pdf_utils import process_pdf_task

config = settings.RABBITMQ_CONFIG
parameters = pika.URLParameters(settings.RABBITMQ_URL)


def main():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare queue to consume if not exist
    channel.queue_declare(queue=config["REQUEST_QUEUE"])
    channel.queue_bind(
        exchange=config["REQUEST_EXCHANGE"],
        queue=config["REQUEST_QUEUE"],
        routing_key="process",
    )

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=config["REQUEST_QUEUE"], on_message_callback=callback, auto_ack=False
    )

    print("Result processor started. Waiting for results...")
    channel.start_consuming()


def callback(channel, method, props, body):
    result_data = json.loads(body)

    result_objects = process_pdf_task(result_data)

    # then reply
    properties = pika.BasicProperties(
        content_type="application/json",
        delivery_mode=pika.DeliveryMode.Persistent,
        correlation_id=props.correlation_id,
        timestamp=int(datetime.now().timestamp()),
    )
    channel.basic_publish(
        exchange=config["REPLY_EXCHANGE"],
        routing_key=props.reply_to,
        body=json.dumps(result_objects),
        properties=properties,
    )

    channel.basic_ack(delivery_tag=method.delivery_tag)
