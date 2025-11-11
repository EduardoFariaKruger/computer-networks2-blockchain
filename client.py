import socket

def main():
    #informacoes do servidor, pode ser que o server esteja rodando em uma maquina diferente, eu mesmo rodei em uma rpi e funcionou
    #mudar para 157.151.0.151 para quando quiser rodar na VM da oracle (dono Eduardo)
    host = '127.0.0.1'
    port = 5000
 
    # Cria e conecta o socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("=====================================")
    print("   CLIENTE - BLOCKCHAIN BANCÁRIA     ")
    print("=====================================")
    print("1 - Depósito")
    print("2 - Saque")
    print("3 - Ver saldo")
    print("4 - Ver BlockChain")
    print("0 - Sair")
    print("=====================================")

    while True:
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = input("Valor do depósito: ")
            mensagem = f"tadd:{valor}"

        elif opcao == "2":
            valor = input("Valor do saque: ")
            mensagem = f"twit:{valor}"

        elif opcao == "3":
            mensagem = "tbal:qualquercoisa"

        elif opcao == "0":
            print("Encerrando conexão...")
            client_socket.send("FIN".encode())
            client_socket.close()
            break
        elif opcao == "4":
            mensagem = "tdra:qualquercoisa..."
    
        else:
            print("Opção inválida! Tente novamente.")
            continue

        # Envia a mensagem ao servidor, depende do tipo que o pseudo-switch definiu
        client_socket.send(mensagem.encode())

        # Aguarda e exibe a resposta, sempre vai ser uma confirmacao ou uma mensagem de erro
        resposta = client_socket.recv(1024).decode()
        print("-------------------------------------")
        print("Resposta do servidor:", resposta)
        print("-------------------------------------")


if __name__ == "__main__":
    main()
