#!/usr/bin/env python

import pika
import threading
import ast

# mensajes -> '{emisor;Cliente-0,receptor;[Cliente-X],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme,tipo;N°}'
# mensaje tipo 0: pedir ID
# mensaje tipo 1: pedir usuarios conectados
# mensaje tipo 2: enviar mensajes
# mensaje tipo 3: pedir mensajes recibidos
# mensaje tipo 4: pedir mensajes enviados

#crear diccionario {fantasma: ID real}

FILE = 'log.txt'

class ServerChat():
    
    #contructor, inicia variables de ids cliente, el diccionario de los clientes y el archivo log.txt,
    #llama a la funcion de crear cola
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
        print('diccionario entrada',self.BandejaEntrada)
        print('diccionario salida',self.BandejaSalida)
        #self.CrearColaMSG()

    #crear cola de mensajes de chat
    def CrearColaMSG(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='cola_MSG')

        self.channel.basic_consume(queue='cola_MSG', on_message_callback=self.RecibirMSG,auto_ack=True)
        #print('voy al thread')
        #threading.Thread(target=self.Escuchar(),daemon = True).start()
        self.channel.start_consuming()
        

    #recibe el mensaje y dependiendo de si es un saludo o un mensaje, llama a la funcion que corresponde
    def RecibirMSG(self, ch, method, prop, body):
        print("RM [X] llega ",body.decode())
        entra = ast.literal_eval(body.decode('utf-8'))
        print(entra) 
        #emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW,tipoRAW = body.decode().strip("{}").split(",")
        #emisor = emisorRAW.split(":")[1]
        #receptor = receptorRAW.split(":")[1]
        #time = timeRAW.split(":")[1]
        #mensaje = mensajeRAW.split(":")[1]
        #cola = colaRAW.split(":")[1]
        #tipo = tipoRAW.split(":")[1]
        #print('emisor ',emisor)
        #print('receptor ',receptor)
        #print('time ',time)
        #print('mensaje ',mensaje)
        #print('cola ',cola)
        #print('tipo ', tipo)

        '''if 'Cliente' not in emisor:#no tiene ID
            self.AddClient(cola)
        elif receptor in self.BandejaEntrada.keys():#revisa si el receptor esta dentro de los clientes
            self.EnviarMensaje(body.decode())'''
        #'{emisor;Cliente-0,receptor;[Cliente-X],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme,tipo;N°}'
        MSG = ''

        if entra['tipo'] == str(0): #solicita ID -> OK
            print('mando: ',entra['cola'],' ',entra['emisor'])
            self.AddClient(entra['emisor'])

        elif entra['tipo'] == str(1): #pide self.BandejaEntrada.keys() -> OK
            usuarios = self.ObtenerClientes(entra['emisor'])
            #MSG = "{emisor:"+entra['emisor']+",receptor:"+entra['emisor']+",time:"+entra['tiempo']+",mensaje:"+usuarios+",tipo:1}"
            #print("llamo a enviar mensaje con: ", MSG)
            MSG = self.ArmarDiccionarioMSG(entra['emisor'],entra['emisor'],entra['tiempo'],usuarios,entra['cola'],entra['tipo'])
            self.EnviarMensaje(MSG,entra['emisor'],entra['emisor'],'1')
            #llamar a funcion enviar mensaje-> con cola receptora y tipo =1

        elif entra['tipo'] == str(2): #enviar mensaje ->  cambiar por solo guardar el mensaje en la cola y guardar en log.txt
            if entra['receptor'] in self.BandejaEntrada.keys():
                #self.EnviarMensaje(body.decode())
                self.GuardarMSG(entra)# entra es un diccionario
        elif entra['tipo'] == str(3): #pedir mensajes recibidos... self.BandejaEntrada[]
            print('piden mensajes entrantes')
            mensajes = self.ObtenerRecibidos(entra['emisor'])
            MSG = self.ArmarDiccionarioMSG(entra['emisor'],entra['emisor'],entra['tiempo'],mensajes,entra['cola'],entra['tipo'])
            self.EnviarMensaje(MSG,entra['emisor'],entra['emisor'],entra['tipo'])
            #llamar a función enviar mensaje con cola y tipo 3
        elif entra['tipo'] == str(4): #pedir mensajes enviados...
            a=0
            #crear una funcion que lea el log.txt y saque los mensajes de usuario

    #retorna los clientes
    def ObtenerClientes(self,cliente):
        listaUsuarios = ''
        for user in self.BandejaEntrada.keys():
            if user != cliente:
                listaUsuarios = listaUsuarios+user+' '
        return listaUsuarios

    def ObtenerRecibidos(self, cliente):
        print('recibidos consultados ',self.BandejaEntrada)
        mensajesRecibidos = ''
        for mensaje in self.BandejaEntrada[cliente]:
            print('mensaje: ', mensaje)
            mensajesRecibidos = mensajesRecibidos+mensaje+"\n"
        return mensajesRecibidos


    #cre un ID para el nuevo cliente y se lo manda a la "cola virtual"
    def AddClient(self, cola):
        #print('add client')
        self.cantidadConexiones+=1
        NewID = 'Cliente-'+str(self.cantidadConexiones)#crear ID

        #print('cola ',cola)
        #print('new id ', NewID)

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
        print ('diccionario mensajes ', self.BandejaEntrada)
        print('Usuario: ',NewID,' creado.')
        print ('diccionario colas', self.diccionarioColas)
        print('diccionario de salida: ', self.BandejaSalida)
        #mandar a cola virtual
        ##'{emisor;Cliente-0,receptor;[Cliente-X],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme,tipo;N1}'
        #MSG ="{emisor:Cliente-0,receptor:Cliente-X,time:dd-mmm-yyy,mensaje:"+NewID+",COLA:"+cola+",tipo:0}" 
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.basic_publish(exchange='',routing_key=str(cola),body=str(diccionarioMSG))
        connection.close()

    def EnviarMensaje(self, RAW, emisor, receptor,codigo):#'{e,r,t,M,c,t}'
        print("EN[X] llega ", RAW)#.decode())
        '''misorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW,tipoRAW = RAW.strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]
        tipo = tipoRAW.split(";")[1]'''

        #MSG = emisor+'_'+time+': '+mensaje
        '''destino = ''
        if codigo == str(1):
            MSG = RAW
            destino = receptor
        elif codigo == str(2):
            MSG = 'ver que onda'
        elif codigo == str(3):
            MSG = 'ver que onda'
        elif codigo == str(4):
            MSG = 'ver que onda'
            '''
        MSG = RAW
        
        #print('destino ',destino)

        print('Envio: ', MSG)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        #channel.basic_publish(exchange='',routing_key=str(destino),body=MSG)
        channel.basic_publish(exchange='',routing_key=self.diccionarioColas[receptor],body=MSG)

        connection.close()
        #self.GuardarMSG(RAW)

    def GuardarMSG(self, diccionario):
        '''emisorRAW,receptorRAW,timeRAW,mensajeRAW,colaRAW,tipoRAW = RAW.strip("{}").split(",")
        emisor = emisorRAW.split(";")[1]
        receptor = receptorRAW.split(";")[1]
        time = timeRAW.split(";")[1]
        mensaje = mensajeRAW.split(";")[1]
        cola = colaRAW.split(";")[1]
        tipo = tipoRAW.split(";")[1]

        MSGtoWrite = emisor+'_'+receptor+'_'+time+'#'+mensaje'''

        emisor = diccionario['emisor']
        receptor = diccionario['receptor']
        tiempo = diccionario['tiempo']
        mensaje = diccionario['mensaje']
        cola = diccionario['cola']
        tipo = diccionario['tipo']

        MSGtoWrite = emisor+'_'+receptor+'_'+tiempo+'#'+mensaje
        try:
            log = open(FILE,"a")
        except IOError:
            print("[ERROR] Algo salio mal, al intentar registrar el mensaje: "+ str(mensaje)+" entre los clientes :"+str(emisor)+" -- "+str(receptor))
            return

        self.BandejaEntrada[receptor].append(MSGtoWrite)
        log.write(MSGtoWrite+'\n')

        log.close()
        #self.BandejaEntrada[receptor].append(MSGtoWrite)
        self.BandejaSalida[emisor].append(MSGtoWrite)
        print('diccionario de entrada ',self.BandejaEntrada)
        print('diccionario de salida ', self.BandejaSalida)

    def Escuchar(self):
        self.channel.start_consuming()

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
