#!/usr/bin/env python
import pika
import threading
import threading

#servidor

class Server():
    def __init__(self): #crea un chanel para escuchar la peticion de ID
        self.conexoines = 0
        self.recepctionID = 0
        self.connectionID = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connectionID.channel()

    def RecibirID(self, ch, method, properties, body):
        #recibe la peticion de ID
        self.recepctionID = body.decode()
        print("[X] recibí ", self.recepctionID)

    def consumirSaludo(self):
        self.channel.basic_consume(queue='saludo', on_message_callback=self.RecibirID, auto_ack=True)

if __name__ == '__main__':
    servidor = Server()
    servidor.consumirSaludo()

