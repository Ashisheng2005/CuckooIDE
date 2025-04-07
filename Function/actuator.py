#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/12 下午7:47 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : actuator.py
# @desc : README.md

try:
    from sys import path as sys_path
    sys_path.append("..")

    # python文件执行器
    from disposition.py.actuator_py import ActuatorPy
    from disposition.c.actuator_c import ActuatorC
    from disposition.java.actuator_java import ActuatorJava
    from disposition.cpp.actuator_Cpp import ActuatorCpp

except FileNotFoundError as error:
    print(f"File not find:{error}")


class Actuator:
    """分类执行器"""

    def __init__(self, script_path=None, receiver_widget=None, controller=True):
        # 执行文件目录
        self.script_path = script_path
        # 接受返回结果控件id
        self.receiver_widget = receiver_widget
        # 线程控制器
        self.controller = controller

        # 对应文件的执行器
        self.file_actuator = None
        # 线程池
        self.thread_pool = {}

        # 启动分类器对文件类型分类
        if self.script_path:
            self.classifier(file_name=self.script_path)

    def set_script_path(self, script_path):
        self.script_path = script_path

    def classifier(self, file_name: str):
        """文件类型分类器"""
        self.script_path = file_name
        print(f"act: {file_name}")

        actuator_dict = {'py': ActuatorPy,
                         'c': ActuatorC,
                         'java': ActuatorJava,
                         'cpp': ActuatorCpp
                         }

        for suffix in actuator_dict.keys():
            if file_name.endswith(suffix):
                # 根据后缀匹配执行器
                self.file_actuator = actuator_dict[suffix]
                break

    def run(self):

        if self.file_actuator:
            test = self.file_actuator(self.script_path, self.receiver_widget, self.controller)
            test.run()

            # _test = Thread(target=test.run, daemon=True)
            # self.thread_pool[self.script_path] = _test
            # _test.start()

        else:
            ...
            # 这里可以添加日志
            # print(self.script_path)

    def stop_thread(self, file_name):
        test = self.thread_pool[file_name]


