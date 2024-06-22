import socket
from _thread import *
import pickle
import pygame
from scripts.entities import Player

PlayerData = [{'movement':[0,0], 'pos': [50,50],}, {'movement':[0,0], 'pos': [75,50],}]

class Server:
    def __init__(self, server='192.168.1.116', port=5555) -> None:
        self.server = server
        self.port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(e)

        self.s.listen(2)
        print('Waiting for Connection, Server Started')

    def threaded_client(self, conn, player):
        print("Player:",player)
        conn.send(pickle.dumps(PlayerData[player]))
        while True:
            try:
                data = pickle.loads(conn.recv(204))
                PlayerData[player] = data

                if player == 1:
                    reply = PlayerData[0]
                else:
                    reply = PlayerData[1]
                
                if not data:
                    print('Disconnected')
                    break
                # else:
                    # print('Received:', data)
                    # print('Sending:', reply)

                conn.sendall(pickle.dumps(reply))

            except :
                break
        print('Lost Connection')
        conn.close()

    def start(self):
        currentPlayer = 0
        while True:
            conn, addr = self.s.accept()  # conn -> obj telling what is connected, addr -> ip address
            print('Connected to:',addr)
            # print(currentPlayer)
            start_new_thread(self.threaded_client, (conn, currentPlayer))
            currentPlayer += 1
            if currentPlayer > 1:
                currentPlayer = 0


server = Server()

server.start()