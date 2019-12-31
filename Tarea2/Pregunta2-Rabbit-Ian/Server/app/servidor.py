#!/usr/bin/env python

import pika
import threading
import ast

# mensaje tipo 0: pedir ID
# mensaje tipo 1: pedir usuarios conectados
# mensaje tipo 2: enviar mensajes
# mensaje tipo 3: pedir mensajes recibidos
# mensaje tipo 4: pedir mensajes enviados

#crear diccionario {fantasma: ID real}

FILE = 'log.txt'

class ServerChat():
    
    #contructor, inicia variables de ids cliente, el diccionario de los clientes y el archivo log.txt,
    def __init__(self):
        self.cantidadConexiones = 0
        self.BandejaEntrada = dict()#entrada (recibo)
        self.serverID = 'S01'
        self.diccionarioColas = dict()
        self.BandejaSalida = dict()#salida (mando)

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

    #crear cola de mensajes de chat
    def CrearColaMSG(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='cola_MSG')

        self.channel.basic_consume(queue='cola_MSG', on_message_callback=self.RecibirMSG,auto_ack=True)
        self.channel.start_consuming()
        

    #recibe el mensaje y dependiendo de si es un saludo o un mensaje, llama a la funcion que corresponde
    def RecibirMSG(self, ch, method, prop, body):
        entra = ast.literal_eval(body.decode('utf-8'))
        MSG = ''

        if entra['tipo'] == str(0): #solicita ID 
            self.AddClient(entra['emisor'])

        elif entra['tipo'] == str(1): #pide self.BandejaEntrada.keys() -> OK
            usuarios = self.ObtenerClientes(entra['emisor'])
            MSG = self.ArmarDiccionarioMSG(entra['emisor'],entra['emisor'],entra['tiempo'],usuarios,entra['cola'],entra['tipo'])
            self.EnviarMensaje(MSG,entra['emisor'],entra['emisor'],'1')

        elif entra['tipo'] == str(2): #enviar mensaje
            if entra['receptor'] in self.BandejaEntrada.keys():
                self.GuardarMSG(entra)

        elif entra['tipo'] == str(3): #pedir mensajes recibidos... self.BandejaEntrada[]
            mensajes = self.ObtenerRecibidos(entra['emisor'],entra['tipo'])
            MSG = self.ArmarDiccionarioMSG(entra['emisor'],entra['emisor'],entra['tiempo'],mensajes,entra['cola'],entra['tipo'])
            self.EnviarMensaje(MSG,entra['emisor'],entra['emisor'],entra['tipo'])

        elif entra['tipo'] == str(4): #pedir mensajes enviados...
            mensajes = self.ObtenerRecibidos(entra['emisor'],entra['tipo'])
            MSG = self.ArmarDiccionarioMSG(entra['emisor'],entra['emisor'],entra['tiempo'],mensajes,entra['cola'],entra['tipo'])
            self.EnviarMensaje(MSG,entra['emisor'],entra['emisor'],entra['tipo'])

    #retorna los clientes
    def ObtenerClientes(self,cliente):
        listaUsuarios = ''
        for user in self.BandejaEntrada.keys():
            if user != cliente:
                listaUsuarios = listaUsuarios+user+' '
        return listaUsuarios

    #obtiene mensajes recibidos o enviados segun corresponde
    def ObtenerRecibidos(self, cliente, tipo):
        mensajesRecibidos = ''
        if tipo == str(3):
            for mensaje in self.BandejaEntrada[cliente]:
                mensajesRecibidos = mensajesRecibidos+mensaje.strip()+"\n"

        elif tipo == str(4):
            for mensaje in self.BandejaSalida[cliente]:
                mensajesRecibidos = mensajesRecibidos+mensaje.strip()+"\n"

        return mensajesRecibidos


    #cre un ID para el nuevo cliente y se lo manda a la "cola virtual"
    def AddClient(self, cola):
        #print('add client')
        self.cantidadConexiones+=1
        NewID = 'Cliente-'+str(self.cantidadConexiones)#crear ID

        diccionarioMSG=dict()
        diccionarioMSG['emisor'] ='server'
        diccionarioMSG['receptor'] = cola
        diccionarioMSG['tiempo'] = ''
        diccionarioMSG['mensaje'] = NewID
        diccionarioMSG['cola'] = cola
        diccionarioMSG['tipo'] = '0'

        self.diccionarioColas[NewID] = cola
        self.BandejaEntrada[NewID] = []#crear lista de mensajes que recibe
        self.BandejaSalida[NewID] = []#crea diccionario de mensajes que manda

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.basic_publish(exchange='',routing_key=str(cola),body=str(diccionarioMSG))
        connection.close()

    def EnviarMensaje(self, RAW, emisor, receptor,codigo):#'{e,r,t,M,c,t}'
        MSG = RAW
 
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.basic_publish(exchange='',routing_key=self.diccionarioColas[receptor],body=MSG)
        connection.close()

    def GuardarMSG(self, diccionario):
        emisor = diccionario['emisor']
        receptor = diccionario['receptor']
        tiempo = diccionario['tiempo']
        mensaje = diccionario['mensaje']
        cola = diccionario['cola']
        tipo = diccionario['tipo']

        MSGtoWrite = emisor+'_'+receptor+'_'+tiempo+'#'+mensaje
        try:
            log = open(FILE,"a")
            print('se ha registrado con exito el mesaje: '+mensaje+' entre los clientes '+emisor+' -- '+receptor)
        except IOError:
            print("[ERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(mensaje)+" entre los clientes :"+str(emisor)+" -- "+str(receptor))
            return

        self.BandejaEntrada[receptor].append(MSGtoWrite)
        log.write(MSGtoWrite+'\n')

        log.close()
        self.BandejaSalida[emisor].append(MSGtoWrite)

    def ArmarDiccionarioMSG(self,emisor,receptor,tiempo,mensaje,cola, tipo):
        diccionarioMSG=dict()
        diccionarioMSG['emisor'] =emisor
        diccionarioMSG['receptor'] = receptor
        diccionarioMSG['tiempo'] = tiempo
        diccionarioMSG['mensaje'] = mensaje
        diccionarioMSG['cola'] = cola
        diccionarioMSG['tipo'] = tipo
        return str(diccionarioMSG)

       
if __name__ == '__main__':
    print('Servidor')
    servidor = ServerChat()
    hiloServer = threading.Thread(target=servidor.CrearColaMSG,args=[])
    hiloServer.start()
