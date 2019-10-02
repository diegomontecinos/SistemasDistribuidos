import socket
import struct
import unicodedata
import threading
import time
from random import random
from datetime import datetime


MCAST_GRP = '224.10.10.10'
MCAST_PORT = 5501
NODE_NAME = ''
DATA_FILE_PATH = './data.txt'
#NODE_NAME = input("ingrese un nombre para este nodo: ")
NODE_NAME = "NODO1"

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

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(('', MCAST_PORT))

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(MCAST_GRP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

try:
    IP = sock.getsockname()[0][0]
except:
    IP = "Error to get ip"

NODE_ACK =  str("-".join( (str(NODE_NAME), str(1) ) )).encode('utf-8')

# Receive/respond loop
while True:
    print("**********************************************************")
    print('\nEsperando mensajes...')
    data, address = sock.recvfrom(1024)

    print('recibidos {} bytes desde {}-{} con mensaje {}'.format(len(data), address[0], address[1], data))
    

    if(str(data.decode('utf-8')) == "state"):
        print('Enviando Estado a', address)
        sock.sendto(NODE_ACK, address)
    
    else:
        nombre, mensaje = str(data.decode()).split("#-#-#")
        if (nombre == str(NODE_NAME)):
            print("soy {} y guardare tus datos: {}".format(NODE_NAME, mensaje))
            WritteData(mensaje, DATA_FILE_PATH)
            sock.sendto(str("saved").encode('utf-8'), address)
    print("**********************************************************")

