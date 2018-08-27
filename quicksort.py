#!/usr/bin/env python
# -*- coding: utf-8 -*-

r'''
learning.py

Usage:

python3 learning.py
'''

import numpy as np
import random,time
n=10
a=np.array([random.randint(1,n) for i in range(n)])
b=a.copy()
c=b.copy()
import pdb
pdb.set_trace()
class item:
    def __init__(self):
        self.name = ''     # 名称
        self.size = 10     # 尺寸
        self.list = []     # 列表
        print(123) 
		while  i<j and a[j]>=m:
			j=j-1
		a[i]=a[j]
		
	a[j]=m
	if(s<i-1):
		quicksort(a,s,i-1)
	if(e>i+1):
		quicksort(a,i+1,e)




def babble(a):
	index=0
	m=0
	index=1
	for i in range(0,a.size-1):
		temp=a[a.size-1-i]
		if 0==index:
			break
		for j in range(a.size-1-i):
			index=0
			if a[j]>=temp:
				index=1
				a[a.size-1-i]=a[j]
				a[j]=temp				temp=a[a.size-1-i]

def sss(a):#总共n(n-1)次比较，n-1次交换
	for i in range(len(a)):
		k=i
		for j in range(i,len(a)):
			if not a[j]>a[k]:
				k=j
		temp=a[k]
		a[k]=a[i]
		a[i]=temp
def sssTWO(a):
	for i in range(len(a)):
		if not i<len(a)-i-1:
			return
		k=i
		m=i
		for j in range(i,len(a)-i-1):
			#print(i,len(a)-i)
			if not a[j]>a[k]:
				k=j
			if not a[j]<a[m]:
				m=j
		temp=a[k]
		a[k]=a[i]
		a[i]=temp
		temp=a[m]
		a[m]=a[len(a)-i-1]
		a[len(a)-i-1]=temp

def bitree():
	pass

#babble(a)
quicksort(b,0,b.size-1)
print(b)
#sss(c)

def devideapple(n,a):
	needMove=0
	if not sum(a)%n==0:
		print("-1")
		return
	else:
		avg=sum(a)/n
		for x in a:
			if x<=avg:
				pass
			elif (x-avg)%2==1:
				print("-2")
				return
			else:
				needMove+=((x-avg)/2)
	print(needMove)
n1=4
a1=[7,15,9,5]
devideapple(n1,a1)

def maxSum(h):
    return int(np.sqrt(h+0.25)-0.5)

#print(maxSum(100))

#for aa in range(1,5):
#print(a==c)

def childStirng(a,b):
	for x in b:
		if a.find(x)==-1:
			print("No")
			return
	print("Yes")
aa="group.jobbole.com"
bb="oko"


#childStirng(aa,bb)
def poppush(n):
	index=[]
	list3=[0 for i in range(n)]
	lists=[i for i in range(1,n+1,1)]
	while len(lists)>0:
		lists.append(lists.pop(0))
		index.append(lists.pop(0))
	i=1
	for x in index:
		list3[x-1]=i
		i+=1
	print(list3)
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
f=lazy_sum(1,2,3,4,5,6)
print(f())

def lazy_sum():
	def g(i):
		def f():
			return i*i
		return f
		return lambda:i*i

	
	listTemp=[]
	for i in range(1,4):
		listTemp.append(g(i))
	return listTemp

def lazy_sum_lambda():
	return [(lambda i:(lambda :i*i))(i)for i in range(1,4)]
#return a function with all variable attached when use the returned function.it will
#finish the calculation and return a function

#lambda x:y
# x is input and y in output
#x can be void mean this function does not need input and return y 
#lambda :y


#list1=lazy_sum_lambda()[2]
#print(list1())
import functools
def log(arg=None):
	def dec(func):
		@functools.wraps(func)
		def a(*args, **kw):
			print("begin")
			if arg:
				print('%s %s():' % (arg, func.__name__))
			else:
				print('%s():' % (func.__name__))
			func(*args, **kw)
			print("end")
		return a
	return dec
    #def wrapper(*args, **kw):
     #   print('call %s():' % func.__name__)
      #  return func(*args, **kw)
    #return wrapper
@log()
def function():
	print("2012")
	return lambda x=2,y=3:x+y#return function with default variable 2,3
b=function()
int2=functools.partial(int ,base=2)
print(int2(str(100)))

def convert(n):
	str1=""
	while(n>0):
		i=n%2
		n/=2
		n=int(n)
		str1=str(i)+str1
	return str1
print(convert(126))

class Student(object):
	def __init__(self,name,score):
		self.__name=name
		self.__score=score
	def get_name(self):
		return self.__name
	def set_name(self,name):
		self.__name=name
	def get_score(self):
		return self.__score
	def study(self):
		print("student is studying")

class boyStudent(Student):
	def study(self):
		print("boy is studying")
class grilStudent(Student):
	def study(self):
		print("gril is studying")




a=Student("mm",89)
a.study()

b=boyStudent("mm",89)
b.study()
c=grilStudent("mm",89)
c.study()
print(c.get_score())

#定义一个父类一个子类
class y(object):
	def __init__(self,proname):
		self.proname=proname
	@property
	def score(self):
		return self._score

	@score.setter
	def score(self, value):
		if not isinstance(value, int):
			raise ValueError('score must be an integer!')
		if value < 0 or value > 100:
			raise ValueError('score must between 0 ~ 100!')
		self._score = value
	def ps(self):
		print('I am in %s'%self.proname)
	def __str__ (self):
		return 'Student object (name: %s)' % self.proname
	__repr__ = __str__

class x(y):
    def __init__(self,proname,cityname):
        self.cityname=cityname
        y.__init__(self,proname)
    def ps1(self):
        print('I\'m in %s-%s' %(self.proname,self.cityname))

#定义一个独立的类
class Timer(object):
    def ps(self):
        print('我不属于Province类或其子类，但我有ps方法我同样可以被调用')
    def ps1(self):
        print('我不属于Province类或其子类，但我有ps1方法我同样可以被调用')
class test(Timer):
	def ps(self):
		print("i am test")
class Student(object):
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
#定义一个函数
class success(test,y):
	def tell(self):
		print("i am using y and Student")
def f(x):
    x.ps()#override multi method
    x.ps1()#success and
#调用部分
f(x('上海','浦东'))
f(Timer())
f(test())
a=y("Liming")
a.score=70
print(a.score)
f(success("123"))

class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, strq):
        return Chain('%s/%s' % (self._path, strq))

    def __str__(self):
        return self._path

    __repr__ = __str__
print(Chain("").user.d12)


#dynamic return a property and function
class name(object):
	def __init__(self,path=""):
		self._path=path
	def __getattr__(self,attr):
		return name("%s/%s" % (self._path,attr))
	def __call__(self,attr):
		return name("%s:%s" % (self._path,attr))
	def __str__(self):
		return self._path

	__repr__=__str__


 #!/usr/bin/env python3
 # -*- coding:utf-8 -*-

class Chain(object):
	def __init__(self, path=''):
		self._path = path

	def __getattr__(self, path):
		return Chain('%s/%s' % (self._path, path))
	def users(self,user):
		return Chain('/users:%s/%s' %(self._path,user))
	def __str__(self):
		return self._path

	__repr__ = __str__


print(Chain().status.user.timeline.list)
print(Chain().users('michael').repos)
class Chain(object):
	def __init__(self, path="path"):
		self._path = path

	def __getattr__(self, item):  # 使用实例不存在的属性时，会尝试用该函数解释
		print("got")
		return Chain("%s/%s" % (self._path, item))

	def __str__(self):
		return self._path

	def __call__(self, *args, **kwargs):  # 使用实例不存在的方法时，会尝试用该函数解释
		print("called")
		return Chain("%s/%s" % (self._path, args))


print(Chain()("1"), Chain("1")("2"), Chain("1")("2")("3"))
print(Chain().status)
print(Chain().status.user("ksven"))
print(Chain().status.user("ksven").timeline)
print(name().status.user("ksven").timeline)

class fib(object):
	def __init__(self):
		self.a,self.b=0,1
	def __iter__(self):
		return self
	def __next__(self):
		self.a,self.b= self.b,self.a+self.b
		if self.a>100000:
			raise StopIteration()
		return self.a
for n in fib():
	print(n)

class Fib(object):
	def __getitem__(self,n):
		if isinstance(n,int):
			self.a,self.b=0,1
			for x in range(n):
				self.a,self.b= self.b,self.a+self.b
			return self.a
		if isinstance(n,slice):
			start=n.start
			stop=n.stop
			step=n.step
			index=start
			L=[]
			if start==None:
				start=0
			while not (start-index)*(stop-index)>0:
				L.append(Fib()[index])
				index+=step
			return L




a=Fib()[9:20:2]
print(a)
print(a[1:3:-1])
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
Week=Enum('Week',('Mon','Tue','Wen','Thu','Fri','Sat','Sun'))
for name,member in Week.__members__.items():
    print(name, '=>', member, ',', member.value)
a=str(123)
with open('/Users/liu/Desktop/hello world.txt','a+') as f:
	f.write("123")
import logging
try:
    print('try...')
    r = 10 / 2
    print('result:', r)
except BaseException as e:
    print('except:', e)
    logging.exception(e)
finally:
    print('finally...')
print('END')

import pdb
import logging

s = '1'
n = int(s)
logging.info('n = %d' % n)

assert n!=0, "n=0"

print(10 / n)

from io import StringIO
f=StringIO()
f.write("123\n")
f.write("234\n")
print(f.getvalue())
with open('/Users/liu/Desktop/hello world.txt','a+') as b:
	b.write(f.getvalue())

from io import BytesIO
from functools import reduce
b=BytesIO("okli".encode('utf8'))
path='path'
str1=b.getvalue().decode('utf8')
print(str1[:])
a=reduce(lambda x, y: x+y,[str(x) for x in range(10)])
print(b.tell())
b.write(a.encode('utf8'))
str1=b.getvalue().decode('utf8')
print(str1[:])

import os
#os.path.split('/Users/michael/testdir/file.txt')
print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]==('.bin')])
def file():
	lists=[]
	for x in os.listdir('.'):
		if os.path.isfile(x):
			lists.append(os.path.split(x)[1])
		elif os.path.isdir(x):
			li=[os.path.join(x,os.path.split(y)[1])for y in os.listdir(x) ]
			lists=lists+li

	return lists
#x1,x2,x3=os.walk(dirc)

import json
d = dict(name='Bob', age=20, score=88)
ming=dict(name='ming',age=20,gender="male",height=1.75)
mi={"gender": "male", "name": "ming", "age": 20, "height": 1.75}
with open('/Users/liu/Desktop/hello world.json','w') as f:
	json.dumps(ming,f)


cc=json.dumps(mi)

#with open('/Users/liu/Desktop/hello world.json','r') as y:
c=json.loads(cc)
print(cc,c)
print(c['name'])


print("process (%s) is function" % (os.getpid(),))
pid=os.fork()
if pid==0:

	print("child(%s),(%s)"%(os.getpid(),os.getppid()))
else:
	print("father(%s)(%s)"%(os.getpid(),pid))

from multiprocessing import Process


def proc(name,i):
	print("i am (%s) in precess(%d)"%(name,i))

def main():
	print('parents process(%s) is runing'%os.getpid())
	p=Process(target=proc,args=('test',0))
	print("child is runing")
	p.start()
	p.join()
	print('child process is ended')

from multiprocessing import Process,Pool
import os,time,random

# 子进程要执行的代码
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

import subprocess
print("i am using the parents process")
p=subprocess.Popen(['nslookup'],)
r=subprocess.call(['nslookup','www.python.org'])
print(r)


#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# task_worker

import time, queue, sys, random, multiprocessing, threading
from multiprocessing.managers import BaseManager

# 创建和服务器类似的QueueManager类
class QueueManager(BaseManager):
    pass
# 负责计算任务
def comp_task():
    global task
    global result
    global t_lock
    while(True):
        try:
            t_lock.acquire()
            n = task.get(timeout = 1)
            print('run task %d * %d...' % (n, n))
            r = '%d * %d = %d' % (n, n, n*n)
            time.sleep(1)
            result.put(r)
        except queue.Empty:
            print('task is empty')
        finally:
            t_lock.release()
# 负责分配任务
def attr_task():
    global task
    global t_lock
    # 放10个任务进去
    for i in range(10):
        try:
            t_lock.acquire()
            n = random.randint(0, 10000)
            print('Put task %d' % n)
            task.put(n)
        finally:
            t_lock.release()
t_lock = multiprocessing.Lock()

QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

manager = QueueManager(address=('127.0.0.1', 61000), authkey=b'abc')
manager.connect()

task = manager.get_task_queue()
result = manager.get_result_queue()

t1 = threading.Thread(target=attr_task, name='AttributeThread')
t2 = threading.Thread(target=comp_task, name='ComputeThread')

t1.start()
t2.start()
t1.teminate()

