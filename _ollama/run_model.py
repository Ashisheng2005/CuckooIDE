#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/26 下午10:07 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : run_model.py
# @desc :

import ollama
import asyncio
from os import system

from sys import path as sys_path
sys_path.append("..")
from Function.ErrorType import *

class ollamaClient:

    def __init__(self, IOobject=None):
        self.model_name = "llama3.1:latest"
        self.role = "user"
        self.character_setting = """
        请记住，你叫尤尼卡，是一个计算机辅系统，当你收到需要编写代码的任务后，你仅需使用纯文本的方式回答代码部分，其他语言都省略掉。
        """
        self.IOobjext = IOobject

    def list_model(self):
        data = ollama.list()
        models = []
        for i in data['models']:
            models.append(i['model'])

        return models

    def self_test(self):
        if self.model_name == "":
            models = self.list_model()
            system(f"ollama run {models[0]}")
            self.model_name = models[0]

    def chat(self, text:str):

        stream = ollama.generate(
            stream=True,
            model=self.model_name,
            prompt=text,
        )

        try:
            for chunk in stream:
                if not chunk['done']:
                    if self.IOobjext:
                        self.IOobjext(chunk['response'])

                    else:
                        print(chunk['response'], end='', flush=True)

                else:
                    print()

        except Exception as error:
            raise ConnectError("ollama服务疑似未启动，请检查服务启动项", error)


if __name__ == '__main__':
    client = ollamaClient()
    # client.list_model()
    while True:
        proment = input(">>>")
        if proment == "exit":
            break

        client.chat(proment)
