'''a= 'cliente-1#cliente-2#2-21-2334#wena compare'
#print (a.split('#')[0].split('-')[-1])
cont = 0
def mas1(n):
    #c0ont+=1
    n+=1
    return n#cont
mas1()
print(cont) 

x= txt = "{emisor;Cliente-0,receptor;[Cliente-X o Server],time;dd-mmm-yyy|hh:mm:ss,mensaje;MSG,COLA;colaNAme}"

#x = txt.strip("{}").split(",")
emisor,receptor,time,mensaje,cola = x.strip("{}").split(",")

print(emisor)
print(receptor)
print(time)
print(mensaje)
print(cola)'''

x = 'cliente'
y = 'hola'
z = 'Cliente-2'

if x  in z:
    print('se puede')
else:
    print('GG')