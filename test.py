__author__ = 'Roshan'
import socket



address = ("127.0.0.1", 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
x = sock.recvfrom(1024)
print(x)