import json
import uuid
from datetime import datetime, timezone

import pika
from django.conf import settings

from ..models import Status, Task

parameters = pika.URLParameters(settings.RABBITMQ_URL)
pdf_exchange = settings.RABBITMQ_CONFIG["PDF_EXCHANGE"]
reply_queue = settings.RABBITMQ_CONFIG["REPLY_QUEUE"]
reply_rk = settings.RABBITMQ_CONFIG["REPLY_RK"]


class ResultListener:
    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(reply_queue, durable=True)
        self.channel.queue_bind(
            queue=reply_queue,
            exchange=pdf_exchange,
            routing_key=reply_rk,
        )

        # Just a demo
        # Ensure fair distribution among consumers
        # Prefetch count requires monitoring
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=reply_queue, on_message_callback=self.callback, auto_ack=False
        )

    def callback(self, channel, method, props, body):
        data = json.loads(body)
        task = Task.objects.get(task_id=uuid.UUID(props.correlation_id))
        task.status = Status.COMPLETED
        task.output_files = data
        task.completed_at = datetime.fromtimestamp(props.timestamp, tz=timezone.utc)
        task.save()
        channel.basic_ack(delivery_tag=method.delivery_tag, multiple=True)

    def run(self):
        print("Started from server's worker.py. Waiting for results...")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.connection.close()
