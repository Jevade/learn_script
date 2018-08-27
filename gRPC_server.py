#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018-08-20 23:08:57
# author:jevade

'''
gRPC_server.py

A Python 3 tutorial func

Usage:

python3 gRPC_server.py
'''
import math
import grpc
import time
from concurrent import future
import pi_pb2
import pi_pb2_grpc

class PiCalculatorServicer(pi_pb2_grpc.PiCalculatorServicer):
    def Calc(self, request, ctx):
        s = 0.0

        for i in range(request.n):
            s += 1.0/(2*i+1)/(2*i+1)
        return pi_pb2.PiResponse(value=math.sqrt(s * 8))
def main():
    server = grpc.server(future.ThreadPoolExecutor(max_workers=10))
    servicer = PiCalculatorServicer()
    pi_pb2_grpc.add_PiCalculatorServicer_to_server(servicer,server)
    server.add_insecure_port('127.0.0.1:8080')
    server.start()
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)
if __name__ == '__main__':
    main()