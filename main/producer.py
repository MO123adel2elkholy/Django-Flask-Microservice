# this will prodcue the evetnts from main service(Flask) to the admin service(Django) to the RabbitMQ and then the events will be consumed by the Flask microservice to update the database accordingly.
import pika, json

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

rabbit_url = os.getenv("CLOUDAMQP_URL")
params = pika.URLParameters(str(rabbit_url))

def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='admin')
    props = pika.BasicProperties( method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=props)
    connection.close()


if __name__ == '__main__':
    publish("initalized",{"id": 5})

print("Start producing ")





