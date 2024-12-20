import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import time


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


# 优化版本
class OptimizedBoard(Board):
    def fill(self, t_x, t_y, side, d_x, d_y):
        """
        递归函数填充棋盘或子棋盘（下文称区块), 进行了优化
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

        # 填充其他3个块
        for i in ls:
            if i != pos:
                x = center[0] + i[0]
                y = center[1] + i[1]
                self.fill_block(x, y)

        self.t += 1

        # 递归填充每个子棋盘
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


def run_experiment(board_class, k):
    """
    执行一次实验，计算运行时间
    :param k: 棋盘大小的指数
    :return: 运行时间
    """
    # 设置特殊点坐标为棋盘中心
    loc_x, loc_y = 2**k // 2, 2**k // 2
    side = 2**k
    board = board_class(side, loc_x, loc_y)

    start_time = time.time()  # 记录开始时间
    board.fill(0, 0, side, loc_x, loc_y)  # 递归填充棋盘
    end_time = time.time()  # 记录结束时间
    return end_time - start_time  # 返回运行时间


def collect_data(board_class):
    """
    收集从 k=1 到 k=12 的实验数据，执行 10 次并计算平均时间
    :return: k 值和对应的平均运行时间
    """
    k_values = list(range(1, 13))  # k 从 1 到 12
    avg_times = []

    for k in k_values:
        times = [
            run_experiment(board_class, k) for _ in range(10)
        ]  # 每个 k 执行 10 次实验
        avg_time = sum(times) / len(times)  # 计算平均时间
        avg_times.append(avg_time)  # 存储平均时间

    return k_values, avg_times


def plot_comparison_data(k_values, avg_times_original, avg_times_optimized):
    """
    绘制优化前后对比图
    :param k_values: k 值
    :param avg_times_original: 原始版本的平均运行时间
    :param avg_times_optimized: 优化版本的平均运行时间
    """
    plt.plot(k_values, avg_times_original, marker="o", label="原始版本")
    plt.plot(k_values, avg_times_optimized, marker="o", label="优化版本")
    plt.title("棋盘覆盖问题的运行时间对比")
    plt.xlabel("k (棋盘大小为 2^k)")
    plt.ylabel("平均运行时间（秒）")
    plt.grid(True)
    plt.legend()
    plt.show()


# 收集原始版本的数据
k_values, avg_times_original = collect_data(Board)

# 收集优化版本的数据
_, avg_times_optimized = collect_data(OptimizedBoard)

# 绘制优化前后对比图
plot_comparison_data(k_values, avg_times_original, avg_times_optimized)

# 计算优化提升的百分比
improvement_percentages = [
    (
        ((avg_times_original[i] - avg_times_optimized[i]) / avg_times_original[i] * 100)
        if avg_times_original[i] > 0
        else 0
    )  # 如果原始时间为 0，则提升百分比为 0
    for i in range(len(k_values))
]

# 输出提升百分比
for k, improvement in zip(k_values, improvement_percentages):
    print(f"k={k}: 提升 {improvement:.2f}%")
