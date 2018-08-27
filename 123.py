#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
learning.py

Usage:

python3 learning.py
'''
import math
from functools import reduce
class Deque:
    """模拟双端队列"""
    items = []
    def __init__(self):
        self.items = []
    def back(self):
        return self.items[-1]
    def front(self):
        return self.items[0]
    def isEmpty(self):
        return self.items == []

    def addBack(self, item):
        self.items.append(item)

    def addFront(self, item):
        self.items.insert(0, item)

    def removeBack(self):
        return self.items.pop()

    def removeFront(self):
        return self.items.pop(0)

    def getItem(self,n):
        return self.items[n-1]
        
    def size(self):
        return len(self.items)
    def value(self):
        return self.items


def quicksort(a, s, e):
    i = s
    j = e
    # m=a[s]
    m = a[e]
    temp = 0
    while i < j:
        while i < j and a[i] <= m:
            i = i + 1
        a[j] = a[i]

        while i < j and a[j] >= m:
            j = j - 1
        a[i] = a[j]

    a[j] = m
    if (s < i - 1):
        quicksort(a, s, i - 1)
    if (e > i + 1):
        quicksort(a, i + 1, e)

class DOT():
    x=0
    y=0
    z=0
    def __init__(self,x=x,y=y,z=z):
        self.x = x
        self.y = y
        self.z = z
def dis(a,b):
    if a and b:
        return abs(a.x-b.x)+abs(a.y-b.y)++abs(a.z-b.z)
    else:
        return 10

def printdot(dot):
    if isinstance(dot,list):
        for d in dot:
            print(d.x,d.y)
    if isinstance(dot,DOT):
        print(d.x,d.y)
def dotPlus(d1,d2):
    sum=DOT()
    sum.x=d1.x+d2.x
    sum.y=d1.y+d2.y
    sum.z = d1.z + d2.z
    return sum
def dotDived(d,n):
    sum=DOT()
    sum.x=d.x/n
    sum.y=d.y/n
    sum.z = d.z / n
    return sum
def showDict(dict):
    for k,v in dict.iteritems():
        if v[0]:
            plt.plot([d.x for d in v[0]], [d.y for d in v[0]], "o")

    pass
if __name__ == "__main__":
    import sys, random
    a1 = DOT(random.randint(-100, 200), random.randint(-100, 200))
    a2 = DOT(random.randint(-100, 200), random.randint(-100, 200))
    a3 = DOT(random.randint(-100, 200), random.randint(-100, 200))
    a4 = DOT(random.randint(-100, 200), random.randint(-100, 200))



    import sys,random
    # name = int(sys.stdin.readline().strip())
    # line = sys.stdin.readline().strip()
    # x_s = list(map(int, line.split()))
    # line = sys.stdin.readline().strip()
    # y_s = list(map(int, line.split()))
    x_s=[]
    y_s =[]
    for x in range(100):
        x_s.append(random.randint(-100, 100))
        y_s.append(random.randint(-100, 100))
    for x in range(100):
        x_s.append(random.randint(50, 100))
        y_s.append(random.randint(-100, -50))

    import matplotlib.pyplot as plt



    dot_list=[]
    map(lambda x,y,z:dot_list.append(DOT(x,y,z)),x_s,y_s,y_s)

    import copy

    old_center_list = []

    n=300
    k=20
    center_list=[DOT(x_s[random.randint(0, 50)],y_s[random.randint(0, 50)] )for x in range(k)]

    dict={center_list[i]:([],i) for i in range(len(center_list))}
    id =0
    import time
    while id<100:
        # if  reduce(lambda x,y:x and y, [len(dict[dot][0])<n for dot in center_list]):
        #     new_dict={}
        #     for dot_in in range(len(center_list)):
        #         v=dict[center_list[dot_in]]
        #         center_list[dot_in]=dot_list[random.randint(0, 50)]
        #         new_dict[center_list[dot_in]] = v
        #     dict=copy.deepcopy(new_dict)

        dis_center=reduce(lambda x,y:x+y,map(lambda x,y:dis(x,y),center_list,old_center_list))
        print(dis_center)
        if dis_center<1:
            break
        dict = {center_list[i]: ([], i) for i in range(len(center_list))}
        old_center_list = copy.deepcopy(center_list)
        for d_d in dot_list:
            dis_list=[]
            for j in range(len(center_list)):
                dot_dis=dis(d_d, center_list[j])
                dis_list.append((dot_dis, j))

            dis_list=sorted(dis_list,key=lambda x:x[0])

            dict[center_list[dis_list[0][1]]][0].append(d_d)

        new_dict = {}
        for k,v in dict.iteritems():
            if not v[0]:
                new_dict[k]=v
                center_list[v[1]] = k
                continue
            dot_sum=DOT()
            for d in v[0]:
                dot_sum =dotPlus(dot_sum,d)
            c=dotDived(dot_sum,len(v[0]))
            new_dict[c]=v
            center_list[v[1]]=c

        dict = new_dict

        printdot(center_list)
        plt.plot([d.x for d in center_list ],[d.y for d in center_list ],"rx")
        showDict(dict)
        plt.show()
        id+=1

    printdot(center_list)
    showDict(dict)
    plt.show()





def maxGap(li):
    quicksort(li, 0, len(li)-1)
    a=Deque()
    b=Deque()
    for i in li:
        a.addFront(i)
    print(a.value())

    b.addBack(a.removeFront())

    while not a.isEmpty() and a.size()>3 :
        k1=a.removeBack()
        k2=a.removeBack()
        k3=a.removeFront()
        k4=a.removeFront()

        b.addFront(min([k1, k2]))
        b.addFront(max([k3, k4]))
        b.addBack(max([k1, k2]))
        b.addBack(min([k3, k4]))
    if a.size()>1:
        k1=a.removeBack()
        k2=a.removeBack()
        #if(abs(k1-a.back())>k2-a.front()):

        b.addFront(min([k1, k2]))
        b.addBack(max([k1, k2]))

    print(b.value())
    if a.size()==1:
        k1 = a.removeBack()
        print(k1,b.front(),b.back())
        if abs(k1-b.front())>=abs(k1-b.front()) :
            b.addBack(k1)
        else:
            b.addFront(k1)

    print(b.value())
    li2 =b.value()
    sum = 0

    for i in range(len(li2) - 1):
        sum += abs(li2[i] - li2[i + 1])
    print(sum)


