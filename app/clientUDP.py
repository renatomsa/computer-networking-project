from socket import *
import os
from datetime import datetime
from utils import BUFFER_SIZE, IP, PORT
from threading import Thread
from threading import Lock
from time import time

data_lock = Lock()

class Client:
    def __init__(self) -> None:
        self.response = ""
        self.pkt_id = '1'
        self.ack_confirm = False
        self.client_socket = socket(AF_INET, SOCK_DGRAM)

        self.sending_thread = Thread(target = self.sending)
        self.receiving_thread = Thread(target = self.receiving)
        self.sending_thread.start()
        
    def sending(self):
        started = False
        try:
            while (1):
                with data_lock:            
                    self.pkt_id = '1' if (self.pkt_id == '0') else '0'
                    self.ack_confirm = False
                
                self.response = input()
                self.response = self.pkt_id + self.response
                self.client_socket.sendto(self.response.encode(), (IP, PORT))
                
                if (not started):
                    self.receiving_thread.daemon = True
                    self.receiving_thread.start()
                    started = True

                t_start = time()

                if (self.response[1:] == "bye"):
                    del(self.receiving_thread)
                    break

                while (not self.ack_confirm):
                    t_curr = time()
                    if (t_curr - t_start > 5):
                        # timeout
                        self.client_socket.sendto(self.response.encode(), (IP, PORT))
                        t_start = time()
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
                        self.ack_confirm = True

                if (data[0] == '2'):
                    print(data[1:])
            return
        except Exception:
            print("ate logo")

novo = Client()