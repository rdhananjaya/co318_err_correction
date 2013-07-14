__author__ = 'Roshan'

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5000
UDP_ADDR = (UDP_IP, UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(UDP_ADDR)

while True:
    data, addr = sock.recvfrom(1024)
    print("RECEVED")
    print(data.decode('UTF-8'))
    print(addr)
    sock.sendto(data, addr)


