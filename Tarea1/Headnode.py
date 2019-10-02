#Envia consulta de estado en multicast
#Guarda el estado de cada nodo luego de verificarlo cada  segundos
#seleccionar un datanode aleatoreo  y le nvia un mensaje para q lo guarde

import socket
import struct
import unicodedata
import threading
import time
from datetime import datetime

HOST = '127.0.0.1' #localhost (TCP)
MCAST_GRP = '224.10.10.10' #(UDP)
MCAST_PORT = 5001
TCP_PORT = 5000
HB_FILE_PATH = './hearbeat_server.txt'
TIMER = 50


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


def MultiCast(message, timer = None ):

    ByteMessage = str(message).encode('utf-8')
    #create datagram socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Set socket timeout 
    udp_sock.settimeout(0.5)
    # set the time-to-live (1 to not past the local network)
    ttl = struct.pack('b',1)
    udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        #Send data to the group
        print('Enviando {!r}'.format(message))
        sent = udp_sock.sendto(ByteMessage, (MCAST_GRP,MCAST_PORT))

        while True:
            print('Esperando respuesta multicast')
            try:
                data, server = udp_sock.recvfrom(16)
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

    if (estado):
        threading.Timer(TIMER, MultiCast(b'Eviar estado'))

    return(True)


def main():
    Waiting = True
    Connect = False

    multicast_timer = threading.Timer(TIMER, MultiCast(b'Eviar estado', multicast_timer))
    
    MultiCast(b'Eviar estado')

    with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as host_socket:

        host_socket.bind((HOST,TCP_PORT))
        host_socket.listen(1)

        print("Esperando conexion...\n")
        
        while (Waiting):
            conn , addr = host_socket.accept()
            print("Conexión establecida con", addr)
            Connect = True
            while(Connect):
                Waiting = False
                in_message = conn.recv(1024)
                time.sleep(0.5)
                if not in_message:
                    Connect = False
                    break   
                else:
                    #conn.sendall(bytearray(in_message, 'utf-8'))
                    print(in_message)
    done.set()

if __name__ == "__main__":
    main()




