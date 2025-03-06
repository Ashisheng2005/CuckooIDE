#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/16 下午12:48 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : MainFrame.py
# @desc : README.md

try:
    from sys import path as sys_path

    # 添加组件路径，跳至上一级目录
    sys_path.append("..")
    from UIComponents import ConvenienceMenu
    from UIComponents import DirectoryTree
    from UIComponents import OpenGLFrame
    from Function import UIFunction
    from Function import ErrorType

    # 内置库
    from tkinter import Tk, Frame

except Exception as error:
    print("MainFrameError:", error)
