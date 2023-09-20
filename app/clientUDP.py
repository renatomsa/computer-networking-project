from socket import *
import os
from datetime import datetime
from utils import BUFFER_SIZE, IP, PORT
from threading import Thread
from threading import Lock
from time import time

data_lock = Lock()  # evitar acesso simultaneo a variaveis compartilhadas entre as threads

class Client:
    def __init__(self) -> None:
        self.response = ""  # mensagem enviada ao server
        self.pkt_id = '1'   # identificador do pacote (0 ou 1)
        self.ack_confirm = False # confirma recebimento do ack
        self.client_socket = socket(AF_INET, SOCK_DGRAM)

        self.sending_thread = Thread(target = self.sending)
        self.receiving_thread = Thread(target = self.receiving)
        self.sending_thread.start() # iniciando thread de envio de mensagens
        
    def sending(self):
        started = False
        try:
            while (1):
                with data_lock:            
                    self.pkt_id = '1' if (self.pkt_id == '0') else '0' # alterna identificador do pacote
                    self.ack_confirm = False    # reseta confirmador
                
                self.response = input()
                with data_lock:
                    self.response = self.pkt_id + self.response     # identificacao do pacote no inicio da mensagem (primeiro caractere)
               
                self.client_socket.sendto(self.response.encode(), (IP, PORT))
                
                if (not started):
                    # inicia thread de recebimento dos envios do server
                    self.receiving_thread.daemon = True   # para que os prints da thread nao interfiram no input
                    self.receiving_thread.start()
                    started = True

                if (self.response[1:] == "bye"):
                    del(self.receiving_thread)  # se a mensagem for um "bye", a thread de recebimento é deletada
                    break

                t_start = time() # tempo inicial de envio da mensagem
                while (not self.ack_confirm):
                    t_curr = time()
                    if (t_curr - t_start > 5):
                        # timeout
                        self.client_socket.sendto(self.response.encode(), (IP, PORT))  # reenvia mensagem
                        t_start = time() # reseta tempo inicial
                        continue

                    if (self.ack_confirm): break  # recebeu o ack correto
            
        except Exception:
            print("closing socket")
        finally:
            self.client_socket.close()
            return
    
    def receiving(self):
        try:
            while (1):
                data, server_address = self.client_socket.recvfrom(1024)
                data = data.decode()
                
                # data[0] == '0' -> ack0
                # data[0] == '1' -> ack1
                # data[0] == '2' -> pertence a outro cliente

                with data_lock:
                    if (data[0] == self.pkt_id):
                        # client recebe o ack correto
                        self.ack_confirm = True

                if (data[0] == '2'):
                    # se a mensagem for de outro usuario (que nao o proprio), a mensagem sera printada com a formatacao
                    print(data[1:])
            return
        except Exception:
            print("ate logo")

novo = Client()