#!/usr/bin/env python
import pika
import uuid
#import logging
from datetime import datetime
import threading

# cliente
# enviar y recibir mensajes

# mensajes  
# texto + timestamp
# cliente-X#Cliente-Y#timestamp#texto

class PublisherC():

    #------------------------------------------------------------------------------------------
    #constructor... se enlaza a la cola de saludos y crea la cola a la que el servidor responde
    #------------------------------------------------------------------------------------------
    def __init__(self):
         # conexion al servidor rabbitmq
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
                        # "crear" cola para mandar mensajes ''
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue  # cola de respuesta
        # crea la cola en la que "consume" o lee la respuesta en la cola callback y cuando hay algo, invoca a la funcion on_response
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response, 
            auto_ack=True)

    #---------------------------------------------
    #guarda si ID con la que debería crear su cola 
    #---------------------------------------------
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()
            self.ID = self.response
            #no se si llamar acá al construcrtor del consumer para crear la cola o dejarlo en el 'main'

    #-------------------------------------------------------------------
    # manda una solicitud RPC y bloquea hasta que recibe una respuesta
    #-------------------------------------------------------------------
    def ID(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='cola_IDS',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response) 

    #-------------------------------------------------------------------------------------------
    #establece conexion con la cola de MSG del servidor, manda el mensaje y cierrra la conexion
    #-------------------------------------------------------------------------------------------
    def enviarMensaje(self,destino,mensaje):
        TimeStamp = datetime.now().strftime("%d-%b-%Y|%H:%M:%S")
        MSG = str(self.ID)+'#'+'cliente-'+str(destino)+'#'+str(TimeStamp)+'#'+mensaje
        self.connectionSalida = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channelSalida = self.connectionSalida.channel()
        self.channelSalida.queue_declare(queue='cola_MSG')
        channel.basic_publish(exchange='',routing_key='cola_MSG',body=str(MSG))
        #print(" [x] Sent ",MSG)
        connection.close ()


class ConsumerC():
    
    #------------
    #constructor
    #------------
    def __init__(self,ID):
        self.ID = str(ID)
        self.ListMSG = []

    #
    #crea la cola correspondiente a cliente-ID
    #
    def PedriMEnsajes(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.ID)
        
        self.channel.basic_consume(queue=str(self.ID),on_message_callback=self.GuardarMSG,auto_ack=True)
        threading.Thread(target=self.Escuchar(),daemon=True).start()

    #-------------------------------
    #guarda los mensajes que llegan
    #-------------------------------
    def GuardarMSG(self, ch, method, props, body):
        mensaje = body.decode().split('#')#['cliente-x','cliente-y','tiempo', 'menaje']
        self.ListMSG.append(str(mensaje[-1]))

    #-----------------------
    # saca cosas de la cola
    #-----------------------
    def Escuchar(self):
        #while True:
        print(" [x] Awaiting mensajes")
        self.channel.start_consuming()




        

if __name__ == '__main__':
    cliente = PublisherC()
    print(" [x] Requesting ID")
    id = cliente.ID(0)
    print(" [.] Got " , id)

'''
#LOGGER = logging.getLogger(__name__)
class Consumer():
    def __init__(self, ):
        self.conexiones = 0
        self.consuming = False
        self.message = ''
        
    def connectar(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

    def callback(self, ch, method, props, body):
        self.message = body.decode()


class Publisher():
    def __init__(self):
        super().__init__()

class Client():
    def __init__(self):
        self.consumidor = Consumer()
        self.publicador = Publisher()

if __name__ == '__main__':
    cliente = Client()
    '''