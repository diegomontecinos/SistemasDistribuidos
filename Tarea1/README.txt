FORMATO:

TAREA1
|
|___PARTE1
|		client.py
|		server.py
|		log.txt
|		respuestas.txt
|
|___PARTE2
	|	docker-compose.yml
	|
	|___HEADNODE
	|	|	dockerfile
	|	|
	|	|___APP
	|			headnode.py
	|			hearthbeat_server.txt
	|			registro_server.txt
	|
	|___CLIENT
	|	|	dockerfile
	|	|
	|	|___APP
	|			client.py
	|			mensajes.txt
	|			registro_clientre.txt
	|
	|___DATANODE1
	|	|	dockerfile
	|	|
	|	|___APP
	|			datanode1.py
	|			data.txt
	|
	|.....


PARTE1:
-en carpeta parte 1:
-correr server.py - server quedara esperando conexion
-correr cliente.py - cliente saludara y pedira mensajes por consola
-se guardaran datos en archivos correspondienres

-se usó puerto 7550 y no 5000


PARTE2:
-en carpeta parte 2:
-correr docker-compose build
-correr docker-compose up

-no nos fue posible correr en modo consola interactiva para ingresar datos (si imprime)
-se trabajó con windows 10
-para recrear comportamiento cliente se incluye archivo extra en parte2/client/app/mensajes.txt
-desde mensajes.txt cliente lee mensajes y los envia a server