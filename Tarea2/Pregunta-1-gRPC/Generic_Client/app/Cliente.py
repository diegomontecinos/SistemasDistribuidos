
#imports de rpc y protos
import grpc
import Chat_pb2
import Chat_pb2_grpc

#Imports Funcionales
import threading
import time

#Windows Ip
IP = "localhost"
#Dockers IPs
#IP = "0.0.0.0"
#IP = "server"

#Windows Port
PORT = "50051"
#Docker Prot
#PORT = "8080"
FILE = "log.txt"

class Client:

    def __init__(self):
        #Variables de clase 
        self.Id = "null"
        self.IdServer = "null"
        self.Mensajes = []
        #Crear grpc Channel y stub
      
        channel = grpc.insecure_channel(IP+":"+PORT)
        #que hace esta wea#grpc.channel_ready_future(channel).result()
        self.stub = Chat_pb2_grpc.ChatStub(channel)

        response = self.stub.Saludo(Chat_pb2.Saludos(Tipo = 0, IdCliente = "", IdServidor = "", Error = "" ))

        if response.Tipo == 1:
            if len(response.IdCliente) > 0 :
                self.Id = response.IdCliente
                self.IdServer = response.IdServidor
                print("Has ingresado al servidor {0} con el Id {1}".format(self.IdServer, self.Id))
            elif len(response.Error) > 0 :
                print(response.Error)
            else:
                print("Algo salio mal al iniciar comunicacion con el servidor")
        threading.Thread(target= self.EsperaMensajes(), daemon= True).start()


    def EnvioSolicitud(self):
        Dest = input("ingrese el Id del destinatario: ")
        Message = input("Ingrese un mensaje: ")
        if Message != "":
            self.stub.EnvioSolicitud(Chat_pb2.MensajeCliente(IdPropietario = self.Id, IdDestinatario = Dest, IdMensaje = "" , TimeStamp = "",Mensaje= Message, Error ="" ))
        else:
            print("Ingrese un mensaje valido")
        
    def EsperaMensajes(self):
        #print("Servicio de espera de mensajes iniciado")
        for element in self.stub.DespachoMensajes(Chat_pb2.Consulta(IdCliente = self.Id)):
            #print("Mensaje recibido :\n"+element.Mensaje)
            Mensaje = " ".join([element.TimeStamp, element.IdPropietario, element.Mensaje])
            self.Mensajes.append(Mensaje)
    
    def GetId(self):
        return str(self.Id)
    def GetIdServer(self):
        return str(self.IdServer)

    def Menu(self):
        option = 0
        while option != 3:
            print("--------------------------------------------\nServidor {0} Usuario {1}\n\nSeleccione una opcion:\n1) Enviar un mensaje\n2) Ver mensajes recibidos.\n3) Salir.\n--------------------------------------------\n".format(Cliente.GetIdServer(), Cliente.GetId()))
            option = str(input("Opcion: "))
            if option == str(1):
                self.EnvioSolicitud()
            elif option == str(2):
                self.EsperaMensajes()
                if not self.Mensajes:
                    print("Aun no hay mensajes")
                else:
                    print("--------------------------------------------\nMensajes recibidos:\n----fecha y hora----|--Emisor--|----Mensaje----\n")
                    for mensaje in self.Mensajes:
                        print(mensaje)
                    "--------------------------------------------\n"
            elif option == str(3):
                break
            else:
                print("Ha seleccionado una opcion no valida, intentelo nuevamente")



if __name__ == '__main__':
    Cliente = Client()
    input("Presione una tecla para continuar")
    Cliente.Menu()

    

