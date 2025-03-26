#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/12 下午8:16 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ReceiverText.py
# @desc : README.md

from tkinter import *
from tkinter.scrolledtext import ScrolledText


class ReceiverText(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.receiver_text = ScrolledText(self.master, height=15, font=("consolas", 11))
        self.receiver_input_list = []  # 存储用户输入内容
        self.last_content = ""  # 记录上一次的内容用于比较变化

        # 绑定事件
        self.receiver_text.bind('<KeyRelease>', self.user_input)  # 改为KeyRelease更适合检测粘贴
        self.receiver_text.bind('<Control-v>', self.handle_paste)  # 专门处理粘贴事件

        # 方向键快速定位输入内容，暂时停用
        # self.command_history = []
        # self.history_index = -1
        # self.receiver_text.bind('<Up>', self.show_prev_command)
        # self.receiver_text.bind('<Down>', self.show_next_command)

        self.placement()

    # def show_prev_command(self, event):
    #     if self.command_history and self.history_index < len(self.command_history) - 1:
    #         self.history_index += 1
    #         self.clear_text()
    #         self.receiver_text.insert('1.0', self.command_history[self.history_index])
    #     return "break"
    #
    # def show_next_command(self, event):
    #     if self.command_history and self.history_index < len(self.command_history) - 1:
    #         self.history_index -= 1
    #         self.clear_text()
    #         self.receiver_text.insert('1.0', self.command_history[self.history_index])
    #     return "break"

    def receiver_insert(self, index, chars, *args):
        """接受输出流"""
        self.receiver_text.insert(index, chars, *args)
        self.receiver_text.see('end')

    def get_current_content(self):
        """获取当前全部内容"""
        return self.receiver_text.get('2.0', 'end-1c')  # -1c去掉末尾换行符

    def handle_paste(self, event):
        """
        处理Ctrl+V粘贴事件，确保正确捕获多行内容
        参数:
            event: tkinter 事件对象，包含粘贴相关的上下文信息
        返回:
            "break" - 阻止默认粘贴行为，由我们自定义处理
        """
        try:
            # 获取剪贴板内容
            clipboard_content = self.master.clipboard_get()

            # 如果剪贴板为空，直接返回
            if not clipboard_content:
                return "break"

            # 清空当前选中内容（如果有的话）
            if self.receiver_text.tag_ranges("sel"):
                self.receiver_text.delete("sel.first", "sel.last")

            # 获取当前插入点位置
            insert_pos = self.receiver_text.index("insert")

            # 插入剪贴板内容到当前光标位置
            self.receiver_text.insert(insert_pos, clipboard_content)

            # 更新 last_content 以保持内容跟踪一致
            self.last_content = self.get_current_content()

            # 处理多行内容
            lines = clipboard_content.split('\n')
            # 过滤空行并去除首尾空白
            processed_lines = [line.strip() for line in lines if line.strip()]

            # 将处理后的行添加到输入列表
            if processed_lines:
                self.receiver_input_list.extend(processed_lines)
                # 本次站贴处理后的数组
                # print(f"Pasted lines: {processed_lines}")

            # 自动滚动到最后
            self.receiver_text.see('end')

            # 延迟处理后续逻辑，确保界面更新完成
            self.master.after(50, self.process_input)

        except TclError:
            # 处理剪贴板为空或无法访问的情况
            print("Clipboard is empty or inaccessible")

        except Exception as e:
            # 捕获其他潜在错误
            print(f"Error in handle_paste: {e}")

        # 返回 "break" 阻止默认粘贴行为
        return "break"

    def user_input(self, event):
        """处理用户输入"""
        current_content = self.get_current_content()

        if event.keysym == 'Return':  # 回车键
            lines = current_content.split('\n')
            new_input = [line.strip() for line in lines if line.strip()]
            if new_input:
                self.receiver_input_list.extend(new_input)
                print(f"Current input list: {self.receiver_input_list}")

        self.last_content = current_content

    def process_input(self):
        """处理输入内容"""
        current_content = self.get_current_content()
        if current_content != self.last_content:
            lines = current_content.split('\n')
            new_input = [line.strip() for line in lines if line.strip()]
            self.receiver_input_list.extend(new_input)
            self.last_content = current_content
            print(f"Pasted content added: {new_input}")

    def receiver_input(self):
        """获取输入流"""
        self.receiver_text.see('end')
        if self.receiver_input_list:
            data = self.receiver_input_list.copy()
            self.receiver_input_list.clear()
            return data
        return None

    def clear_text(self, index1='1.0', index2='end'):
        """清空text内容"""
        self.receiver_text.delete(index1, index2)
        self.last_content = ""
        self.receiver_input_list.clear()

    def placement(self):
        self.receiver_text.pack(fill=BOTH, expand=True)


if __name__ == '__main__':
    root = Tk()
    app = ReceiverText(root)
    root.mainloop()



# class ReceiverText(Frame):
#
#     def __init__(self, master, *args, **kwargs):
#         super().__init__(master=master, *args, **kwargs)
#
#         self.receiver_text = ScrolledText(self.master, height=15, font=("consolas", 11))
#
#         # 默认模式为只读
#         # self.receiver_text['state'] = "disabled"
#         # 绑定回车，当触发回车的时候，获取改行内容，即为input输入内容
#         # self.receiver_text.bind('<Return>', self.get_input_data)
#         self.receiver_text.bind('<KeyRelease>', self.user_input)
#
#         # 用来存放用户输入内容
#         self.receiver_input_list = []
#         # 换行后需要剔除的前缀
#         self.prefixes = ""
#
#         self.placement()
#
#     def receiver_insert(self, index, chars, *args):
#         """接受输出流"""
#
#         # self.receiver_text['state'] = "normal"
#         self.receiver_text.insert(index, chars, *args)
#         # self.receiver_text['state'] = "disabled"
#         # 自动滚动到最后一行
#         self.receiver_text.see('end')
#         return
#
#     def get_line_text(self):
#         row, column = self.receiver_text.index('insert').split('.')
#         text = self.receiver_text.get(row + ".0", 'end')
#         return text
#
#     def user_input(self, event):
#
#         if not self.prefixes:
#             self.prefixes = self.get_line_text()
#
#         # windows 和 linux 下可能不同，13 36
#         if event.keycode == 13:
#             text = self.get_line_text()
#             self.receiver_input_list.append(text.strip(self.prefixes + '\n'))
#             self.prefixes = ""
#             print(self.receiver_input_list)
#
#     def get_input_data(self, event):
#         row, column = self.receiver_text.index('insert').split('.')
#         # text = self.receiver_text.get(row+".0", f'{row}.{column}')
#         text = self.receiver_text.get("2.0", f'{row}.{column}')
#         self.receiver_input_list = text.strip()
#
#     def receiver_input(self, *args):
#         """触发输入流"""
#         # self.receiver_text['state'] = "normal"
#         self.receiver_text.see('end')
#         while True:
#             if self.receiver_input_list:
#                 data = self.receiver_input_list
#                 self.receiver_input_list = ""
#                 # self.receiver_text['state'] = "disabled"
#                 return data
#
#     def clear_text(self, index1='0.0', index2='end'):
#         # 清空text内容
#
#         self.receiver_text.delete(index1, index2)
#
#     def placement(self):
#         self.receiver_text.pack(fill=BOTH, expand=True)
#
#
# if __name__ == '__main__':
#     root = Tk()
#     ReceiverText(root)
#     root.mainloop()

