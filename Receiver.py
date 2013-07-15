__author__ = 'Roshan'
import socket
import threading

import Sender
import makePacket

class Receive:

    BUFSIZ = 1024

    def __init__(self, ip, port):
        self.address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)


    def receive(self):
        data_collection = []
        packet_collection = []
        for i in range(Sender.WINDOW_SIZE):
            data, addr = self.sock.recvfrom(self.BUFSIZ)
            # print("\n------------------------------------------\n"
            #       "Received:", data, "from:", addr)
            data_collection.append(data)
            packet_collection.append(makePacket.Packet.de_serialize(data))

        packet_collection.sort(key = lambda x: x.sequence_no)

        old_sq = 0
        for i in packet_collection:
            sq = i.sequence_no
            if sq > old_sq + 1:
                # err
                break
            old_sq = sq

        ACK = ""

        #WINDOW_SIZE - 1 coz count starts from 0 so even it counts WINDOW_SIZE
        #times it only say WINDOW_SIZE - 1
        if old_sq == Sender.WINDOW_SIZE - 1:
            ACK = "RR-" + str(old_sq)
        else:
            ACK = "REJ-" + str(old_sq)

        print("Sending ACK:", ACK)

        self.sock.sendto(bytes(ACK, 'utf-8'), addr)


    def process_data(self, data_collection):
        pass



if __name__ == '__main__':
    recv = Receive("127.0.0.1", 5000)
    recv.receive()