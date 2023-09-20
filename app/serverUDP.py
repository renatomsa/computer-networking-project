from socket import *
import os
from datetime import datetime
from rdtReceiver import Receiver
from rdtSender import Sender
from utils import BUFFER_SIZE, IP, PORT
import threading 
from threading import Thread
import time


class Server:   

    def __init__(self):
        self.log_thread = Thread(target = self.receive)

        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(('localhost', PORT))
        self.receiver = Receiver(self.server_socket)
        self.sender = Sender(self.server_socket)
        self.dict_users = {} 
        self.is_waiting = True

        self.log_thread.start()

    def final_message(self, message, adress):
        now = datetime.now()
        time = f'{now.hour}:{now.minute}:{now.second} {now.day}/{now.month}/{now.year}'
        
        return f"{adress[0]}:{adress[1]}/~{self.dict_users[adress]}: {message} {time}"
    
    def hi(self, message, client_address):
        self.dict_users[client_address] = message[16:] #15
        return message
    
    
    def receive(self):
        while (1):
            data, client_address = self.server_socket.recvfrom(1024)
            data = data.decode()
            new_thread = Thread(target = self.start2, args = (client_address, data))
            new_thread.start()

        return
            

    def start2(self, target_address, data):
        try:
            if (not (target_address in self.dict_users)):
                data = self.hi(data, target_address)
            
            elif(data == "bye"):
                self.dict_users.pop(target_address)

            elif(data == "list"):
                for user in self.dict_users:
                    print(self.dict_users[user])
                    self.server_socket.sendto(self.dict_users[user].encode(), target_address)

            if (target_address in self.dict_users):
                data = self.final_message(data, target_address)
                print(data)
                for user in self.dict_users:
                    self.server_socket.sendto(data.encode(), user)
                
                
        except KeyboardInterrupt:
            print("bye")

        return

test = Server()