#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/4/3 下午6:25 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ollama_plugin.py
# @desc : README.md

from tkinter import *
from os import system
from ollama import generate
from ollama import list as ollama_list
from Plugins.plugins_base import BasePlugin
from Function.ErrorType import NotFindModel, ModelStartError, ConnectError
from threading import Thread


class OllamaFrame(Frame):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master=master)
        self.master = master
        self.model_text = Text(self.master)
        self.model_name = "qwen2.5:7b" if not kwargs.get("model_name", False) else kwargs["model_name"]
        self.role = "user"
        self.character_setting = """你好， 我需要你的帮助！ """
        self.interaction_frame()

    def list_model(self):
        """获取所有可选的模型名称"""

        data = ollama_list()
        models = []
        for i in data['models']:
            models.append(i['model'])

        return models

    def acquiesce_model(self) -> bool:
        """如果没有指定模型，则调用模型第一位"""

        if self.model_name == "":
            try:
                models = self.list_model()
                if len(models) < 1:
                    raise NotFindModel("可用模型列表为空，请下载模型后检查配置再启动")

                system(f"ollama run {models[0]}")
                print("start ollama model")
                self.model_name = models[0]

            except Exception as error:
                raise ModelStartError(f"模型启动失败，请检查系统环境以及ollama配置[{error}]")

        return True

    def interaction_frame(self):
        """交互frame"""

        self.model_text.pack(fill=BOTH, expand=True)
        use_text = Text(self.master, height=1)
        use_text.pack(fill=Y)

        use_text.bind("<Control-Return>", lambda event: self.submit(use_text))

    def submit(self, widget: Text):
        self.thread_chat(widget.get('0.0', 'end'))
        widget.delete('0.0', 'end')

    def thread_chat(self, text: str):
        """以多线程的方式启动chat功能"""

        Thread(target=self.chat, kwargs={'text': text}, daemon=True).start()

    def chat(self, text: str) -> None:
        """交互，循环读取输出流"""

        if not self.model_text:
            self.acquiesce_model()

        self.model_text.insert('end', f">>> {text.strip()}\n")

        stream = generate(
            stream=True,
            model=self.model_name,
            prompt=text,
        )

        try:
            for chunk in stream:
                if not chunk['done']:
                    self.model_text.insert('end', chunk['response'])
                    self.model_text.see('end')

                else:
                    self.model_text.insert('end', "\n")

        except Exception as error:
            raise ConnectError("ollama服务疑似未启动，请检查服务启动项", error)


class OllamaPlugin(BasePlugin):

    def __init__(self):
        self.ollama_frame = None

    @property
    def name(self) -> str:
        return "ollama服务端"

    @property
    def version(self) -> str:
        return "1.0"

    def activate(self, frame: Frame, *args, **kwargs) -> None:
        OllamaFrame(frame, *args, **kwargs)

    def deactivate(self) -> None:
        self.ollama_frame.end()
        self.ollama_frame.destroy()


if __name__ == '__main__':
    from tkinter import Tk, Frame

    demo = Tk()
    f_text = Frame(demo)
    Debugging = OllamaPlugin()
    Debugging.activate(f_text)
    f_text.pack(fill=BOTH, expand=True)
    demo.mainloop()


