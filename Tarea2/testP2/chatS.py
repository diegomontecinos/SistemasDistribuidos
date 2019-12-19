#!/usr/bin/env python
import pika
import threading
from datetime import datetime

# Servidor
# envíar y recivir mensajes
# excribir en log.txt los mensajes enviados
# ver clientes
# ver todos los mensajes enviados de un cliente

# mensajes  
# ID unico
# texto + timestamp
# cliente-X#Cliente-Y#timestamp#texto

class ConsumerS(): 
    #-------------------------------------------------------------------------------------
    #constructor... declara la cola de IDS y llama a las funciones para sacar datos de ahí
    #-------------------------------------------------------------------------------------
    def __init__(self):
        self.conexiones = 0 #ID clientes
        self.cant_mensajes = 0 #ID Mensajes
        self.dir_mensajes = dict() #diccionario de 

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
            )
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='cola_IDS')
        self.channel.basic_qos(prefetch_count=10)#cambiar para mas conexiones
        self.channel.basic_consume(queue='cola_IDS', on_message_callback=self.handShake, auto_ack=True) #se ejecuta al recibir una request y manda una respuesta
        threading.Thread(target=self.escuchar(),daemon = True).start()#no bloque el codigo
        

    #-----------------------------------------
    # mandar respuesta de ID del nevo cliente
    #-----------------------------------------
    def handShake(self,ch, method, props, body):#on_request
        self.conexiones+=1
        response = "Cliente-"+str(self.conexiones)#new ID

        if response not in self.dir_mensajes.keys():
            self.dir_mensajes[response] = []#crea la lista de mensajes del nnuevo cliente
        else:
            self.erorr = 'ID ya existe'

        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                            props.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        #threading.Thread(target=self.escuchar(),daemon = True).start()#no bloque el codigo

    #-----------------------------------
    #saca cosas de la cola de saludo
    #-------------------------------------
    def escuchar(self):
        #while True:
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

    #------------------------------------------------------------------
    #crea la cola de los mensajes a la que el cliente envia el mensaje
    #------------------------------------------------------------------
    def RecibirMensajes(self): 
        self.connectionMSG = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        ) 
        self.channelMSG = self.connectionMSG.channel()
        self.channelMSG.queue_declare(queue='cola_MSG')

        self.channelMSG.basic_consume(queue='cola_MSG',on_message_callback=self.GuardarMSG, auto_ack=True)
        threading.Thread(target=self.leerColaChat(),daemon=True).start()

    #-----------------------------------------------------------------------------------
    #lee mensajes de la cola y revisa si el receptor ha sido creado
    #-----------------------------------------------------------------------------------
    def GuardarMSG(self, ch, method, props, body): 
        mensaje = body.decode().strip('#') #['cliente-x','cliente-y','tiempo', 'menaje']
        cliente2 = mensaje[1]#.split('-')[1] 
        if cliente2 in self.dir_mensajes.keys():
            self.dir_mensajes[cliente2].append(mensaje[-1])
            #falta agregar el id del mensaje
            #self.cant_mensajes +=1
            #falta escribir en log.txt
            #mandar el mensaje a la cola que corresponde
        else:
            self.erorr = 'Cliente receptor no existe'
    
    #-----------------------------
    #saca cosas de la cola de MSG
    #-----------------------------
    def leerColaChat(self):
        #while True:
        print(" [x] Awaiting Chan MSGs")
        self.channelMSG.start_consuming()

    


class Publishers():
    def __init__(self):
        super().__init__()
    

if __name__ == '__main__':
    server = ConsumerSS()
    #print('Pasamos la declaracion de la clase')
    #server.handShake()
    