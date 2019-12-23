#!/usr/bin/env python

import pika
import threading
import random
from datetime import datetime
import time

# mensajes -> '{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme,tipo;N1}'

class ClientChat():

    #constructor manda peticion de ID
    def __init__(self):
        azar = random.randint(0,99999)
        self.name = "ElThanos"+str(azar)
        self.IdCliente = ''
        self.BandejaEntrada = [] #cuando lee mensajes, guardarlos aca
        self.BandejaSalida = [] #cuando manda mensajes guardarlos aca
        print ('nombre fantasma ', self.name)
        tiempo = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
        mensaje = '{emisor;'+str(self.name)+',receptor;Server,time;'+tiempo+',mensaje;Nedd new ID,cola;'+str(self.name)+',tipo;0}'

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
        #self.FisrtQueue()
    

    def crearCola(self, QueueName):
        self.connectionQ = pika.BlockingConnection(
            pika.ConnectionParameters(host='localHost')
        )
        self.channelQ = self.connectionQ.channel()
        self.channelQ.queue_declare(queue=str(QueueName))
        '''if self.IdCliente == '':
            self.channelQ.basic_consume(queue=str(QueueName),on_message_callback=self.LecturaId,auto_ack=True)
            self.channelQ.start_consuming()
        else:
            self.channelQ.basic_consume(queue=str(QueueName), on_message_callback=self.LecturaChat,auto_ack=True)
            selfchannelQ.start_consuming()'''

    def getID(self, cola):
        self.channelQ.start_consuming(queue =str(cola), on_message_callback=self.LecturaId,auto_ack=True)

    '''#crea cola temporal
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
        threading.Thread(target=self.FisrtListen(),daemon=True).start()'''

    def LecturaId(self, ch ,method, props, body):
        print("LId[X] llega ", body.decode())
        self.IdCliente = body.decode()    
        #self.RealQueue()
        #llamar a la cola real
        #'{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme,tipo;N1}'
        emisorRAW, receptorRAW, timeRAW, mensajeRAW, colaRAW, tipoRAW, extraRAR= body.decode().strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]
        tipo = tipoRAW.split(";")[1]

        print('emisor ',emisor)
        print('receptor ',receptor)
        print('time ',time)
        print('mensaje ',mensaje)
        print('cola ',cola)
        print('tipo ', tipo)
        print("extraRAW ",extraRAR)
        if tipo == str(0):
            self.IdCliente = mensaje
            print("mi ID es ",mensaje)
        elif tipo == str(1):
            print("Clientes actuales: ",mensaje)
        
        

    '''def FisrtListen(self):
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

        threading.Thread(target=self.ListenChat(),daemon=True).start()'''

    def LecturaChat(self, ch, method, props, body):
        print("[X] llega ", body.decode())
        emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW,tipoRAW= body.decode().strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]
        tipo = tipoRAW.split(";")[1]

        if tipo == str(1):
            print("Mensajes recibidos:")
            print(mensaje)
        
        #MSG = emisor+'_'+time+': '+mensaje
        #self.BandejaEntrada.append(str(MSG))
    
    '''def ListenChat(self):
        self.channel.start_consuming()'''

    def VerMensajes(self):
        for MSG in self.BandejaEntrada:
            print(MSG)
    

    def EnviarMensaje(self, mensaje, receptor,tipo):
        tiempo = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
        MSG = '{emisor;'+str(self.IdCliente)+',receptor;'+receptor+',time;'+tiempo+',mensaje;'+mensaje+',cola;cola_MSG,tipo;'+tipo+'}'
        print("[X] mando: ",MSG)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='cola_MSG')
        channel.basic_publish(exchange='',routing_key='cola_MSG',body=str(MSG))
        connection.close()


     

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
    hiloID = threading.Thread(target=cliente.getID,args=[cliente.name])
    hiloID.start()
    print('newID ', cliente.IdCliente)
    time.sleep(1)
    flag = True
    if cliente.IdCliente != '':
        #hiloCola = threading.Thread(target=cliente.crearCola,args=[cliente.IdCliente])
        #hiloCola.start()
        while flag:
            print("--------------------------------------------\nUsuario "+cliente.IdCliente+"\n\nSeleccione una opcion:\n1) Ver clientes conectados\n2) Enviar un mensaje\n3) Ver mensajes recibidos.\n4) Ver mensajes enviados\n5) Salir.\n--------------------------------------------\n")
            opcion = str(input("Opcion: "))

            #clientes conectados
            if opcion == str(1):
                cliente.EnviarMensaje("necesito ver usuarios conectados",cliente.name,"1")
                #en la recepcion, revisar si el mensaje es de tipo 2, printearlo
            
            #enviar mensaje
            elif opcion == str(2):
                receptor = input("ingrese el Id del destinatario: ")
                mensaje = input("Ingrese un mensaje: ")
                cliente.EnviarMensaje(mensaje,receptor,'2')
            
            #mensajes recibidos
            elif opcion == str(3):
                if not cliente.BandejaEntrada:
                    print("Aún no recibes mensajes")
                else:
                    for MSG in cliente.BandejaEntrada:
                        print(MSG)
                    print("------------------------------------------------")

            #mensajes enviados
            elif opcion == str(4):
                if not cliente.BandejaSalida:
                    print("Aún no mandas mensajes")
                else:
                    cliente.EnviarMensaje("necesito mis mensajes enviados","Server","4")
                    print(0)
                    ''' a lo pajero
                    for MSG in cliente.BandejaSalida:
                        print(MSG)
                    print("------------------------------------------------")'''

            #salir
            elif opcion == str(5):
                flag = False
            
            #opcion no válida
            else:
                print('opción no válida, intente nuevamente')
            
    #matar hiloID


    