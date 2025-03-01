import json
import time

import pika

RABBITMQ_HOST = "localhost"

connection_parameters = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=5672,
    credentials=pika.PlainCredentials("guest", "guest"),
    heartbeat=5,
)

connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.exchange_declare(
    exchange="ts-heartbeat",
    exchange_type="direct",
)
channel.queue_declare(queue="my_queue")
channel.queue_bind(
    queue="my_queue",
    exchange="ts-heartbeat",
    routing_key="test",
)

properties = pika.BasicProperties(
    content_type="application/json",
    delivery_mode=pika.DeliveryMode.Persistent,
)
body = {"data": "fake"}
channel.basic_publish(
    exchange="ts-heartbeat",
    routing_key="test",
    body=json.dumps(body),
    properties=properties,
)


def callback(ch, method, properties, body):
    print(f"Processing: {body}")
    time.sleep(20)
    print("Done!")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue="my_queue", on_message_callback=callback)
print("Start consuming")
channel.start_consuming()
