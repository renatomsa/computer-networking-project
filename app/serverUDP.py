from socket import *
import os
from datetime import datetime
from utils import BUFFER_SIZE, IP, PORT
import threading 
from threading import Thread
import time


class Server:   

    def __init__(self):
        self.log_thread = Thread(target = self.receive)

        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(('localhost', PORT))
        self.dict_users = {}    # mapeando ip + porta -> username
        self.map_adr_pkt = {}   # mapeando user -> pacote esperado

        self.log_thread.start()  # iniciando thread de recebimento de pacotes

    def final_message(self, message, adress):
        # formatando mensagem que sera exibida no chat
        now = datetime.now()
        time = f'{now.hour}:{now.minute}:{now.second} {now.day}/{now.month}/{now.year}'
        
        return f"{adress[0]}:{adress[1]}/~{self.dict_users[adress]}: {message} {time}"
    
    def hi(self, message, client_address):
        # funcao para adicionar chave (endereco do user) -> nome
        self.dict_users[client_address] = message[16:] #15
        self.map_adr_pkt[client_address] = '0'
        return message
    
    def receive(self):
        while (1):
            data, client_address = self.server_socket.recvfrom(1024)
            data = data.decode()
            new_thread = Thread(target = self.start2, args = (client_address, data))  # thread sendo criada para cada mensagem recebida
            new_thread.start()
        return
            
    def start2(self, target_address, data):
        try:
            listc=False
            if (not (target_address in self.dict_users)):
                # adicionando user aos dicionarios da classe
                data = self.hi(data, target_address)
            
            elif(data[1:] == "bye"):

                data = self.final_message(data[1:], target_address)
                self.dict_users.pop(target_address)  # removendo user do dicionario
                self.map_adr_pkt.pop(target_address) # removendo user do mapeamento
                for users in self.dict_users:
                    # envia a mensagem para os usuarios restantes
                    self.server_socket.sendto(("2" + data).encode(), users)

            elif(data[1:] == "list"):
                string = ""
                listc = True
                if (data[0] == self.map_adr_pkt):
                    # se o pacote esperado é o recebido, atualiza o identificador do pacote esperado 
                    self.map_adr_pkt[target_address] = '1' if (self.map_adr_pkt[target_address] == '0') else '0'

                ack = data[0]
                for user in self.dict_users:
                    string += f'/ {self.dict_users[user]} -> {user}\n'
                print(string)
                string = ack + string
                self.server_socket.sendto(string.encode(), target_address)
            
            if (target_address in self.dict_users and not listc):
                if (self.map_adr_pkt[target_address] == data[0]):
                    # se o server recebe o pacote esperado, atualiza id do pacote esperado
                    self.map_adr_pkt[target_address] = '1' if (self.map_adr_pkt[target_address] == '0') else '0'
                
                ack = data[0]
                data = data[1:]
                for user in self.dict_users:
                    # enviando a mensagem para os usuarios presentes na sala
                    data_aux = self.final_message(data, target_address)

                    #enviando ack para o user que mandou a mensagem e enviando "2" como prefixo para os demais
                    data_aux = '2' + data_aux if(user != target_address) else ack + data_aux
                    
                    self.server_socket.sendto(data_aux.encode(), user)    
        except KeyboardInterrupt:
            print("bye")
            return

test = Server()