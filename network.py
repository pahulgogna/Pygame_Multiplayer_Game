import socket
import pickle
import time
class Network:
    def __init__(self) -> None:

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.62.148'
        self.port = 5555
        self.addr = (self.server,self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            dat= pickle.loads(self.client.recv(2048))
            return dat
        except socket.error as e:
            print(e)

if __name__ == '__main__':
    n = Network()
    for i in range(6):
        print(n.send(f'hello{i}'))