#!/usr/bin/env python

import pika
import threading
import random

# mensajes -> '{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme}'

class ClientChat():

    #constructor manda peticion de ID
    def __init__(self):
        azar = random.randint(0,99999)
        self.name = "ElThanos"+str(azar)
        self.IdCliente = ''
        print ('nombre fantasma ', self.name)

        mensaje = '{emisor;'+str(self.name)+',receptor;Server,time;dd-mmm-yyy,mensaje;Nedd new ID,cola;'+str(self.name)+'}'

        #mandar peticion de ID
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='cola_MSG')
        channel.basic_publish(exchange='',routing_key='cola_MSG',body=str(mensaje))
        connection.close()
        #llamar a la función que crea la cola fantasma y que escuche
        print("llama a crear la cola ficticia")
        self.FisrtQueue()

    #crea cola temporal
    def FisrtQueue(self):
        print('firsQueue')
        print('fantasma: ',self.name)
        self.connectionGhost = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channelGhost = self.connectionGhost.channel()
        self.channelGhost.queue_declare(queue=str(self.name))
        self.channelGhost.basic_consume(queue=str(self.name),on_message_callback=self.LecturaId,auto_ack=True)
        print("hace el thread")
        self.channelGhost.start_consuming()
        #threading.Thread(target=self.FisrtListen(),daemon=True).start()

    def LecturaId(self, ch ,method, props, body):
        print("[X] llega ", body.decode())
        self.IdCliente = body.decode()    

    def FisrtListen(self):
        self.channelGhost.start_consuming()


if __name__ == '__main__':
    print('Cliente')
    cliente = ClientChat()