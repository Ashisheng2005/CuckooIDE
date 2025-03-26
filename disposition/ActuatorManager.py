#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/3/26 上午8:56 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ActuatorManager.py
# @desc : README.md

from pathlib import Path
from importlib import util
from inspect import getmembers, isclass
from os import listdir, getcwd, path
from disposition.ActuatorTemplate import ActuatorTemplate


def getActuatorSuffix(key=None, path_ = None):
    if not path_:
        path_ = getcwd()
    # 自动检测插件并生成字典

    load_actuators = {}

    for _ in listdir(path_):
        if not path.isfile(_):
            actuator_dir = Path(__file__).parent / _
            for file in actuator_dir.glob("*.py"):
                # 遍历所有文件，跳过以_开头的文件
                if file.name.startswith("_"):
                    continue

                    # 构建插件名称
                module_name = f".{_}"
                try:
                    spec = util.spec_from_file_location(module_name, file)
                    if spec is None:
                        continue

                    module = util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # 查找继承ActuatorTemplate的类
                    for _, cls in getmembers(module, isclass):
                        # print(_, cls)
                        if issubclass(cls, ActuatorTemplate) and cls != ActuatorTemplate:
                            # 实例化满足要求的类，将其存储在字典中
                            plugin = cls()
                            if plugin.suffix not in load_actuators:  # 避免重复加载
                                load_actuators[plugin.suffix] = _

                except Exception as e:
                    print(f"Error loading plugin {file.name}: {e}")

    return load_actuators if not key else load_actuators.keys()


if __name__ == '__main__':
    print(getActuatorSuffix())