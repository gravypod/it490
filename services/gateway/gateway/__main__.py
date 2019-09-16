import pika
from gateway import config
from time import sleep

connection = pika.BlockingConnection(pika.URLParameters(config.QUEUE_URL))
channel = connection.channel()
channel.queue_declare(queue='hello')


while True:
	print("Sending message")
	channel.basic_publish(
		exchange='',
		routing_key='hello',
		body='Hello World!'
	)
	sleep(1)

connection.close()

