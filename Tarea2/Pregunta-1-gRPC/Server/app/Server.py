#python -m grpc_tools.protoc -I ./Server/Protos --python_out=./Server --grpc_python_out=./Server ./Server/Protos/Chat.proto ; python -m grpc_tools.protoc -I ./Server/Protos --python_out=./Client --grpc_python_out=./Client ./Server/Protos/Chat.proto

#imports de rpc y protos
import grpc
import Chat_pb2
import Chat_pb2_grpc

#imports Funcionales
import threading
from datetime import datetime
from concurrent import futures


IP = "[::]"
#IP = "0.0.0.0"
#Windows port
PORT = "50051"
#Docker port
#PORT = "8080"
FILE = "log.txt"
EVENTS = []


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

    def AddMessage(self, ClientId, SecondId, Message):
        TimeStamp = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
        #IdMensaje = IDEMISOR-IDRECEPTOR-TIMESTAMP
        IdMessage = str(ClientId)+"_"+str(SecondId)+"_"+str(TimeStamp)
        try:
            log = open(FILE,"a")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))
            return

        Data = "{0}#{1}".format(str(IdMessage),str(Message))

        if ClientId in self.Clients.keys():
            if SecondId in self.Clients.keys():
                    self.Clients[SecondId].append(Data)          
                    log.write(Data+"\n")
                    print("[EXITO] El mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId)+ " Se registro correctame")
                    return Chat_pb2.Confirmacion(Tipo = 1, IdPropietario=ClientId, IdMensaje = IdMessage, Error =  "" )
            else:
                print("El receptor {0} no se ecnuentra registrado".format(SecondId))
                return Chat_pb2.Confirmacion(Tipo = 0, IdPropietario=ClientId, IdMensaje = IdMessage, Error =  "El receptor {0} no se ecnuentra registrado".format(SecondId) )
        else:
            print("El emisor {0} no se encuentra registrado".format(ClientId))
            return Chat_pb2.Confirmacion(Tipo = 0, IdPropietario=ClientId, IdMensaje = IdMessage, Error =  "El emisor {0} no se encuentra registrado".format(ClientId))
        log.close()
    
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
        
        return temp
    def GetClients(self, ClientId):
        for client in self.Clients.keys():
            if client != ClientId:
                mensaje = Chat_pb2.MensajeCliente(IdPropietario = "", IdDestinatario = "", IdMensaje = "", TimeStamp = "", Mensaje = client, Error = "" )
                yield mensaje


                   
class ChatServicer (Chat_pb2_grpc.ChatServicer):

    #Directorio de clientes

    def __init__(self):
        self.Directorio = ChatDB()
        self.ServerId = "S01"
        self.ClientNumber = 0
        self.Events = []
        print("iniciando servicios")
        #threading.Thread(target= self.Menu()).start()
    
    def Saludo(self, request, context):

        NewId = "Cliente-"+str(self.ClientNumber+1)
        if (request.Tipo == 0):
            if (self.Directorio.AddClient(NewId)):
                self.ClientNumber = self.ClientNumber +1
                print("Se ha agregado a {0} a la lista de clientes".format(NewId))
                return Chat_pb2.Saludos(Tipo = 1, IdCliente = NewId, IdServidor = str(self.ServerId), Error = "")
            else:
                return Chat_pb2.Saludos(Tipo = 1, IdCliente = "", IdServidor = "", Error = "Error al ser agregado al servidor, El cliente ya existe")
        elif (request.Tipo == 1):
            print("USTED NO DEBERIA ESTAR AQUI! ¬¬")

    def EnvioSolicitud(self, request, context):
        return self.Directorio.AddMessage(request.IdPropietario, request.IdDestinatario, request.Mensaje)

    def DespachoMensajes(self, request, context):
        if (request.Tipo == "r"):
            while True:
                return self.Directorio.GetMessages(request.IdCliente)
        elif (request.Tipo == "e"):
            while True:
                return self.Directorio.GetRecord(request.IdCliente)
        elif (request.Tipo == "c"):
            while True:
                return self.Directorio.GetClients(request.IdCliente)
        else:
            print("Usted NO DEBERIA ESTAR AQUI! ¬¬")
""" 
    def Menu(self):
        option = 0
        while option != 4:
            print("--------------------------------------------\nServidor {0}\n\nSeleccione una opcion:\n1) Revisar eventos del servidor\n2) Ver clientes activos.\n3) Ver mensajes almacenados\n4) Salir.\n--------------------------------------------\n".format(self.ServerId))
            option = str(input("Opcion: "))
            
            if option == str(1):
                for event in self.Events:
                    print(event)
            elif option == str(2):
                i = 1
                for client in self.Directorio.GetClients():
                    print("{0}) {1}".format(i, client))
                    i=i+1
            elif option == str(3):
                AllMessages = self.Directorio.GetAllMessages()
                print("--------------------------------------------\nMensajes almacenados en log.txt:\n----fecha y hora----|-Emisor-|-Receptor-|----Mensaje----\n")
                for IdEmisor,IdReceptor,IdMensaje, TimeStamp, Mensaje in AllMessages:
                    print("{0} {1} {2} {3}".format(TimeStamp, IdEmisor, IdReceptor, Mensaje))
                print("--------------------------------------------\n")
            elif option == str(4):
                break
            else:
                print("Ha seleccionado una opcion no valida, intentelo nuevamente")
def serve():
    
    ChatServer = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    Chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), ChatServer)
    ChatServer.add_insecure_port(IP+":"+PORT)
    ChatServer.start()
    ChatServer.wait_for_termination()
"""
if __name__ == '__main__':
    #serve()
    ChatServer = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    Chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), ChatServer)
    ChatServer.add_insecure_port(IP+":"+PORT)
    ChatServer.start()
    ChatServer.wait_for_termination()