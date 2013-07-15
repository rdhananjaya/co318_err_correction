__author__ = 'Roshan'

import hashlib

PACKET_SIZE = 512
DELIMINATOR = 0b10101011

class Packet:

    def __init__(self, data, sequence_no):
        """
        Packet expects data size to be 100 or less
        if its less rest will be padded with 0
        """
        # new_data = self.stuffing(data)
        new_data = data

        if sequence_no > PACKET_SIZE: # I know this doesnt make much sense
            raise ValueError("Sequence Number must be smaller than 9999 but {} is given".format(sequence_no))
        if len(new_data) > PACKET_SIZE:
            raise ValueError("Data length (with stuffing) should be less than of 9999  but {} is given".format(len(new_data)))

        self.data = new_data
        self.sequence_no = sequence_no

    def __str__(self):
        # data = self.destuffing(self.data)
        data = self.data
        if isinstance(data, bytes):
            data = str(data)

        return "Data: " + data + "\n" + "Seq No: " + str(self.sequence_no)

    def __len__(self):
        return len(self.data)

    # @staticmethod
    # def stuffing(data):
    #     new_data = ""
    #     for i in data:
    #         if i == chr(DELIMINATOR):
    #             i += chr(DELIMINATOR)
    #         new_data += i
    #     return new_data

    # @staticmethod
    # def destuffing(stuffed):
    #     j = ''
    #     data = ''
    #     for i in stuffed:
    #         if i == chr(DELIMINATOR):
    #             if j == chr(DELIMINATOR):
    #                 continue
    #             j = i
    #         data += i
    #     return data

    def extract_data(self):
        # return "".join(i for i in self.data if ord(i) != 0)
        # return self.destuffing(self.data)
        return self.data

    @staticmethod
    def hasher(data):
        md5 = hashlib.md5()
        md5.update(data)
        hash = md5.digest()
        return hash

    def serialize(self):
        """ Serialize the packet
         packet = data + sequence number + hash code
        """
        sequence_number = bytes("{:04}".format(self.sequence_no), 'utf-8')
        data_length = bytes("{:04}".format(len(self)), 'utf-8')
        # print("###", sequence_number, data_length)
        # data = bytes(self.data, 'utf-8')
        data = self.data

        tmp = data_length + sequence_number +  data
        hash = self.hasher(tmp)

        return  hash + tmp #+ bytes(str(DELIMINATOR), 'utf-8')

    @classmethod
    def de_serialize(cls, packet):
        """de_serialize make a new packet out of the serialized packet
         if the input serialized packet is altered then de_serialize will return None
         otherwise it returns new packet object
        """

        # print(">>>", packet)

        hash = packet[:16]
        # print('hash', hash)

        rest_of_stuff = packet[16:]
        re_hash = Packet.hasher(rest_of_stuff)
        # print('re_hash', re_hash)

        if hash != re_hash:
            return None

        data_length = packet[16:20]
        sequence_no = packet[20:24]
        data = packet[24:]
        #print("-------------", data_length, sequence_no, data)

        #sequence number encoded with ntohs to its 4byte long
        sequence_no = int(sequence_no)
        # print("sequence_no in host int:", sequence_no)

        #data length encoded with socket.htons() to its a short; that is 4bytes
        data_length = int(data_length)
        # print("data length (hot int):", data_length)

        # new_packet = cls(data.decode(), sequence_no)
        new_packet = cls(data, sequence_no)
        return new_packet
