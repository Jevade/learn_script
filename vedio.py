#!/usr/bin/env python  
  
import numpy as np  
import cv2  
cap = cv2.VideoCapture(0)  
i = 0  
while( i < 18):  
    i = i+1  
    print(cap.get(i))  
  
ret = (3,320)  
ret = cap.set(4,240)  
  
#output info  
fourcc = cv2.VideoWriter_fourcc(*'XVID')  
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (320,240))  
while(cap.isOpened()):  
    ret, frame = cap.read()  
    if ret == True:  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
      
        out.write(frame)  
  
        cv2.imshow('image', gray)  
        k = cv2.waitKey(1)  
        if (k & 0xff == ord('q')):  
            break  
    else:  
        break  
  
cap.release()  
out.release()  
cv2.destroyAllWindows() 
