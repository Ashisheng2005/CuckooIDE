# keyword.json

- ### **文件结构说明**

  1. **`keyword`**:
     - 包含 C 语言的所有关键字（如 `int`、`for`、`if` 等）。
     - 这些关键字是 C 语言的核心语法，用于定义变量、控制流程等。
  2. **`builtins`**:
     - 包含 C 语言标准库中的常用函数（如 `printf`、`malloc`、`strlen` 等）。
     - 这些函数是 C 语言标准库的一部分，开发者可以直接调用。
  3. **`dir_sys`**:
     - 包含 C 语言标准库中的宏、常量和类型定义（如 `NULL`、`FILE`、`EOF` 等）。
     - 这些通常用于系统编程和文件操作。
  4. **`lineComment`**:
     - 定义 C 语言的单行注释符号为 `//`。

  ------

  ### **如何使用该文件**

  1. **语法高亮**：
     - 在 IDE 中读取 `keyword.json` 文件，解析 `keyword`、`builtins` 和 `dir_sys` 列表。
     - 在代码编辑器中，遍历代码文本，匹配这些关键字和函数，并为它们应用不同的颜色或样式。
  2. **代码补全**：
     - 使用 `builtins` 和 `dir_sys` 列表提供代码补全建议。
  3. **错误检查**：
     - 检查用户输入的代码是否包含未定义的关键字或函数。

  ------

  ### **示例代码（语法高亮）**

  以下是一个简单的 Python 示例，展示如何使用 `keyword.json` 实现 C 语言的语法高亮：

  python

  复制

  ```python
  import json
  import re
  from tkinter import Tk, Text, END
  
  # 加载 keyword.json
  with open("keyword.json", "r", encoding="utf-8") as f:
      keywords = json.load(f)
  
  # 定义高亮样式
  def apply_highlight(text_widget):
      # 清除旧的高亮
      text_widget.tag_remove("keyword", "1.0", END)
      text_widget.tag_remove("builtin", "1.0", END)
      text_widget.tag_remove("dir_sys", "1.0", END)
  
      # 高亮关键字
      for word in keywords["keyword"]:
          matches = re.finditer(rf"\b{word}\b", text_widget.get("1.0", END))
          for match in matches:
              start, end = match.span()
              text_widget.tag_add("keyword", f"1.0+{start}c", f"1.0+{end}c")
  
      # 高亮内置函数
      for word in keywords["builtins"]:
          matches = re.finditer(rf"\b{word}\b", text_widget.get("1.0", END))
          for match in matches:
              start, end = match.span()
              text_widget.tag_add("builtin", f"1.0+{start}c", f"1.0+{end}c")
  
      # 高亮系统定义
      for word in keywords["dir_sys"]:
          matches = re.finditer(rf"\b{word}\b", text_widget.get("1.0", END))
          for match in matches:
              start, end = match.span()
              text_widget.tag_add("dir_sys", f"1.0+{start}c", f"1.0+{end}c")
  
  # 创建 GUI
  root = Tk()
  text = Text(root)
  text.pack(fill="both", expand=True)
  
  # 设置高亮样式
  text.tag_configure("keyword", foreground="blue")
  text.tag_configure("builtin", foreground="green")
  text.tag_configure("dir_sys", foreground="purple")
  
  # 绑定事件
  text.bind("<KeyRelease>", lambda event: apply_highlight(text))
  
  root.mainloop()
  ```

  ------

  ### **总结**

  - 该 `keyword.json` 文件包含了 C 语言的关键字、标准库函数和系统定义。
  - 你可以根据需要在 IDE 中实现语法高亮、代码补全和错误检查等功能。
  - 如果有其他需求（如添加更多库函数或宏），可以进一步扩展 `builtins` 和 `dir_sys` 列表。