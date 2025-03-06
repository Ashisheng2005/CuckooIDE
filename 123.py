#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/2/24 下午10:06 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : SyntaxOn_plugin.py
# @desc : README.md

import re
from tkinter import *
from json import loads, dumps
from Plugins.plugins_base import BasePlugin


def read_resources(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = loads(f.read())

    return data


class SyntaxOnPlugin(BasePlugin):
    """针对文本编辑框的语法高亮和跨级操作插件"""

    def __init__(self, widget: Text, keyword_path=None, syntax_path=None):
        self.text = widget
        self.keyword_path = keyword_path
        self.syntax_path = syntax_path
        # 如果两个文件有一个不存在，则关闭渲染模式
        self.rendering_mode = True if self.keyword_path and self.syntax_path else False
        # 如果存在资源文件，加载文件内容
        if self.rendering_mode:
            self.keyword = read_resources(self.keyword_path)
            self.syntax = read_resources(self.syntax_path)

        self.activate()

    @property
    def name(self) -> str:
        return "语法高亮和快捷填充"

    @property
    def version(self) -> str:
        return "1.0"

    def configure_tags(self):
        if self.rendering_mode:
            # 配置颜色标签
            for item in self.syntax.keys():
                self.text.tag_configure(item, foreground=self.syntax[item])

    # 该函数通常弃用，对于text的键盘事件调用冗余api绑定self.delay_highlight函数
    def bind_events(self):
        self.text.bind('<KeyRelease>', self.delay_highlight)

    def delay_highlight(self, event=None):
        self.text.after(300, self.highlight_syntax)

    def highlight_syntax(self):
        # 删除旧标签
        for item in self.syntax.keys():
            self.text.tag_remove(item, '1.0', 'end')

        # 获取文本内容
        full_text = self.text.get("1.0", END)

        # 定义正则表达式和对应的标签
        patterns = [
            (rf'{self.keyword["lineComment"]}.*?$', "lineComment", re.MULTILINE),
            (r'("(?:\\.|[^"\\])*")|(\'(?:\\.|[^\'\\])*\')', "string", re.MULTILINE),
            (r'\b(0x[0-9a-fA-F]+|0b[01]+|\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?\b', "number", re.MULTILINE),
            (r'\b(' + '|'.join(map(re.escape, self.keyword['keyword'])) + r')\b', "keyword",
             re.MULTILINE | re.IGNORECASE),
            (r'\b(' + '|'.join(map(re.escape, self.keyword['function'])) + r')\b', "function",
             re.MULTILINE | re.IGNORECASE),
            (r'\b(' + '|'.join(map(re.escape, self.keyword['builtins'])) + r')\b', "builtins",
             re.MULTILINE | re.IGNORECASE),
            (r'\b(' + '|'.join(map(re.escape, self.keyword['string_properties'])) + r')\b', "string_properties",
             re.MULTILINE | re.IGNORECASE),
        ]

        # 遍历每个正则表达式
        for pattern, tag, flags in patterns:
            regex = re.compile(pattern, flags)
            for match in regex.finditer(full_text):
                if match.group():

                    self._apply_tag(match, tag)

    def _apply_tag(self, match, tag_name):
        start = f"1.0 + {match.start()}c"
        end = f"1.0 + {match.end()}c"
        print(f"Matched {tag_name}: {match.group()}")
        self.text.tag_add(tag_name, start, end)

    def activate(self, rows: str = None) -> bool:
        # self.bind_events()
        self.configure_tags()
        return True

    def deactivate(self) -> bool:
        self.text.unbind('<KeyRelease>')
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, "1.0", END)
        return True


if __name__ == "__main__":
        root = Tk()
        root.title("Python IDE")
        text = Text(root)
        sy = SyntaxOnPlugin(text, r"E:\IDE\disposition\py\keyword.json", r"E:\IDE\disposition\py\Syntax.json")
        text.bind("<KeyRelease>",sy.delay_highlight )
        text.pack(expand=True, fill='both')
        root.mainloop()