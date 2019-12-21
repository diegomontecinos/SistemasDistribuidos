#!/usr/bin/env python

import pika
import threading
import random
from datetime import datetime
import time

# mensajes -> '{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme}'

class ClientChat():

    #constructor manda peticion de ID
    def __init__(self):
        azar = random.randint(0,99999)
        self.name = "ElThanos"+str(azar)
        self.IdCliente = ''
        self.BandejaEntrada = []
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
        print('firstQueue')
        print('fantasma: ',self.name)
        self.connectionGhost = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channelGhost = self.connectionGhost.channel()
        self.channelGhost.queue_declare(queue=str(self.name))
        self.channelGhost.basic_consume(queue=str(self.name),on_message_callback=self.LecturaId,auto_ack=True)
        print("hace el thread")
        #self.channelGhost.start_consuming()
        threading.Thread(target=self.FisrtListen(),daemon=True).start()

    def LecturaId(self, ch ,method, props, body):
        print("[X] llega ", body.decode())
        self.IdCliente = body.decode()    
        self.RealQueue()
        #llamar a la cola real

    def FisrtListen(self):
        self.channelGhost.start_consuming()


    def RealQueue(self):
        print('Real Cola')
        print('new ID ', self.IdCliente)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=str(self.IdCliente))
        self.channel.basic_consume(queue=str(self.IdCliente),on_message_callback=self.LecturaChat,auto_ack=True)

        threading.Thread(target=self.ListenChat(),daemon=True).start()

    def LecturaChat(self, ch, method, props, body):
        emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW = body.decode().strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]

        MSG = emisor+'_'+time+': '+mensaje
        self.BandejaEntrada.append(str(MSG))
    
    def ListenChat(self):
        self.channel.start_consuming()

    def VerMensajes(self):
        for MSG in self.BandejaEntrada:
            print(MSG)
    

    def EnviarMensaje(self,mensaje, receptor):
        tiempo = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
        MSG = '{emisor;'+str(self.IdCliente)+',receptor;'+receptor+',time;'+tiempo+',mensaje;'+mensaje+',cola;cola_MSG}'
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='cola_MSG')
        channel.basic_publish(exchange='',routing_key='cola_MSG',body=str(MSG))
        connection.close()

    def crearCola(self, QueueName):
        connectionQ = pika.BlockingConnection(
            pika.ConnectionParameters(host='localHost')
        )
        channelQ = connectionQ.channel()
        channelQ.queue_declare(queue=str(QueueName))
        channelQ.basic_consume(queue=str(QueueName),on_message_callback=self.EnviarMensaje,auto_ack=True)
     

'''  
    def Run(self):
        print("---------------------\nBienvenido: ",self.IdCliente)
        print("---------------------\n")
        opcion = 0
        while opcion != 5:
            print("\nSeleciones una opcion:\n1) Ver Clientes conectados.\n2)Enviar un mensaje.\n3)Ver mensajes recibidos.\n4)Ver mensajes enviados.\n5)Salir.\n--------------------------------------------\n")
            opcion = str(input("Opcion: "))

            if opcion == str(1):
                #buscar usuarios
                if 0:
                    print()
'''



if __name__ == '__main__':
    print('Cliente')
    cliente = ClientChat()
    cliente.EnviarMensaje('hola Cliente-2','Cliente-2')