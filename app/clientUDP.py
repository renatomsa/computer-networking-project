from socket import *
from PIL import Image
import os

# Função para enviar arquivos ao servidor
def send_file(client_socket, _file, server_address, buffer_size):
    # Envia o arquivo para o servidor
    client_socket.sendto(_file.encode(), server_address)
    
    # Abre o arquivo em modo binário para leitura
    with open(_file, "rb") as f:
        data_file = f.read()
        
        # Calcula o número de partes (chunks) que o arquivo será dividido para envio
        num_chunks = len(data_file) // buffer_size + (len(data_file) % buffer_size != 0)
        
        # Envia o número de partes para o servidor
        client_socket.sendto(num_chunks.to_bytes(4, byteorder='big'), server_address)
        
        # Envia o arquivo em partes para o servidor
        for i in range(0, len(data_file), buffer_size):
            client_socket.sendto(data_file[i:i+buffer_size], server_address)
    return num_chunks

# Função para receber o arquivo modificado do servidor
def receive_modified_file(client_socket, original_file, buffer_size, num_chunks):
    print(f"Esperando {num_chunks} partes do servidor...")
    
    # Verifica se o arquivo original é uma imagem
    if original_file.endswith('.jpg'):
        expected_file = "udp_sent_back.jpg"
        with open(expected_file, 'wb') as file:
            # Recebe o arquivo em partes e escreve no disco
            for _ in range(num_chunks):
                data, _ = client_socket.recvfrom(buffer_size)
                file.write(data)

        print("Recebido")
        
        # Mostra a imagem recebida
        with open(expected_file, 'rb') as file:
            im = Image.open(file)
            im.show()
    else:
        # Caso o arquivo original não seja uma imagem, trata como texto
        expected_file = "udp_sent_back.txt"
        received_text = ''
        
        # Recebe o arquivo em partes e concatena o texto
        for _ in range(num_chunks):
            data, _ = client_socket.recvfrom(buffer_size)
            received_text += data.decode()

        # Escreve o texto recebido no disco
        with open(expected_file, 'w') as file:
            file.write(received_text)
        print("Recebido pelo cliente")

# Configurações do servidor e porta
server_name = "localhost"
server_port = 12000
buffer_size = 1024

# Criação do socket do cliente
client_socket = socket(AF_INET, SOCK_DGRAM)

# Lista todos os arquivos no diretório atual
files = os.listdir()

# Procura por arquivos .txt ou .jpg no diretório para enviar ao servidor
for file in files:
    if file.endswith('.txt') or file.endswith('.jpg'):
        # Envia o arquivo encontrado para o servidor
        num_chunks_sent = send_file(client_socket, file, (server_name, server_port), buffer_size)
        
        # Recebe o arquivo modificado do servidor
        receive_modified_file(client_socket, file, buffer_size, num_chunks_sent)
        break

# Fecha o socket do cliente
client_socket.close()
