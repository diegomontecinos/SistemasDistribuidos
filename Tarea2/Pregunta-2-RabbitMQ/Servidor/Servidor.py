import pika

#imports Funcionales
import threading
from datetime import datetime
import json
import time


IP = "localhost"

FILE = "log.txt"

class ChatDB ():
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


    def AddClient(self, ClientId):

        if ClientId in self.Clients.keys():
            print("El cliente {0} ya existe".format(ClientId))
            return False
        else:
            self.Clients[ClientId] = []
            print("Cliente {0} agregado exitosamente!".format(ClientId))
            return True

    def AddMessage(self, ClientId, SecondId,TimeStamp, Message):
        #IdMensaje = IDEMISOR-IDRECEPTOR-TIMESTAMP
        IdMessage = str(ClientId)+"_"+str(SecondId)+"_"+str(TimeStamp)
        try:
            log = open(FILE,"a")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))
            return False
        Data = "#".join([str(IdMessage), str(Message)])
        if ClientId in self.Clients.keys():
            if SecondId in self.Clients.keys():
                    self.Clients[SecondId].append(Data)          
                    log.write(Data)
                    print("[EXITO] El mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId)+ " Se registro correctame")
                    return True
            else:
                print("El receptor {0} no se ecuentra registrado".format(SecondId))
                return False
        else:
            print("El emisor {0} no se encuentra registrado".format(ClientId))
            return False
        log.close()
"""
    #Mensajes que he recibido por ClienteId
    def GetMessages(self,ClientId):
        temp = []
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
            mensaje = Chat_pb2.MensajeCliente(IdPropietario = IdEmisor, IdDestinatario = IdReceptor, IdMensaje = IdMensaje,
            TimeStamp = TimeStamp, Mensaje = Mensaje, Error = "" )
            yield mensaje
    #Mensajes enviados por ClietntID
    def GetRecord(self, ClientId):
        temp = []
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
        for tupla in temp:
            IdEmisor,IdReceptor,IdMensaje, TimeStamp, Mensaje = tupla
            mensaje = Chat_pb2.MensajeCliente(IdPropietario = IdEmisor, IdDestinatario = IdReceptor, IdMensaje = IdMensaje,
            TimeStamp = TimeStamp, Mensaje = Mensaje, Error = "" )
            yield mensaje
    
    def GetClients(self, ClientId):
        for client in self.Clients.keys():
            if client != ClientId:
                mensaje = Chat_pb2.MensajeCliente(IdPropietario = "", IdDestinatario = "", IdMensaje = "", TimeStamp = "", Mensaje = client, Error = "" )
                yield mensaje
"""

class Servidor():



    def __init__(self):

        #Variables del servidor 
        self.Directorio = ChatDB()
        self.NombreClientes = {}
        self.ServerId = "Servidor-1"
        self.ClientNumber = 0
        self.Esquema_Mensaje = {
            "Emisor":"",
            "Receptor":"",
            "TimeStamp":"",
            "IdMensaje":"",
            "Mensaje":"",
            "Tipo":"",
        }
        #Crear conexion con localhost
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(IP))
        self.channel = self.connection.channel()
        #definir una cola inicial    
        #threading.Thread(target= self.Crear_Cola("Entrada"), daemon=True).start()
    
    def Crear_Cola(self, conec, nombre):
        print("Creando Canal...")
        #connection = pika.BlockingConnection(pika.ConnectionParameters(IP))
        #channel = connection.channel()
        channel = conec.channel()
        print("Creando Cola {0}...".format(nombre))
        channel.queue_declare(queue = nombre)
        print("Escuchando la cola {0}".format(nombre))
        channel.basic_consume(
            queue=nombre,
            auto_ack=True,
            on_message_callback=self.callback)
        print("Esperando por mensajes...")
        channel.start_consuming()

    #un callback por cola
    def callback(self,ch, method, properties, body):
        objeto_mensaje = json.loads(body)
        
        if str(objeto_mensaje["Tipo"]) == str(1): 
            NewId = "Cliente-"+str(self.ClientNumber+1)
            self.NombreClientes[NewId] = objeto_mensaje["Emisor"]
            if (self.Directorio.AddClient(NewId)):
                self.ClientNumber = self.ClientNumber +1
                print("Se ha agregado a {0} a la lista de clientes".format(NewId))
                respuesta = self.LLenado_Mensaje(Emisor=self.ServerId, Receptor= objeto_mensaje["Emisor"], Mensaje= NewId, Tipo= str(1))
            else:
                respuesta = self.LLenado_Mensaje(Emisor=self.ServerId, Receptor= objeto_mensaje["Error al ser agregado al servidor, El cliente ya existe"], Mensaje= NewId, Tipo= str(0))
            self.Publicar(objeto_mensaje["Emisor"], respuesta)
        #Retornar la lsita de clietnes conectados
        elif str(objeto_mensaje["Tipo"]) == str(2):
            pass
        
        #Guardar y reenviar mensaje a destinatario
        elif str(objeto_mensaje["Tipo"]) == str(3):
            TimeStamp = str(datetime.now().strftime("%d-%b-%Y|%H:%M:%S"))
            if self.Directorio.AddMessage(objeto_mensaje["Emisor"],objeto_mensaje["Receptor"], TimeStamp,objeto_mensaje["Mensaje"]):
                mensaje = " ".join([TimeStamp, objeto_mensaje["Emisor"], objeto_mensaje["Mensaje"]])
                respuesta = self.LLenado_Mensaje(Emisor=self.ServerId, Receptor= objeto_mensaje["Receptor"], Mensaje= mensaje,Tipo= str(3))

            else:
                respuesta = self.LLenado_Mensaje(Emisor=self.ServerId, Receptor= objeto_mensaje["Emisor"], Mensaje= "Ha ocurido un error al enviar el mensaje: {0}".format(objeto_mensaje["Mensaje"]), Tipo= str(0))

            self.Publicar(objeto_mensaje["Emisor"], respuesta)
        
        #Responder con los mensajes recibidos pro el cliente
        elif str(objeto_mensaje["Tipo"]) == str(4):
            pass
        #Responder con los mensajes enviados por el cliente    
        elif str(objeto_mensaje["Tipo"]) == str(5):
            pass
        else:
            print("USTED NO DEBERIA ESTAR AQUI! ¬¬")
    
    def Publicar(self,nombre_cola, mensaje):
        self.channel.basic_publish(exchange='',
                            routing_key=nombre_cola,
                            body= mensaje)
        print("[x] Sent {0}".format(mensaje))

    def LLenado_Mensaje(self, Emisor = "", Receptor = "", IdMensaje = "", Mensaje ="", Tipo =""):
        mensaje = self.Esquema_Mensaje.copy()
        mensaje["Emisor"] = Emisor
        mensaje["Receptor"] = Receptor
        mensaje["TimeStamp"] = str(datetime.now().strftime("%d-%b-%Y|%H:%M:%S"))
        mensaje["IdMensaje"] = IdMensaje
        mensaje["Mensaje"] = Mensaje
        mensaje["Tipo"] = Tipo
        return json.dumps(mensaje)


if __name__ == "__main__":
    servidor = Servidor()
    hilo_saludo = threading.Thread(target= servidor.Crear_Cola, args= [servidor.connection,"Entrada"], daemon=True)
    hilo_saludo.start()
    time.sleep(5)
    input("aprete algo para salir")

