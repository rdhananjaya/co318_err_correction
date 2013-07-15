__author__ = 'Roshan'
import socket
import _thread

class Sender:

    def __init__(self, ip, port, window_size=8):
        self.address = (ip, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.window_size = window_size
        # sock.bind(self.address)

    def set_my_address(self, ip, port):
        self.sock.bind((ip, port))

    def set_window_size(self, size):
        self.window_size = size

    def send(self, data):
        _thread.start_new_thread(self._send, data)
        data, addr = self.sock.recvfrom(1024)

    def _send(self, data):
        self.sock.sendto(data, self.address)




