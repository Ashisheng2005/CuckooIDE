#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/4/2 下午10:13 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : PluginFrame.py
# @desc : README.md

from tkinter import *
from UIComponents.PluginBox import PluginBox


class PluginFrame(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.Plugin_frame_index = Frame(self.master)
        self.plug_object = PluginBox()
        self.plug_object.activate(self.Plugin_frame_index, width=300, height=500)
        self.Plugin_frame_index.pack(side=LEFT, fill=BOTH, expand=True)

    def set_plug(self, plug_name: str, *args, **kwargs) -> None:
        """设置插件属性"""

        # 更新插件名称
        self.plug_object.update_plug_name(plug_name)
        self.plug_object.activate(self.Plugin_frame_index, *args, **kwargs)


if __name__ == '__main__':
    demo = Tk()
    PluginFrame(demo)
    demo.mainloop()

