#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/30 下午8:08 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : live2d_plugin.py
# @desc : README.md

import os.path
import tkinter as tk

from OpenGL.GL import *
from pyopengltk import OpenGLFrame
from pyautogui import position
from os import path
import live2d.v3 as live2d

from sys import path as sys_path
sys_path.append("..")

from plugins_base import BasePlugin


class MyOpenGLFrame(OpenGLFrame):

    def __init__(self, *args, model_path=False, **kwargs):

        self.live2d_model_path = model_path

        OpenGLFrame.__init__(self, *args, **kwargs)
        # 相对路劲调整
        parent_path = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
        # 构建到live2d下的相对路劲
        self.live2d_dir = path.join(parent_path, 'live2d')
        # 识别live2d的模型路径
        if not self.live2d_model_path:
            self.live2d_dir_join(r"米塔\\3.model3.json")

        else:
            self.live2d_dir_join(self.live2d_model_path)

        self.global_coordinates = True
        self.MAPP = round(200 / 980, 2)
        self.model = None

    @classmethod
    def on_start_callback(cls, group: str, no: int):
        """动作开始触发事件"""

        print(f"touched and motion [{group}_{no}] is started")

    @classmethod
    def on_finish_callback(cls):
        """动作结束调用函数"""

        print("motion finished")

    @classmethod
    def end(cls):
        """结束之后的资源释放事件"""

        live2d.dispose()

    def touch(self):
        """被点击事件"""

        print("被点击")
        x, y = 100, 100
        self.model.Touch(x, y, self.on_start_callback, self.on_finish_callback)
        self.model.StartMotion("LipSync", 0, live2d.MotionPriority.FORCE)

    def live2d_dir_join(self, model_path):
        """模型路径的更新"""

        self.live2d_model_path = path.join(self.live2d_dir, model_path)

    def coordinate_compression(self):
        """坐标压缩函数，将UI内，live2dframe外的坐标压缩为frame内地映射坐标"""

        screen_x, screen_y = position()
        y = screen_y - self.winfo_rooty()

        if y > 160:
            y *= 0.2

    def initgl(self):
        """初始化"""

        self.animate = 1
        live2d.init()
        live2d.setLogEnable(False)
        live2d.glewInit()

        self.model = live2d.LAppModel()
        if live2d.LIVE2D_VERSION == 2:
            # print(self.live2d_model_path)
            self.model.LoadModelJson(self.live2d_model_path)

        else:
            self.model.LoadModelJson(self.live2d_model_path)

        self.model.Resize(self.width, self.height)

    def _live2d_(self):
        """live2d模型的相关设置"""

        screen_x, screen_y = position()
        x = screen_x - self.winfo_rootx()
        y = screen_y - self.winfo_rooty()
        # sleep(0.02)
        live2d.clearBuffer()
        self.model.Update()
        self.model.Drag(x, y)
        self.model.Draw()

    def redraw(self):
        """重绘，刷新时调用"""

        glClear(GL_COLOR_BUFFER_BIT)
        self._live2d_()


class Live2dPlugin(BasePlugin):
    """live2d和LLM集成环境的插件接口"""

    def __init__(self):
        self.live2d_frame = None

    @property
    def name(self) -> str:
        return "live2d集成环境"

    @property
    def version(self) -> str:
        return '1.0'

    def activate(self, frame: tk.Frame, **kwargs) -> None:
        self.live2d_frame = MyOpenGLFrame(frame, **kwargs)
        self.live2d_frame.pack()

    def deactivate(self) -> None:
        self.live2d_frame.end()
        self.live2d_frame.destroy()


if __name__ == '__main__':
    from tkinter import Tk, Frame

    demo = Tk()
    frame = Frame(demo)
    frame.pack()
    Debugging = Live2dPlugin()
    Debugging.activate(frame, width=1000, height=1000)
    demo.mainloop()
