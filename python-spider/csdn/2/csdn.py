# -*- coding:utf-8 -*-  
#import urllib.request, http.cookiejar, re
import urllib.request, http.cookiejar
import time  
import threading  
# tools是我的自定义工具类  
import tools  
  
''''' 
模拟访问博客增加访问量 
'''  
  
  
class Csdn(threading.Thread):  
    'csdn增加访问量'  
    headers = [('host', 'blog.csdn.net'),  
               ('User-Agent',  
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101'),
               ]  
    domain = 'http://blog.csdn.net'  
    url = 'http://blog.csdn.net/%s/article/list/%s'  
  
    def __init__(self, username, page):  
        threading.Thread.__init__(self)  
        self.username = username  
        self.createOpener()  
        self.page = page  
 
    @staticmethod  
    def getListPages(username):  
        '获取总页数'  
        Csdn.headers.append(('Referer', 'http://blog.csdn.net/' + username))  
        cookie = http.cookiejar.CookieJar()  
        cookieProc = urllib.request.HTTPCookieProcessor(cookie)  
        opener = urllib.request.build_opener(cookieProc)  
        opener.addheaders = Csdn.headers  
        url = Csdn.url % (username, 1)  
        response = opener.open(url)  
        contents = contents = response.read().decode('utf-8', 'ignore')  
        pattern = r'<div id="papelist" class="pagelist">([\s\S]*?)共(\d+)页'  
        match = re.search(pattern, contents)  
        pages = int(match.group(2))  
        return pages  
  
    def createOpener(self):  
        cookie = http.cookiejar.CookieJar()  
        cookieProc = urllib.request.HTTPCookieProcessor(cookie)  
        opener = urllib.request.build_opener(cookieProc)  
        opener.addheaders = Csdn.headers  
        self.opener = opener  
  
    def visitUrl(self):  
        '访问列表页获取内容'  
        opener = self.opener  
        url = Csdn.url % (self.username, self.page)  
        response = opener.open(url)  
        self.contents = contents = response.read().decode('utf-8', 'ignore')  
        self.addVisitNum()  
  
    def addVisitNum(self):  
        opener = self.opener  
        contents = self.contents  
        divPattern = r'<div id="article_list" ([\s\S]*)<div id="papelist" class="pagelist">'  
        ulMatch = re.search(divPattern, contents)  
        divText = ulMatch.group(1)  
        smallPattern = r'<div class="list_item article_item">([\s\S]*?)<span class="link_title"><a href="(.*?)">([\s\S]*?)</a></span>([\s\S]*?)阅读</a>(\d+)'  
        match = re.findall(smallPattern, divText)  
        for i in match:  
            list = {'url': Csdn.domain + i[1], 'name': i[2].strip(), 'num': i[4]}  
            opener.open(list['url'])  
            print(self.page, list['url'])  
  
    def run(self):  
        '线程主方法'  
        self.visitUrl()  
 
 
@tools.runTime  
def main():  
    '主方法'  
    # csdn昵称  
    #username = 'digyso888'  
    username = 'ygtlovezf'  
    pages = Csdn.getListPages(username)  
    threads = []  
    for page in range(1, pages + 1):  
        thread = Csdn(username, page)  
        thread.start()  
        threads.append(thread)  
    # 等待所有线程完成  
    for t in threads:  
        t.join()  
    print("退出主线程")  
  
  
if __name__ == '__main__':  
    main()  
