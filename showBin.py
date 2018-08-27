#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import struct 
from numpy import * 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from PIL import Image

import os, sys
import sqlite3,random, time,threading
from tkinter import *
import tkinter.filedialog

def showBin(filename):
    f = open(filename, 'rb')#Fan_rebin_Filt_236
    f.seek(-12,2) 
    width=fromfile(f, np.int32,1)[0]
    height=fromfile(f, np.int32,1)[0]       
    f.seek(0,0) 
    a=np.memmap(filename, dtype=np.float32, shape=(height,width))
    #print(np.shape(a),a.max(),a.min())
    plt.imshow(a, cmap=plt.cm.gray)
    plt.show() 
class BIN():
    __fimename=''
    def loginSys(self):
        root=Tk()
        root.title("显示图像")
        def choose():
            filename=tkinter.filedialog.askopenfilename()
            showBin(filename)
        ButtonEnter = Button(root, text="查找", command=choose, bg="grey")
        ButtonEnter.grid(row=1, column=0)
        mainloop()
if __name__=='__main__':
    windows=BIN()
    windows.loginSys()       