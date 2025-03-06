#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/20 下午4:20 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : actuator_c.py
# @desc : README.md

from subprocess import Popen, PIPE
from threading import Thread

from queue import Empty
from os import getcwd

from disposition.ActuatorTemplate import ActuatorTemplate


class ActuatorC(ActuatorTemplate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 初始化bat文件
        self.bat_path = self.get_bat_path()
        self.write_bat()

    def get_bat_path(self):
        path = "\\".join(getcwd().split('\\')[:-1])
        path += "\\disposition\\c\\run.bat"
        return path

    def write_bat(self):
        file_name = self.script_path[:-2]

        bat_text = rf"""gcc -c {file_name}.c -o {file_name}.o
gcc {file_name}.o -o {file_name}.exe
{file_name}.exe"""

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
            encoding="ISO-8859-1"
        )

        def read_stream(stream, stream_type):
            """读取子进程的输出流（stdout 或 stderr）"""

            # 如果子进程任在运行
            while process.poll() is None:
                output = stream.read()
                # output = stream.readline()
                output = output.encode("ISO-8859-1").decode("utf-8")
                if output:
                    self._receiver(f"{output.strip()}\n")

                else:

                    break  # 流已关闭

        # 启动输出读取线程
        stdout_thread = Thread(target=read_stream, args=(process.stdout, "stdout"), daemon=True)
        stderr_thread = Thread(target=read_stream, args=(process.stderr, "stderr"), daemon=True)
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

