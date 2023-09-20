from socket import *
import os
from datetime import datetime
from rdtReceiver import Receiver
from rdtSender import Sender
from utils import BUFFER_SIZE, IP, PORT
from threading import Thread

class Client:
    def __init__(self) -> None:
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.receiver = Receiver(self.client_socket)
        self.sender = Sender(self.client_socket)

        self.sending_thread = Thread(target = self.sending)
        self.receiving_thread = Thread(target = self.receiving)
        self.sending_thread.start()
        
    def sending(self):
        started = False
        while (1):
            response = input()
            self.client_socket.sendto(response.encode(), (IP, PORT))
            if (not started):
                self.receiving_thread.daemon = True
                self.receiving_thread.start()
                started = True

    def receiving(self):
        while (1):
            data, server_address = self.client_socket.recvfrom(1024)
            data = data.decode()
            print(data)
        return
      
novo = Client()