import json
import os
import sys
import time

import pika

from task_models import Task

def main():
    
    
    credentials = pika.PlainCredentials('swtugwcb', 'TVDdnfxpbnBI7RCBca5vU83bvccvu1Ko')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='cow-01.rmq2.cloudamqp.com', port=5672, credentials=credentials, 
                                                               virtual_host='swtugwcb'))
    
    channel = connection.channel()

    channel.queue_declare(queue='web_17_campaign', durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()
        task = Task.objects(id=pk, completed=False).first()
        if task:
            task.update(set__completed=True, set__fullname="Yaroslav", set__email="yaros@yaros.com")
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='web_17_campaign', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)