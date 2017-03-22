# -*- coding: utf-8 -*-
####################################################
# coding by 刘云飞
####################################################
import requests
import re
import time
import random
from random import choice

ips = []
blog_ads = []

with open('ip.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        ip_one = line.strip()
        ips.append(ip_one)

#with open('blogdizhi.txt', 'r', encoding='utf-8') as f2:
with open('blogdizhi.txt', 'r',) as f2:
    lines = f2.readlines()
    line_num = len(lines)
    pag = 0
    for line in lines:
        pag += 1
        if pag % 2 == 0:
            ads = line.strip()
            #blog_ads.append(ads)
        else:
            ads = line.strip()

        blog_ads.append(ads)

headers = {
    'Host': 'blog.csdn.net',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/42.0',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    #'Referer': 'http://www.google.com',
    'Referer': 'http://blog.csdn.net/ygtlovezf?viewmode=list',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

i = 0
j = 0
while i < 500:
    blog = random.choice(blog_ads)
    ip_i = random.choice(ips)
    proxies = {'http': ip_i}
    print(blog)
    print(proxies)
    i += 1
    print("now trying " + str(i) + ',failed ' + str(j))
    sleep_time = random.randint(5, 10)
    print('------>sleep ' + str(sleep_time) + " s")
    time.sleep(sleep_time)
    session = requests.session()
    try:
        #response = session.get(blog, headers=headers, proxies=proxies)
        response = session.get(blog, headers=headers)
        str_code = response.status_code
        print('>>>>>' + str(str_code))
        if str_code > 200:
            j += 1
    except:
        print('time out')
        j += 1
        pass
    session.close()
