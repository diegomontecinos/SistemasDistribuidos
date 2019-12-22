#!/usr/bin/env python

import pika
import threading

# mensajes -> '{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme,tipo;N°}'
# mensaje tipo 0: pedir ID
# mensaje tipo 1: pedir usuarios conectados
# mensaje tipo 2: enviar mensajes
# mensaje tipo 3: pedir mensajes recibidos
# mensaje tipo 4: pedir mensajes enviados

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
        #self.CrearColaMSG()

    #crear cola de mensajes de chat
    def CrearColaMSG(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='cola_MSG')

        self.channel.basic_consume(queue='cola_MSG', on_message_callback=self.RecibirMSG,auto_ack=True)
        print('voy al thread')
        #threading.Thread(target=self.Escuchar(),daemon = True).start()
        self.channel.start_consuming()
        

    #recibe el mensaje y dependiendo de si es un saludo o un mensaje, llama a la funcion que corresponde
    def RecibirMSG(self, ch, method, prop, body):
        print("RM [X] llega ",body.decode())
        emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW,tipoRAW = body.decode().strip("{}").split(",")
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

        '''if 'Cliente' not in emisor:#no tiene ID
            self.AddClient(cola)
        elif receptor in self.directorioUser.keys():#revisa si el receptor esta dentro de los clientes
            self.EnviarMensaje(body.decode())'''
        #'{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme,tipo;N°}'
        MSG = ''
        if tipo == str(0): #solicita ID
            self.AddClient(cola)
        elif tipo == str(1): #pide self.directorioUser.keys()
            usuarios = self.ObtenerClientes(emisor)
            MSG = "{emisor;"+emisor+",receptor;"+receptor+",time;"+time+",mensaje;"+usuarios+",tipo;1}"
            print("llamo a enviar mensaje con: ", MSG)
            self.EnviarMensaje(MSG,receptor,'1')
            #llamar a funcion enviar mensaje-> con cola receptora y tipo =1
        elif tipo == str(2): #enviar mensaje ->  cambiar por solo guardar el mensaje en la cola y guardar en log.txt
            if receptor in self.directorioUser.keys():
                #self.EnviarMensaje(body.decode())
                self.GuardarMSG(body.decode())
        elif tipo == str(3): #pedir mensajes recibidos... self.directorioUser[]
            a=1
            #llamar a función enviar mensaje con cola y tipo 3
        elif tipo == str(4): #pedir mensajes enviados...
            a=0
            #crear una funcion que lea el log.txt y saque los mensajes de usuario

    #retorna los clientes
    def ObtenerClientes(self,cliente):
        listaUsuarios = ''
        for user in self.directorioUser.keys():
            if user != cliente:
                listaUsuarios = listaUsuarios+user+'\n'
        return listaUsuarios

    #cre un ID para el nuevo cliente y se lo manda a la "cola virtual"
    def AddClient(self, cola):
        print('add client')
        self.cantidadConexiones+=1
        NewID = 'Cliente-'+str(self.cantidadConexiones)#crear ID

        print('cola ',cola)
        print('new id ', NewID)

        self.directorioUser[NewID] = []#crear lista de mensajes
        print ('diccionario ', self.directorioUser)
        print('Usuario: ',NewID,' creado.')
        #mandar a cola virtual
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.basic_publish(exchange='',routing_key=str(cola),body=str(NewID))
        connection.close()

    def EnviarMensaje(self, RAW, receptor,codigo):#'{e,r,t,M,c,t}'
        print("EN[X] llega ", RAW)#.decode())
        '''emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW,tipoRAW = RAW.strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]
        tipo = tipoRAW.split(";")[1]'''

        #MSG = emisor+'_'+time+': '+mensaje
        if codigo == str(1):
            MSG = RAW
        elif codigo == str(2):
            MSG = 'ver que onda'
        elif codigo == str(3):
            MSG = 'ver que onda'
        elif codigo == str(4):
            MSG = 'ver que onda'

        print('Envio: ', MSG)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.basic_publish(exchange='',routing_key=str(receptor),body=MSG)

        connection.close()
        #self.GuardarMSG(RAW)

    def GuardarMSG(self, RAW):
        emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW,tipoRAW = RAW.strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]
        tipo = tipoRAW.split(";")[1]

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
    hiloServer = threading.Thread(target=servidor.CrearColaMSG,args=[])
    hiloServer.start()
