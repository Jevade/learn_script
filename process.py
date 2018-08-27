from multiprocessing import Process,Pool
import os,time,random
def run_proc(name):
	print('Run task %s (%s)...' % (name, os.getpid()))
	start=time.time()
	time.sleep(random.random()*10)
	end=time.time()
	print(name)
	print('child process%s %s run(%s)ms' % (name, os.getpid(),end-start))
def callprecess():
	p=Pool(20)
	print('Parent process %s.' % os.getpid())
	for x in range(4):
		
		p.apply_async(run_proc, args=(x,))
	p.apply_async(run_proc, args=(6,))

	print('Child process will start.')
	p.close()
	p.join()
	print('Child process end.')

import threading, multiprocessing
lock = threading.Lock()
balance=0
def change_it(n):
	n=int(n)
	global balance
	lock.acquire()
	balance=balance-n
	balance=balance+n
	lock.release()
def run(n):
	for x in range(1000):
		change_it(x)



# 创建全局ThreadLocal对象:
local_school = threading.local()

def tell():
	name=local_school.name
	print(name)
def chooseWhichTell(name):
	local_school.name=name
	tell()
t1=threading.Thread(target=chooseWhichTell,args=("LIU",))
t2=threading.Thread(target=chooseWhichTell,args=("GUO",))
t1.start()
t2.start()
t1.join()
t2.join()

#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# task_master.py

import random, time, queue
from multiprocessing.managers import BaseManager

# 发送任务队列
task_queue = queue.Queue()

# 接受结果的队列
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager
class QueueManage(BaseManager):
    pass

# 把两个队列都注册到网络上,callable参数关联了Queue对象
QueueManage.register('get_task_queue', callable=lambda: task_queue)
QueueManage.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000，设置验证码abc
manager = QueueManage(address=('',61000), authkey=b'abc')
# 启动Queue
server = manager.get_server()

server.serve_forever()






