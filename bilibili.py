import requests
from bs4 import BeautifulSoup
from functools import reduce
def gethtml(url):
    html=requests.get(url).text
    return html
def getComments(url):
    html=gethtml(url)
    soup=BeautifulSoup(html)
    p_s=soup.findAll("d")
    test=reduce(lambda x,y:x+"\n"+y,map(lambda s:s.text,p_s))
    return test
if __name__=="__main__":
    url=u"https://comment.bilibili.com/27045762.xml"
    print(getComments(url))
    



