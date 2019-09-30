import json
from multiprocessing import Process

import pika
from pika.adapters.blocking_connection import BlockingChannel


class QueueConnection(Process):
    def __init__(self, queue_url: str, queue_app_topic: str):
        super().__init__(daemon=True, name='queue-connection-process')

        self.connection = pika.BlockingConnection(pika.URLParameters(queue_url))
        self.channel: BlockingChannel = self.connection.channel()

        # Setup topic for account
        request_queue_requests = self.channel.queue_declare(queue=queue_app_topic)

        self.request_queue = request_queue_requests.method.queue

    def __rpc(self, message: dict):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.request_queue,
            properties=pika.BasicProperties(),
            body=json.dumps(message)
        )

    def send(self, method: str, payload: dict):
        self.__rpc({
            'method': method,
            'user': {},
            'payload': payload
        })
