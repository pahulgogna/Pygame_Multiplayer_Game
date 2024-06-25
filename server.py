# the server and network with a 2 in their names use the UDP protocol, which results in faster response times

import random
import socket
from _thread import *
import pickle

positions = [[150,-250], [-40,-250],[-153, 33.6],[-306, -79], [829, -207],[172, 81.6],[629, 33]]

start = {'movement':[0,0], 'pos': [-40,-250]}
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

        print('Server Startup Complete')

    # def get_players():


    def start(self):
        # while True:
        #     recv, addr = self.s.recvfrom(1024)
        #     dat = pickle.loads(recv)
        #     print(dat)
        #     if dat == 'start':
        #         self.s.sendto(pickle.dumps(start), addr)
        #         break

        while True:
            try:
                data, addr = self.s.recvfrom(1024)
                data = pickle.loads(data)
                if data == 'start':
                    start['pos'] = random.choice(positions)
                    PlayerData[make_key(addr)] = start
                    self.s.sendto(pickle.dumps(start), addr)
                    # print(PlayerData)
                    continue

                elif data == 'quit':
                    del PlayerData[make_key(addr)]
                
                elif make_key(addr) in PlayerData:
                    PlayerData[make_key(addr)] = data
                    print(PlayerData)
                    
                # else:
                #     key = make_key(addr)
                #     PlayerData[key] = start
                #     new_player = key
                #     PlayerData[key] = data
                    # self.s.sendto(pickle.dumps({'playerData':copy, 'new_player': new_player}), addr)

                self.s.sendto(pickle.dumps(PlayerData), addr)
            except socket.error as e:
                print(e)

def make_key(addr: tuple):
    return addr[0] + ';' + str(addr[1])

server = Server()

server.start()