#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Aug 14, 2018 11:37
# author:jevade

'''
rpc_server.py

A Python 3 tutorial placeholder

Usage:

python3 rpc_server.py
'''


import os
import socket
import json
import struct
import time
import _thread
import math
from queue import Queue
from io import BytesIO,StringIO
import asyncore 
from threading import Thread
import ctypes
import threading
import random
import errno
list_error = [errno.EPERM,errno.ENOENT]
from redis_test import RedisPool
host_list=[('localhost',1024),('localhost',1024),('localhost',1024) ]
weight = []
def weight_gredient(weight,hostlist):
    pass

class Handlers():
    """处理请求的类"""
    handlers = {}
    redis_pool = None

    def __init__(self):
        self.handlers= {
            "ping":self.process_ping,
            "febric":self.process_febric,
            "get":self.process_redis,
            "set":self.process_redis,
            "delete":self.process_redis,
            "pi":self.process_pi,
        }

    @staticmethod
    def febric(n):
        '''斐波那契计算函数'''
        if n<2:
            return 1
        return Handlers.febric(n-1) + Handlers.febric(n-2)
        
    @staticmethod
    def pi(n):
        """处理PI计算请求"""
        result = 0
        for i in range(n):
            result += 1.0/(2 * i + 1)/(2 * i + 1)
        return math.sqrt(8*result)

    def process_ping(self,request):
        '''处理ping请求'''
        params = request["params"]
        response = {
            "method":"pong",
            "params":params,
        }
        return response

    def process_febric(self,request):
        '''处理斐波那契计算请求'''
        febric_n = int(request["n"])
        febric_value = Handlers.febric(febric_n)
        response = {
            "method":"febric",
            "febric_n":febric_n,
            "febric_value":febric_value,
        }
        return response

    def process_redis(self,request):
        '''处理redis请求'''
        key = request["key"]
        value = request.get('value','')
        method = request.get('method','set')

        with RedisPool() as redis_conn:
            if str(method).startswith('set'):
                redis_conn.set(key, value) 
            if str(method).startswith('delete'):
                redis_conn.delete(key)
            if str(method).startswith('get'):
                value = redis_conn.get(key)

        response = {
            "method":method,
            "key":key,
            "value":value,
        }
        return response

    def process_pi(self,request):
        """处理圆周率计算"""
        pi_n = int(request["pi_n"])
        method = request.get('method','pi')
        pi_value = Handlers.pi(pi_n)
        
        response = {
            "method":method,
            "pi_n":pi_n,
            "pi_value":pi_value,
        }
        return response

       
    def get_handle(self, request):
        """根据请求返回处理函数"""
        method = request.get("method",None)
        handle = self.handlers.get(method,None)
        return handle

    def process(self, request):
        """处理客户端请求"""
        handle = self.get_handle(request)
        if not handle:
            return None ,False
        pid = os.getpid()
        request['os_pid'] = pid
        #tid = ctypes.CDLL('libc.so.6').syscall(186)# linux 下可用
        tid = threading.current_thread()
        request['os_tid'] = tid
        print(request)
        response = handle(request)
        return response, True

class RedisProtocol():
    ONE_CHAR_ARROW = '+'
    MUL_CHAR_ARROW = '$'
    INT_ARROW = ':'
    ERROE_ARROW = '-'
    ARRAY_ARROW = '*'
    def text_decode(self,text):
        value = None
        return value
    def value_encode(self,value):
        text = None
        return text


class Server():
    """服务器处理请求的类"""
    handlers = None
    host = "localhost"
    port = 8080
    sock = None
    queue = None

    def receive(self,conn,n):
        '''封装sock的recv方法，防止网络传输时数据读取不全'''
        rs = []
        while n>0:
            r = conn.recv(n)
            if not r:
                break
            rs.append(r.decode())
            n -= len(r)
        return ''.join(rs).encode()


    def __init__(self):
        """初始化套接字"""
        self.queue = Queue()
        self.handlers = Handlers()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def connect(self, host=host, port=port):
        """绑定ip和端口，开始监听"""
        self.sock.bind((host,port))
        self.sock.listen(1)

    def prefork(self,n=10):
        for i in range(n):
            pid = os.fork() # 多进程
            if pid<0:     # 创建错误，退出
                return
            if pid > 0:   # 父进程，继续创建子进程  
                continue
            if pid == 0:  # 子进程，退出防止冗余创建
                break

    def prethread(self,thread_n=10):
        """开启线程池"""
        for i in range(thread_n):
            t = Thread(target=self.echo_client,args=(self.queue,))
            t.daemon = True
            t.start()

    def echo_client(self,queue):
        """线程池处理"""
        func,conn,addr = queue.get()
        func(conn,addr)

    def loop(self,flag=0):
        """服务器循环处理连接"""
        try:
            while True:        
                conn, addr = self.sock.accept()

                if flag is -1: #  线程池
                    self.queue.put((self.handle_conn,conn,addr))
                
                if flag is 0: #  单线程
                    self.handle_conn(conn, addr) 
                
                if flag is 1: #  多线程
                    _thread.start_new_thread(self.handle_conn,(conn, addr))
                
                if flag is 2:#  多进程
                    pid = os.fork() 
                    if pid<0:
                        return
                    if pid > 0:
                        conn.close()
                        continue
                    if pid == 0:
                        self.sock.close()
                        self.handle_conn(conn, addr)
                        break
                
                if flag is 3: # 多进程嵌套多进程     
                    pid = os.fork() 
                    if pid<0:
                        return
                    if pid > 0:
                        conn.close()
                        continue
                    if pid == 0:
                        self.sock.close()
                        _thread.start_new_thread(self.handle_conn,(conn, addr))#  多线程
                        break
        except KeyboardInterrupt:
            if self.sock:
                self.sock.close()
            print('键盘中断')
            

    def handle_conn(self, conn, addr):
        """处理连接的函数"""
        print(addr ,"comes")
        while True:
            request,flag = self.decode(addr, conn)
            if not flag:
                conn.close()
                print(addr,"bye")
                break
            response = self.handele(request)
            self.encode(response,conn)
            

    def handele(self,request):
        """处理访问信息"""
        response ,flag = self.handlers.process(request)
        if not flag:
            return {'status':500,}
        return response

    def decode(self, addr, conn):
        """接受客户端数据并解码"""
        length_prefix = self.receive(conn, 4)
        if not length_prefix:
            return None, False
        length, = struct.unpack("!I",length_prefix)
        body = self.receive(conn,length).decode()
        request = json.loads(body)
        return request, True
    
    def encode(self, response, conn):
        """将消息加码发送给客户端"""
        resonse = json.dumps(response)
        length_prefix = struct.pack("!I" , len(resonse))
        conn.sendall(length_prefix)
        conn.sendall(resonse.encode())


class RPCServer(asyncore.dispatcher):

    def __init__(self, host, port):
        """初始化server"""
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)
        # self.prefork()

    def handle_accept(self):
        """处理连接"""
        pair = self.accept()
        if pair is not None: #  轮询API
            sock,addr = pair
            RPCHandle(sock,addr)

    def prefork(self,n=10):
        """开启多进程"""
        for i in range(n):
            pid = os.fork() # 多进程
            if pid<0:     # 创建错误，退出
                return
            if pid > 0:   # 父进程，继续创建子进程  
                continue
            if pid == 0:  # 子进程，退出防止冗余创建
                break
class RPCHandle(asyncore.dispatcher_with_send):
    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self,sock=sock)
        self.addr = addr
        self.handlers = Handlers() 
        self.rbuf = BytesIO()
    
    def handle_connect(self):
        print(self.addr,'comes')

    def handle_close(self):
        """关闭连接"""
        print(self.addr,'bye')
        self.close()

    def handle_read(self):
        """读客户端请求，写入缓冲区，调用函数处理"""
        while True:
            try:
                content = self.recv(1024)
            except Exception as e:
                print(e)
            if content:
                try:
                    self.rbuf.write(content)
                except Exception as e:
                    print(e)
            if len(content) < 1024:
                break
          
        self.handle_rpc()

    def handle_rpc(self):
        """处理RPC请求"""
        while True:
            request,length,flag = self.decode()
            if not flag:
                break
            response = self.handle(request)
            self.encode(response)
            self.fresh_buf(length)
        self.rbuf.seek(0,2)

    def decode(self):
        """从客户端接受请求"""
        self.rbuf.seek(0)
        length_prefix = self.rbuf.read(4)
        if len(length_prefix)<4:
            return None,None,False
        length, = struct.unpack("!I",length_prefix)
        body = self.rbuf.read(length)
        request = json.loads(body.decode())
        return request,length,True
    
    def fresh_buf(self,length):
        """缓冲区截断，处理消息之后"""
        left = self.rbuf.getvalue()[length + 4:]
        self.rbuf = BytesIO()
        self.rbuf.write(left)

    def encode(self,response):
        """返回response"""
        body = json.dumps(response)
        length_prefix = struct.pack("!I", len(body))
        self.send(length_prefix)
        self.send(body.encode())

    def handle(self,request):
        """处理request的handele"""
        response ,flag = self.handlers.process(request)
        if not flag:
            return {'status':500,}
        return response


if __name__=="__main__":
    RPCServer("localhost",8080)
    asyncore.loop()
    # server =Server()  
    # server.connect()    
    # server.prefork(n=10) # 线程池
    # #server.prethread() # 进程池
    # server.loop(flag=0)


