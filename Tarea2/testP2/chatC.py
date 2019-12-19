#!/usr/bin/env python
import pika
import uuid


class Consumidor():
    def __init__(self):
         # conexion al servidor rabbitmq
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
                        # "crear" cola para mandar mensajes ''
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        # cliente manda una direccion de la cola 'calback' para rcibir respuestas
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
     # manda una solicitud RPC y bloquea hasta que recibe una respuesta
    def ID(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='cola-saludos',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


if __name__ == '__main__':
    cliente = Consumidor()
    print(" [x] Requesting ID")
    id = cliente.ID(0)
    print(" [.] Got " , id)