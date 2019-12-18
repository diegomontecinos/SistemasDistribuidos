#!/usr/bin/env python
import pika
#se establece la conexion y se declara la cola de mensajes
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')#nombre de la cola

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = \
            props.correlation_id),
        body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)#cambiar para mas conexiones
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request) #se ejecuta al recibir una request y manda una respuesta

print(" [x] Awaiting RPC requests")
channel.start_consuming()