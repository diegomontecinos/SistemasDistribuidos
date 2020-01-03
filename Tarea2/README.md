# Readme Tarea 2 "Servicio de mensajeria"

### Ambiente de desarrollo:
    Esta tarea se desarrolló y testeó en windows 10 Education, con la version 2.1.0.5 de docker desktop community, 
    se recomienda utilizar la misma configuración para el correcto funcionamiento, sin embargo el desarrollo fue
    realizado con el objetivo de poder levantar la arquitectura en cualquier sistema compatible, aunque no se 
    garantiza que este funcione correctamente.

### Informe de tarea
    El archivo Informe_tarea_2_Montecinos_Mora.pdf contiene las comparaciones técnicas entre ambas implementaciones 
    y la recomendación final.

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

- Para detener todos los contenedores que se encuentran activos, se puede utlizar el siguiente comando.
```console
docker stop $(docker ps -a -q)
```
## Pregunta-2-RabbitMQ
