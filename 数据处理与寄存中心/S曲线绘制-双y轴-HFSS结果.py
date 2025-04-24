import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import numpy as np
from matplotlib import transforms

script_dir = os.path.dirname(os.path.abspath(__file__))
# 读取CSV文件


# 预设配置字典（修改部分）
configs = {
    "boxconfig": {
        "filedir": r"chapter2/盒型窗验证S曲线/S Parameter Plot 1.csv",
        "bbox_to_anchor": (0.62, 0.5),
        "figsize": (6.5, 5.5),
    },
    "xshell": {
        "filedir": r"chapter3/加上铜制外壳后的S参数.csv",
        "bbox_to_anchor": (0.5, 0.5),
        "figsize": (6.5, 5.5),
    },
}

# 通过修改这里切换配置 ↓
config_selector = "xshell"
selected_config = configs[config_selector]

# filedir = r"chapter2/盒型窗验证S曲线/S Parameter Plot 1.csv"
filedir = selected_config["filedir"]
datafile = pd.read_csv(os.path.join(script_dir, filedir))


# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix
# 设置字体的大小，
label_size = 20  # xy轴标签的大小
legend_size = 20  # 图例的大小
axis_size = 18  # 坐标轴刻度标签的大小

# 创建画布和主Y轴
fig, axis_y1 = plt.subplots(figsize=selected_config["figsize"])

# 绘制S21曲线（左轴）
axis_y1.plot(
    datafile["Freq [GHz]"],
    datafile["dB(S(2,1)) []"],
    "b-",  # 移除了冗余的color参数
    label=r"$\mathrm{S_{21}}$",  # 添加r前缀处理转义字符
    lw=2,
)
axis_y1.spines["left"].set_color("b")
axis_y1.spines["left"].set_linewidth(3)
axis_y1.set_ylabel(r"$\mathrm{S_{21}}$/dB", color="b", fontsize=label_size)
axis_y1.tick_params(
    axis="y",
    color="b",
    labelcolor="b",
    width=2,
    length=6,
    labelsize=axis_size,  # 新增：设置左轴刻度标签大小
)

# 设置X轴标签和刻度
axis_y1.set_xlabel("频率/GHz", fontsize=label_size)  # 添加字体大小
axis_y1.tick_params(axis="x", labelsize=axis_size)  # 新增X轴刻度字体设置

# 创建次Y轴绘制S11曲线
axis_y2 = axis_y1.twinx()
axis_y2.plot(
    datafile["Freq [GHz]"],
    datafile["dB(S(1,1)) []"],
    "r--",  # 移除了冗余的color参数
    label=r"$\mathrm{S_{11}}$",  # 添加r前缀处理转义字符
    lw=2,
)
axis_y2.spines["right"].set_color("r")
axis_y2.spines["right"].set_linewidth(3)
axis_y2.set_ylabel(r"$\mathrm{S_{11}}$ /dB", color="r", fontsize=label_size)
axis_y2.tick_params(
    axis="y",
    color="r",
    labelcolor="r",
    width=2,
    length=6,
    labelsize=axis_size,  # 新增：设置右轴刻度标签大小
)

# 设置图例
lines = axis_y1.get_lines() + axis_y2.get_lines()  # 合并两个轴的图例
labels = [line.get_label() for line in lines]
# plt.legend(
#     lines,
#     labels,
#     frameon=False,
#     fontsize=legend_size,
#     # loc="upper right",
#     bbox_to_anchor=(0.4, 0.9),
# )  # 保持与之前相同的位置
plt.legend(
    lines,
    labels,
    frameon=False,
    fontsize=legend_size,
    # loc="upper right",
    bbox_to_anchor=selected_config["bbox_to_anchor"],
)  # 保持与之前相同的位置

plt.tight_layout()

plt.show()
