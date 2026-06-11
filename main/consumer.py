# this is the consumer file which will consume the messages from the queue and process them accordingly.
import pika, json, os, django

from pathlib import Path
import os
from dotenv import load_dotenv

# BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(BASE_DIR / '.env')
load_dotenv()


rabbit_url = os.getenv("CLOUDAMQP_URL")
print('rabbit url is  from flask app concumer ', rabbit_url)
params =  pika.URLParameters(str(os.getenv("CLOUDAMQP_URL")))


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main app =>Flask Servics ')
    print("the recived meassage is ",json.loads(body))
    # id = json.loads(body)
    # print(id)
    # product = Product.objects.get(id=id)
    # product.likes = product.likes + 1
    # product.save()
    # print('Product likes increased!')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming from the flask service ')

channel.start_consuming()

channel.close()
