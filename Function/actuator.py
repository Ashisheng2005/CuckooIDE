#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/12 下午7:47 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : actuator.py
# @desc : README.md

import time

from subprocess import Popen, PIPE
from threading import Thread, Event

from queue import Queue, Empty

try:
    from sys import path as sys_path
    sys_path.append("..")

    # python文件执行器
    from disposition.py.actuator_py import ActuatorPy
    from disposition.c.actuator_c import ActuatorC
    from disposition.java.actuator_java import ActuatorJava

except FileNotFoundError as error:
    print(f"File not find:{error}")


class Actuator:
    """分类执行器"""

    def __init__(self, script_path, receiver_widget):
        # 执行文件目录
        self.script_path = script_path
        # 接受返回结果控件id
        self.receiver_widget = receiver_widget
        # 对应文件的执行器
        self.file_actuator = None
        # 启动分类器对文件类型分类
        self.classifier(file_name=self.script_path)

    def classifier(self, file_name: str):
        """文件类型分类器"""
        actuator_dict = {'py': ActuatorPy,
                         'c': ActuatorC,
                         'java': ActuatorJava
                         }

        for suffix in actuator_dict.keys():
            if file_name.endswith(suffix):
                self.file_actuator = actuator_dict[suffix]
                break

    def run(self):

        if self.file_actuator:

            test = self.file_actuator(self.script_path, self.receiver_widget)
            test.run()

        else:
            print(self.script_path)


