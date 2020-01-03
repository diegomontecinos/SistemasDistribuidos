# Readme Tarea 2 "Servicio de mensajeria"

### Ambiente de desarrollo:
    Esta tarea se desarrollo y testeo en windows 10 Education, con la version 2.1.0.5 de docker desktop community se recomienda utilizar la misma configuracion para el correcto funcionamiento, sin embargo el desarrollo fue realizado con el objetivo de poder levantar la arquitectura en cualquier sistema compatible, aun que no se garantiza que este funcione correctamente.

### Informe de tarea
    El archivo Informe_tarea_2_Montecinos_Mora.pdf contiene las comparaciones tecnicas entre ambas implementaciones y la recomendacion final.

## Pregunta-1-gRPC
### Estructura de archivos.
    -Pregunta-1-gRPC
        |-Generic_Client
        |    |-app
        |       |-Cliente.py --->> Codigo python del cliente
        |    |-Chat.proto --->> Definicion de servicios Protocol Buffer
        |    |-Dockerfile --->> Dockerfile container del cliente
        |    |-requirements.txt --->> Librerias requeridas por el cliente
        |-Protos
        |    |-Chat.proto
        |-Server
        |    |-app
        |    |    -Server.py --->> Codigo python del cliente
        |    |-Chat.proto --->> Definiciond de servicios Protocol Bufffer
        |    |-Dockerfile --->> Dockerfile container del servidor
        |    |-requirements.txt --->> Librerias requeridos por el servidor
        |-Docker_command.txt
        |-docker-compose.yml --->> docker-compose para levantar la arquitectura distribuida
        |-Proto_compiler.bat --->> Script para compilar Chat.proto en windows al momento de testear
        |-Run_1S_2C-bat --->> Script para levantar 1 cliente y 2 servidores en Windows Powershell


## Pregunta-2-RabbitMQ