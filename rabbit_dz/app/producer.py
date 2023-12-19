import json
from datetime import datetime

import pika

from task_models import Task
from faker import Faker

fake = Faker('uk-UA')

credentials = pika.PlainCredentials('swtugwcb', 'TVDdnfxpbnBI7RCBca5vU83bvccvu1Ko')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='cow-01.rmq2.cloudamqp.com', port=5672, credentials=credentials, 
                                                               virtual_host='swtugwcb'))

channel = connection.channel()


channel.exchange_declare(exchange='Web17 service', exchange_type='direct')
channel.queue_declare(queue='web_17_campaign', durable=True)
channel.queue_bind(exchange='Web17 service', queue='web_17_campaign')

def create_tasks(nums: int):
    for i in range(nums):
        task = Task(fullname=fake.name(), email=fake.email()).save()

        channel.basic_publish(
            exchange='Web17 service',
            routing_key='web_17_campaign',
            body=str(task.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == '__main__':
    create_tasks(1000)