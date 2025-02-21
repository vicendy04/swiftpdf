import os
import time

import rabbitpy
from detect_mocks import detect, utils

# Open the connection and the channel
connection = rabbitpy.Connection()
channel = connection.channel()

# Create the worker queue
queue_name = "rpc-worker-%s" % os.getpid()
queue = rabbitpy.Queue(
    channel, queue_name, auto_delete=True, durable=False, exclusive=True
)

# Declare the worker queue
if queue.declare():
    print("Worker queue declared")

# Bind the worker queue
if queue.bind("direct-rpc-requests", "detect-faces"):
    print("Worker queue bound")

# Consume messages from RabbitMQ
for message in queue.consume_messages():
    # Display how long it took for the message to get here
    duration = time.time() - int(message.properties["timestamp"].strftime("%s"))
    print("Received RPC request published %.2f seconds ago" % duration)

    # Write out the message body to a temp file for facial detection process
    temp_file = utils.write_temp_file(message.body, message.properties["content_type"])

    # Detect faces
    result_file = detect.faces(temp_file)

    # Build response properties
    properties = {
        "app_id": "Chapter 6 Listing 2 Consumer",
        "content_type": message.properties["content_type"],
        "correlation_id": message.properties["correlation_id"],
        "headers": {"first_publish": message.properties["timestamp"]},
    }

    # Read the result file
    body = utils.read_image(result_file)

    # Clean up files
    os.unlink(temp_file)
    os.unlink(result_file)

    # Publish the response
    response = rabbitpy.Message(channel, body, properties, opinionated=True)
    response.publish("rpc-replies", message.properties["reply_to"])

    # Acknowledge so that RabbitMQ can remove it from the queue
    message.ack()
    img_id = message.properties["correlation_id"]
    print(f"[WORKER] Successfully processed message {img_id} and sent response")
