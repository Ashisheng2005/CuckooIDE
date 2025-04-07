#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/16 下午8:37 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : DirectoryTree.py
# @desc : README.md


import os
import tkinter as tk
from tkinter import ttk, Menu
from tkinter.filedialog import askdirectory
from os import listdir
from os.path import basename, join, isdir, normpath
from functools import lru_cache


class DirectoryTree(ttk.Frame):
    def __init__(self, master, path, refresh_interval=10000):
        super().__init__(master)
        self.master = master
        self.path = normpath(path)
        self.refresh_interval = refresh_interval
        self.file_types = ['.py', '.c', '.asm', '.jar']

        # 使用 PanedWindow 来允许调整大小
        self.paned = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # 初始化Treeview框架
        self.tree_frame = ttk.Frame(self.paned)
        self.paned.add(self.tree_frame, weight=1)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # 初始化Treeview
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 初始化滚动条
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # 初始化上下文菜单
        self.context_menu = Menu(self.master, tearoff=0)
        self._init_context_menu()

        # 绑定事件
        self.tree.bind("<<TreeviewSelect>>", self._update_selection)
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self._toggle_node)
        self.tree.bind("<<TreeviewOpen>>", self._on_open)  # 改为 TreeviewOpen 事件

        self.pack()

        # 添加调整大小的功能
        self.resize_handle_width = 5  # 调整手柄的宽度（像素）
        self.tree.bind('<Motion>', self._on_mouse_motion)
        self.tree.bind('<ButtonPress-1>', self._on_mouse_press)
        self.tree.bind('<B1-Motion>', self._on_mouse_drag)
        self.tree.bind('<ButtonRelease-1>', self._on_mouse_release)
        self.resizing = False
        self.default_cursor = self.tree['cursor']

        # 初始加载根节点
        self._load_initial()
        self.auto_refresh()

    def _on_mouse_motion(self, event):
        """鼠标移动时检查是否在右边缘"""
        x = event.x
        tree_width = self.tree.winfo_width()
        if abs(x - tree_width) <= self.resize_handle_width and x > 10:  # 避免与节点交互冲突
            self.tree.configure(cursor='sb_h_double_arrow')
        else:
            self.tree.configure(cursor=self.default_cursor)

    def _on_mouse_press(self, event):
        """鼠标按下时开始调整大小"""
        x = event.x
        tree_width = self.tree.winfo_width()
        if abs(x - tree_width) <= self.resize_handle_width:
            self.resizing = True

    def _on_mouse_drag(self, event):
        """拖动时调整宽度"""
        if self.resizing:
            new_width = event.x
            if new_width > 80:  # 设置最小宽度
                # self.tree.column("#0", width=new_width)
                self.configure(width=new_width)

    def _on_mouse_release(self, event):
        """鼠标释放时结束调整"""
        self.resizing = False

    def _load_initial(self):
        """只加载根节点"""
        root_node = self.tree.insert('', 'end', text=basename(self.path),
                                     values=(self.path,), open=False)
        if self._has_children(self.path):
            self.tree.insert(root_node, 'end', text='Loading...')  # 占位符

    @lru_cache(maxsize=128)
    def _has_children(self, path):
        """检查目录是否有子项，使用缓存"""
        try:
            return any(True for _ in listdir(path))
        except (PermissionError, OSError):
            return False

    def _load_children(self, parent, path):
        """按需加载子节点"""
        # 先删除占位符
        children = self.tree.get_children(parent)

        # if children and self.tree.item(children[0])['text'] == 'Loading...':
        #     self.tree.delete(children[0])

        # 不做判断，全部删除
        self.tree.delete(*children)

        try:
            for name in sorted(listdir(path)):
                abs_path = join(path, name)
                node = self.tree.insert(parent, 'end', text=basename(abs_path),
                                        values=(abs_path,), open=False)
                if isdir(abs_path) and self._has_children(abs_path):
                    self.tree.insert(node, 'end', text='Loading...')
        except (PermissionError, OSError):
            pass

    def _on_open(self, event):
        """节点展开时加载子节点"""
        node = self.tree.focus()
        if not node:
            return
        path = self.tree.item(node)['values'][0]
        if isdir(path):
            self._load_children(node, path)

    def _toggle_node(self, event):
        """双击切换节点展开状态"""
        node = self.tree.identify_row(event.y)
        if node and isdir(self.tree.item(node)['values'][0]):
            if self.tree.item(node)['open']:
                self.tree.item(node, open=False)
            else:
                self.tree.item(node, open=True)
                # 这里不再需要手动调用 _load_children，因为 <<TreeviewOpen>> 会处理

    def _on_expand(self, event):
        """节点展开时加载子节点"""
        node = self.tree.focus()
        if not node:
            return
        path = self.tree.item(node)['values'][0]
        if isdir(path):
            self._load_children(node, path)

    def auto_refresh(self):
        """定时检查变化并局部刷新"""
        self._check_changes()
        self.after(self.refresh_interval, self.auto_refresh)

    def _check_changes(self):
        """检查变化并局部更新"""
        for node in self.tree.get_children(''):
            if self.tree.item(node)['open']:
                path = self.tree.item(node)['values'][0]
                current_children = set(self.tree.item(c)['text']
                                       for c in self.tree.get_children(node)
                                       if self.tree.item(c)['text'] != 'Loading...')
                disk_children = set(basename(join(path, name))
                                    for name in listdir(path))

                if current_children != disk_children:
                    self.tree.delete(*self.tree.get_children(node))
                    self._load_children(node, path)

    def _init_context_menu(self):
        """初始化右键上下文菜单"""
        new_menu = Menu(self.context_menu, tearoff=0)
        for ext in self.file_types:
            new_menu.add_command(
                label=f"新建 {ext} 文件",
                command=lambda e=ext: self._create_file(e)
            )
        new_menu.add_separator()
        new_menu.add_command(label="新建目录", command=self._create_folder)

        self.context_menu.add_cascade(label="新建", menu=new_menu)
        self.context_menu.add_command(label="删除", command=self._delete_item)
        self.context_menu.add_command(label="刷新", command=self._check_changes)
        self.context_menu.add_command(label="切换目录", command=self._select_mkdir)

    def _update_selection(self, event):
        selected = self.tree.selection()
        self.current_selection = self.tree.item(selected[0])['values'][0] if selected else None

    def _select_mkdir(self):
        new_path = askdirectory()
        if new_path:
            self.path = normpath(path=new_path)
            self._load_initial()

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def select_file(self, event):
        """选中项目时候触发事件"""

        file_names = event.widget.selection()
        for item in file_names:
            # 文件名
            # file_name = self.tree.item(item)['text']
            # 文件或文件夹路径
            file_path = self.tree.item(item)['values'][0].replace('-', '\\')
            # print(file_name, file_path)

            return file_path

    def _create_file(self, extension):
        if not self.current_selection:
            return
        try:
            base_path = self.current_selection if isdir(self.current_selection) else os.path.dirname(
                self.current_selection)
            counter = 1
            while True:
                new_file = join(base_path, f"新建文件{counter}{extension}")
                if not os.path.exists(new_file):
                    open(new_file, 'w').close()
                    self._check_changes()
                    break
                counter += 1
        except Exception as e:
            print(f"创建文件失败: {e}")

    def _create_folder(self):
        if not self.current_selection:
            return
        try:
            base_path = self.current_selection if isdir(self.current_selection) else os.path.dirname(
                self.current_selection)
            counter = 1
            while True:
                new_dir = join(base_path, f"新建文件夹{counter}")
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                    self._check_changes()
                    break
                counter += 1
        except Exception as e:
            print(f"创建目录失败: {e}")

    def _delete_item(self):
        if not self.current_selection or self.current_selection == self.path:
            return
        try:
            if os.path.isfile(self.current_selection):
                os.remove(self.current_selection)
            elif os.path.isdir(self.current_selection):
                os.rmdir(self.current_selection)
            self._check_changes()
        except Exception as e:
            print(f"删除失败: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    tree = DirectoryTree(root, r"E:\IDE")
    tree.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

