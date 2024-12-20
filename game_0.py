# 用来处理棋盘数据，创建和操作二维数组，也就是棋盘
import numpy as np

# 用于可视化显示棋盘填充状态
import matplotlib.pyplot as plt


class Board:
    # self就相当于c++中的this指针
    def __init__(self, side, x, y):
        """
        初始化棋盘

        :param side: 棋盘边长
        :param x: 特殊点横坐标
        :param y: 特殊点纵坐标
        """
        # 记录特殊方块位置
        self.special_block = (x, y)
        # 创建棋板先初始化整块棋板均为0，默认类型为int
        self.board = np.zeros((side, side), dtype=int)
        """
        填充特殊方块对应的值

        计算方法为：
            1.先通过(side * side - 1) / 3算出一共需要多少个L型骨牌
            2.然后再加1使其完成标注特殊方块
        """
        self.board[x][y] = (side * side - 1) / 3 + 1
        # 初始化标注从1开始
        self.t = 1
        # 边长
        self.side = side

    # 绘制棋盘
    def visualize(self):
        """
        可视化函数

        :return: None
        """
        # 显示棋盘 因为将特殊方块标注成最大值即所需L型骨牌加1的数字
        # 因此在灰度空间中 最小的也就是第一块L型骨牌会被标注为最黑的一块 然后大小依次递增，变白，最终会停在最大即特殊方块最白的地方
        plt.imshow(self.board, cmap=plt.cm.gray)
        # 加一个颜色条参照
        plt.colorbar()
        plt.show()

    def fill_block(self, x, y):
        """
        填充点(x, y)

        :param x: x
        :param y: y
        :return: None
        """
        # 如果是0即没有被填充才会填充数值
        if self.board[x][y] == 0:
            self.board[x][y] = self.t
        else:
            # 抛出异常
            raise Exception

    def fill(self, t_x, t_y, side, d_x, d_y):
        """
        递归函数填充棋盘或子棋盘（下文称区块)

        :param t_x: 区块左上角x
        :param t_y: 区块左上角y
        :param side: 区块边长
        :param d_x: 区块特殊点坐标x
        :param d_y: 区块特殊点坐标x
        :return: None
        """
        # 如果被划分到最小的一个单元就会退出 递归出口
        if side == 1:
            return
        # 判断特殊方块在划分的四个区域中的那一个
        # round是四舍五入函数
        # 注意加1的细节
        #  /side的目的就是将其映射到0，1
        pos = (round((d_x - t_x + 1) / side), round((d_y - t_y + 1) / side))
        # 计算中心点
        center = (round(t_x + side / 2 - 1), round(t_y + side / 2 - 1))
        # 以(0,0)...划分四个区域
        ls = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i in ls:
            if i != pos:
                # 如果不是原有特殊点所在区块，则构造特殊点并填充
                x = center[0] + i[0]
                y = center[1] + i[1]
                self.fill_block(x, y)
        # 标记号加一，标记下一骨牌
        self.t += 1
        for i in ls:
            if i != pos:
                # 如果不是原有特殊点所在区块
                # 所构造特殊点位置(x, y)
                x = center[0] + i[0]
                y = center[1] + i[1]
                x1 = t_x + i[0] * (side / 2)
                y1 = t_y + i[1] * (side / 2)
                self.fill(x1, y1, side / 2, x, y)
            else:
                # 如果是原有特殊点所在区块
                x1 = t_x + i[0] * (side / 2)
                y1 = t_y + i[1] * (side / 2)
                self.fill(x1, y1, side / 2, d_x, d_y)


# 主函数
if __name__ == "__main__":
    k = eval(input("请输入正整数K(棋盘大小2^k,2^k):\n"))
    loc_x = eval(input("请输入特殊点横坐标:\n"))
    loc_y = eval(input("请输入特殊点纵坐标:\n"))
    # 边长
    side = 2**k
    # 实例化对象
    b = Board(side, loc_x, loc_y)
    # 递归填充
    b.fill(0, 0, side, loc_x, loc_y)
    # 可视化
    b.visualize()
    # 打印
    print(b.board)
