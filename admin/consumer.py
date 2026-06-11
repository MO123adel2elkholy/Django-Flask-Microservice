# this is the consumer file which will consume the messages from the queue and process them accordingly.
import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params =  pika.URLParameters('amqps://mpvhpugc:XsdQm-Hn1AbBSPZv8Bsw9SC0I7XaX8nr@warthog.lmq.cloudamqp.com/mpvhpugc')


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    print("the recived meassage is ",json.loads(body))
    # id = json.loads(body)
    # print(id)
    # product = Product.objects.get(id=id)
    # product.likes = product.likes + 1
    # product.save()
    # print('Product likes increased!')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
