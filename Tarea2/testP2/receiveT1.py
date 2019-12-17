#!/usr/bin/env python
import pika
#conexion al servidor rabbitmq... cambiar localhots por ip p nombre de otor host
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#crear cola de recepcion en caso de que este cosdigo se ejecute antes que el que envia
channel.queue_declare(queue='hello')
#recibir un mensaje... hay que suscribire a una cola
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
# 'decir' a rabbitmq que la funcion anterior recibe un mensaje de la cola declarada anteriormente
channel.basic_consume(queue='hello',
    auto_ack=True,
    on_message_callback=callback)
#'loop' infinito para que reciba
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()