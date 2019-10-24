#python -m grpc_tools.protoc -I ./Server/Protos --python_out=./Server --grpc_python_out=./Server ./Server/Protos/Chat.proto

#imports de rpc y protos
import grpc
import Chat_pb2
import Chat_pb2_grpc


IP = "[::]"
PORT = "50051"


class ChatDB ():
    
    def __init__(self):

        self.Directorio = dict()

    def AddClient(ClientId):
        Enviados = dict()
        Recibidos = dict()
        try:
            InfClient = self.Directorio[ClientId]
            if (len(InfClient.lengt) > 0):
                print("El Cliente Ya existe")
            else:
                self.Directorio[ClientId] = [Enviados, Recibidos]
                print("Cliente Agregado Exitosamente")
        except KeyError:
            print("Error al agregar Cliente")
    
    def AddMensaje(MessageType, ClientId, SecondId, Message):

        #Mensajes Enviados
        if (MessageType == 0):
            try:
                self.Directorio[ClientId][0][SecondId] = Message
                print("[EXITO] El mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId)+ " Se registro correctame")
            except KeyError:
                print("[KEYERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))

        #Mensaje Recibido
        elif(MessageType == 1):
            
            try:
                self.Directorio[ClientId][1][SecondId] = Message
                print("[EXITO] El mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId)+ " Se registro correctame")
            except KeyError:
                print("[KEYERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))
        
        #Otro caso o error
        else:
            print("[ERROR DE TIPO] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))
            
        

        
        

class ChatServicer (Chat_pb2_grpc.ChatServicer):

    #Directorio de clientes

    def __init__(self):
        self.Directorio = ChatDB()
        self.ServerId = S01
        self.ClientNumber = 0

        print("iniciando servicios")
    
    def Saludo(self, request, context):
        if (request.Tipo == 0):
            self.Directorio.AddClient(request.IdCliente)
        elif (request.Tipo == 1):
            print("DEBO HACER ALGO AQUI")
        
    def EnvioMensaje(self, request, context):
        pass


def serve():
    
    ChatServer = grpc.server(futures.thread_poolExecutor(max_workers = 10))
    Chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer, ChatServer)
    ChatServer.add_insecure_port(IP+":"+PORT)
    ChatServer.start()

if __name__ == '__main__':

    #serve()
    datos = ChatDB()
    datos.AddClient("C01")
