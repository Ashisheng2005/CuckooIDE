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
from disposition.ActuatorTemplate import ActuatorTemplate


class ActuatorPy(ActuatorTemplate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def thread_monitoring(self):

        process = Popen(
            # 启动无缓冲模式
            ["python", "-u", self.script_path],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            bufsize=1,  # 行缓冲
            universal_newlines=True,
            encoding="utf-8"
        )

        def read_stream(stream, stream_type):
            """读取子进程的输出流（stdout 或 stderr）"""

            # 如果子进程任在运行
            while process.poll() is None:
                output = stream.read()
                # output = stream.readline()
                if output:
                    self._receiver(f"{output.strip()}\n")

                else:

                    break  # 流已关闭

        # 启动输出读取线程
        stdout_thread = Thread(target=read_stream, args=(process.stdout, "stdout"),
                               daemon=True)
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
