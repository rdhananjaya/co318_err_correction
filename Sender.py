__author__ = 'Roshan'
import socket
import _thread

import  makePacket

PKT_SIZE = 100
WINDOW_SIZE = 8

class Sender:

    def __init__(self, ip, port, window_size=8):
        self.address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.window_size = window_size
        # sock.bind(self.address)

    def set_my_address(self, ip, port):
        self.sock.bind((ip, port))

    def set_window_size(self, size):
        self.window_size = size

    def send(self, data):
        ## todo: only send a window at a time
        self._send(data)
        # data, addr = self.sock.recvfrom(1024)

    def _send(self, data):

        data_len = len(data)

        packet_num = 0
        for i in range(0, data_len, PKT_SIZE):
            data_chunk = data[i:i+PKT_SIZE]

            #make packets with the data_chunks

            pkt = makePacket.Packet(data_chunk, packet_num)
            serial_pkt = pkt.serialize()


            i = self.sock.sendto(serial_pkt, self.address)
            packet_num += 1
            print(packet_num, ": ", "send: ", i)

    def _receive_ack(self):
        data, addr = self.sock.recvfrom(self.BUFSIZ)
        print("_receive_ack:", data, "from", addr)




