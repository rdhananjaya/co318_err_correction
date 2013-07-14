__author__ = 'Roshan'
import socket

class Sender:

    def __init__(self, ip, port):
        self.address = (ip, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind(self.address)

    def set_my_address(self, ip, port):
        self.sock.bind((ip, port))

    def send(self, data):
        self.sock.sendto(data, self.address)
        data, addr = self.sock.recvfrom(1024)


