import re
import urllib.request
import time
#url=input('请输入网址\n')
url='http://www.dytt8.net/'
html=urllib.request.urlopen(url).read()
r=re.compile(r'<a href=\'(.*?)\'>(.*?)</a>')
#与上式的区别在与上式是得出一个数组！
#r=re.compile(r'<a href=\'.*?\'>.*?</a>')
#与上式的区别在与后面html不需装换格式，是binary格式，多了一个‘b’
#r=re.compile(rb'<a href=\'(.*?)\'>(.*?)</a>')
html=html.decode('GBK')
data=r.findall(html)
fp=open('D:/movie.txt','w+')
fp.write('*'*26+time.ctime()+'*'*26+'\n')
for x in data:
		fp.write('片子名：'+x[1]+'\n'+'网址：'+'http://www.dytt8.net'+x[0]+'\n\n')
fp.close()
print('已完成更新'+time.ctime())
input()
