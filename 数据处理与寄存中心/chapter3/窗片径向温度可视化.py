import os
import matplotlib.pyplot as plt
import matplotlib as mpl
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
label_size = 16  # xy轴标签的大小
legend_size = 18  # 图例的大小
axis_size = 16  # 坐标轴刻度标签的大小
plt.figure(figsize=(6, 5.5))  # 设置图片大小

filepath = os.path.dirname(
    os.path.abspath(__file__)
)  # 获取当前py文件所在文件夹路径，字体已经安装好啦
filename = "窗片径向温度分布.txt"
filepath = os.path.join(filepath, filename)

temp = np.loadtxt(filepath, skiprows=0, unpack=True)
print(temp)

plt.plot(temp[1], temp[2], color="red", linewidth=3)

# 设置坐标轴标签和标题
plt.xlabel("距离中心/mm", fontsize=label_size)
plt.ylabel("温度/℃", fontsize=label_size)

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
# 设置X轴次要刻度步长为1 GHz
ax.xaxis.set_minor_locator(ticker.MultipleLocator(2.5 / 2))
# 设置Y轴次要刻度步长为5 dB
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25 / 2))

plt.grid(which="both", linestyle="--", linewidth=0.5)

plt.grid()
plt.show()
pass
