# this will prodcue the evetnts from admin service(Django) to the RabbitMQ and then the events will be consumed by the Flask microservice to update the database accordingly.
import pika, json

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

rabbit_url = os.getenv("CLOUDAMQP_URL")
params = pika.URLParameters(str(rabbit_url))

def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='main')
    props = pika.BasicProperties( method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=props)
    connection.close()


if __name__ == '__main__':
    publish("initalized",{"id": 2})

print("Start producing ")





