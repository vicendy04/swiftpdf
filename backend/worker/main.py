import json

import pika

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
    correlation_id = header.correlation_id
    print(result_data)
    print(correlation_id)

    # Lưu kết quả vào database
    # then reply

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
    channel.basic_consume(queue=request_queue, on_message_callback=callback)

    print("Result processor started. Waiting for results...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
