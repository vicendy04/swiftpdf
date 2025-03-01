import functools
import json
import threading
import time

import pika

RABBITMQ_HOST = "localhost"

connection_parameters = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=5672,
    credentials=pika.PlainCredentials("guest", "guest"),
    heartbeat=2,
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
for _ in range(0, 5):
    channel.basic_publish(
        exchange="ts-heartbeat",
        routing_key="test",
        body=json.dumps(body),
        properties=properties,
    )


def callback(ch, method, properties, body, args):
    thrds = args
    processing_thread = threading.Thread(
        target=process, args=(ch, method, properties, body)
    )
    processing_thread.start()
    thrds.append(processing_thread)


def process(ch, method, properties, body):
    print(f"Processing: {body}")
    time.sleep(10)
    print("Done!")

    connection.add_callback_threadsafe(
        functools.partial(ack_message, ch, method.delivery_tag)
    )


def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same Pika channel instance via which
    the message being acknowledged was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
        print(f"[ACK] {delivery_tag}")
    else:
        print("Something's wrong")


threads = []
on_message_callback = functools.partial(callback, args=(threads))
channel.basic_consume(queue="my_queue", on_message_callback=on_message_callback)

try:
    print("Start consuming")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

for thread in threads:
    thread.join()

connection.close()
