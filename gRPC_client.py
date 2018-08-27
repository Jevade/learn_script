#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018-08-20 23:08:47
# author:jevade

'''
gRPC_client.py

A Python 3 tutorial gRPC_client

Usage:

python3 gRPC_client.py
'''
import grpc 

import pi_pb2
import pi_pb2_grpc

def main():
    channel = grpc.insecure_channel("localhost:8080")
    client = pi_pb2_grpc.PiCalculatorStub(channel)
    for i in range(1, 1000):
        print("pi=", i , client.Calc(pi_pb2.PiRequest(n=i)).value)

if __name__ == '__main__':
    main()