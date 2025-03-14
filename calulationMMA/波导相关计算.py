import math
import matplotlib.pyplot as plt
import numpy as np


# 新增中文字体配置，方便在标签显示中文 ================
plt.rcParams["font.sans-serif"] = ["SimHei"]  # Windows系统字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

c = 3e8


class WaveGuide:
    """波导类"""

    frequency = -np.inf
    lambda_ = -np.inf
    lambda_c = -np.inf
    freq_c = -np.inf
    lambda_g = -np.inf
    PUimpedance = -np.inf

    def __init__(self, frequency):
        # 初始化波导实例
        self.frequency = frequency  # 设置工作频率
        self.lambda_ = c / frequency  # 计算自由空间波长
        self.calculate_lambda_c()  # 计算截止波长
        self.freq_c = c / self.lambda_c  # 计算截止频率
        self.calculate_lambda_g()  # 计算波导工作波长
        self.calculate_PUimpedance()  # 计算波导PU定义的阻抗
        pass  # 占位符无需关注

    def calculate_lambda_g(self):
        """计算波导工作波长"""

        self.lambda_g = self.lambda_ / math.sqrt(
            1 - (self.lambda_ / self.lambda_c) ** 2
        )

    def calculate_lambda_c(self):
        """计算波导截止波长"""

        pass

    def calculate_PUimpedance(self):
        """计算波导特性阻抗"""

        pass


class RectWaveGuide(WaveGuide):
    """矩形波导类"""

    a = np.inf
    b = np.inf

    def __init__(self, frequency, a, b):
        self.a = a
        self.b = b
        super().__init__(frequency)

    def calculate_lambda_c(self):
        """计算波导截止波长"""

        self.lambda_c = 2 * self.a

    def calculate_PUimpedance(self):
        """计算矩形波导特性阻抗"""

        self.PUimpedance = (
            (2 * self.b / self.a)
            * 120
            * math.pi
            / math.sqrt(1 - (c / (2 * self.a * self.frequency)) ** 2)
        )


class CircularWaveGuide(WaveGuide):
    """圆形波导类"""

    R = np.inf
    miu11 = 1.841

    def __init__(self, frequency, R):
        self.R = R
        super().__init__(frequency)

    def calculate_lambda_c(self):
        """计算波导截止波长"""
        self.lambda_c = (2 * math.pi * self.R) / self.miu11
        pass

    def calculate_PUimpedance(self):
        """计算圆形波导特性阻抗"""
        self.PUimpedance = (
            2.02
            * 120
            * math.pi
            / math.sqrt(1 - (c / (3.413 * self.R * self.frequency)) ** 2)
        )
        pass


class DoubleRidgeWaveguide(WaveGuide):
    """双脊波导类"""

    a = np.inf
    b = np.inf
    s = np.inf
    d = np.inf
    theta1 = np.inf
    theta2 = np.inf

    def __init__(self, frequency, a, b, s, d):
        self.a = a
        self.b = b
        self.s = s
        self.d = d
        super().__init__(frequency)
        pass

    def calculate_lambda_c(self):
        """计算波导截止波长"""
        DRWfactor = self.a / (2 * (self.a - self.s))
        DRWsum1 = (
            2
            / math.pi
            * (1 + 0.2 * math.sqrt(self.b / (self.a - self.s)))
            * (self.b / (self.a - self.s))
            * math.log(1 / math.sin(math.pi * self.d / (2 * self.b)))
        )
        DRWsum2 = (2.45 + 0.2 * (self.s / self.a)) * (
            self.s * self.b / (self.d * (self.a - self.s))
        )

        rightsum = 1 + DRWsum1 + DRWsum2
        self.lambda_c = self.a / (DRWfactor * math.sqrt(1 / rightsum))
        pass

    def calculate_PUimpedance(self):
        """计算波导特性阻抗"""
        self.theta1 = math.pi * (self.a - self.s) / self.lambda_c
        self.theta2 = math.pi * (self.s) / self.lambda_c

        eta0 = 120 * math.pi
        b_on_a = self.b / self.a
        d_on_b = self.d / self.b
        a_on_lambda_c = self.a / self.lambda_c

        DRWfactor0 = math.pi * eta0 * b_on_a * d_on_b * a_on_lambda_c

        DRWsum1 = (
            d_on_b
            * b_on_a
            * 2
            * a_on_lambda_c
            * math.log(1 / math.sin(math.pi * self.d / (2 * self.b)))
            * math.cos(self.theta2) ** 2
        )
        DRWsum2 = self.theta2 / 2 + math.sin(2 * self.theta2) / 4
        DRWsum3 = (
            d_on_b
            * (self.theta1 / 2 - math.sin(2 * self.theta1) / 4)
            * (math.cos(self.theta2) / math.sin(self.theta1)) ** 2
        )
        PU_characteristic_impedance = DRWfactor0 / (DRWsum1 + DRWsum2 + DRWsum3)
        self.PUimpedance = PU_characteristic_impedance * (self.lambda_g / self.lambda_)


if __name__ == "__main__":
    frequency = 8e9
    a = 20e-3
    b = 10e-3
    d = 5e-3
    s = 4e-3

    wg = DoubleRidgeWaveguide(frequency, a, b, s, d)
    pass
