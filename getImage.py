# -*- coding: utf-8 -*-    
#---------------------------------------    
#   程序：网页图片抓取  
#   作者：lqf    
#   日期：2013-08-10    
#   语言：Python 2.7    
#   功能：抓取网页jpg链接图片  
#---------------------------------------    
import re  
import string  
import sys  
import os  
import urllib  

url="http://tieba.baidu.com/p/2521298181"#这个是某贴吧地址  
imgcontent=urllib.urlopen(url).read()#抓取网页内容  
urllist=re.findall(r'src="(http.+?\.jpg)"',imgcontent,re.I)#提取图片链接  
if not urllist:  
    print 'not found...'  
else:  
    #下载图片,保存在当前目录的pythonimg文件夹下  
    filepath=os.getcwd()+'\pythonimg'  
    if os.path.exists(filepath) is False:  
        os.mkdir(filepath)  
    x=1  
    print u'爬虫准备就绪...'  
    for imgurl in urllist:  
        temp= filepath + '\%s.jpg' % x  
        print u'正在下载第%s张图片' % x  
        print imgurl  
        urllib.urlretrieve(imgurl,temp)  
        x+=1  
    print u'图片下载完毕，保存路径为'
    print filepath 