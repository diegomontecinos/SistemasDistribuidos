import socket

HOST = '127.0.0.1' #localhost
PORT = 7550 #listen port

f = open('respuestas.txt', 'w')
f.close()

waiting = True

#crewar socket y establecer conexion
socket_tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.connect((HOST,PORT))
socket_tcp.sendall(str("Hola servidor").encode('utf-8'))

while waiting:
    msje = socket_tcp.recv(1024)
    decod = str(msje.decode('utf-8'))
    print(decod)
    waiting = False

#pide mensajes a ser enviados al server y guarda respuestas
while True:
    mensaje = input("ingrese mensaje a enviar: ")
    socket_tcp.sendall(str(mensaje).encode('utf-8'))
    waiting = True
    while waiting:
        msje = socket_tcp.recv(1024)
        decod = str(msje.decode('utf-8'))
        print(decod)
        f = open("respuestas.txt", "a")
        f.write(decod+"\n")
        f.close()
        waiting = False