#Envia consulta de estado en multicast
#Guarda el estado de cada nodo luego de verificarlo cada  segundos
#seleccionar un datanode aleatoreo  y le nvia un mensaje para q lo guarde

import socket
import struct
import unicodedata
from datetime import datetime


MCAST_GRP = '224.10.10.10'
MCAST_PORT = 5000
HB_FILE_PATH = './hearbeat_server.txt'

def WritteData(data, file_path):
    fecha= str(datetime.now())
    try:
        file = open(file_path, 'a')
        file.write(str("{0}-{1}\n".format(fecha, data) ))
    except FileNotFoundError :
        file = open(file_path, 'w')
        file.write("FECHA-IP-PUERTO-NOMBRE-ESTADO\n")
        file.write(str("{0}-{1}\n".format(fecha, data) ))
    except IOError:
        print('Error al abrir {}'.format(file_path))
        return False



def MultiCast(message):
    
    ByteMessage = str(message).encode('utf-8')
    #create datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Set socket timeout 
    sock.settimeout(0.5)
    # set the time-to-live (1 to not past the local network)
    ttl = struct.pack('b',1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        #Send data to the group
        print('Enviando {!r}'.format(message))
        sent = sock.sendto(ByteMessage, (MCAST_GRP,MCAST_PORT))

        while True:
            print('Esperando respuesta multicast')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print('Se acabo el tiempo y no hay respuestas')
                break
            else:
                format_data = "-".join((str(server[0]),str(server[1]), str(data.decode('utf-8')))) 
                print('recivido:{!r} desde {}'.format(data, server))
                print("formatdata: {}".format(format_data))
                WritteData(format_data, HB_FILE_PATH)
    finally:
        print('cerrando socket multicast')
    return(True)

MultiCast(b'Mensaje ql')






