#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/14 下午8:04 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ToolFrame.py
# @desc : README.md

from tkinter import *

from UIComponents.ToolTip import ToolTip


class ToolFrame(Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.root = Frame(self.master)
        self.placement()

    def placement(self):
        self.root.pack(fill=Y, expand=True)

    def add_command(self, widget, tip=None):
        widget.pack()
        if tip:
            ToolTip(widget, tip)

        self.master.update()
        # RoundedButton(
        #     self.root,
        #     text=text,
        #     command=command,
        #
        # )


if __name__ == '__main__':
    demo = Tk()
    root = Frame(demo)
    frame_root = ToolFrame(root)
    test = Button(root, text="测试")
    frame_root.add_command(test)
    root.pack()
    demo.mainloop()