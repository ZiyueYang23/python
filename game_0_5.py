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


class OptimizedBoard:
    def __init__(self, side, x, y):
        """
        初始化棋盘

        :param side: 棋盘边长
        :param x: 特殊点横坐标
        :param y: 特殊点纵坐标
        """
        self.special_block = (x, y)
        self.side = side
        self.board = np.zeros((side, side), dtype=int)
        self.board[x][y] = (side * side - 1) / 3 + 1
        self.t = 1

    def fill_block(self, x, y):
        """
        填充点(x, y)
        :param x: x
        :param y: y
        :return: None
        """
        if self.board[x][y] == 0:
            self.board[x][y] = self.t

    def fill(self, t_x, t_y, side, d_x, d_y):
        """
        优化递归填充函数
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

        # 使用NumPy批量填充区块
        fill_coords = [(center[0] + i[0], center[1] + i[1]) for i in ls if i != pos]
        for x, y in fill_coords:
            self.fill_block(x, y)

        self.t += 1

        for i in ls:
            if i != pos:
                x1 = t_x + i[0] * (side / 2)
                y1 = t_y + i[1] * (side / 2)
                self.fill(x1, y1, side / 2, x, y)
            else:
                x1 = t_x + i[0] * (side / 2)
                y1 = t_y + i[1] * (side / 2)
                self.fill(x1, y1, side / 2, d_x, d_y)


def run_experiment():
    """
    运行从k=1到k=12的实验，并记录运行时间
    :return: k值的列表与对应的平均运行时间
    """
    k_values = list(range(1, 13))
    avg_times = []

    for k in k_values:
        times = []
        for _ in range(10):  # 每个k值运行10次
            loc_x, loc_y = 2**k // 2, 2**k // 2  # 使用棋盘的中心作为特殊点
            side = 2**k
            board = OptimizedBoard(side, loc_x, loc_y)

            start_time = time.time()
            board.fill(0, 0, side, loc_x, loc_y)
            end_time = time.time()

            elapsed_time = end_time - start_time
            times.append(elapsed_time)

        avg_times.append(np.mean(times))  # 计算平均运行时间

    return k_values, avg_times


def run_original_experiment():
    """
    运行原始算法的实验
    :return: k值的列表与对应的平均运行时间
    """
    k_values = list(range(1, 13))
    avg_times = []

    for k in k_values:
        times = []
        for _ in range(10):  # 每个k值运行10次
            loc_x, loc_y = 2**k // 2, 2**k // 2  # 使用棋盘的中心作为特殊点
            side = 2**k
            board = Board(side, loc_x, loc_y)  # 使用原始算法

            start_time = time.time()
            board.fill(0, 0, side, loc_x, loc_y)
            end_time = time.time()

            elapsed_time = end_time - start_time
            times.append(elapsed_time)

        avg_times.append(np.mean(times))  # 计算平均运行时间

    return k_values, avg_times


def plot_comparison(original_times, optimized_times, k_values):
    """
    绘制对比图并记录数据
    :param original_times: 原始算法的运行时间
    :param optimized_times: 优化算法的运行时间
    :param k_values: k值的列表
    """
    plt.figure(figsize=(10, 6))

    # 绘制原始和优化算法的对比图
    plt.plot(k_values, original_times, label="原始算法", marker="o", color="blue")
    plt.plot(k_values, optimized_times, label="优化算法", marker="o", color="orange")

    # 计算性能提升百分比
    improvement_percent = [
        (orig - opt) / orig * 100 if opt != 0 else 0
        for orig, opt in zip(original_times, optimized_times)
    ]

    # 输出性能提升百分比
    print("性能提升百分比：", improvement_percent)

    # 保存数据到文件
    with open("performance_comparison.txt", "w") as file:
        file.write("k值, 原始算法时间 (秒), 优化算法时间 (秒), 性能提升百分比\n")
        for k, orig, opt, imp in zip(
            k_values, original_times, optimized_times, improvement_percent
        ):
            file.write(f"{k}, {orig:.6f}, {opt:.6f}, {imp:.2f}%\n")

    # 添加图表标题与标签
    plt.title("原始算法与优化算法运行时间对比", fontsize=14)
    plt.xlabel("k值", fontsize=12)
    plt.ylabel("平均运行时间 (秒)", fontsize=12)
    plt.legend()
    plt.grid(True)

    # 显示图表
    plt.show()


def main():
    # 运行原始算法实验
    original_k_values, original_times = run_original_experiment()

    # 运行优化算法实验
    optimized_k_values, optimized_times = run_experiment()

    # 绘制性能对比图，并记录数据
    plot_comparison(original_times, optimized_times, original_k_values)


if __name__ == "__main__":
    main()
