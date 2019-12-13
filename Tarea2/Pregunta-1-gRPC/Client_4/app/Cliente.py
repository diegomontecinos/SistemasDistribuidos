
#imports de rpc y protos
import grpc
import Chat_pb2
import Chat_pb2_grpc

#Imports Funcionales
import threading


IP = "localhost"
PORT = "50051"
FILE = "log.txt"

class Client:

    def __init__(self):
        #Variables de clase 
        self.Id = "null"
        self.IdServer = "null"
        #Crear grpc Channel y stub
        channel = grpc.insecure_channel(IP+":"+PORT)
        self.stub = Chat_pb2_grpc.ChatStub(channel)

        response = self.stub.Saludo(Chat_pb2.Saludos(Tipo = 0, IdCliente = "", IdServidor = "", Error = "" ))

        if response.Tipo == 1:
            if len(response.IdCliente) > 0 :
                self.Id = response.IdCliente
                self.IdServer = response.IdServidor
            elif len(response.Error) > 0 :
                print(response.Error)
            else:
                print("Algo salio mal al iniciar comunicacion con el servidor")

        threading.Thread(target= self.EsperaMensajes(), daemon= True).start()

    def EnvioSolicitud(self):
        Dest = input("ingrese el Id del destinatario")
        Message = input("Ingrese un mensaje: ")
        if Message != "":
            self.stub.EnvioSolicitud(Chat_pb2.MensajeCliente(IdPropietario = self.Id, IdDestinatario = Dest, IdMensaje = "" ,Mensaje= Message, Error ="" ))
        else:
            print("Ingrese un mensaje valido")
        
    def EsperaMensajes(self):
        for element in self.stub.DespachoMensajes(Chat_pb2.Consulta(IdCliente = self.Id)):
            print("Mensaje recibido :\n"+element.Mensaje)


if __name__ == '__main__':
    Client = Client()
    Client.EnvioSolicitud()
