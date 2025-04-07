#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/21 下午12:02 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ActuatorTemplate.py
# @desc : README.md

# from subprocess import Popen, PIPE
# from threading import Thread, Event

from queue import Queue
from abc import abstractmethod


class ActuatorTemplate:
    """执行器模板"""

    def __init__(self, script_path=None, receiver_widget=None, controller=True):
        # 执行文件目录
        self.script_path = script_path
        # 接受返回结果控件id
        self.receiver_widget = receiver_widget
        # 线程锁, 为False 终止执行, 线程控制器
        self.thread_lock = controller
        # 占用线程
        self.thread_current = None
        # 不同执行器占用后缀
        self.suffix = None
        if self.receiver_widget:
            # 用户输入的列表
            self.user_input = self.receiver_widget.receiver.receiver_input_list

        # 用于线程间通信的队列
        self.input_queue = Queue()

    def _receiver(self, data: str):
        self.receiver_widget.insert('end', data)
        # Thread(target=self.receiver_widget.insert, args=('end', data), daemon=True).start()

    def _receiver_input(self, *args):
        data = self.receiver_widget.get_input()
        return data

    def receive_init(self, text=None):
        """每一次运行时候，都对receive控件内容进行初始化"""

        # 清空
        self.receiver_widget.delete()
        # 插入提示文字
        self._receiver(text)

    @property
    @abstractmethod
    def thread_monitoring(self):
        """线程监控，具体执行文件的Popen方法再次实现"""
        pass

    @property
    @abstractmethod
    def get_suffix(self) -> str:
        pass

    def run(self):
        """根据不同语言编写不同的执行器"""
        self.receive_init(f"{self.__class__.__name__}  {self.script_path}\n")
        self.thread_monitoring()
        self._receiver('\n\n进程已结束\n')

    def send_input(self, user_input: str):
        # 将用户输入压住队列
        self.input_queue.put(user_input)