import json
import threading
import uuid

import pika

from ..models import Status, Task

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
parameters = pika.URLParameters(RABBITMQ_URL)
reply_exchange = "reply_exchange"
reply_queue = "reply_queue"


# works independently of Django
class ResultListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=reply_queue)
        self.channel.queue_bind(
            exchange=reply_exchange,
            queue=reply_queue,
            routing_key="reply",
        )

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=reply_queue, on_message_callback=self.callback, auto_ack=False
        )

    def callback(self, channel, method, props, body):
        data = json.loads(body)
        task = Task.objects.get(task_id=uuid.UUID(props.correlation_id))
        task.status = Status.COMPLETED
        task.output_files = data
        task.save()
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print("Started from server's worker.py. Waiting for results...")
        self.channel.start_consuming()


# def callback(channel, method, props, body):
#     data = json.loads(body)
#     print("hello")
#     task = Task.objects.get(id=1)
#     task.status = Status.COMPLETED
#     task.output_files = data
#     task.save()
#     channel.basic_ack(delivery_tag=method.delivery_tag)


# def main():
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()

#     # Declare queue to consume if not exist
#     channel.queue_declare(queue=reply_queue)
#     channel.queue_bind(
#         exchange=reply_exchange,
#         queue=reply_queue,
#         routing_key="reply",
#     )

#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(
#         queue=reply_queue, on_message_callback=callback, auto_ack=False
#     )

#     print("Result processor started from server's worker.py. Waiting for results...")
#     channel.start_consuming()


# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("Interrupted")
