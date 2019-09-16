import socket
import time

HOST = '127.0.0.1' #localhost
PORT = 7000 #listen port

Waiting = True
Connect = False

with socket.socket( socket.AF_INET, socket.SOCK_STREAM) as host_socket:

    host_socket.bind((HOST,PORT))
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
        
            




