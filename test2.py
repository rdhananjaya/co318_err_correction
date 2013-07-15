__author__ = 'Roshan'
import socket

address = ("127.0.0.1", 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(bytes("abcdefg", 'utf-8'), address)
sock.sendto(bytes("abcdefg", 'utf-8'), address)
