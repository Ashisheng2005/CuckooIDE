import tkinter as tk

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, radius=25, bg="#ffffff", border_width=0, border_color=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(highlightthickness=0, bg=parent.cget("bg"))

        # 初始化参数
        self._radius = radius
        self._bg = bg
        self._border_width = max(border_width, 0)  # 确保非负
        self._border_color = border_color if border_color else bg

        # 创建内容容器
        self.container = tk.Frame(self, bg=self._bg)
        self.container.pack_propagate(False)  # 禁止自动调整大小

        # 修正2：设置Canvas初始尺寸
        self.config(width=kwargs.get('width', 200),
                    height=kwargs.get('height', 150))

        self.create_window(
            (self._border_width, self._border_width),
            window=self.container,
            anchor="nw",
            tags=("inner",)
        )

        # 绑定尺寸变化事件（添加防抖）
        self.bind("<Configure>", lambda e: self.after(10, self._draw_rounded_rect))
        self._draw_rounded_rect()

    def _draw_rounded_rect(self, event=None):
        # 清除之前的绘制（不包括内容容器）
        self.delete("bg", "border")

        # 获取实际尺寸
        width = self.winfo_width()
        height = self.winfo_height()

        # 动态计算有效半径（核心修正）
        effective_radius = min(
            self._radius,
            (width - 2 * self._border_width) // 2,
            (height - 2 * self._border_width) // 2,
        )
        effective_radius = max(effective_radius, 1)  # 最小1像素

        # 绘制边框层
        if self._border_width > 0:
            self._draw_layer(
                0, 0, width, height,
                effective_radius + self._border_width,
                self._border_color,
                tag="border"
            )

        # 绘制背景层
        self._draw_layer(
            self._border_width,
            self._border_width,
            width - self._border_width,
            height - self._border_width,
            effective_radius,
            self._bg,
            tag="bg"
        )

        # 更新内容容器尺寸（带保护机制）
        inner_width = max(width - 2 * self._border_width, 1)
        inner_height = max(height - 2 * self._border_width, 1)
        self.itemconfigure("inner", width=inner_width, height=inner_height)
        self.container.config(width=inner_width, height=inner_height)  # 设置明确尺寸
        self.container.update_idletasks()  # 更新布局

    def _draw_layer(self, x1, y1, x2, y2, radius, color, tag=None):
        """ 通用绘制方法 """
        points = []
        r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)

        # 生成顺时针坐标点
        points += [x1 + r, y1]  # 上边左起点
        points += [x2 - r, y1]  # 上边右起点
        points += [x2, y1, x2, y1 + r]  # 右上弧
        points += [x2, y2 - r, x2, y2]  # 右下边
        points += [x2 - r, y2]  # 下边右起点
        points += [x1 + r, y2]  # 下边左起点
        points += [x1, y2, x1, y2 - r]  # 左下弧
        points += [x1, y1 + r, x1, y1]  # 左上边

        self.create_polygon(
            points,
            smooth=True,
            splinesteps=20,
            fill=color,
            outline="",
            tags=tag
        )

    # 确保控件可见
    def _on_configure(self, event):
        self._draw_rounded_rect()
        self.container.lift(aboveThis=self)  # 提升内容容器的层级
        self.container.update_idletasks()

    def _set_container_size(self):
        inner_width = self.winfo_width() - 2 * self._border_width
        inner_height = self.winfo_height() - 2 * self._border_width
        self.container.config(width=inner_width, height=inner_height)
        self.container.update_idletasks()


# 测试用例
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")
    root.config(bg="#2b2b2b")  # 深色背景测试

    frame = RoundedFrame(root,
                         radius=40,
                         bg="#f0f0f0",
                         border_width=2,
                         border_color="#ff6b6b",
                         width=250,
                         height=180)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # 测试控件
    tk.Label(frame.container, text="自适应圆角容器",
             bg="#f0f0f0", fg="black").pack(pady=10, fill='x')  # 添加fill参数

    tk.Entry(frame.container, bg="white").pack(pady=5, fill='x', padx=10)  # 添加边距

    tk.Button(frame.container, text="测试按钮",
              relief="raised", bg="#4ecdc4", fg="white").pack(pady=10, ipadx=20)

    # 添加这一行确保容器可见
    # frame._set_container_size()
    # frame.bind("<Configure>", frame._on_configure)

    root.mainloop()

