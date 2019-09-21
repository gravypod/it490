import json
from traceback import print_exc
from typing import Dict, Callable, Optional, Union

import pika
from pika.adapters.blocking_connection import BlockingChannel


class QueueServer:
    def __init__(self, queue_url: str, queue_app_topic: str):
        self.connection = pika.BlockingConnection(pika.URLParameters(queue_url))
        self.channel: BlockingChannel = self.connection.channel()

        # Setup topic for account
        self.channel.queue_declare(queue=queue_app_topic)
        self.channel.basic_consume(
            queue=queue_app_topic,
            on_message_callback=self.__on_request,
            auto_ack=False
        )

        self.methods: Dict[str, Callable[[dict, dict], Optional[Union[dict, list]]]] = {}

    def __on_request(
            self,
            channel: BlockingChannel,
            method: pika.spec.Basic.Deliver,
            properties: pika.BasicProperties,
            body: bytes
    ):
        try:
            print('Got message')
            message = json.loads(body.decode())
            print(message)

            # Reserved for when auth is implemented.
            metadata: dict = {}
            payload: dict = message['payload']

            response = self.methods[message['method']](payload, metadata)
            print('Response', response)

            channel.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response)
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print('Acked')
        except:
            print_exc()
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def register(self, method: str, handler: Callable[[dict, dict], Optional[Union[dict, list]]]):
        self.methods[method] = handler

    def start(self):
        print('Serving RPC API')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()
        self.channel.close()
        self.connection.close()

    def route(self, method):
        print('Registering route')
        original = self

        def handler(fn):
            print('Returning same handler')
            original.register(method, fn)
            return fn

        return handler
