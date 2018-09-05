# coding=utf-8
from threading import Thread
from time import sleep
import json


class HookThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.message = "模拟驱动启动"

    def print_message(self, strdate):
        print(self.message, strdate)

    def run(self):
        print("程序开始运行。。。")
        x = 0
        while x < 100:
            self.print_message(str(x))
            sleep(0.0001)
            x += 1
        print("程序运行结束")


print("行情进程开启")
MainRun = HookThread()
MainRun.start()
print("行情进程终止")
