import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix
# 设置字体的大小，
label_size = 23  # xy轴标签的大小
legend_size = 23  # 图例的大小
axis_size = 20  # 坐标轴刻度标签的大小

filepath = os.path.dirname(os.path.abspath(__file__))
filename = "TOTALV3.1S参数.txt"
filepath = os.path.join(filepath, filename)

S11 = np.loadtxt(filepath, delimiter="\t", skiprows=0, max_rows=5001, unpack=True)
S21 = np.loadtxt(filepath, delimiter="\t", skiprows=5004, max_rows=5001, unpack=True)

plt.figure(figsize=(6.8, 5.5))

plt.plot(S11[0], S11[1], label=r"$\mathrm{S_{11}}$", color="red", lw=2)
plt.plot(S21[0], S21[1], label=r"$\mathrm{S_{21}}$", color="blue", lw=2)
plt.xlabel("频率/ GHz", fontsize=label_size)
plt.ylabel("幅值/ dB", fontsize=label_size)

# 启用次要刻度
plt.minorticks_on()

# 自定义次要刻度位置
plt.tick_params(
    axis="both", which="minor", bottom=True, top=False, left=True, right=False
)

# 设置坐标轴刻度标签大小
plt.tick_params(axis="both", which="major", labelsize=axis_size)
plt.tick_params(axis="both", which="minor")

# 设置图例
plt.legend(frameon=False, fontsize=legend_size)

# 获取当前轴，准备设置子刻度
ax = plt.gca()
# 设置X/Y轴次要刻度（修改部分）
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))

plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

plt.show()
pass
