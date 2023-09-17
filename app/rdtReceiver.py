from utils import BUFFER_SIZE

class Receiver:
    def __init__(self, socket):
        self.socket = socket
        self.seq_number = 0

        def alternate(self):
            if self.seq_number == 1:
                self.seq_number = 0

            else:
                self.seq_number = 1
                
        def contrary(self):
            if self.seq_number == 1:
                return 0

            else:
                return 1

        def check(self, seq_number):
            return (not (self.seq_number == seq_number))
        
        def receiver(self, seqnum, address):
            while check(seqnum):
                ACK = self.contary().encode()
                self.socket.sendto(ACK, address)
                
                message, _ = self.socket.recvfrom(BUFFER_SIZE)
                seqnum, _ = message.decode().split(',')
            
            ACK = self.seq_number
            alternate()
            
            self.socket.sendto(ACK, address)
