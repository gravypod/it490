from traceback import print_exc
import json
import uuid
from concurrent.futures import Future
from multiprocessing import Process, Queue
from threading import Thread
from traceback import print_exc
from typing import Callable, Optional, Union, Tuple
from typing import Dict

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


class QueueClient(Process):
    def __init__(self, queue_url: str, queue_app_topic: str):
        super().__init__(daemon=True, name='queue-connection-process')

        self.connection = pika.BlockingConnection(pika.URLParameters(queue_url))
        self.channel: BlockingChannel = self.connection.channel()

        # Setup topic for account
        request_queue_requests = self.channel.queue_declare(queue=queue_app_topic)
        request_queue_responses = self.channel.queue_declare(
            queue='',
            exclusive=True,

        )

        self.request_queue = request_queue_requests.method.queue
        self.response_queue = request_queue_responses.method.queue

        self.channel.basic_consume(
            queue=self.response_queue,
            on_message_callback=self.__on_response,
            auto_ack=True,
        )

        self.resulting_messages = Queue()
        self.futures: Dict[str, Future] = {}

        # Copy messages into future dict in main thread
        self.copy_thread = Thread(target=self.__on_message_main_thread)
        self.copy_thread.start()

    def __on_message_main_thread(self):
        while True:
            correlation_id, body = self.resulting_messages.get(block=True)

            print('Getting response', correlation_id)
            if correlation_id not in self.futures:
                print('\tNo known futures')
                return

            result_future = self.futures[correlation_id]

            try:
                print('Setting result')
                result_future.set_result(json.loads(body.decode()))
            except Exception as e:
                print('Setting exception')
                result_future.set_exception(e)

    def __on_response(
            self,
            channel: BlockingChannel,
            method: pika.spec.Basic.Deliver,
            properties: pika.BasicProperties,
            body: bytes
    ):
        self.resulting_messages.put((properties.correlation_id, body))

    def __rpc(self, message: dict) -> dict:
        correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.request_queue,
            properties=pika.BasicProperties(
                reply_to=self.response_queue,
                correlation_id=correlation_id,
            ),
            body=json.dumps(message)
        )

        self.futures[correlation_id] = result_future = Future()

        try:
            result = result_future.result(timeout=2)
        except TimeoutError:
            raise
        finally:
            del self.futures[correlation_id]

        return result

    def send(self, method: str, payload: dict):
        response = self.__rpc({
            'method': method,
            'user': {},
            'payload': payload
        })

        return response['body'], response['statusCode']

    def run(self) -> None:
        print('Starting queue connection thread')
        self.channel.start_consuming()
        self.channel.close()
        self.connection.close()
