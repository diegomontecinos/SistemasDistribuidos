import socket
import time

HOST = '127.0.0.1' #localhost
PORT = 7000

with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST,PORT))
    client_socket.sendall(bytearray("Mensaje del cliente", 'utf-8'))
    in_message = client_socket.recv(1024)

    print('respuesta servidor: ', in_message)
