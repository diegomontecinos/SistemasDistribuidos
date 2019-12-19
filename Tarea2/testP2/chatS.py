#!/usr/bin/env python
import pika
import threading

# Servidor
# envíar y recivir mensajes
# excribir en log.txt los mensajes enviados
# ver clientes
# ver todos los mensajes enviados de un cliente

# mensajes  
# ID unico
# texto + timestamp

class Servidor():
    def __init__(self):
        self.conexiones = 0 #ID clientes
        self.cant_mensajes = 0 #ID Mensajes
        self.dir_mensajes = dict() #diccionario de 


        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
            )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='cola_IDS')
        self.channel.basic_qos(prefetch_count=10)#cambiar para mas conexiones
        self.channel.basic_consume(queue='cola_IDS', on_message_callback=self.handShake, auto_ack=True) #se ejecuta al recibir una request y manda una respuesta
        threading.Thread(target=self.escuchar(),daemon = True).start()#no bloque el codigo
        
        

    def handShake(self,ch, method, props, body):#on_request

        self.conexiones+=1
        response = "Cliente-"+str(self.conexiones)

        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                            props.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        #threading.Thread(target=self.escuchar(),daemon = True).start()#no bloque el codigo

    def escuchar(self):
        #while True:
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()
    
    

if __name__ == '__main__':
    server = Servidor()
    #print('Pasamos la declaracion de la clase')
    #server.handShake()
    