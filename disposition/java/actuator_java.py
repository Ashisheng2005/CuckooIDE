#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/20 下午9:33 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : actuator_java.py
# @desc : README.md

from os import getcwd
from subprocess import Popen, PIPE
from threading import Thread, Event

from queue import Queue, Empty
from disposition.ActuatorTemplate import ActuatorTemplate


class ActuatorJava(ActuatorTemplate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 初始化bat文件
        self.bat_path = self.get_bat_path()
        self.write_bat()

    def get_bat_path(self):
        path = "\\".join(getcwd().split('\\')[:-1])
        path += "\\disposition\\java\\run.bat"
        return path

    def splitting_paths(self, path):
        parent_path, file_name = "\\".join(path.split("\\")[:-1]) , path.split("\\")[-1]
        return parent_path, file_name

    def write_bat(self):
        # 这个是去除文件后缀的文件路径
        file_name = self.script_path[:-5]
        # 将文件父路径和文件名称拆分
        parent, filename = self.splitting_paths(file_name)

        bat_text = rf"""javac {file_name}.java
java -cp {parent} {filename}"""

        with open(self.bat_path, 'w', encoding='utf-8') as file:
            file.write(bat_text)

    def thread_monitoring(self):

        process = Popen(
            # 启动无缓冲模式
            [self.bat_path],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            # shell=True,
            text=True,
            bufsize=1,  # 行缓冲
            universal_newlines=True,
            encoding="utf-8"
        )

        def read_stream(stream, stream_type):
            """读取子进程的输出流（stdout 或 stderr）"""

            # 如果子进程任在运行
            while process.poll() is None:
                # output = stream.read()
                output = stream.readline()
                if output:
                    self._receiver(f"{output.strip()}\n")

                else:

                    break  # 流已关闭

        # 启动输出读取线程
        stdout_thread = Thread(target=read_stream, args=(process.stdout, "stdout"),
                               daemon=True)

        stderr_thread = Thread(target=read_stream, args=(process.stderr, "stderr"),
                               daemon=True)
        stdout_thread.start()
        stderr_thread.start()

        # 主线程处理输入
        while process.poll() is None:

            try:
                user_input = self.input_queue.get(timeout=0.1)
                process.stdin.write(user_input + "\n")
                process.stdin.flush()
                # 重置等待状态

            except Empty:

                if len(self.user_input) > 0:
                    self.send_input(self.user_input[0])
                    del self.user_input[0]

        # 等待输出线程结束
        stdout_thread.join()
        stderr_thread.join()

        # 确保子进程终止
        if process.poll() is None:
            process.terminate()
            process.wait()
