__author__ = 'Roshan '


import socket

import makePacket



pac = makePacket.Packet("AAAAA\xabrrrrr", 1)

print("pakect: ", pac)

p = pac.serialize()

# print(len(p))
# print(p)
# print()

new_p = makePacket.Packet.de_serialize(p)

print("pakcet: ", new_p)
print(new_p.extract_data())
print(bytes(new_p.extract_data(), 'utf-8'))








