#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/18 下午5:51 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : UIFunction.py
# @desc : README.md

from os import getcwd
from tkinter import filedialog, Text

from chardet import detect

# 因为父级调用提升了路径，所以这里也同时提升
from Function.ErrorType import FilePathNotFind, ParametersNotFind


def _get_file_code(file_path):
    """ 获取文件的编码方案，为后续的文件操作，单独重写一个函数为了减少历史遗留问题"""

    if not file_path:
        raise FilePathNotFind("The type of the argument file_path cannot be <class 'NoneType'>")

    with open(file_path, "rb") as f:
        encoding = detect(f.read())['encoding']

    return encoding


def _get_bytecode_code(bytecode):
    """返回一段字节码的可能编码格式，如果无法识别，则默认cp936"""

    if not bytecode:
        return 'cp396'

    code_type = detect(bytecode)['encoding']
    return code_type if code_type else 'cp936'


def get_file_text(file_path):
    """获取指定文件的内容，与 _get_file_code一同完成"""

    with open(file_path, "r", encoding=_get_file_code(file_path)) as file:
        data = file.read()

    return data


def _save_file(file_path, file_txt):
    """保存文件内容"""

    try:
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(file_txt)

        return True

    except Exception as error:
        print(error)


def _find(parameters, text):
    pass


class UIFunction:

    def __init__(self, **kwargs):
        self.Edit_table = kwargs.get("Edit_table", None)
        self.TextSet = kwargs.get("TextSet", None)

        # 如果未传参
        if not self.Edit_table:
            raise ParametersNotFind("Parameters Not Find Error: 关键参数未找到[Edit_table]")

    def _file_from_path_index(self, file_id):
        """查询注册表中是否存在对应控件的注册信息"""

        for i in range(len(self.Edit_table)):
            if self.Edit_table[i] == file_id:
                return i

        return None

    def ui_find_text(self, table_id):
        """UI级别的查找函数"""

        pass

    def ui_save_file(self, table_id):
        """UI级别的保存函数，直接与UI中的控件相互绑定"""

        # 查找出对应的记录
        table_tuple = list(self.Edit_table[table_id])

        # 文件未选择保存路径
        if not table_tuple[2]:
            # 开启路劲选择对话框
            file_path = filedialog.asksaveasfilename(
                            title=u"保存文件", initialdir=getcwd(),
                            filetypes=[
                                ("Source files", [".py", ".c", ".asm", ".jar"]),
                                ("Text files", [".txt", ".ini", ".md"])
                            ],
                            initialfile=table_tuple[1]
                        )

            # 确认用户选择了文件路径
            if file_path:
                # 更新注册表信息
                table_tuple[2] = file_path
                self.Edit_table[table_id] = tuple(table_tuple)

            else:
                # 用户未选择具体的目录，跳出函数，不必保存
                return False

        # 路径部分处理完成后，则开始调用函数保存文件内容, 并返回执行结果状态
        return _save_file(file_path=table_tuple[2], file_txt=table_tuple[0].get('0.0', 'end'))

    def word_tab(self, widget: Text):
        """接管Tab模式，缩进自动使用自定义的数值"""

        widget.insert("insert", " " * self.TextSet["Tabs"])
        return "break"

    def path_loop_permutation(self):
        pass
