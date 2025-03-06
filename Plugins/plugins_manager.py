#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/30 下午9:02 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : plugins_manager.py
# @desc : README.md

import tkinter as tk
from tkinter import ttk
from importlib import util
import inspect
from pathlib import Path
from Plugins.plugins_base import BasePlugin


class PluginManager:
    """插件管理器"""

    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        """加载插件"""

        plugins_dir = Path(__file__).parent / "plugins"
        for file in plugins_dir.glob("*.py"):
            # 遍历所有文件，跳过以_开头的文件
            if file.name.startswith("_"):
                continue

            # 构建插件名称
            module_name = f"plugins.{file.stem}"
            try:
                spec = util.spec_from_file_location(module_name, file)
                if spec is None:
                    continue

                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 查找继承BasePlugin的类
                for _, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, BasePlugin) and cls != BasePlugin:
                        # 实例化满足要求的类，将其存储在字典中
                        plugin = cls()
                        if plugin.name not in self.plugins:  # 避免重复加载
                            self.plugins[plugin.name] = plugin

            except Exception as e:
                print(f"Error loading plugin {file.name}: {e}")


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.content_frame = None
        self.plugin_var = None
        self.title("IED插件系统")
        self.geometry("800x600")

        # 初始化插件管理器
        self.plugin_mgr = PluginManager()

        # 创建主界面
        self.create_widgets()

    def create_widgets(self):
        # 顶部控制栏
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # 插件选择
        self.plugin_var = tk.StringVar()
        plugins = list(self.plugin_mgr.plugins.keys())
        plugin_selector = ttk.Combobox(
            control_frame,
            textvariable=self.plugin_var,
            values=plugins
        )
        plugin_selector.pack(side=tk.LEFT, padx=5)

        # 加载按钮
        load_btn = ttk.Button(
            control_frame,
            text="加载插件",
            command=self.load_selected_plugin
        )
        load_btn.pack(side=tk.LEFT)

        # 内容展示区域
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def load_selected_plugin(self):
        # 清空现有内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # 获取选中插件
        plugin_name = self.plugin_var.get()
        if not plugin_name:
            return

        plugin = self.plugin_mgr.plugins.get(plugin_name)
        if plugin:
            plugin.activate(self.content_frame)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
