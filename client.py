import socket

# Cria um socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o servidor e porta
host = '127.0.0.1'
port = 5000

# Conecta ao servidor
client_socket.connect((host, port))

# Envia mensagem
client_socket.send("tadd:qualquer coisa".encode())

# Recebe resposta
response = client_socket.recv(1024).decode()
print("Resposta do servidor:", response)

# Fecha o socket
client_socket.close()
