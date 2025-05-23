#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/16 下午6:23 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ToolTip.py
# @desc : README.md

import tkinter as tk
from tkinter import ttk


class ToolTip:
    """控件注释标签"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """鼠标进入控件范围执行函数"""

        # 首相执行控件自带的动画
        self.widget.mouse_enter(event)

        # 获取绝对位置
        x, y, _, _ = self.widget.bbox("insert")

        # 设置偏移量
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        """鼠标离开控件范围执行函数"""

        # 首相执行控件自带的动画
        self.widget.mouse_leave(event)

        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


if __name__ == '__main__':
    root = tk.Tk()
    button = ttk.Button(root, text="Hover over me")
    button.pack(pady=20)

    tooltip = ToolTip(button, "This is a tooltip")

    root.mainloop()