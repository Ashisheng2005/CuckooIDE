#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/4/2 下午2:49 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : PluginBox.py
# @desc : README.md

from tkinter import *
from Plugins.plugins_manager import PluginManager


class PluginBox(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.plug_name = "ollama服务端"       # 用这个测试
        self.plug_function = None
        self.plugins = PluginManager().load_plugins()

    def update_plug_name(self, new_name: str) -> None:
        self.plug_name = new_name

    def get_all_plug(self) -> dict:
        """获取全部插件映射表"""

        return self.plugins

    def restart(self, *args, **kwargs) -> None:
        """重启插件系统"""

        # 先结束原插件
        self.deactivate()
        # 重新加载新插件
        self.activate(*args, **kwargs)

    def activate(self, *args, **kwargs) -> None:
        """启动插件，附带启动参数"""
        if self.plug_name:
            self.plug_function = self.plugins[self.plug_name]
            self.plug_function.activate(*args, **kwargs)

    def deactivate(self) -> None:
        if self.plug_function:
            self.plug_function.deactivate()



