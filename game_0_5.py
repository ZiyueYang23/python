import numpy as np
import matplotlib.pyplot as plt
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


class BoardOptimized:
    def __init__(self, side, x, y):
        """
        初始化棋盘

        :param side: 棋盘边长
        :param x: 特殊点横坐标
        :param y: 特殊点纵坐标
        """
        self.special_block = (x, y)
        self.board = np.zeros((side, side), dtype=int)
        self.board[x][y] = (side * side - 1) // 3 + 1
        self.t = 1
        self.side = side

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

        # 计算区块中的特殊点所在的位置
        pos = (round((d_x - t_x + 1) / side), round((d_y - t_y + 1) / side))

        # 计算区块中心
        center = (round(t_x + side / 2 - 1), round(t_y + side / 2 - 1))

        # 填充其他三个块
        ls = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i in ls:
            if i != pos:
                x = center[0] + i[0]
                y = center[1] + i[1]
                self.fill_block(x, y)

        self.t += 1
        # 递归调用
        for i in ls:
            if i != pos:
                self.fill(
                    t_x + (i[0] * side // 2),
                    t_y + (i[1] * side // 2),
                    side // 2,
                    d_x,
                    d_y,
                )


def run_experiment(k_range, trials, board_class):
    """
    运行实验，计算每个k值的平均运行时间
    :param k_range: k值范围
    :param trials: 每个k值的实验次数
    :param board_class: 棋盘类
    :return: 每个k值的平均时间
    """
    avg_times = []
    for k in k_range:
        total_time = 0
        for _ in range(trials):
            side = 2**k
            x, y = side // 2, side // 2  # 设置特殊点
            board = board_class(side, x, y)
            start_time = time.time()
            board.fill(0, 0, side, x, y)
            end_time = time.time()
            total_time += end_time - start_time
        avg_times.append(total_time / trials)
    return avg_times


def plot_comparison(k_range, avg_times_optimized, avg_times_unoptimized):
    """
    绘制对比图
    :param k_range: k值范围
    :param avg_times_optimized: 优化后的平均时间
    :param avg_times_unoptimized: 未优化的平均时间
    :return: None
    """
    plt.plot(k_range, avg_times_optimized, label="Optimized")
    plt.plot(k_range, avg_times_unoptimized, label="Unoptimized")
    plt.xlabel("k value")
    plt.ylabel("Average Time (seconds)")
    plt.legend()
    plt.title("Comparison of Optimized and Unoptimized Versions")
    plt.show()


def calculate_speedup(avg_times_optimized, avg_times_unoptimized):
    """
    计算效率提升百分比
    :param avg_times_optimized: 优化后的平均时间
    :param avg_times_unoptimized: 未优化的平均时间
    :return: 提升百分比
    """
    speedup = []
    for opt, unopt in zip(avg_times_optimized, avg_times_unoptimized):
        speedup.append((unopt - opt) / unopt * 100)
    return speedup


if __name__ == "__main__":
    k_range = range(1, 13)  # k从1到12
    trials = 10  # 每个k值进行10次实验

    # 运行优化后的实验
    avg_times_optimized = run_experiment(k_range, trials, BoardOptimized)

    # 运行未优化的实验
    avg_times_unoptimized = run_experiment(k_range, trials, Board)

    # 绘制对比图
    plot_comparison(k_range, avg_times_optimized, avg_times_unoptimized)

    # 计算并打印效率提升百分比
    speedup = calculate_speedup(avg_times_optimized, avg_times_unoptimized)
    print("Efficiency improvement: ", speedup)
