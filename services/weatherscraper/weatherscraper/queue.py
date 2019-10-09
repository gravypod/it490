import json
from traceback import print_exc
from typing import Dict, Callable, Optional, Union, Tuple

import pika
from pika.adapters.blocking_connection import BlockingChannel


class ResponseException(Exception):
    status_code: int = 500


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

        self.methods: Dict[str, Callable[[dict, dict], Optional[Tuple[int, Union[dict, list]]]]] = {}

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

            metadata: dict = {
                'user': message['user'] if 'user' in message else None
            }
            payload: dict = message['payload']

            status_code, response = self.methods[message['method']](payload, metadata)
            print('Response', response)

        except ResponseException as e:
            print_exc()
            status_code, response = e.status_code, str(e)
        except Exception as e:
            print_exc()
            status_code, response = 500, 'Internal Server Error: ' + str(e)

        if properties.reply_to:
            channel.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps({
                    'statusCode': status_code,
                    'body': response
                })
            )
        else:
            print('Async, one way, message handled')
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print('Acked')

    def register(self, method: str, handler: Callable[[dict, dict], Optional[Tuple[int, Union[dict, list]]]]):
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
