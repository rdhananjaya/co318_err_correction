__author__ = 'Roshan'
import socket
import threading

class Receive:

    BUFSIZ = 1024

    def __init__(self, ip, port):
        self.address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)


    def receive(self):
        data, addr = self.sock.recvfrom(self.BUFSIZ)
        print(data)
        print("from:", addr)
