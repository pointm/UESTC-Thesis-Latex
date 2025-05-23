import math
import matplotlib.pyplot as plt
import numpy as np

# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix
# 设置字体的大小，
label_size = 20  # xy轴标签的大小
legend_size = 19  # 图例的大小
axis_size = 18  # 坐标轴刻度标签的大小


def qwq_part1():
    # 计算计算结果和测量值之间的关系的函数
    # ## QWQ的结果
    # R = 8.0
    # phi = 2.0  # rad
    # d = 1.561
    # theta = -0.003523  # rad

    # ## 修正QWQ的结果
    # R = 8.0
    # phi = 2.0  # rad
    # d = -1.56  # 修正符号
    # theta = 0.003523  # 修正为正值

    ## DP的结果 目前最好的版本
    # R = 8.0
    # phi = 2.0909  # rad
    # d = 1.4901
    # theta = -0.0037  # rad

    ## 更改公式之后的QWQ的一个结果，看起来还行但是不是完全拟合。方向向量：[-0.49695884  0.86777412  0.        ]，直线的方程为：0.86777412*x + 0.49695884*y = 1.4901
    # R = 8.0
    # phi = 0.5201  # rad
    # d = -1.4901
    # theta = 0.0037  # rad

    # # 更改公式之后的DP的一个解，线性拟合的一个结果并不是很满意。
    R = 8.0
    phi = 0.5200906874811719  # rad
    d = -1.4900683628083566
    theta = 0.0036911141973496897  # rad

    points = [
        (0, -0.018),
        (45, 0.000),
        (90, 0.021),
        (135, 0.022),
        (180, 0.011),
        (225, -0.014),
        (270, -0.032),
        (315, -0.034),
    ]

    # 提取实际测量数据
    angles_deg = [p[0] for p in points]
    actual_dz = [p[1] for p in points]

    # 计算理论值并存储
    computed_dz = []
    print("验证结果：")
    for angle_deg, delta_z in points:
        alpha = math.radians(angle_deg)
        term = d + R * math.sin(alpha - phi)
        computed = math.sin(theta) * term
        computed_dz.append(computed)
        print(f"Angle: {angle_deg}°, 实际Δz: {delta_z:.4f}, 计算Δz: {computed:.4f}")

    # 可视化结果
    plt.figure(figsize=(6, 4.5))
    plt.plot(angles_deg, computed_dz, "r-", label="理论计算值", marker="o")
    plt.scatter(
        angles_deg,
        actual_dz,
        marker="x",
        color="blue",
        s=100,
        label="测量值",
        zorder=3,
    )

    plt.xlabel("角度 / 度", fontsize=label_size)
    plt.ylabel("Δz / mm", fontsize=label_size)
    plt.xticks(range(0, 360, 45), fontsize=axis_size)
    plt.yticks(fontsize=axis_size)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=legend_size)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    qwq_part1()
