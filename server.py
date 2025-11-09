# libs usadas no trabalho, elas vao estar no venv, entao tem que rodar o source venv/bin/activate
from datetime import datetime
import socket


current_datetime = datetime.now()

print("====================================")
print("INICIO DA EXECUCAO DO SERVIDOR")
print("TRABALHO DE REDES 2 PROFESSOR ELIAS")
print(f"UNIVERSIDADE FEDERAL DO PARANÁ, {current_datetime}")



#cria o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#endereco e porta que o servidor vai ficar na maquina que esta rodando
host = '127.0.0.1'  # localhost
port = 5000

# Faz o socket bind
server_socket.bind((host, port))

# Começa a escutar, o 1 eh o valor maximo de execucoes na fila (poderia ser 5, mas o trabalho eh simples)
server_socket.listen(1)
print(f"Servidor escutando em {host}:{port}...")


while True:
    print(f"[{datetime.now()}] AGUARDANDO CONEXAO EM {host}:{port}")

    
    # Aceita uma conexão
    conn, addr = server_socket.accept()
    print(f"[{datetime.now()}] CONEXAO ESTABELECIDA COM {addr}")


    while True:
        data = conn.recv(1024).decode()
        print(f"[{datetime.now()}] MENSAGEM RECEBIDA: {data}")
        if not data:
            #client nao ta mandando nada, logo ele desconectou
            print(f"[{datetime.now()}] CLIENT DECONECTOU")
            break

        if data == 'FIN':
            conn.send("FINALIZA CONEXAO".encode())
            conn.close()
            print(f"[{datetime.now()}] Conexão com {addr} encerrada.")
            break

        if data[0:4] == "tadd":
            print(f"[{datetime.now()}] RECEBIDA UMA OPERACAO DE ADD NA CONTA")  
            conn.send("RECEBIDO CONN ADD".encode())


    # Envia resposta
    # print(f"[{datetime.now()}] MENSAGEM SENDO ENVIADA para {addr}")
    # conn.send("MESSAGE".encode())

#fecha o servidor (caso de borda)
server_socket.close()
