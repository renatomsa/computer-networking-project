import socket
from utils import BUFFER_SIZE

class Sender:
    def __init__(self, socket) -> None:
        self.socket = socket
        self.sequence_number = '0'
        self.waiting = True
        self.error = False ## Verificar se é necessário uma função/classe para indicar um erro

    def check_ack(self, ack):
       return ack == self.sequence_number

    def change_seq_number(self):
        self.sequence_number = '0' if self.sequence_number == '1' else '1'

    def send(self, chunk, adress):
        self.waiting = False
        pkt = self.sequence_number + "," + chunk

        while not self.waiting:
            if  self.error == True:
                pass
            else:
                self.socket.sendto(pkt.encode(), adress)
            self.socket.settimeout(5)

            try:
                ack, adress = self.socket.recvfrom(BUFFER_SIZE)

                if self.check_ack(ack.decode()):
                    self.socket.settimeout(0)
                    self.change_seq_number()
                    self.waiting = True
            except socket.timeout:
                print("timeout!")
    
    def is_waiting(self):
        return self.waiting
        
