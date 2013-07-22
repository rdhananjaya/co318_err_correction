import ErrorMaker

__author__ = 'Roshan'
import socket
import threading

import Sender
import makePacket

class Receive:

    BUFSIZ = 256

    def __init__(self, ip, port):
        self.address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)


    def receive(self):
        data_collection = []
        packet_collection = []
        print("Packet Sq no: ", end=" ")
        for i in range(Sender.WINDOW_SIZE):
            # print("RECEIVING:", i, end=" ")
            data, addr = self.sock.recvfrom(self.BUFSIZ)
            # print("RECEIVED:", i, end=" ")
            data_collection.append(data)
            tmp_pkt = makePacket.Packet.de_serialize(data)
            print(tmp_pkt.sequence_no, end=" ")
            packet_collection.append(tmp_pkt)
            if tmp_pkt is not None and len(tmp_pkt) != makePacket.PACKET_SIZE:
                break

        print()

        #Assuming packets will not arrive out of order
        # If want to to remove above assumption we will have to sort the packet list
        # accordingly and its hard to do so
        # packet_collection.sort() won't cut it !

        counter = 0
        sq = -1
        end = False # indicate end of receiving
        for i in packet_collection:
                ## packet with corrupt data will have wrong hash code
                ## hence de_serialize will return None
                ## lets catch the none here
                if i is None:
                    break
                sq = i.sequence_no
                counter += 1
                if len(i) < makePacket.PACKET_SIZE:
                    end =  True

        ACK = ""


        #### forcibly introduce a error to the relieved packets
        counter = ErrorMaker.add_err(counter, 10)

        if end:
            ACK = "RR-" + str(sq) + "-END"
            print("END OF Receiving...")
        elif counter == Sender.WINDOW_SIZE:
            ACK = "RR-" + str((sq+1)%8)
        else:
            ACK = "REJ-" + str((sq+1)%8)
            print("\t\tPacket Rejected ###################################")

        print("## Sending ACK:", ACK, end=" ")
        self.sock.sendto(bytes(ACK, 'utf-8'), addr)
        print("ACK send")

        return not end #if sender is done with sending return false; otherwise return true


    def process_data(self, data_collection):
        pass

    @staticmethod
    def packet_sort(pkt):
        sno = pkt.sequence_no





if __name__ == '__main__':
    recv = Receive("127.0.0.1", 5000)
    while recv.receive():
        pass
