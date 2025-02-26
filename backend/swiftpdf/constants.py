from django.conf import settings


# Avoid using Enum for dynamic configurations from settings.py.
# class RabbitMQConfig(Enum):
class RabbitMQConfig:
    RABBITMQ_URL = settings.RABBITMQ_URL
    REQUEST_EXCHANGE = settings.REQUEST_EXCHANGE
    REPLY_EXCHANGE = settings.REPLY_EXCHANGE
    REQUEST_QUEUE = settings.REQUEST_QUEUE
    REPLY_QUEUE = settings.REPLY_QUEUE
