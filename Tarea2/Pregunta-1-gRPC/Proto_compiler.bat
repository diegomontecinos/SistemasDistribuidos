powershell.exe -Command "& {python -m grpc_tools.protoc -I ./Protos --python_out=./Server/app --grpc_python_out=./Server/app ./Protos/Chat.proto; python -m grpc_tools.protoc -I ./Protos --python_out=./Generic_Client/app --grpc_python_out=./Generic_Client/app ./Protos/Chat.proto}"

