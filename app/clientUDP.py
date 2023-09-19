from socket import *
import os
from datetime import datetime
from rdtReceiver import Receiver
from rdtSender import Sender
from utils import BUFFER_SIZE, IP, PORT

class Client:
    def __init__(self) -> None:
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.receiver = Receiver(self.client_socket)
        self.sender = Sender(self.client_socket)
        self.name = ""
        
        
    def final_message(self, message):
        now = datetime.now()
        time = f'{now.hour}:{now.minute}:{now.second} {now.day}/{now.month}/{now.year}'
        message = f"{IP}:{PORT}/~{self.name}: {message} {time}"
        print(message)
        
        return message
        
    def register(self):
        for i in range(2):
            if self.sender.is_waiting():
                response = input("Digite o nome:")
                self.sender.send(response, (IP, PORT))
                
            if i == 1:
                self.name = response
