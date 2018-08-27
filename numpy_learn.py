#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
numpy_learning.py

Usage:

python3 numpy_learn.py
'''
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt




def pythonsum(n):
    print('pythonsum',n)
    a = list(range(n))
    b = list(range(n))
    c = []
    for i in range(len(a)):
        a[i] = i * i * i
        b[i] = i * i
        c.append(a[i] + b[i])
    return c

def pythonsum2(n):
    print('pythonsum',n)
    a = list(range(n))
    b = list(range(n))
    c = []
    for i in range(len(a)):
        a[i] = i ** 3
        b[i] = i ** 2
        c.append(a[i] + b[i])
    return c     
def numpysum(n):
    print('numpysum',n)
    a = np.arange(n) ** 2
    b = np.arange(n) ** 3
    c = a + b
    return c

def add_timedelta(func,n):
    start = datetime.now()
    c = func(n)
    end = datetime.now()
    delta = end-start
    return c ,delta.microseconds


import sys
# size = int(sys.argv[1])
size =100
loops = []
times_python = []
times_numpy = []
for i in range(100,size,500):
    loops.append(i)
    c,time = add_timedelta(pythonsum,i)
    times_python.append(time)

for i in range(100,size,500):
    c,time = add_timedelta(numpysum,i)
    times_numpy.append(time)

plt.plot(loops, times_numpy)
plt.plot(loops, times_python)
plt.legend('numpy' , 'python')
# plt.show()

import numpy as np
from random import randint
age_diff = [randint(-100,200) for i  in range(400)]
indics = {}
for i in range(len(age_diff)):
    lists = indics.get(i%5,[])
    lists.append(age_diff[i])
    indics[i%5] = lists






