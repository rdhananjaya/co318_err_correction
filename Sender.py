__author__ = 'Roshan'
import socket


import  makePacket

PKT_SIZE = 100
WINDOW_SIZE = 5
BUFSIZ = 256

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


        data = [ i for i in zip(self._get_sequence_number(), self._data_chunk(data))]


        index = 0
        while index <= len(data):
            current_frame_set = data[index: index+WINDOW_SIZE]

            for data_chunk in current_frame_set:
                pkt = makePacket.Packet(data_chunk[1], data_chunk[0])
                serial_pkt = pkt.serialize()
                # print("PKT:", pkt.sequence_no, end=" ")
                i = self.sock.sendto(serial_pkt, self.address)
                print("PKT:", pkt.sequence_no, "sent", i, "bytes")

            ack = self._receive_ack()
            ack = ack.decode()

            if ack[-3:] == "END":
                break

            if ack[:2] == "RR":
                index += WINDOW_SIZE
            else:
                index += int(ack[-1])

            # print("INDEX", index)


    def _data_chunk(self, data):
        for i in range(0, len(data), makePacket.PACKET_SIZE):
            yield data[i:i+makePacket.PACKET_SIZE]

    @staticmethod
    def _get_sequence_number():
        seq = 0
        while True:
            yield seq

            seq += 1
            if seq >= makePacket.MAX_SEQUENCE_NUMBER:
                seq = 0



    def _receive_ack(self):
        data, addr = self.sock.recvfrom(BUFSIZ)
        print("_received_ack:", data, "from", addr)

        return data




