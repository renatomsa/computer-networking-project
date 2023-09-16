from socket import *
from PIL import Image

# Função para receber arquivos do cliente
def receive_file(server_socket, buffer_size):
    # Recebe o arquivo do cliente
    _file, client_address = server_socket.recvfrom(buffer_size)
    _file = _file.decode()
    
    # Recebe o número de partes (chunks) em que o arquivo foi dividido
    num_chunks, _ = server_socket.recvfrom(4)
    num_chunks = int.from_bytes(num_chunks, byteorder='big')
    
    # Recebe o arquivo em partes e concatena
    data = b''
    for _ in range(num_chunks):
        chunk, _ = server_socket.recvfrom(buffer_size)
        data += chunk
    return _file, data, client_address

# Função para enviar o arquivo modificado de volta para o cliente
def send_back_file(server_socket, _file, data, client_address, buffer_size):
    # Lê e envia o arquivo em partes para o cliente
    with open(_file, 'rb') as f:
        for i in range(0, len(data), buffer_size):
            server_socket.sendto(data[i:i+buffer_size], client_address)
    print("Mandado de volta para o cliente")

server_port = 12000
buffer_size = 1024

# Criação do socket do servidor e associação à porta
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))

while True:
    quit = False
    while(1):    
        # Espera pelo comando do usuário para iniciar ou encerrar
        command = input('send/quit: ')
        if command == 'send':
            print("O servidor está pronto para receber")
            break
        elif command == 'quit':
            quit = True
            break
        else:
            print('Digite "send" para enviar um arquivo, ou "quit" para encerrar conexão')
    if quit: break
                  
    # Recebe o arquivo do cliente
    _file, data, client_address = receive_file(server_socket, buffer_size)

    # Verifica o tipo de arquivo recebido e processa de acordo
    if _file == "udp_sending.jpg":
        with open("udp_sent.jpg", 'wb') as file:
            file.write(data)
        with open("udp_sent.jpg", 'rb') as file:
            im = Image.open(file)
            im.show()
        send_back_file(server_socket, "udp_sent.jpg", data, client_address, buffer_size)
    elif _file == "udp_sending.txt":
        with open("udp_sent.txt", "w") as file:
            file.write(data.decode())
        # Converte o texto para maiúsculas
        data = data.decode().upper().encode()
        send_back_file(server_socket, "udp_sent.txt", data, client_address, buffer_size)

# Fecha o socket do servidor
server_socket.close()
