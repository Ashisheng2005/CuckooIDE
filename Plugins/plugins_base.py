#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/30 下午7:59 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : plugins_base.py
# @desc : README.md

from abc import ABC, abstractmethod
import tkinter as tk


class BasePlugin(ABC):
    """插件基类，后续所有插件都必须继承该类，才能够被正确识别"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    # 生命周期方法
    @abstractmethod
    def activate(self, frame: tk.Frame) -> None:
        """插件激活时调用"""
        pass

    @abstractmethod
    def deactivate(self) -> None:
        """插件停用时调用"""
        pass

    # 可选扩展方法
    def on_config_load(self, config: dict):
        """加载配置时调用"""
        pass

    def on_config_save(self) -> dict:
        """保存配置时调用"""
        return {}
