import json
from datetime import datetime

import pika
from django.conf import settings

from .pdf_utils import process_pdf_task

parameters = pika.URLParameters(settings.RABBITMQ_URL)
pdf_exchange = settings.RABBITMQ_CONFIG["PDF_EXCHANGE"]
dlx_exchange = settings.RABBITMQ_CONFIG["DLX_EXCHANGE"]
pdf_queue = settings.RABBITMQ_CONFIG["PDF_QUEUE"]
dlq = settings.RABBITMQ_CONFIG["DLQ"]
pdf_rk = settings.RABBITMQ_CONFIG["PDF_RK"]
dlq_rk = settings.RABBITMQ_CONFIG["DLQ_RK"]


def main():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(dlq, durable=True)
    channel.queue_bind(
        queue=dlq,
        exchange=dlx_exchange,
        routing_key=dlq_rk,
    )
    channel.queue_declare(
        pdf_queue,
        durable=True,
        arguments={
            "x-dead-letter-exchange": dlx_exchange,
            "x-dead-letter-routing-key": dlq_rk,
        },
    )
    channel.queue_bind(
        queue=pdf_queue,
        exchange=pdf_exchange,
        routing_key=pdf_rk,
    )

    # Just a demo
    # Ensure fair distribution among consumers
    # Prefetch count requires monitoring
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=pdf_queue, on_message_callback=callback, auto_ack=False)

    print("Result processor started. Waiting for results...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


def callback(channel, method, props, body):
    result_data = json.loads(body)
    print(f"Received: {result_data}")

    result_objects = process_pdf_task(result_data)

    properties = pika.BasicProperties(
        content_type="application/json",
        delivery_mode=pika.DeliveryMode.Persistent,
        correlation_id=props.correlation_id,
        timestamp=int(datetime.now().timestamp()),
    )
    channel.basic_publish(
        exchange=pdf_exchange,
        routing_key=props.reply_to,
        body=json.dumps(result_objects),
        properties=properties,
    )

    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=True)
