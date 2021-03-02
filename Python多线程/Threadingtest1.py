# -*- coding: UTF-8 -*-

import threading
import time
import urllib.request


class myThread (threading.Thread):
    def __init__(self, threadID, start_num, end_num):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.start_numA = start_num
        self.end_numA = end_num


    def run(self):
        print("开始线程:"+str(self.threadID))


# 创建新线程
# thread1 = myThread(1, 1, 1000)
thread2 = myThread(2, 1001, 2000)
thread3 = myThread(3, 2001, 3000)
thread4 = myThread(4, 3001, 4000)
thread5 = myThread(5, 4001, 5000)
thread6 = myThread(6, 5001, 6000)
thread7 = myThread(7, 6001, 7000)
thread8 = myThread(8, 7001, 8000)
thread9 = myThread(9, 8001, 9000)
thread10 = myThread(10, 9001, 9999)


# 开启新线程
# thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()

# thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
thread10.join()


print ("退出主线程")