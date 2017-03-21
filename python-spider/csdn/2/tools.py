import time  
  
''''' 
自定义工具方法,tools.py 
'''  
  
  
def runTime(func):  
    '记录程序运行时间'  
  
    def newFunc(*args, **kwargs):  
        start = time.clock()  
        res = func(*args, **kwargs)  
        end = time.clock()  
        print("read: %f s" % (end - start))  
        return res  
  
    return newFunc  
  
  
def log(content, file='test.log', type=1):  
    if type == 1:  
        f = open(file, 'a+', encoding='utf-8')  
    else:  
        f = open(file, 'w+', encoding='utf-8')  
    f.write(content)  
