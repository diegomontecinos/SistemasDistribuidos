#!/usr/bin/env python
import pika
import threading
from datetime import datetime

# Servidor
# envíar y recivir mensajes
# excribir en log.txt los mensajes enviados
# ver clientes
# ver todos los mensajes enviados de un cliente

# mensajes  
# ID unico
# texto + timestamp
# cliente-X_Cliente-Y_timestamp#texto
# {tipo:[012345],emisor:Cliente-X,receptor:Cliente-Y,mensaje:mensaje,tiempo:timestamp}
# 
# #


IP = "0.0.0.0"
#Windows port
#PORT = "50051"
#Docker port
PORT = "8080"
FILE = "./Server/log.txt"
EVENTS = []

'''
class chatDB()
class server() main class que tiene objetos chatDB, publisher y consumer
class publichreS()
class consumerS()
'''

class ChatDB ():

    #---------------------------------------------------------------------------
    #contructor, crea el diccionario clientes e intenta abrir el archivo log.txt
    #---------------------------------------------------------------------------
    def __init__(self):
        self.Clients = {}
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

    #-------------------------------------------------------------------------------------------------------
    #agregar clientes, recibe un id y agrega al cliente al diccionario y crea su lista de mensajes recibidos
    #-------------------------------------------------------------------------------------------------------
    def AddClient(self, ClientId):

        if ClientId in self.Clients.keys():
            print("El cliente {0} ya existe".format(ClientId))
            return False
        else:
            self.Clients[ClientId] = []
            print("Cliente {0} agregado exitosamente!".format(ClientId))
            return True

    #------------------------------------------
    #agrega el mensaje a la lista del receptor, retorna el mensaje RAW en caso de existir
    #--------------------------------------
    def AddMessage(self, ClientId, SecondId, Message):
        TimeStamp = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
        #IdMensaje = IDEMISOR_IDRECEPTOR_TIMESTAMP
        IdMessage = str(ClientId)+"_"+str(SecondId)+"_"+str(TimeStamp)
        try:
            log = open(FILE,"a")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))
            return

        Data = "#".join([str(IdMessage), str(Message)])

        if ClientId in self.Clients.keys():
            if SecondId in self.Clients.keys():
                    self.Clients[SecondId].append(Data)          
                    log.write(Data)
                    print("[EXITO] El mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId)+ " Se registro correctame")
                    return Data
            else:
                print("El receptor {0} no se ecnuentra registrado".format(SecondId))
                return 
        else:
            print("El emisor {0} no se encuentra registrado".format(ClientId))
            return 
        log.close()
    
    #
    #obtiene los mensajes en el diccionario
    #
    def GetMessages(self,ClientId):
        temp = []
        temp2 = []
        try:
            for mensaje in self.Clients[ClientId]:
                temp.append(mensaje)
            print("se obtubieron los mensajes del usuario {0}".format(ClientId))
        
        except Exception as error:
            print(error)
            print("Error al acceder al buffer de mensajes del cliente {0}".format(ClientId))
        
        self.Clients[ClientId].clear()
        for m in temp:
            IdMensaje, Mensaje = m.split(sep="#", maxsplit=1)
            IdEmisor,IdReceptor, TimeStamp = IdMensaje.split(sep="_", maxsplit = 2)
            #mensaje = Chat_pb2.MensajeCliente(IdPropietario = IdEmisor, IdDestinatario = IdReceptor, IdMensaje = IdMensaje,
            #TimeStamp = TimeStamp, Mensaje = Mensaje, Error = "" )
            #yield mensaje
            temp2.append((IdEmisor,IdReceptor,TimeStamp,Mensaje))
        return temp2

    # obtener mensajes mandado por el cliente
    # REVISAR
    # 
    def GetRecord(self, ClientId):
        temp = []
        #temp2 = []
        try:
            log = open(FILE,"r")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar abrir el archivo log.txt")
            return
        for linea in log:
            IdMensaje, Mensaje = linea.split(sep="#", maxsplit=1)
            IdEmisor,IdReceptor, TimeStamp = IdMensaje.split(sep="_", maxsplit = 2)
            if IdEmisor == ClientId:
                temp.append((IdEmisor,IdReceptor,IdMensaje, TimeStamp, Mensaje))
        log.close()
        #for tupla in temp:
            #IdEmisor,IdReceptor,IdMensaje, TimeStamp, Mensaje = tupla

            #mensaje = Chat_pb2.MensajeCliente(IdPropietario = IdEmisor, IdDestinatario = IdReceptor, IdMensaje = IdMensaje,
            #TimeStamp = TimeStamp, Mensaje = Mensaje, Error = "" )
            #yield mensaje
        return temp
    
    '''
    def GetAllMessages(self):
        temp = []
        try:
            log = open(FILE,"r")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar abrir el archivo log.txt")
            return
        for linea in log:
            IdMensaje, Mensaje = linea.split(sep="#", maxsplit=1)
            IdEmisor,IdReceptor, TimeStamp = IdMensaje.split(sep="_", maxsplit = 2)
            temp.append((IdEmisor,IdReceptor,IdMensaje, TimeStamp, Mensaje))
        
        return temp'''

    #
    # retorna la lista de clientes menos el que pide
    # 
    def GetClients(self, ClientId):
        temp = []
        for client in self.Clients.keys():
            if client != ClientId:
                #mensaje = Chat_pb2.MensajeCliente(IdPropietario = "", IdDestinatario = "", IdMensaje = "", TimeStamp = "", Mensaje = client, Error = "" )
                #yield mensaje
                temp.append(client)
        return temp



class ConsumerS(): 
    #-------------------------------------------------------------------------------------
    #constructor... declara la cola de IDS y llama a las funciones para sacar datos de ahí
    #-------------------------------------------------------------------------------------
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
        

    #-----------------------------------------
    # mandar respuesta de ID del nevo cliente
    #-----------------------------------------
    def handShake(self,ch, method, props, body):#on_request
        self.conexiones+=1
        response = "Cliente-"+str(self.conexiones)#new ID

        if response not in self.dir_mensajes.keys():
            self.dir_mensajes[response] = []#crea la lista de mensajes del nnuevo cliente
        else:
            self.erorr = 'ID ya existe'

        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                            props.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        #threading.Thread(target=self.escuchar(),daemon = True).start()#no bloque el codigo

    #-----------------------------------
    #saca cosas de la cola de saludo
    #-------------------------------------
    def escuchar(self):
        #while True:
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

    #------------------------------------------------------------------
    #crea la cola de los mensajes a la que el cliente envia el mensaje
    #------------------------------------------------------------------
    def RecibirMensajes(self): 
        self.connectionMSG = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        ) 
        self.channelMSG = self.connectionMSG.channel()
        self.channelMSG.queue_declare(queue='cola_MSG')

        self.channelMSG.basic_consume(queue='cola_MSG',on_message_callback=self.GuardarMSG, auto_ack=True)
        threading.Thread(target=self.leerColaChat(),daemon=True).start()

    #-----------------------------------------------------------------------------------
    #lee mensajes de la cola y revisa si el receptor ha sido creado
    #-----------------------------------------------------------------------------------
    def GuardarMSG(self, ch, method, props, body): 
        mensaje = body.decode().strip('#') #['cliente-x','cliente-y','tiempo', 'menaje']
        cliente2 = mensaje[1]#.split('-')[1] 
        if cliente2 in self.dir_mensajes.keys():
            self.dir_mensajes[cliente2].append(mensaje[-1])
            #falta agregar el id del mensaje
            #self.cant_mensajes +=1
            #falta escribir en log.txt
            #mandar el mensaje a la cola que corresponde
        else:
            self.erorr = 'Cliente receptor no existe'
    
    #-----------------------------
    #saca cosas de la cola de MSG
    #-----------------------------
    def leerColaChat(self):
        #while True:
        print(" [x] Awaiting Chan MSGs")
        self.channelMSG.start_consuming()

    

if __name__ == '__main__':
    server = ConsumerS()
    #print('Pasamos la declaracion de la clase')
    #server.handShake()
    