import ErrorMaker
import sys
import os
from random import random

__author__ = 'Roshan'
import socket
import threading

import Sender
import makePacket

ERR_RATE = 10 # initial error rate is 10%; this is changed in __main__
WINDOW_SIZE = 5


class Receive:

    BUFSIZ = 256

    def __init__(self, ip, port):
        self.address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)


    def receive(self, ERR_RATE):
        data_collection = []
        packet_collection = []

        # print("Packet Sq no recv: ", end=" ")
        for i in range(WINDOW_SIZE):
            data, addr = self.sock.recvfrom(self.BUFSIZ)
            data_collection.append(data)
            tmp_pkt = makePacket.Packet.de_serialize(data)
            # print(tmp_pkt.sequence_no, end=" ")
            packet_collection.append(tmp_pkt)
            if tmp_pkt is not None and len(tmp_pkt) != makePacket.PACKET_SIZE:
                break
        # print()

        #Assuming packets will not arrive out of order
        # If want to to remove above assumption we will have to sort the packet list
        # accordingly and its hard to do so
        # packet_collection.sort() won't cut it !

        #####################################################################################################
        ## INJECT a error at randome place at given error rate
        # print("rejecting sq:", end=" ")

        for i in range(len(packet_collection)):
            r = random()*100
            if r < ERR_RATE:
                pkt = packet_collection[i]
                # print(pkt.sequence_no, end= " ")
                packet_collection[i] = None
        # print()

        counter = 0
        sq = -1 # this is the solution to the first ever packet with sq no 0 being in error and then ACK being REJ-1
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
        # counter = ErrorMaker.add_err(counter, ERR_RATE)

        if end:
            ACK = "RR-" + str(sq) + "-END"
            # print("END OF Receiving...")
        elif counter == WINDOW_SIZE:
            # print("No errors where introduced by simulator")
            ACK = "RR-" + str((sq+1)%8)
        else:
            if sq >= 0:
                ACK = "REJ-" + str((sq+1)%8)
            else:
                ACK = "REJ-" + "ALL"
            # print("\t\tPacket Rejected ################################### sq ", sq)

        self.sock.sendto(bytes(ACK, 'utf-8'), addr)


        return not end #if sender is done with sending return false; otherwise return true


    def process_data(self, data_collection):
        pass

    @staticmethod
    def packet_sort(pkt):
        sno = pkt.sequence_no





if __name__ == '__main__':

    if len(sys.argv) <= 2:
        print("\nUsage:\n\tpython Reciever.py <error rate> <window size>")
        print("\terror rate  -- the percentage error rate this is from 0% to 100%")
        print("\twindow size -- size of the sliding window (this must be same in both receiver and sender)")
        exit()

    if len(sys.argv) > 2:
        try:
            ERR_RATE = int(sys.argv[1])
            # print("ERROR RATE: ", ERR_RATE)
            WINDOW_SIZE = int(sys.argv[2])
            # print("WINDOW_SIZE ", WINDOW_SIZE)

        except ValueError as e:
            print("arguments must be ints")
            exit()


    recv = Receive("127.0.0.1", 5000)
    counter = 0
    while recv.receive(ERR_RATE):
        # print("............................. counter:", counter)
        counter += 1

    print("End of recv..")
