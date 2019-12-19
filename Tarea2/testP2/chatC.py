#!/usr/bin/env python
import pika
import uuid
import logging

# cliente
# enviar y recibir mensajes
# 

class Consumer():
    def __init__(self):
         # conexion al servidor rabbitmq
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
                        # "crear" cola para mandar mensajes ''
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue  # cola de respuesta
        # crea la cola en la que "consume" o le la respuesta en la cola callback y cuando hay algo, invoca a la funcion on_response
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response, 
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()
            self.ID = self.response

    
     # manda una solicitud RPC y bloquea hasta que recibe una respuesta
    def ID(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='cola_IDS',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response) 


if __name__ == '__main__':
    cliente = Consumer()
    print(" [x] Requesting ID")
    id = cliente.ID(0)
    print(" [.] Got " , id)

'''
#LOGGER = logging.getLogger(__name__)
class Consumer():
    def __init__(self, ):
        self.conexiones = 0
        self.consuming = False
        self.message = ''
        
    def connectar(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

    def callback(self, ch, method, props, body):
        self.message = body.decode()


class Publisher():
    def __init__(self):
        super().__init__()

class Client():
    def __init__(self):
        self.consumidor = Consumer()
        self.publicador = Publisher()

if __name__ == '__main__':
    cliente = Client()
    '''