import pika
import json
import random
import string
from datetime import datetime
import threading
import time

IP = "localhost"

class Cliente():

    Esquema_Mensaje = {
        "Emisor":"",
        "Receptor":"",
        "TimeStamp":"",
        "IdMensaje":"",
        "Mensaje":"",
        "Tipo":"",
    }

    def __init__(self):
        
        #Variables de clase
        #rand =  str(''.join(random.choices(string.ascii_letters + string.digits, k=32)))
        rand =  str(''.join(random.choices(string.digits, k=4)))
        self.Id = rand
        self.NombreCola = rand
        self.IdServer = rand
        self.Mensajes = []

        #Crear y escuchar la cola del cliente
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(IP))
        self.channel = self.connection.channel()
    
        #Saludar al servidor
        #saludo = self.LLenado_Mensaje(Emisor= self.Id, Tipo= str(1))
        #self.Publicar("Entrada", saludo)
    
    def Crear_Cola(self, con, nombre):
        print("Creando Canal...")
        #connection = pika.BlockingConnection(pika.ConnectionParameters(IP))
        #channel = connection.channel()
        channel = con.channel()
        print("Creando Cola {0}...".format(nombre))
        channel.queue_declare(queue = nombre)
        print("Escuchando la cola {0}".format(nombre))
        channel.basic_consume(
            queue=nombre,
            auto_ack=True,
            on_message_callback=self.callback)
        print("Esperando por mensajes...")
        channel.start_consuming()
        print("terminando de consumir")
    
    def callback(self,ch, method, properties, body):
        objeto_mensaje = json.loads(body)
        #saludo
        if str(objeto_mensaje["Tipo"]) == str(1):
            print("Se recivio un nuevo Id {0}".format(objeto_mensaje["Mensaje"]))
            self.Id = objeto_mensaje["Mensaje"]
        #lista de clientes
        elif str(objeto_mensaje["Tipo"]) == str(2):
            print("Desplegand lista de clientes") 
            if not objeto_mensaje["Mensaje"]:
                print("Eres el unico cliente conectado ")
            else:
                print("---Listado Clientes-----\n")
                i = 1
                for cliente in objeto_mensaje["Mensaje"]:
                    print("{0}) {1}".format(i, cliente))
                    i=i+1
                print("-------------------------------")
        #Respuesta luego de enviar un mensaje
        elif str(objeto_mensaje["Tipo"]) == str(3):
            self.Mensajes.append(objeto_mensaje["Mensaje"])

        #mensajes recibidos
        elif str(objeto_mensaje["Tipo"]) == str(4):
            if not self.Mensajes:
                print("Aun no recibes mensajes")
            else:
                print("--------------------------------------------\nMensajes recibidos:\n----fecha y hora----|--Emisor--|----Mensaje----\n")
                for mensaje in self.Mensajes:
                    print(mensaje)
                print("--------------------------------------------\n")
        #mensajes enviados
        elif str(objeto_mensaje["Tipo"]) == str(5):
            if not objeto_mensaje["Mensaje"]:
                print("Aun no envias mensajes")
            else:
                print("--------------------------------------------\nMensajes enviados:\n----fecha y hora----|--Receptor--|----Mensaje----\n")
                for mensaje in objeto_mensaje["Mensaje"]:
                    print(mensaje)
                print("--------------------------------------------\n")
        elif str(objeto_mensaje["Tipo"]) == str(0):
            print(objeto_mensaje["Mensaje"])
        else:
            print("USTED NO DEBERIA ESTAR AQUI! ¬¬")

    def LLenado_Mensaje(self, Emisor = "", Receptor = "", IdMensaje = "", Mensaje ="", Tipo =""):

        mensaje = self.Esquema_Mensaje.copy()
        mensaje["Emisor"] = Emisor
        mensaje["Receptor"] = Receptor
        mensaje["TimeStamp"] = str(datetime.now().strftime("%d-%b-%Y|%H:%M:%S"))
        mensaje["IdMensaje"] = IdMensaje
        mensaje["Mensaje"] = Mensaje
        mensaje["Tipo"] = Tipo
        return json.dumps(mensaje)
    
        
    def Publicar(self,nombre_cola, mensaje):
        self.channel.basic_publish(exchange='',
                            routing_key=nombre_cola,
                            body= mensaje)
        print("[x] Sent {0}".format(mensaje))

    def Salir(self):
        self.connection.close()

if __name__ == "__main__":

    cliente = Cliente()
    #se crea la cola del cliente y queda escuchandp
    hilo_cola_cliente = threading.Thread(target= cliente.Crear_Cola, args= [cliente.connection, cliente.NombreCola])
    hilo_cola_cliente.start()
    #Cliente Envia mensaje de saludo a servidor
    cliente.Publicar("Entrada", cliente.LLenado_Mensaje(Emisor= cliente.Id, Tipo= str(1)))

    while cliente.Id == cliente.NombreCola:
        time.sleep(1)
    option = 0
    entrada = input("Presione una tecla para continuar")
    while option != 5:
        print("--------------------------------------------\nServidor {0} Usuario {1}\n\nSeleccione una opcion:\n1) Ver clientes conectados\n2) Enviar un mensaje\n3) Ver mensajes recibidos.\n4) Ver mensajes enviados\n5) Salir.\n--------------------------------------------\n".format(cliente.IdServer, cliente.Id))
        option = str(input("Opcion: "))
        
        #ver clientes conectados
        if option == str(1):
            cliente.Publicar("Entrada", cliente.LLenado_Mensaje(Emisor= cliente.Id, Tipo= str(2)))
        
        #Enviar mensaje
        elif option == str(2):
            Dest = input("ingrese el Id del destinatario: ")
            Message = input("Ingrese un mensaje: ")
            cliente.Publicar("Entrada", cliente.LLenado_Mensaje(Emisor= cliente.Id, Receptor=str(Dest), Mensaje= Message, Tipo= str(3)))
        
        #Mensajes recibidos
        elif option == str(3):
            if not cliente.Mensajes:
                print("Aun no recibes mensajes")
            else:
                print("--------------------------------------------\nMensajes enviados:\n----fecha y hora----|--Receptor--|----Mensaje----\n")
                for mensaje in cliente.Mensajes:
                    print(mensaje)
                print("--------------------------------------------\n")

           #cliente.Publicar("Entrada", cliente.LLenado_Mensaje(Emisor= cliente.Id, Tipo= str(4)))
        
        #Mensajes Enviados
        elif option == str(4):
            cliente.Publicar("Entrada", cliente.LLenado_Mensaje(Emisor= cliente.Id, Tipo= str(5)))
        
        #salir
        elif option == str(5):
            break
        else:
            print("Ha seleccionado una opcion no valida, intentelo nuevamente")

    input("aprete algo")
