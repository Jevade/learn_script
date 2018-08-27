# coding: utf-8
# server
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8080))
sock.listen(1)
print(12333)
i = 0
while True:
#   conn, addr = sock.accept()
#   print(conn.recv(1024))
#   conn.sendall(b"world")
#   conn.close()
    i +=1
