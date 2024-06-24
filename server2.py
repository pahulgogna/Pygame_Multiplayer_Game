# the server and network with a 2 in their names use the UDP protocol, which results in faster response times

import socket
from _thread import *
import pickle

start = {'movement':[0,0], 'pos': [75,50]}
PlayerData = {} 

class Server:
    def __init__(self, server='', port=5555) -> None:
        self.server = server
        self.port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(e)

        print('Binded')

    def start(self):
        # flag_, __ = self.s.recvfrom(1024)
        while True:
            # print(PlayerData)
            reply = start
            data, addr = self.s.recvfrom(1024)
            # if pickle.loads(flag_) != 'start':
            if make_key(addr) in PlayerData:
                PlayerData[make_key(addr)] = pickle.loads(data)
            else:
                PlayerData[make_key(addr)] = start
                print('after -',PlayerData)

            for i in PlayerData:
                if i != make_key(addr):
                    reply = PlayerData[i]
                    break
            flag_ = ''
            self.s.sendto(pickle.dumps(reply), addr)

def make_key(addr: tuple):
    return addr[0] + ';' + str(addr[1])

server = Server()

server.start()