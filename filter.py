# -*- coding:utf-8 -*-  
import math,struct
from PIL import Image
import numpy as np
PI=3.1415926535


def readTsk():
    (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)=(None,None,None,None,None,None,None,None,None)
    path='F:\\data\\config.tsk'
    fileTsk=open(path)
    try:
        Tsk = fileTsk.readlines()
    finally:
        fileTsk.close()
    for line in Tsk:
        if line.startswith('FDD='):
            m=line[len('FDD='):-1]
            if FDD==None:
                FDD=float(m)
        elif line.startswith('Pixel Size='):
            m=line[len('Pixel Size='):]
            PixelSize=float(m) 
        elif line.startswith('Total Frames='):
            m=line[len('Total Frames='):]
            if TotalFrames==None:
                TotalFrames=int(m)            
        elif line.startswith('Prj_ROI_width='):
            m=line[len('Prj_ROI_width='):]
            Prj_ROI_width=int(m)            
        elif line.startswith('Prj_ROI_height='):
            m=line[len('Prj_ROI_height='):]
            Prj_ROI_height=int(m)           
        elif line.startswith('ROI_offset_z='):
            m=line[len('ROI_offset_z='):]
            ROI_offset_z=int(m)            
        elif line.startswith('ROI_offset_x='):
            m=line[len('ROI_offset_x='):]
            ROI_offset_x=int(m)           
        elif line.startswith('Focus_z='):
            m=line[len('Focus_z='):]
            Focus_z=int(m)
        elif line.startswith('Focus_x='):
            m=line[len('Focus_x='):]
            Focus_x=int(m)           
        else:
            pass
    return (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)
     
def loadAndFilter():
    (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)=readTsk()
    pathorign='F:\data\BMP Conversion\proj_'
    for i in range(0,1):
        strNum=str('%04.0d' % i)
        path=pathorign+strNum+'.bmp'
        
        print(path)
        #the formore is included and letter is excluded
        img = Image.open('F:\\image\\lena.bmp')
        print(img.format,img.size)
        imgNew=Image.new('I', img.size)
        Prj_ROI_width,Prj_ROI_height=img.size      
        maxPixelRow=0
        imageNew=[]
        temp=[]
        #for y in range(0,Prj_ROI_height):  
            
            #for x in range(0,Prj_ROI_width):        
                #tem=img.getpixel((x,y))
                #temp.append(tem)
                #print(tem)
                #maxPixelRow=maxPixelRow if (maxPixelRow>tem) else tem
            #if abs(maxPixelRow)<0.0001:
                    #return False
            #print('开始取对数')   
            #for x in range(0,Prj_ROI_width):
                #if temp[x]>0:
                    #value=math.log(maxPixelRow)-math.log(temp[x])
                    #print(value)
                    #temp1=value if value>0 else 0
                    #img.putpixel((x,y),(int(temp1),))       
                #else:
                    #img.putpixel((x,y),(0,))  
            #temp.clear() 
                
                
        imageFilter=filter(Prj_ROI_width, Prj_ROI_height, img)
        imageFilter.show()
        imageFilter.save('F:\data\Filter BMP\proj_'+strNum+'.png','PNG')
        
 
def createFilter(nWidth,nHight ,filter_kind):
#,Device_ID,frequency,nBart):
    d=1
    k=0
    if filter_kind==0 or filter_kind==1:
        h_SL_filter=[]
        band_width=int(nWidth/2)
        for i in range(-band_width,band_width):
            if filter_kind==1:
                h_SL=-2/ ( ( 4 * i * i - 1) * PI * PI * d * d )#SL
            else:#RL
                if i==0:
                    h_SL=1.0/(4 * d * d)
                elif i%2==0:
                    h_SL_filter=0
                else:
                    h_SL=-1.0/( i * i * PI * PI * d * d)
            k=k+1
            h_SL_filter.append(h_SL)
    return h_SL_filter
            
def CalFFTWidth(nWidth):
    k=0
    width_fft = 0
    while(pow(2.0,k)<nWidth):
        k+=1
    width_fft=int(pow(2.0,k))
    return width_fft
def readPNG():
    path="C:\\Users\\Public\\Pictures\\Sample Pictures\\remadeImage3.png"
    temp=open(path,'rb')
    rawdata=temp.read()
    print(rawdata[:100])
    
    
def filter(nWidth, nHight, image):    
    h_SL_filter=createFilter(nWidth, nHight, 1)
    width_temp=CalFFTWidth(nWidth)
    
    
    for x in range(0,nWidth):
        for y in range(0,nHight):
            print(x,y)
            tp=0.0
            for i in range(0,int(x)):                
                a=image.getpixel((i,y))
                tp +=h_SL_filter[x-i]*a            
            image.putpixel((x,y),(int(tp),))  
    return image
def createFBP():
    (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)=readTsk()
    pathorign='F:\data\BMP Conversion\proj_'
    imgNew=Image.new('L', (Prj_ROI_width,TotalFrames))
    frame=int(Prj_ROI_height/2)
    for i in range(0,TotalFrames):
        strNum=str('%04.0d' % i)
        path=pathorign+strNum+'.bmp'
        img = Image.open(path)       
        for x in range(0,Prj_ROI_width):
            imgNew.putpixel((x,i), img.getpixel((x,frame)))
        img.close()        
    imgNew.show()
    imgNew.save('sigmode'+str(frame),'bmp')
    
    
    
loadAndFilter()
#readPNG()









    
    
        
        
        
    