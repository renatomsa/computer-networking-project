from socket import *
import os
from rdtReceiver import Receiver
from rdtSender import Sender

class Client:
    def __init__(self) -> None:
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.receiver = Receiver(self.client_socket)
        self.sender = Sender(self.client_socket)
        self.name = ""
        