import socket
import pickle

class Network:
    def __init__(self) -> None:

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = '127.0.0.1'
        self.port = 5555
        self.addr = (self.server,self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p
    
    def connect(self):
        self.client.sendto(pickle.dumps('start'), self.addr)
        return pickle.loads(self.client.recvfrom(1024)[0])

    def send(self, data):
        try:
            self.client.sendto(pickle.dumps(data), self.addr)
            dat= pickle.loads(self.client.recvfrom(1024)[0])
            return dat
        except socket.error as e:
            print(e)

if __name__ == '__main__':
    n = Network()
    for i in range(6):
        print(n.send(f'hello{i}'))