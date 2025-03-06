#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/21 下午6:24 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : EditFrame.py
# @desc : README.md
import os

from tkinter import Tk, Frame, Button, LEFT, BOTH, CHAR
from os import path as os_path
from pathlib import Path as pathlib_path
from threading import Thread
from UIComponents.EditText import EditText
from UIComponents.NotBook import NotBook
from UIComponents.ConvenienceMenu import ConvenienceMenu
from UIComponents.DirectoryTree import DirectoryTree
from Function import UIFunction
from Function.actuator import Actuator
try:
    from Plugins.plugins.SyntaxOn_plugin import SyntaxOnPlugin
except FileNotFoundError as error:
    print(error)


def _image_file(file_name):
    suffix = file_name.split(".")[-1]
    if suffix == 'py':
        return r"..\resources\python.png"

    elif suffix == 'c':
        return r"..\resources\c.png"

    elif suffix == 'java':
        return r"..\resources\java.png"


def _resources_file(file_name):
    suffix = file_name.split(".")[-1]
    if suffix == 'py':
        return r"..\disposition\py\keyword.json", r"..\disposition\py\Syntax.json"

    elif suffix == 'c':
        return r"..\disposition\c\keyword.json", r"..\disposition\c\Syntax.json"

    elif suffix == 'java':
        return r"..\disposition\java\keyword.json", r"..\disposition\c\Syntax.json"


class EditFrame(Frame):

    def __init__(self, master, receiver_widget=None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        # edit注册表 结构画像: List( Tuple( Text_width_Name, file_Name, file_path, frame_id ), ... )
        self.Edit_table = []
        # 初始化执行器变量
        self.actuator = None
        # 向下传递的接收器
        self.receiver_widget = receiver_widget
        # 初始状态的edit框架
        frame_1 = Frame(self.master)
        frame_1.pack(side=LEFT, fill=BOTH)
        # 标签页控件
        self.not_book = NotBook(self.master)
        frame_2 = self.not_book.get_frame()
        # frame_2.pack()
        # 目录框显示文件, path=父路径 E:\IDE
        self.Dir_Tree = DirectoryTree(frame_1, path=pathlib_path(os.getcwd()).parent)
        # 绑定双击事件
        self.Dir_Tree.tree.bind('<Double-Button-1>', self.add_edit_frame)
        # 标签右双击取消(会自动保存文件
        self.not_book.user_bind_command = self.not_book_table_select
        # self.not_book.bind('<Double-Button-3>', self.not_book_table_select)

        # 编辑框
        self.Text = EditText(frame_2, file_name='Main.py')
        # 挂载语法插件
        _kw, _sy = _resources_file("Main.py")
        sy = SyntaxOnPlugin(self.Text.Text, _kw, _sy)
        # 因为事件触发函数过多，启用冗余api
        self.Text.key_release_command = sy.highlight_syntax
        # 绑定
        self.not_book.add(frame_2, text="Main.py", height=2, image_file=_image_file("Main.py"))
        # 注册信息
        self.Edit_table.append((self.Text.Text, "Main.py", None, frame_2))
        # 工具库初始化, 必须存在一条注册信息才能初始化成功
        self.ui_function = UIFunction.UIFunction(Edit_table=self.Edit_table)
        # 为初始化edit挂载menu
        self.mount_edit_menu(frame_2, self.Text)
        # 显示挂载
        self.placement()

    def add_edit_frame(self, event):
        path = self.Dir_Tree.select_file(event)
        # 如果不是文件，则不执行
        if not os_path.isfile(path):
            return

        # 如果文件已经打开，焦点聚焦
        for _path in self.Edit_table:
            if _path[2] == path:
                self.not_book.select(_path[3])
                return

        # 挂载edit
        file_name = os_path.basename(path)
        frame_current = self.not_book.get_frame()
        text = EditText(frame_current, file_name=file_name)
        text.pack()
        # 挂载语法插件
        _kw, _sy = _resources_file(file_name)
        sy = SyntaxOnPlugin(text.Text, _kw, _sy)
        # 同上，调用冗余api
        text.key_release_command = sy.highlight_syntax
        # 为edit挂载menu
        self.mount_edit_menu(frame_current, text)
        # 挂载frame
        self.not_book.add(frame_current, text=file_name + " ", image_file=_image_file(file_name))
        # 注册控件信息
        self.Edit_table.append((text.Text, file_name, path, frame_current))
        # 焦点聚焦
        self.not_book.select(frame_current)

        # 读取文件，显示在edit中
        text.insert('end', UIFunction.get_file_text(file_path=path))
        sy.highlight_syntax()

    def mount_edit_menu(self, frame_id, edit_id):
        # 右击菜单栏
        text_menu = ConvenienceMenu(frame_id, tearoff=False)
        text_menu.add_command(label='粘贴', accelerator='Ctrl+V')
        text_menu.add_command(label='回滚', accelerator='Ctrl+H')
        text_menu.add_command(label='重构', accelerator='Ctrl+R')
        text_menu.add_separator()
        text_menu.add_command(label=f'运行\'{edit_id.text_file_name}\'',
                              accelerator='Ctrl+Shift+F10',
                              command=self.run_file
                              )
        text_menu.add_command(label='调试', accelerator='Ctrl+D')
        text_menu.show_menu(edit_id.Text)

    def run_file(self):
        # 获取选择对象id
        current = self.not_book.select()
        tab_id = self.not_book.index(current)
        # 保存文件内容, 接受返回状态
        saving_state = self.ui_function.ui_save_file(tab_id)
        if not saving_state:
            self.receiver_widget.insert('end', f'Save File Error:{self.Edit_table[tab_id][1]}')

        # 初始化一个执行器
        self.actuator = Actuator(self.Edit_table[tab_id][2], self.receiver_widget)
        # self.actuator.run()
        run = Thread(target=self.actuator.run, daemon=True)
        run.start()

    def all_file_save(self):
        """全体文件保存函数, 所有文件都保存"""

        for i in range(len(self.Edit_table)):
            self.ui_function.ui_save_file(i)

    def not_book_table_select(self, savefile=True):
        """通过坐标判断是否触发点在标签上，如果在，则消除标签, 因为tab_id和注册表顺序保持一致，所哟可以通用"""
        # 获取选择对象id
        tab_id = self.not_book.table_find(self.not_book.select_id)

        if savefile:
            # 保存文件内容, 接受返回状态
            saving_state = self.ui_function.ui_save_file(tab_id)
            if not saving_state:
                return 'break'

        else:
            return 'break'

        # 删除注册表记录
        del self.Edit_table[tab_id]

    def placement(self):
        self.Dir_Tree.pack(side=LEFT)
        self.Text.pack()

        self.not_book.pack(fill=BOTH, expand=True)


if __name__ == '__main__':
    demo = Tk()
    edit_Frame = EditFrame(demo)
    edit_Frame.pack()

    demo.mainloop()
