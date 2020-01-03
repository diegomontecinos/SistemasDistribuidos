# Readme Tarea 2 "Servicio de mensajeria"

### Ambiente de desarrollo:
    Esta tarea se desarrolló y testeó en windows 10 Education, con la version 2.1.0.5 de docker desktop community, 
    se recomienda utilizar la misma configuración para el correcto funcionamiento, sin embargo el desarrollo fue
    realizado con el objetivo de poder levantar la arquitectura en cualquier sistema compatible, aunque no se 
    garantiza que este funcione correctamente.

### Informe de tarea
    El archivo Informe_tarea_2_Montecinos_Mora.pdf contiene las comparaciones técnicas entre ambas implementaciones 
    y la recomendación final.
### Instrucciones de uso

- Iniciar el servicio de docker.
- Segundo paso, crear las imagenes de containers
```console
docker-compose buildd
```
- Tercer paso, levantar la arquitectura utilizando los containers previamente creados. se puede cambiar
el número de clientes a levantar mediante el comando scale, se recomienda utilizar 4 pero puede utilizarse cualquier numero mayor a 1. Este comando puede utilizarse para agregar más clientes en caliente, esto quiere decir que aunque ya se hayan iniciado 4 clientes se puede re ingresar el comando con un nuemero mayor y se agregaran nuevos clientes sin detener a los que ya se encuentran ejecutandose.
```console
docker-compose up --scale cliente=4
```
- Cuarto paso, una vez los contenedores estan levantados y en ejecucion se debe abrir una consola para cada cliente donde se ingresaran los comandos y se mostraran los mensajes. Una vez ejecutados los contenedores quedan esperando que se precione enter para desplegar el menu. Por lo que una vez realizado el tercer paso se debe ejecutar el comando

```console
docker attach "Nombre del contenedor"
```
Con esto se genera la coneccion al cliente y queda en estado de espera de ordenes, se apreta enter y se desplegara el menu donde se indica que opciones disponibles existen.

Seleccione una opcion:  
    1) Ver clientes conectados.  
    2) Enviar un mensaje.  
    3) Ver mensajes recibidos.  
    4) Ver mensajes enviados.  
    5) Salir.  
- Para ver los nombres de los contenedores activos utilizar

```console
docker ps
```

- Para detener todos los contenedores que se encuentran activos, se puede utlizar el siguiente comando.
```console
docker stop $(docker ps -a -q)
```

## Pregunta-1-gRPC
### Estructura de archivos.
    -Pregunta-1-gRPC
        |-Generic_Client
        |    |-app
        |       |-Cliente.py    --->> Código python del cliente
        |    |-Chat.proto       --->> Definición de servicios Protocol Buffer
        |    |-Dockerfile       --->> Dockerfile container del cliente
        |    |-requirements.txt --->> Librerias requeridas por el cliente
        |-Protos
        |    |-Chat.proto
        |-Server
        |    |-app
        |    |    -Server.py    --->> Código python del cliente
        |    |-Chat.proto       --->> Definición de servicios Protocol Bufffer
        |    |-Dockerfile       --->> Dockerfile container del servidor
        |    |-requirements.txt --->> Librerias requeridos por el servidor
        |-Docker_command.txt
        |-docker-compose.yml    --->> docker-compose para levantar la arquitectura distribuida
        |-Proto_compiler.bat    --->> Script para compilar Chat.proto en windows al momento de testear
        |-Run_1S_2C-bat         --->> Script para levantar 1 cliente y 2 servidores en Windows Powershell

## Pregunta-2-RabbitMQ
### Estructura de archivos.
    -Pregunta-2-RabbitMQ-
        |Client
        |    |-app
        |       |-cliente.py    --->> Código python del cliente
        |    |-Dockerfile       --->> Dockerfile container del cliente
        |    |-requirements.txt --->> Librerias requeridas por el cliente
        |-Server
        |    |-app
        |       |-server.py     --->> Código python del cliente
        |    |-Dockerfile       --->> Dockerfile container del servidor
        |    |-requirements.txt --->> Librerias requeridos por el servidor
        |-docker-compose.yml    --->> docker-compose para levantar la arquitectura distribuida
        |-1S_3C-bat             --->> Script para levantar 1 servidor y 3 clientes en Windows Powershell
