import socket

HOST = '127.0.0.1' #localhost
PORT = 7550 #listen port

f = open('log.txt', 'w')
f.close()

waiting = True

#crea socket y espera conexion
socket_tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.bind((HOST,PORT))
socket_tcp.listen()
print("Esperando conexion...\n")

#recive mensajes del cliente, los guarda y envia respuesta
while True:
    conn , addr = socket_tcp.accept()
    print('conexion establecida con: ', addr)
    while True:
        waiting = True
        while waiting:
            msje = conn.recv(1024)
            decod = str(msje.decode('utf-8'))
            print(decod)
            f = open('log.txt', 'w')
            f.write(decod)
            f.close()
            conn.sendall(str("acuso recivo de: "+decod).encode('utf-8'))
            wainting = False
