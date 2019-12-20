#!/usr/bin/env python

import pika
import threading

# mensajes -> '{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme}'

FILE = 'log.txt'

class ServerChat():
    
    #contructor, inicia variables de ids cliente, el diccionario de los clientes y el archivo log.txt,
    #llama a la funcion de crear cola
    def __init__(self):
        self.cantidadConexiones = 0
        self.directorioUser = dict()
        self.serverID = 'S01'

        try:
            file = open(FILE,"r")
            print("Ya existe un archivo log")
            file.close()
        except IOError:
            print("No se encontro un archivo log")
            try: 
                file = open(FILE, "w")
                print("Archivo log creado exitosamente")
                file.close()
            except IOError:
                print("Ha ocurrido un error inesperado al crear el archivo log")
        print('diccionario ',self.directorioUser)
        self.CrearColaMSG()

    #crear cola de mensajes de chat
    def CrearColaMSG(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='cola_MSG')

        self.channel.basic_consume(queue='cola_MSG', on_message_callback=self.RecibirMSG,auto_ack=True)
        #hacer el thread que busca mensajes
        print('voy al thread')
        threading.Thread(target=self.Escuchar(),daemon = True).start()
        

    #recibe el mensaje y dependiendo de si es un saludo o un mensaje, llama a la funcion que corresponde
    def RecibirMSG(self, ch, method, prop, body):
        print("[X] llega ",body.decode())
        emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW = body.decode().strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]
        print('emisor ',emisor)
        print('receptor ',receptor)
        print('time ',time)
        print('mensaje ',mensaje)
        print('cola ',cola)

        if 'Cliente' not in emisor:#no tiene ID
            self.AddClient(cola)
        elif receptor in self.directorioUser.keys():#revisa si el receptor esta dentro de los clientes
            self.EnviarMensaje(body.decode())
        
    #cre un ID para el nuevo cliente y se lo manda a la "cola virtual"
    def AddClient(self, cola):
        print('add client')
        self.cantidadConexiones+=1
        NewID = 'Cliente-'+str(self.cantidadConexiones)#crear ID

        print('cola ',cola)
        print('new id ', NewID)

        self.directorioUser[NewID] = []#crear lista de mensajes
        print ('diccionario ', self.directorioUser)
        #mandar a cola virtual
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.basic_publish(exchange='',routing_key=str(cola),body=str(NewID))
        connection.close()

    def EnviarMensaje(self, RAW):
        print("[X] llega ", RAW.decode())
        emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW = RAW.strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]

        MSG = emisorRAW+'_'+time+': '+mensaje

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.basic_publish(exchange='',routing_key=str(receptor),body=MSG)

        connection.close()
        self.GuardarMSG(RAW)

    def GuardarMSG(self, RAW):
        emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW = RAW.strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]

        MSGtoWrite = emisor+'_'+receptor+'_'+time+'#'+mensaje

        try:
            log = open(FILE,"a")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(mensaje)+" entre los clientes :"+str(emisor)+" -- "+str(receptor))
            return

        self.directorioUser[receptor].append(MSGtoWrite)
        log.write(MSGtoWrite+'\n')

        log.close()

    def Escuchar(self):
        self.channel.start_consuming()

       


if __name__ == '__main__':
    print('Servidor')
    servidor = ServerChat()
