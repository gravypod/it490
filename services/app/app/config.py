from os import getenv

QUEUE_URL = getenv('APP_QUEUE_URL', 'amqp://root:root@rabbitmq:5672/%2F')
QUEUE_TOPIC_APP = getenv('APP_QUEUE_TOPIC_APP', 'requests-app')
DATABASE_URL = getenv('APP_DATABASE_URL', 'mysql+pymysql://app:app@mysql:3306/app')
