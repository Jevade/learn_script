# encoding=utf8  

import requests
import re
def getcontent(url):
	r=requests.get(url)
	return r.content.decode("utf8")
	re.combile
print(getcontent("http://www.baidu.com?"))