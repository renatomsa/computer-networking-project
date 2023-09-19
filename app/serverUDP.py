from socket import *
import os
from datetime import datetime
from rdtReceiver import Receiver
from rdtSender import Sender
from utils import BUFFER_SIZE, IP, PORT


class Server:   

    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(('localhost', PORT))
        self.receiver = Receiver(self.server_socket)
        self.sender = Sender(self.server_socket)

    def run(self):
        data, client_address = self.server_socket.recvfrom(1024)
        print(data)

    
test = Server()
test.run()