#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018-08-16 15:08:34
# author:jevade

'''
zk_client.py

A Python 3 tutorial zk client

Usage:

python3 zk_client.py
'''
import os
import json
import time
import struct
import socket
import random
from kazoo.client import KazooClient 
from rpc_client import RPCClient

zk_root = os.path.dirname(os.path.abspath(__file__))  
zk_root = "/tmp/rpc"
zk_rpc = zk_root + "/rpc"

G={"servers":None}
class ZKClient(RPCClient):

    @property
    def addr(self):
        return ":".join([self.host,str(self.port)])

    @addr.setter
    def addr(self,addr):
        try:
            node = addr.split(":")
            self.host,self.port=node[0],node[-1]
        except:
            self.host = addr["host"]
            self.port = addr["port"]
    @property
    def socket(self): # 懒链接
        if self.sock is None:
            self.connect()
        return self.sock


    def reconnect(self):
        self.close()
        self.connect()

    def close(self):
        if self.sock:
            self.sock.close()
        self.sock = None

    @staticmethod
    def create_object(addr):
        addr = json.loads(addr)
        theobject = ZKClient()
        theobject.addr = addr
        return theobject
    @classmethod
    def create_client(cls,addr):
        ob = cls()
        ob.addr = addr
        return ob
current_addrs = set()
del_servers = []
def get_server():
    zk = KazooClient(hosts="127.0.0.1:2184")
    zk.start()
    global current_addrs
    global del_servers
    def watch_servers(*args):
        new_addrs = set()
        for child in zk.get_children(zk_root,watch=watch_servers):
            node = zk.get(zk_root + "/" + child)
            if node[0] not in current_addrs and node[0] not in del_addrs:
                new_addrs.add(node[0])
        # 新增的地址
        add_addrs = new_addrs - current_addrs
        # 删除的地址
        del_addrs = current_addrs - new_addrs

        for addr in del_addrs:
            for server in G["servers"]:
                if server.addr == addr:
                    del_servers.append(server)
                    break
        for server in del_servers:
            G["servers"].remove(server)
            current_addrs.remove(server.addr)
        for addr in add_addrs:
            zKClient = ZKClient()
            zKClient.addr = addr
            G["servers"].append(zKClient)
            current_addrs.add(addr)
    for child in zk.get_children(zk_root,watch=watch_servers):
        node = zk.get(zk_root + "/" + child)
        current_addrs.add(node[0])
    

    G["servers"] = [ ZKClient.create_object(s) for s in current_addrs]
    return G["servers"]

def fresh_serer(server):
    pass

def random_server(i):
    get_server()
    if G["servers"] is None:
        get_server()
    if not G["servers"]:
        return
    return random.choice(G["servers"])
if __name__ == "__main__":
    for i in range(500):
        server = random_server(i) 
        if not server:
            break
        time.sleep(0.5)
        try:
            method ="pi" 
            # if  else "febric" if i%3 else "set" if i%7  else "get"
            params =  "pid:"+str(os.getpid())+", thread  ireader " + str(i)

            request = {
            "method":server.methods[method],
            "params":params,
            "n":i%7,
            "key":i%7,
            "pi_n":i,
            # "value":i%7,
            }
            sock = server.socket
            response = server.rpc(request)
            print(server.host,server.port,response)
        except Exception as ex:
            server.close()
            fresh_serer(server)
            print(ex,server.host,server.port)


    # zKClient = ZKClient()
    # zKClient.connect()
    # print(zKClient.socket)

