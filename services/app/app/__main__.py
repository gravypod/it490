import pika
from example import config

connection = pika.BlockingConnection(pika.URLParameters(config.QUEUE_URL))
channel = connection.channel()
channel.queue_declare(queue='hello')


channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
	print("Got Message:", body)


channel.basic_consume(
	queue='hello',
	on_message_callback=callback,
	auto_ack=True
)

channel.start_consuming()
connection.close()
