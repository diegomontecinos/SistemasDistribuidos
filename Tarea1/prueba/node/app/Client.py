import socket
import struct
import unicodedata
import threading
import time
from random import random
from datetime import datetime

TCP_HOST = '127.0.0.1' #localhost (TCP)
MCAST_GRP = '224.10.10.10' #(UDP)
MCAST_PORT = 5501
TCP_PORT = 5000
REG_FILE_PATH = './registro_cliente.txt'
TIMER = 50

def WritteData(data, file_path):
    fecha= str(datetime.now())
    try:
        file = open(file_path, 'a')
        file.write(str("{0}-{1}\n".format(fecha, data) ))
        file.close()
    except FileNotFoundError :
        file = open(file_path, 'w')
        file.write("FECHA-IP-PUERTO-NOMBRE-ESTADO\n")
        file.write(str("{0}-{1}\n".format(fecha, data) ))
        file.close()
    except IOError:
        print('Error al abrir {}'.format(file_path))
        return False

mensaje = "Este es un mensaje por defecto para que sea guardado por el headnode"
tcp_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_HOST,TCP_PORT))

try:
    print("###############################################")
    print("Cliente enviando mensaje")
    #Send data
    tcp_socket.sendall(str(mensaje).encode('utf-8'))

    in_message = ""

    #Esperar respuesta
    while (len(in_message) < 1):
        print("en el while")
        in_message = tcp_socket.recv(1024)
        print('Respuesta del Headnode: ', in_message)
        WritteData(str(in_message.decode('utf-8')), REG_FILE_PATH)
        print("###############################################")
except:
    pass
