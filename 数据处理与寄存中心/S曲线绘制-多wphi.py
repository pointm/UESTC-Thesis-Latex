import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker
import numpy as np

# 初始化配置
script_dir = os.path.dirname(os.path.abspath(__file__))
config = {
    "filedir": r"chapter5/旋转的仿真S参数结果/S Parameter Plot 1.csv",
    "figsize": (11.5, 7),
    "colormap": "Accent",
    "linewidth": 3,
}


# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix

# 设置字体的大小，
label_size = 23  # xy轴标签的大小
legend_size = 19  # 图例的大小
axis_size = 20  # 坐标轴刻度标签的大小

# 加载数据
data_path = os.path.join(script_dir, config["filedir"])
df = pd.read_csv(data_path)

# 预处理数据
wphi_values = df["wphi [deg]"].unique()
wphi_values = np.array([w for w in wphi_values if w % 45 == 0])  # 新增过滤条件
wphi_values.sort()  # 确保角度按升序排列

# 创建画布
plt.figure(figsize=config["figsize"])

# 绘制各角度曲线
colors = plt.get_cmap(config["colormap"])(np.linspace(0, 1, len(wphi_values)))
for wphi, color in zip(wphi_values, colors):
    subset = df[df["wphi [deg]"] == wphi]
    plt.plot(
        subset["Freq [GHz]"],
        subset["dB(S(1,1)) []"],
        color=color,
        lw=config["linewidth"],
        label=f"$\\psi$ = {wphi}°",
    )

# 设置坐标轴
plt.xlabel("频率 / GHz", fontsize=label_size)
plt.ylabel(r"$\mathrm{S_{11}}$ / dB", fontsize=label_size)
plt.grid(True, alpha=0.3)

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

# 获取当前轴，准备设置子刻度
ax = plt.gca()
# 设置X/Y轴次要刻度（修改部分）
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1 / 2))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5 / 2))

# 优化图例显示
plt.legend(
    title="窗片旋转角",
    title_fontsize=legend_size,
    fontsize=legend_size,
    ncol=1,  # 修改为两列布局
    framealpha=0.8,
)

# 显示结果
plt.tight_layout()
plt.show()
