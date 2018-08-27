# coding :utf-8
# server

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(("localhost", 8080))
#sock.sendall(b"hello")
#print('123')
#print(sock.recv(1024))
#sock.close()
def varint_encode(x):

    result = 0
    tail = x & 0x7f

    i = 1
    r = x >> 7
    while r > 0:
        n = (r & 0x7f) | 0x80
        result |= n << (8 * i)
        r = r >> 7
        i += 1

    return result | tail
print(varint_encode(13333))
