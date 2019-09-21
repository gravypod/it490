import uuid
from multiprocessing import Process, Queue
from threading import Thread
from time import sleep
from typing import Dict

import pika
import json

from pika.adapters.blocking_connection import BlockingChannel
from concurrent.futures import Future


class QueueConnection(Process):
    def __init__(self, queue_url: str, queue_app_topic: str):
        super().__init__(daemon=True, name='queue-connection-process')

        self.connection = pika.BlockingConnection(pika.URLParameters(queue_url))
        self.channel: BlockingChannel = self.connection.channel()

        # Setup topic for account
        request_queue_requests = self.channel.queue_declare(queue=queue_app_topic)
        request_queue_responses = self.channel.queue_declare(
            queue='',
            exclusive=True
        )

        self.request_queue = request_queue_requests.method.queue
        self.response_queue = request_queue_responses.method.queue

        self.channel.basic_consume(
            queue=self.response_queue,
            on_message_callback=self.__on_response,
            auto_ack=True
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

    def send(self, method: str, payload: dict) -> dict:
        return self.__rpc({
            'method': method,
            'payload': payload
        })

    def run(self) -> None:
        print('Starting queue connection thread')
        self.channel.start_consuming()
        self.channel.close()
        self.connection.close()
