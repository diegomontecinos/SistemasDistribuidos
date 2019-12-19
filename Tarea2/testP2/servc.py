#!/usr/bin/env python
import pika
import threading
import threading

#clientes


class Producer():
    def __init__(self): #funcion que envia un mensaje al servidor para obtener ID [SOLO ENVÍA]
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='saludo')
        self.channel.basic_publish(exchange='', routing_key='saludo',body='0')
        self.channel.close()#manda su ID 0 y muere
    
    def ConexionEntrada(self): #crea chanel para recibir nuevo ID
        self.connectionMSG = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channelMSG = self.connectionMSG.channel()

    def recibirID(self, ch, method, props, body):#funcion para recibir su ID y crear una cola con ese nombre
        self.ID =  int(body.decode())
        print("[X] recibí ", self.MSG)
        #crear mi cola de recibi mensajes


    def consumir(self):
        self.channelMSG.basic_consume(queue='[]')

    def conexionChat(self):
        self.connectionChat = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channelChat = self.connectionChat.channel()
    
    def recibirChat(self, ch, method, props, body):
        self.MSG = str(body.decode())
        print("[Chat]: ", self.MSG)

    