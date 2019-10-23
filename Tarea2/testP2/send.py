#!/usr/bin/env python
import pika
#conexion al servidor rabbitmq... cambiar localhots por ip p nombre de otor host
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')) #('localhost') 
channel = connection.channel()
#crear cola para mandar mensajes
channel.queue_declare(queue='hello')
#el paso de mensajes es por inermediario... routing_key es el nombre de la cola que declaramos antes
channel.basic_publish(exchange='',
    routing_key='hello',
    body='Hello World!')
print(" [x] Sent 'Hello World!'")
#cerrar la conexion
connection.close ()