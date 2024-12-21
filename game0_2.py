import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import time  # 导入时间模块


class Board:
    def __init__(self, side, x, y):
        """
        初始化棋盘

        :param side: 棋盘边长
        :param x: 特殊点横坐标
        :param y: 特殊点纵坐标
        """
        self.special_block = (x, y)
        self.board = np.zeros((side, side), dtype=int)
        self.board[x][y] = (side * side - 1) / 3 + 1
        self.t = 1
        self.side = side

    def visualize(self):
        """
        可视化函数
        :return: None
        """
        plt.imshow(self.board, cmap=plt.cm.gray)
        plt.colorbar()
        plt.show()

    def fill_block(self, x, y):
        """
        填充点(x, y)
        :param x: x
        :param y: y
        :return: None
        """
        if self.board[x][y] == 0:
            self.board[x][y] = self.t
        else:
            raise Exception

    def fill(self, t_x, t_y, side, d_x, d_y):
        """
        递归函数填充棋盘或子棋盘（下文称区块)
        :param t_x: 区块左上角x
        :param t_y: 区块左上角y
        :param side: 区块边长
        :param d_x: 区块特殊点坐标x
        :param d_y: 区块特殊点坐标y
        :return: None
        """
        if side == 1:
            return
        pos = (round((d_x - t_x + 1) / side), round((d_y - t_y + 1) / side))
        center = (round(t_x + side / 2 - 1), round(t_y + side / 2 - 1))
        ls = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i in ls:
            if i != pos:
                x = center[0] + i[0]
                y = center[1] + i[1]
                self.fill_block(x, y)
        self.t += 1
        for i in ls:
            if i != pos:
                x = center[0] + i[0]
                y = center[1] + i[1]
                x1 = t_x + i[0] * (side / 2)
                y1 = t_y + i[1] * (side / 2)
                self.fill(x1, y1, side / 2, x, y)
            else:
                x1 = t_x + i[0] * (side / 2)
                y1 = t_y + i[1] * (side / 2)
                self.fill(x1, y1, side / 2, d_x, d_y)


def on_start_button_click():
    try:
        # 获取用户输入的棋盘大小和特殊点坐标
        k = int(entry_k.get())
        loc_x = int(entry_x.get())
        loc_y = int(entry_y.get())

        # 检查输入是否有效
        if loc_x < 0 or loc_y < 0 or loc_x >= 2**k or loc_y >= 2**k:
            raise ValueError("特殊点坐标超出棋盘范围")

        # 边长
        side = 2**k
        # 实例化对象
        board = Board(side, loc_x, loc_y)

        # 记录开始时间
        start_time = time.time()

        # 递归填充
        board.fill(0, 0, side, loc_x, loc_y)

        # 记录结束时间
        end_time = time.time()

        # 计算并显示运行时间
        elapsed_time = end_time - start_time
        print(f"程序运行时间: {elapsed_time:.12f} 秒")

        # 可视化
        board.visualize()

        # 显示提示框
        messagebox.showinfo("成功", f"棋盘填充完成！\n运行时间: {elapsed_time:.12f} 秒")

    except ValueError as e:
        messagebox.showerror("输入错误", f"输入无效: {str(e)}")



root = tk.Tk()
root.title("棋盘覆盖问题")


root.geometry("400x300")


label_k = tk.Label(root, text="请输入正整数K (棋盘边长为2^k):")
label_k.pack(pady=10)
entry_k = tk.Entry(root)
entry_k.pack(pady=5)

label_x = tk.Label(root, text="请输入特殊点横坐标:")
label_x.pack(pady=10)
entry_x = tk.Entry(root)
entry_x.pack(pady=5)

label_y = tk.Label(root, text="请输入特殊点纵坐标:")
label_y.pack(pady=10)
entry_y = tk.Entry(root)
entry_y.pack(pady=5)

# 开始按钮
start_button = tk.Button(root, text="开始", command=on_start_button_click)
start_button.pack(pady=20)

# 运行Tkinter事件循环
root.mainloop()
