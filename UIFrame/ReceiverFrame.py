#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/13 下午7:48 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ReceiverFrame.py
# @desc : README.md

from tkinter import *

from UIComponents.ReceiverText import ReceiverText
from UIComponents.RoundedCornerButton import RoundedButton


class ReceiverFrame(Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.master = master
        # 对于这个控件，通常出书隐藏状态，所以存在一个状态属性，创建时将其设置为True
        self.state = True

        self.root_frame = Frame(self.master)

        self.receiver_frame = Frame(self.root_frame)
        self.receiver = ReceiverText(self.receiver_frame)
        self.placement()

    def remember_frame(self):
        self.root_frame.pack(fill=BOTH, expand=True)

    def forget_frame(self):
        self.root_frame.pack_forget()

    def insert(self, index, chars, *args):
        """接管最底层控件的插入函数，和执行器的调用同步"""

        self.receiver.receiver_insert(index, chars, *args)

    def delete(self, *args, **kwargs):
        """清空"""
        self.receiver.clear_text(*args, **kwargs)

    def get_input(self, *args):
        """触发input函数执行获取用户输入"""

        return self.receiver.receiver_input(*args)

    def placement(self):
        self.receiver_frame.pack(fill=BOTH, expand=True)
        self.root_frame.pack(fill=BOTH, expand=True)
        # self.receiver.pack(fill=BOTH, expand=True)


if __name__ == '__main__':
    root = Tk()
    ReceiverFrame(root)

    root.mainloop()
