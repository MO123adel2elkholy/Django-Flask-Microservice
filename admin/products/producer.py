# this will prodcue the evetnts from admin service(Django) to the RabbitMQ and then the events will be consumed by the Flask microservice to update the database accordingly.
import pika, json

params = pika.URLParameters('amqps://mpvhpugc:XsdQm-Hn1AbBSPZv8Bsw9SC0I7XaX8nr@warthog.lmq.cloudamqp.com/mpvhpugc')

def publish(message):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='admin')
    props = pika.BasicProperties(content_type='application/json')
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(message), properties=props)
    connection.close()


if __name__ == '__main__':
    publish({"id": 1})

print("Start producing ")