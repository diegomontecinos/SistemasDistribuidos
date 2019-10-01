
import socket
import struct


MCAST_GRP = '224.10.10.10'
MCAST_PORT = 5000
NODE_NAME = ''

NODE_NAME = input("ingrese un nombre para este nodo: ")

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
    print('\nEsperando mensajes...')
    data, address = sock.recvfrom(1024)

    print('recibidos {} bytes desde {}'.format(
        len(data), address))
    print(data)

    print('Enviando acknowledgement a', address)
    sock.sendto(NODE_ACK, address)

