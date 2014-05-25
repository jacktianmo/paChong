#encoding=utf-8
import re
import time
import urllib.request
import urllib
import _thread
import time
import mysql
import mysql.connector
from datetime import datetime
#----------- 处理页面上的各种标签 -----------
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex=re.compile('((\t|\n| |<a.*?>|<img.*?>))')
    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex=re.compile('<.*?>')
    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex=re.compile('<p.*?>')
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")
    # 将一些html的符号实体转变为原始符号
    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]

    def Replace_Char(self,x):
      x = self.BgnCharToNoneRex.sub("",x)
      x = self.BgnPartRex.sub("\n    ",x)
      x = self.CharToNewLineRex.sub("\n",x)
      x = self.CharToNextTabRex.sub("\t",x)
      x = self.EndCharToNoneRex.sub("",x)

#----------- 处理页面上的各种标签 -----------


#----------- 加载处理糗事百科 -----------
     
class HTML_Model:  
      
    def __init__(self):  
        self.page = 1  
        self.pages = []  
        self.myTool = HTML_Tool()  
        self.enable = False  
  
    # 将所有的段子都扣出来，添加到列表中并且返回列表  
    def GetPage(self,page):
        myUrl = "http://m.qiushibaike.com/hot/page/" + page
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            }
        req=urllib.request.Request(url=myUrl,headers=headers)
        myResponse=urllib.request.urlopen(req)
        myPage=myResponse.read()
        #encode的作用是将unicode编码转换成其他编码的字符串  
        #decode的作用是将其他编码的字符串转换成unicode编码  
        unicodePage = myPage.decode("utf-8")  
        # 找出所有class="content"的div标记  
        #re.S是任意匹配模式，也就是.可以匹配换行符
        r=re.compile('<div.*?class="content".*?title="(.*?)">(.*?)</div>',re.DOTALL)
        myItems = r.findall(unicodePage)  
        items = []  
        for item in myItems:  
            # item 中第一个是div的标题，也就是时间  
            # item 中第二个是div的内容，也就是内容  
            items.append([item[0].replace("\n",""),item[1].replace("\n","")])#试着修改
            #print(item[0],item[1],'\n')
        return items  
  
    # 用于加载新的段子  
    def LoadPage(self):  
        # 如果用户未输入quit则一直运行  
        while self.enable:  
            # 如果pages数组中的内容小于2个  
            if len(self.pages) < 2:  
                try:  
                    # 获取新的页面中的段子们  
                    myPage = self.GetPage(str(self.page))  
                    self.page += 1  
                    self.pages.append(myPage)
                    #print('loadPage',self.page)
                except:  
                    print ('无法链接糗事百科！\n')  
            else:  
                #print('休眠\n')
                time.sleep(1)  
                  
    def ShowPage(self,np,page):
        for items in np:  
            print (items[0]) 
            #print (self.myTool.Replace_Char(items[1]))
            conn=mysql.connector.connect(user='root',database='young',password='dhu@123')
            cur=conn.cursor()
            form='%Y-%m-%d %H:%M:%S'
            cur.execute("insert into qiushibaike(datetime,content) values ( %s,%s)",(items[0],items[1]))
            print(items[1][:])   #'%r' 原样输出。
            cur.close()
            conn.commit()   #记得commit事务
            conn.close()
            
            #myInput = input()  
            #if myInput == "quit":  
            #    self.enable = False  
             #   break  
          
    def Start(self):  
        self.enable = True  
        page = self.page  
  
        print (u'正在加载中请稍候......')  
          
        # 新建一个线程在后台加载段子并存储  
        _thread.start_new(self.LoadPage,())
        
          
        #----------- 加载处理糗事百科 -----------  
        while self.enable:  
            # 如果self的page数组中存有元素  
            if self.pages:  
                nowPage = self.pages[0]
                #print(len(nowPage))
                del self.pages[0]
                print(u'第%d页' % page,'*'*26)
                self.ShowPage(nowPage,page)
                print(u'第%d页结束' % page,'*'*26,'\n')
                myInput = input()  
                if myInput == "quit":  
                        self.enable = False  
                        break  
                page += 1  
  
  
#----------- 程序的入口处 -----------  
print (u""" 
--------------------------------------- 
   程序：糗百爬虫 
   版本：0.1 
   作者：young 
   日期：2014-05-14 
   语言：Python 3.3 
   操作：输入quit退出阅读糗事百科 
   功能：按下回车依次浏览今日的糗百热点 
--------------------------------------- 
""" ) 
  
  
print (u'请按下回车浏览今日的糗百内容：'  )
input('')  
myModel = HTML_Model()  
myModel.Start()
