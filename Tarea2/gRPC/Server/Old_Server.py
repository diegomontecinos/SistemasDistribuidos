#python -m grpc_tools.protoc -I ./Server/Protos --python_out=./Server --grpc_python_out=./Server ./Server/Protos/Chat.proto

#imports de rpc y protos
import grpc
import Chat_pb2
import Chat_pb2_grpc

#imports Funcionales
import json
from datetime import datetime


IP = "[::]"
PORT = "50051"
JSONNAME = "BDMensajes.json"


class ChatDB ():
    
    def __init__(self):
        JsonBd = {
            "Servidor": "Serv1",
            "Clientes": []
        }
        json.dump(JsonBd, JSONNAME)



    def AddClient(self, ClientId):
        JsonBd = json.loads(JSONNAME)
        JsonClient= {
            "IdCliente": ClientId,
            "Enviados":[],
            "Recibidos": []
        }

        try:
            for client in JsonBd["Clientes"]:
                if (client["IdCliente"] == ClientId):
                    print("El cliente"+str(ClientId)+" ya existe")
                else:
                    JsonBd["Clientes"].append(JsonClient)
                    json.dump(JsonBd, JSONNAME)
                    print("Cliete"+str(ClientId)+" agregado con exito")
        except KeyError:
            print("Error al agregar Cliente")
    
    def AddMensaje(self, ClientId, SecondId, Message):
        JsonBd = json.loads(JSONNAME)
        TimeStamp = datetime.now().strftime("%d-%b-%Y--%H-%M-%S")
        #IDEMISOR _ IDRECEPTOR _ TIMESTAMP
        IdMensaje = str(ClientId)+" / "+str(SecondId)+str(TimeStamp)

        JsonMensajeEnviado = {
            "IdMensaje": IdMensaje,
            "IdReceptor": str(SecondId),
            "Mensaje": str(Message)
        }

        JsonMensajeRecibido = {
            "IdMensaje": IdMensaje,
            "IdEmisor": str(ClientId),
            "Mensaje": str(Message)
        
        }
        for cliente in JsonBd["Clientes"]:
            #El destinatario existe
            if cliente["IdCliente"] == SecondId:
                


        try:
            self.Directorio[ClientId][0][SecondId] = Message
            print("[EXITO] El mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId)+ " Se registro correctame")
        except KeyError:
            print("[KEYERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(Message)+" entre los clientes :"+str(ClientId)+" -- "+str(SecondId))

            
        

        
        

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
