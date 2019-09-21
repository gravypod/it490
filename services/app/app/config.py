from os import getenv

QUEUE_URL = getenv('APP_QUEUE_URL', 'amqp://root:root@rabbitmq:5672/%2F')

