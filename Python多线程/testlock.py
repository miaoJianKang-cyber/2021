# -*- coding: UTF-8 -*-
# 两个线程访问同一个数据，这个数据不会错乱

import threading
import time

money = 0
def Order(n):
    global money
    money = money + 1
    return money

class thread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name='线程' + threadname)
        self.threadname = int(threadname)

    def run(self):
        for i in range(20):
            lock.acquire()
            print(self.name,Order(self.threadname))
            lock.release()
            time.sleep(1)
#        print('%s:Now timestamp is %s'%(self.name,time.time()))

for i in range(0,10):
    print(Order(1))



lock = threading.Lock()

t1 = thread('1')
t2 = thread('5')
t1.start()
t2.start()
t1.join()
t2.join()
print(money)
