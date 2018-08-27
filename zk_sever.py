#!/usr/bin/python
# -*- coding: utf-8 -*-
# Aug 15, 2018 22:55
# author:placeholder

'''
placeholder

A Python 3 tutorial placeholder

Usage:

python3 placeholder
'''

import os
import sys
import math
import json
import errno
import struct
import signal
import socket
import asyncore
from io import BytesIO
from kazoo.client import KazooClient
from rpc_server import RPCHandle,RPCServer
class ZKRPCServer(asyncore.dispatcher):
    zk_root = os.path.dirname(os.path.abspath(__file__))  
    zk_root = "/tmp/rpc"
    zk_rpc = zk_root + "/rpc"
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)
        self.child_pids = []
        if self.prefork(10):
            self.register_zk()
            self.register_parent_signal()
        else:
            self.register_child_signal()

    def prefork(self, n = 10):
        for i in range(n):
            pid = os.fork()
            if pid < 0:
                raise
            if pid > 0:
                self.child_pids.append(pid)
                continue
            if pid == 0:
                return False
        return True
    
    def register_zk(self):
        self.zk = KazooClient(hosts="127.0.0.1:2184")
        self.zk.start()
        self.zk.ensure_path(self.zk_root)
        value = json.dumps({"host" : self.host,"port":self.port}).encode()
        path=self.zk.create(self.zk_rpc, value, ephemeral=True, sequence=True)
        print(path)

    def exit_parent(self, sig, frame):
        self.zk.stop()
        self.close()
        asyncore.close_all()
        pids = []
        for pid in self.child_pids:
            print("before kill")
            try:
                os.kill(pid, signal.SIGINT)
                pids.append(pid)
                pass
            except OSError as ex:
                if ex.args[0] == errno.ECHILD:
                    continue
                raise ex
            finally:
                pass
        for pid in pids:
            while True:
                try:
                    os.waitpid(pid, 0)
                    break
                except OSError as ex:
                    if ex.args[0] == errno.ECHILD:
                        break
                    if ex.args[0] == errno.EINTR:
                        raise ex 
            print("wait over",pid)
    def reap_child(self):
        print("before reap")
        while True:
            try:
                info = os.waitpid(-1, os.WNOHANG)
                break
            except OSError as ex:
                if ex.args[0] == errno.ECHILD:
                    return
                if ex.args[0] != errno.EINTR:
                    raise ex 
        pid = info[0]
        try:
            self.child_pids.remove(pid)
        except ValueError:
            pass
        print("after reap")
    def register_parent_signal(self):
        signal.signal(signal.SIGINT ,self.exit_parent)
        signal.signal(signal.SIGTERM ,self.exit_parent)
        signal.signal(signal.SIGCHLD ,self.exit_child)

    def exit_child(self,sig, frame):
        self.close()
        asyncore.close_all()
        print("all close")

    def register_child_signal(self):
        signal.signal(signal.SIGINT, self.exit_child)
        signal.signal(signal.SIGTERM, self.exit_child)

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    # host = "localhost"
    # port = 8082
    ZKRPCServer(host=host,port=port)
    asyncore.loop()