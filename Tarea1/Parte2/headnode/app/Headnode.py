#Envia consulta de estado en multicast
#Guarda el estado de cada nodo luego de verificarlo cada  segundos
#seleccionar un datanode aleatoreo  y le nvia un mensaje para q lo guarde

import socket
import struct
import unicodedata
import threading
import time
from random import random
from datetime import datetime

HOST = '0.0.0.0' #localhost (TCP)
MCAST_GRP = '224.10.10.10' #(UDP)
MCAST_PORT = 5501
TCP_PORT = 6000
HB_FILE_PATH = './hearbeat_server.txt'
REG_FILE_PATH = './registro_server.txt'
TIMER = 50

NODOS = list()



class Nodo:
    nombre = ''
    estado = -1
    direccion = ''
    puerto = -1



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

def SetNodes(data):
    #data -> IP-PUERTO-NOMBRE-ESTADO
    existe = False
    ip, puerto, nombre, estado = data.split("-")

    nodo_temp = Nodo()
    nodo_temp.nombre = nombre
    nodo_temp.estado = estado
    nodo_temp.direccion =  ip
    nodo_temp.puerto = puerto

    for n in NODOS:
        if (n.nombre == nombre and n.direccion == ip):
            print("Error al agregar el nodo, este ya existe")
            existe = True
    
    if  not existe:
        NODOS.append(nodo_temp)
    
def MultiCast(message):

    #create datagram socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Set socket timeout 
    udp_sock.settimeout(0.5)
    # set the time-to-live (1 to not past the local network)
    ttl = struct.pack('b',1)
    udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    ByteMessage = str(message).encode('utf-8')
    try:
        #Send data to the group
        print("-----------------------------------------------------------")
        print('Enviando {}'.format(message))
        udp_sock.sendto(ByteMessage, (MCAST_GRP,MCAST_PORT))
        while True:
            print('Esperando respuesta multicast')
            try:
                data, server = udp_sock.recvfrom(16)
            except socket.timeout:
                print('Se acabo el tiempo y no hay respuestas')
                break
            else:
                #Caso donde envie datos para guardar en un datanode
                if (str(data.decode('utf-8')) == "saved"):
                    nombre= str(message).split("#-#-#")[0]
                    registro = "-".join((str(server[0]),str(server[1]), nombre))
                    WritteData(registro, REG_FILE_PATH)
                    #Datos guardados correctamente en el datanode
                    print("Datos guardados correctamente en el datanode [{}]".format(nombre))
                    
                #caso donde quiero saber el estado de los datanodes
                elif ( len(str(data.decode('utf-8'))) >= 6 ):
                    NODOS.clear()
                    format_data = "-".join((str(server[0]),str(server[1]), str(data.decode('utf-8'))))
                    SetNodes(format_data)
                    print('recivido:{!r} desde {}'.format(data, server))
                    print("formatdata: {}".format(format_data))
                    WritteData(format_data, HB_FILE_PATH)
                else:
                    pass
    finally:
        print('cerrando socket multicast')
        print("-----------------------------------------------------------")

    return(True)

class Repeat(threading.Thread):

    def __init__(self, seconds):
        super().__init__()
        self.delay = seconds
        self.is_done = False
    
    def done(self):
        self.is_done = True
    
    def run(self):
        while not self.is_done:
            MultiCast("state")
            time.sleep(self.delay)
            

def StoreData(data):
    
    nodos_online = len(NODOS)

    if (nodos_online < 1):
        print("No hay nodos online")
        print(NODOS)
        time.sleep(0.5)
        return()
    else:
        r = round(random() * (nodos_online - 1))
        nodo = NODOS[r]
        str_data = str(data.decode('utf-8'))
        mensaje = "#-#-#".join((nodo.nombre, str_data))
        print("Enviando datos mediante multicast")
        MultiCast(mensaje)  
    return(nodo.nombre)

def main():

    timer = Repeat(5)
    timer.start()
    

    #Create tcp socket
    tcp_socket =  socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    #ind socket to the port
    tcp_socket.bind((HOST,TCP_PORT))
    print("Levantadon socket en {} puerto {}".format(HOST, TCP_PORT))
    #Seteando capacidad para un cliente
    tcp_socket.listen()
    
    print("Esperando conexion...\n")
    
    while True:
        #Esperando conexiones
        conn, addr = tcp_socket.accept()
        print("Conexion establecida con ", addr)
        try:
            print("*********************************************")
            while True:
                in_message = conn.recv(1024)
                #se recivieron datos
                if(in_message):
                    nombre = StoreData(in_message)
                    print("Guardando datos....")
                    print("*********************************************")
                    conn.sendall(str(nombre).encode('utf-8'))
                else:
                    print("No se recivieron datos desde {} - {}".format(HOST , PORT))
                    break
        except:
            pass
    
    timer.done()
    return 0

        

if __name__ == "__main__":
    main()




