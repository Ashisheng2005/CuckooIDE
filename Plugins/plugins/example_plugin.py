#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/30 下午8:01 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : example_plugin.py
# @desc : README.md

import tkinter as tk
from Plugins.plugins_base import BasePlugin


class DemoPlugin(BasePlugin):

    def __init__(self):
        self.label = None
        self.btn = None

    @property
    def name(self):
        return "示例插件"

    @property
    def version(self) -> str:
        return "1.0"

    def activate(self, frame):
        self.label = tk.Label(frame, text="这是一个示例插件！")
        self.label.pack(pady=20)

        self.btn = tk.Button(
            frame,
            text="点击测试",
            command=lambda: print("插件功能被触发")
        )
        self.btn.pack()

    def deactivate(self) -> None:
        self.label.destroy()
        self.btn.destroy()
