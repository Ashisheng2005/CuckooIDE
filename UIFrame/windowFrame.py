#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/23 下午8:00 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : windowFrame.py
# @desc : README.md

from tkinter import *
from sys import path as sys_path
sys_path.append("..")

from EditFrame import EditFrame
from UIComponents.RoundedCornerButton import RoundedButton
from ReceiverFrame import ReceiverFrame
from ToolFrame import ToolFrame


class WindowFrame(Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.root = Frame(self.master)

        self.root.pack(side=LEFT, fill=BOTH, expand=True)

        self.receive = Frame(self.root)
        self.receive_frame = ReceiverFrame(self.receive)

        self.edit = Frame(self.root)
        self.edit_frame = EditFrame(self.edit, receiver_widget=self.receive_frame)

        self.tool = Frame(self.master)
        self.tool_Frame = ToolFrame(self.tool)

        self.remember_button = RoundedButton(
            self.tool_Frame.root,
            text=' - ',
            radius=30,
            width=30,
            height=30,
            command=self.set_receive_frame,
            select_foreground='#FFFFFF'
        )

        self.run_status = RoundedButton(
            self.tool_Frame.root,
            image=[r"..\resources\stop.png","../resources/run.png"],
            radius=30,
            width=30,
            height=30,
            command=self.set_run_status,
            select_foreground='#FFFFFF'
        )
        self.placement()

    def placement(self):
        self.edit_frame.pack(fill=BOTH, expand=True)
        self.edit.pack(fill=BOTH, expand=True)
        self.receive.pack(fill=BOTH, expand=True)
        self.tool_Frame.add_command(self.remember_button, "运行")
        self.tool_Frame.add_command(self.run_status, "状态")
        self.tool.pack(fill=Y, expand=True)

    def forget_frame(self):
        self.receive_frame.forget_frame()
        self.receive.pack_forget()
        self.receive_frame.state = False

    def remember_frame(self):
        self.receive_frame.remember_frame()
        self.receive.pack(fill=BOTH, expand=True)
        self.receive_frame.state = True

    def set_receive_frame(self):

        # 如果状态为真，则表示当前处于显示状态
        if self.receive_frame.state:
            self.forget_frame()

        else:
            self.remember_frame()

    def set_run_status(self): ...


if __name__ == '__main__':
    demo = Tk()
    frame = WindowFrame(demo)
    demo.mainloop()
