1. The following code from `init.py` to declare an exchange to route RPC requests through and an exchange to route RPC replies through.

2. `worker.py` Once an image has been processed, the new image will be published back through RabbitMQ, using the routing information provided in the original message’s properties.

3. `publisher.py` Declare a response queue which the publisher will retrieve processed images. Create a blocking application instead of an asynchronous one for this demo.

Source: RabbitMQ In Depth.
