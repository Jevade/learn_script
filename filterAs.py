# -*- coding:utf-8 -*-  
import math,struct
from PIL import Image
import numpy as np
PI=3.1415926535
pi=PI
def readTsk(filename):
    (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)=(None,None,None,None,None,None,None,None,None)
    fileTsk=open(filename)
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
     
def loadAndFilter(pathorign):
    (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)=readTsk()
    for i in range(0,TotalFrames):
        strNum=str('%04.0d' % i)
        path=pathorign+'BMP Conversion\proj_'+strNum+'.bmp'
        
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
def FBPSLFilter(L):
    
    
    S_L_Filter=[0 for x in range(1+2*L)]
    R_L_Filter=[0 for x in range(1+2*L)]
    d=float(1)
    for n in range(0,(2*L+1)):
        if divmod((n-L),2)[1]==0:
            R_L=0
        else:
            R_L=(-1)/(math.pi*math.pi*d*d*(n-L)*(n-L))
        R_L_Filter[n]=R_L
        
        
        S_L=(-2)/(math.pi*math.pi*d*d*(4*(n-L)*(n-L)-1))
        S_L_Filter[n]=S_L        
    R_L_Filter[L]=1.00/(4*d*d)
    
    return S_L_Filter
    
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
    pathorign
    (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)=readTsk()
    imgNew=Image.new('L', (Prj_ROI_width,TotalFrames))
    simodeNum=Prj_ROI_height/2
    for i in range(0,TotalFrames):
        if i%1==1:
            continue
        print(i)
        strNum=str('%04.0d' % i)
        path=pathorign+'BMP Conversion\proj_'+strNum+'.bmp'
        img = Image.open(path)
        
        for x in range(0,Prj_ROI_width):
            imgNew.putpixel((x,i), img.getpixel((x,simodeNum)))
        img.close()        
            
    #imgNew.show()
    imgNew.save(pathorign+'sigmod'+str(simodeNum)+'.png','PNG')
    return imgNew


def filterFBP(pathorign):
    (FDD,PixelSize,TotalFrames,Prj_ROI_width,Prj_ROI_height,ROI_offset_z,ROI_offset_x,Focus_z,Focus_x)=readTsk()    
    simodeNum=Prj_ROI_height/2    
    try:
    #image=scipy.io.loadmat(pathorign+'newdata.mat')
        image=Image.open(pathorign)
    except:
        image=createFBP()  
    L=64
    
    
    SLFilter=FBPSLFilter(L)
    Rrow,Rcol=image.size
    print()
    
    lists = [[0 for x in range(Rrow+2*L)] for i in range(Rcol)]
    pixel = [[0 for x in range(Rrow)] for i in range(Rcol)]
    print(len(lists))
    
    for y in range(0,Rcol):
        print(y)
        for x in range(0,Rrow+2*L):
            if x<L:
                a=(image.getpixel((0,y))+image.getpixel((1,y)))*0.5#
            elif x<Rrow+L:
                a=image.getpixel((x-L,y))
            else:
                a=(image.getpixel((Rrow-2,y))+image.getpixel((Rrow-1,y)))*0.5                
            lists[y][x]=a
            
    print(image.size)
    
    for y in range(0,int(Rcol)):
        print('filte'+str(y)+'th row')
        for x in range(0,int(Rrow)):
            for m in range(0,2*L+1):
                pixel[y][x]=pixel[y][x]+SLFilter[m]*lists[y][m+x]
            image.putpixel((x,y),(int(pixel[y][x]),))
    #image.show()
    image.save(pathorign+'filter.png','PNG')
    image.show()
    return image
def FBPRecon(pathorign): 
 
    try:
        #image=scipy.io.loadmat(pathorign+'newdata.dat')
        image=Image.open(pathorign) 
        print('good')
    except:
        image=filterFBP()
    Rrow,Rcol=image.size
    #Rcol,Rrow=image.size
    temp=CalFFTWidth(round(Rrow/1.414)-20)
    row=temp
    col=temp
    sin=[]
    cos=[]
    offset=math.floor(Rrow/2)+1
    delta=2*pi/Rcol
    n_view=Rcol
    lists = [[] for i in range(Rcol)]
    imgNew=Image.new('L', (row,col))
    I_rec=[[0 for x in range(row)] for y in range(col)]
    for theta in range(0,Rcol):
        rad=theta*delta
        si=math.sin(rad)
        co=math.cos(rad)
        #if theta%30==0:
            #imgNew.show()
        for j in range(0,row):
            for k in range(0,col):
                #if theta%30==0:
                    #print(I_rec[j][k])                
                print(j,k)
                j0=j-row/2
                k0=k-col/2
                xr=j0*co+k0*si+offset
                xr_n=math.floor(xr)
                xr_m=xr_n+1
                R1=image.getpixel((xr_n,theta))
                R2=image.getpixel((xr_m,theta))
                temp=(R2-R1)/(xr_m-xr_n)*(xr-xr_n)+R1               
                I_rec[j][k]=I_rec[j][k]+temp/Rcol
                k1=int(I_rec[j][k])
                imgNew.putpixel((j,k),(k1,))                
    imgNew.save('reconLena.png','PNG')     









    
    
        
        
        
    