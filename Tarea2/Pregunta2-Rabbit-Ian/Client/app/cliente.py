#!/usr/bin/env python

import pika
import threading
import random
from datetime import datetime
import time
import ast
import sys


class ClientChat():

    #constructor manda peticion de ID
    def __init__(self):
        azar = random.randint(0,99999)
        self.name = "ElThanos"+str(azar)
        self.IdCliente = ''
        self.BandejaEntrada = [] #cuando lee mensajes, guardarlos aca
        self.BandejaSalida = [] #cuando manda mensajes guardarlos aca
        self.MensajesDeEntrada = ''
       
        diccionarioMSG=dict()
        diccionarioMSG['emisor'] =self.name
        diccionarioMSG['receptor'] = self.name
        diccionarioMSG['tiempo'] = ''
        diccionarioMSG['mensaje'] = 'necesito Id'
        diccionarioMSG['cola'] = self.name
        diccionarioMSG['tipo'] = '0'

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='0.0.0.0')
        )
        channel = connection.channel()
        channel.queue_declare(queue='cola_MSG')
        channel.basic_publish(exchange='',routing_key='cola_MSG',body=str(diccionarioMSG))
        connection.close()
       

    def crearCola(self, QueueName):
        connectionQ = pika.BlockingConnection(
            pika.ConnectionParameters(host='localHost')
        )
        channelQ = connectionQ.channel()
        channelQ.queue_declare(queue=str(QueueName))
        channelQ.basic_consume(queue=str(QueueName), on_message_callback=self.Lectura,auto_ack=True)
        channelQ.start_consuming()


    def Lectura(self, ch, method, props, body):
        entra = ast.literal_eval(body.decode('utf-8'))
        
        if entra['tipo'] == str(0):
            self.IdCliente = entra['mensaje']
            print("me llega "+entra['mensaje']+"como Id")
        elif entra['tipo'] == str(1):
            self.MensajesDeEntrada = entra['mensaje']

        elif entra['tipo'] == str(3):
            self.MensajesDeEntrada = entra['mensaje']

        elif entra['tipo'] == str(4):
            self.MensajesDeEntrada = entra['mensaje']


    def EnviarMensaje(self, mensaje, receptor,tipo):
        tiempo = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
        diccionarioMSG=dict()
        diccionarioMSG['emisor'] =self.IdCliente
        diccionarioMSG['receptor'] = receptor
        diccionarioMSG['tiempo'] = tiempo
        diccionarioMSG['mensaje'] = mensaje
        diccionarioMSG['cola'] = receptor
        diccionarioMSG['tipo'] = tipo
        MSG = str(diccionarioMSG)
        #print("[X] mando: ",MSG)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='cola_MSG')
        channel.basic_publish(exchange='',routing_key='cola_MSG',body=MSG)
        connection.close()



# mensaje tipo 0: pedir ID
# mensaje tipo 1: pedir usuarios conectados
# mensaje tipo 2: enviar mensajes
# mensaje tipo 3: pedir mensajes recibidos
# mensaje tipo 4: pedir mensajes enviados

if __name__ == '__main__':
    print('Cliente')
    cliente = ClientChat()
    #ver opcion de reiniciar el thread si es que no llega el id
    hiloID = threading.Thread(target=cliente.crearCola,args=[cliente.name])
    hiloID.start()
    time.sleep(0.5)
    flag = True
    entrada = input("Presione una tecla para continuar")
    if cliente.IdCliente != '':
        while flag:
            #print("mi ID: ", cliente.IdCliente)
            print("--------------------------------------------\nUsuario "+cliente.IdCliente+"\n\nSeleccione una opcion:\n1) Ver clientes conectados\n2) Enviar un mensaje\n3) Ver mensajes recibidos.\n4) Ver mensajes enviados\n5) Salir.\n--------------------------------------------\n")
            opcion = str(input("Opcion: "))

            #clientes conectados
            if opcion == str(1):
                cliente.EnviarMensaje("necesito ver usuarios conectados",cliente.IdCliente,opcion)
                time.sleep(0.5)
                print("usuarios conectados: ",cliente.MensajesDeEntrada)
                cliente.MensajesDeEntrada=''
          
            #enviar mensaje
            elif opcion == str(2):
                receptor = input("ingrese el Id del destinatario: ")
                mensaje = input("Ingrese un mensaje: ")
                cliente.EnviarMensaje(mensaje,receptor,opcion)
            
            #mensajes recibidos
            elif opcion == str(3):
                cliente.EnviarMensaje("necesito leer mensajes",cliente.IdCliente,opcion)
                time.sleep(0.5)
                if cliente.MensajesDeEntrada=='':
                    print('aun no has recibido mensajes')
                else:
                    print("Mensajes recibidos:\n"+cliente.MensajesDeEntrada)
                cliente.MensajesDeEntrada=''

            #mensajes enviados
            elif opcion == str(4):
                cliente.EnviarMensaje("necesito mis mensajes enviados",cliente.IdCliente,opcion)
                time.sleep(0.5)
                if cliente.MensajesDeEntrada=='':
                    print('aun no has enviado mensajes')
                else:
                    print("Mensajes enviados:\n"+cliente.MensajesDeEntrada)
                cliente.MensajesDeEntrada=''

            #salir
            elif opcion == str(5):
                flag = False
            
            #opcion no válida
            else:
                print('opcion no valida, intente nuevamente')
        print("ha decidido salir")
        print("adios.")
        sys.exit()
            
    #matar hiloID
    sys.exit()
    


    