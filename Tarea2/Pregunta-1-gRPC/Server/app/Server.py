#python -m grpc_tools.protoc -I ./Server/Protos --python_out=./Server --grpc_python_out=./Server ./Server/Protos/Chat.proto ; python -m grpc_tools.protoc -I ./Server/Protos --python_out=./Client --grpc_python_out=./Client ./Server/Protos/Chat.proto

#imports de rpc y protos
import grpc
import Chat_pb2
import Chat_pb2_grpc

#imports Funcionales
import json
from datetime import datetime
from concurrent import futures


IP = "[::]"
PORT = "50051"
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


    
    def AddMessage(self, ClientId, SecondId, Message):
        TimeStamp = datetime.now().strftime("%d-%b-%Y/%H-%M-%S")
        #IdMensaje = IDEMISOR-IDRECEPTOR-TIMESTAMP
        IdMessage = str(ClientId)+"#"+str(SecondId)+"#"+str(TimeStamp)
        try:
            log = open(FILE,"a")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))
            return

        Data = "{0}#{1}\n".format(IdMessage,str(Message))

        if ClientId in self.Clients.keys():
            if SecondId in self.Clients.keys():
                    self.Clients[SecondId].append(Data)          
                    log.write(Data)
                    print("[EXITO] El mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId)+ " Se registro correctame")
                    return Chat_pb2.Confirmacion(Tipo = 1, IdPropietario=ClientId, IdMensaje = IdMessage, Error =  "" )

            else:
                print("El receptor {0} no se ecnuentra registrado".format(SecondId))
                return Chat_pb2.Confirmacion(Tipo = 0, IdPropietario=ClientId, IdMensaje = IdMessage, Error =  "El receptor {0} no se ecnuentra registrado".format(SecondId) )
        else:
            print("El emisor {0} no se encuentra registrado".format(ClientId))
        log.close()
        return Chat_pb2.Confirmacion(Tipo = 0, IdPropietario=ClientId, IdMensaje = IdMessage, Error =  "El emisor {0} no se encuentra registrado".format(ClientId))
    
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
            IdEmisor, IdReceptor, TimeStamp, Mensaje = m.split(sep="#", maxsplit= 3 )
            mensaje = Chat_pb2.MensajeCliente(IdPropietario = IdEmisor, IdDestinatario = IdReceptor, IdMensaje = "#".join([IdEmisor,IdReceptor, TimeStamp]), Mensaje = Mensaje, Error = "" )
            yield mensaje

        
            
class ChatServicer (Chat_pb2_grpc.ChatServicer):

    #Directorio de clientes

    def __init__(self):
        self.Directorio = ChatDB()
        self.ServerId = "S01"
        self.ClientNumber = 0

        print("iniciando servicios")
    
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
        while True:
            return self.Directorio.GetMessages(request.IdCliente)



def serve():
    
    ChatServer = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    Chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), ChatServer)
    ChatServer.add_insecure_port(IP+":"+PORT)
    ChatServer.start()
    ChatServer.wait_for_termination()

if __name__ == '__main__':

    serve()
