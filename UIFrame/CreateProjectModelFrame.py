#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/3/1 下午10:28 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : CreateProjectModelFrame.py
# @desc : README.md
from tkinter import *


class CreateProject(Frame):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.frame_root = Frame(self)

    def draw(self):
        # project name frame
        project_name = Frame(self.frame_root)
        Label(project_name, text="项目名称")


        # project path frame
        project_path = Frame(self.frame_root)


