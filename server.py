# libs usadas no trabalho, elas vao estar no venv, entao tem que rodar o source venv/bin/activate
from datetime import datetime
import socket
from BlockChain import Bloco, Blockchain

current_datetime = datetime.now()
print("============================================================")
print("INICIO DA EXECUCAO DO SERVIDOR")
print("TRABALHO DE REDES 2 PROFESSOR ELIAS")
print(f"UNIVERSIDADE FEDERAL DO PARANÁ, {current_datetime}")
print("============================================================")


conta_blockchain = Blockchain("Joao", 3000)  # saldo inicial da conta e criacao de fato da conta no servidor

#cria o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#endereco e porta que o servidor vai ficar na maquina que esta rodando
#mudar para 0.0.0.0 quando ta na VM pra permitir conexoes vindas de fora
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

        #tadd pois eh "type add" (de adicionar na conta)
        if data[0:4] == "tadd":
            print(f"[{datetime.now()}] RECEBIDA UMA SOLICITACAO DE DEPOSITO")
            try:
                conta_blockchain.adicionar_bloco('deposito', int(data[5:]))
                conn.send(f"[{datetime.now()}] OPERACAO DE DEPOSITO BEM SUCEDIDA".encode())
                print(f"[{datetime.now()}] OPERACAO DE DEPOSITO BEM SUCEDIDA")
            except:
                print(f"[{datetime.now()}] FALHA NA OPERACAO DE DEPOSITO")                
                conn.send(f"[{datetime.now()}] FALHA NA OPERACAO DE DEPOSITO".encode())
            
        #twit pois eh "type withdraw" (de retirar da conta)
        if data[0:4] == "twit":
            print(f"[{datetime.now()}] RECEBIDA UMA SOLICITACAO DE SAQUE")
            try:
                conta_blockchain.adicionar_bloco('saque', int(data[5:]))
                conn.send(f"[{datetime.now()}] OPERACAO DE SAQUE BEM SUCEDIDA".encode())
                print(f"[{datetime.now()}] OPERACAO DE SAQUE BEM SUCEDIDA")
            except:
                print(f"[{datetime.now()}] FALHA NA OPERACAO DE SAQUE, VERIFIQUE SE VOCÊ TEM SALDO PARA ESTA OPERACAO")                
                conn.send(f"[{datetime.now()}] FALHA NA OPERACAO DE SAQUE".encode()) #deu ruim tentar mandar so string, tem que ter o encode pra transformar em byte

        #tbal pois eh type balance (de ver o balanco da conta)
        if data[0:4] == "tbal":
            print(f"[{datetime.now()}] RECEBIDA UMA SOLICITACAO DE VER BALANCO")
            try:
                balance = conta_blockchain.calcular_saldo()
                conn.send(f"[{datetime.now()}] BALANCO DA CONTA: {balance}".encode())
                print(f"[{datetime.now()}] OPERACAO DE VER BALANCO BEM SUCEDIDA")
            except:
                conn.send(f"[{datetime.now()}] FALHA NA OPERACAO DE VER BALANCO".encode())
                print(f"[{datetime.now()}] FALHA NA OPERACAO DE VER BALANCO")                

        #tdra pois eh type draw (pra desenhar a blockchain)
        if data[0:4] == 'tdra':
            print(f"[{datetime.now()}] RECEBIDA UMA SOLICITACAO DE DESENHO".encode())
            conn.send(f"[{datetime.now()}] SEGUE O DESENHO:".encode())
            conn.send(f"{conta_blockchain.imprimir_cadeia()}".encode())
            
    # Envia resposta
    # print(f"[{datetime.now()}] MENSAGEM SENDO ENVIADA para {addr}")
    # conn.send("MESSAGE".encode())

#fecha o servidor (caso de borda)
server_socket.close()
