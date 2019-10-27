import json
import uuid
from typing import Optional

import pika
from flask import jsonify
from flask_jwt_extended import get_jwt_claims
from pika.adapters.blocking_connection import BlockingChannel


class QueueClientSession:
    def __init__(
            self,
            parameters: Optional[pika.connection.Parameters],
            request_queue_topic: str
    ):
        self.parameters = parameters
        self.request_queue_topic = request_queue_topic
        self.connection: Optional[BlockingChannel] = None
        self.channel: Optional[BlockingChannel] = None

        self.request_queue: Optional[str] = None
        self.response_queue: Optional[str] = None

    def __enter__(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel: BlockingChannel = self.connection.channel()

        # Setup topic for account
        self.request_queue = self.channel.queue_declare(queue=self.request_queue_topic).method.queue
        self.response_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.queue_delete(self.response_queue)
        self.channel.close()
        self.connection.close()


class QueueConnection:
    def __init__(self, queue_url: str, queue_app_topic: str):
        self.parameters = pika.URLParameters(queue_url)
        self.request_queue_topic = queue_app_topic

    def __rpc(self, message: dict) -> dict:
        correlation_id = str(uuid.uuid4())

        with QueueClientSession(self.parameters, self.request_queue_topic) as session:
            # Publish our message
            session.channel.basic_publish(
                exchange='',
                routing_key=session.request_queue,
                properties=pika.BasicProperties(
                    reply_to=session.response_queue,
                    correlation_id=correlation_id,
                ),
                body=json.dumps(message)
            )

            # Read our reply

            for deliver, properties, message in session.channel.consume(
                    queue=session.response_queue,
                    auto_ack=True,
                    exclusive=True,
                    inactivity_timeout=5
            ):
                return json.loads(message.decode())

    def send(self, method: str, payload: dict, make_jsonified: bool = True):
        response = self.__rpc({
            'method': method,
            'user': get_jwt_claims(),
            'payload': payload
        })

        if make_jsonified:
            body = jsonify(response['body'])
        else:
            body = response['body']

        return body, response['statusCode']
