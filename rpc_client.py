#!/usr/bin/python3 
# -*- coding: utf-8 -*-
# Aug 14, 2018 11:39
# author:jevade

'''
rpc_client.py

A Python 3 tutorial rpc_client.py

Usage:

python3 rpc_client.py
'''

import socket
import json
import struct
import time
import _thread
import os

class Client():
    """基本类定义client的基本功能"""
    def run(self):
        return
    def connect(self):
        return
    def close(self):
        return
    def encode(self):
        return
    def decode(self):
        return
    def rpc(self):
        return


class RPCClient(Client):
    """定义RPC客户端"""
    host = "localhost"
    port = 8080
    sock = None
    methods ={
        "ping":"ping",
        "febric":"febric",
        "set":"set",
        "get":'get',
        "delete":"delete",
        "pi":"pi",
    }

    def receive(self, n):
        """
        封装了sock的recv方法，防止网络传输时数据读取不全
        params:n
        return:bytes
        """
        rs = []
        while n>0:
            r = self.sock.recv(n)
            if not r:
                break
            rs.append(r.decode())
            n -= len(r)
        return ''.join(rs).encode()

    def __init__(self, host=host, port=port): 
        """
        初始化链接
        params:host,port,default 127.0.0.1,8080
        """
        self.port = port
        self.host = host
    def connect(self):
        """
        建立连接
        params:None
        return:None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        self.sock = sock
    
    def close(self):
        """关闭连接"""
        self.sock.close()

    def run(self):
        """客户端运转"""
        for i in range(10):
            time.sleep(1)
            method ="pi" if i%2 else "febric" if i%3 else "set" if i%7  else "get"
            params =  "pid:"+str(os.getpid())+", thread  ireader " + str(i)

            request = {
            "method":self.methods[method],
            "params":params,
            "n":i%7,
            "key":i%7,
            "pi_n":i,
            # "value":i%7,
            }
            response = self.rpc(request)
            print(response)

    def encode(self,request):
        """编码request"""
        request = json.dumps(request)
        length_prefix = struct.pack("!I", len(request))
        return request, length_prefix

    def decode(self):
        """解码Response"""
        length_prefix = self.receive(4)
        length, = struct.unpack("!I", length_prefix)
        body = self.receive(length)
        response = json.loads(body.decode())
        return response


    def rpc(self, request):
        """RPC"""
        request, length_prefix = self.encode(request)        
        try:
            self.sock.sendall(length_prefix)
            self.sock.sendall(request.encode())
            response = self.decode()  
            return response
        except Exception as ex:
            return ex

turn = 1
number = 2
interest = [False] * number
def enter_region(process):
    other = number - process
    interest[process] = True
    turn = process
    # turn is process 本线程是不是最后进入，当 interest[other] 都为true时 表示都在等待，
    # 这时让先申请接管cpu的线程得到cpu,后进入的等待:
    while turn is process and interest[other] is True:
        pass
        
def leave_region(process):
    interest[process] = False

if __name__=="__main__":
    client = RPCClient()
    client.connect()
    client.run()
    client.close()