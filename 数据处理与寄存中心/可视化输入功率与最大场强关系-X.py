import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

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

# 提取文件的路径
filepath = os.path.dirname(os.path.abspath(__file__))
# chaptername = r"chapter3/输入功率VS最大场强"
chaptername = r"chapter4/输入功率VS最大场强"
filename = "输入功率VS最大场强.txt"
file_path = os.path.join(filepath, chaptername, filename)

# 读取数据（跳过注释行）
data = np.loadtxt(
    file_path,
    delimiter="\t",
    skiprows=2,
)

# 提取功率和场强数据
power = data[:, 0]  # 输入功率（单位：W）
field_strength = data[:, 1]  # 最大电场强度（单位：V/m）

# 创建图表
plt.figure(figsize=(6, 4.5))
plt.plot(
    power / 1e3, field_strength / 1e5, "ro-", linewidth=2
)  # 将将横轴转化为kW，纵轴转化为场强转换为 kV/cm


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
# plt.legend(frameon=False, fontsize=legend_size)

# 获取当前轴，准备设置子刻度
ax = plt.gca()
# 设置X/Y轴次要刻度（修改部分）
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(1 / 2))  # 这个是X 频段窗用的X轴
ax.xaxis.set_minor_locator(ticker.MultipleLocator(20 / 2))  # 这个是L 频段用的X轴
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5 / 2))

# 添加标签和网格
# plt.title("输入功率与最大电场强度关系", fontsize=14)
plt.xlabel("输入功率 / kW", fontsize=label_size)
plt.ylabel("最大电场强度 / kV / cm", fontsize=label_size)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tick_params(axis="both", which="major", labelsize=axis_size)  # 坐标轴刻度

# 显示图表
plt.tight_layout()

plt.show()  # 取消注释以显示交互式窗口
