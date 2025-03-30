import matplotlib.pyplot as plt
import numpy as np

# 数据读取
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))

# 重构后的文件数据结构 (章节路径, 文件名)
# files = [
#     ("chapter3", "X6GHZ-12.5kW.txt"),
#     ("chapter3", "X6GHZ-14.4kW.txt"),
#     ("chapter3", "X6GHZ-14.9kW.txt"),
#     ("chapter3", "X6GHZ-14.8kW.txt"),
#     ("chapter3", "X6GHZ-15.3kW-kick.txt"),
# ]
# y_max = 2e4  # 设置y轴显示的最大值，根据需求调整

files = [
    ("chapter4", "L-1.15kW-BACK.txt"),
    ("chapter4", "L-1.175kW-BACK.txt"),
    ("chapter4", "L-1.2kW-KICK.txt"),
    ("chapter4", "L-1.25kW-KICK.txt"),
]
# 新增y轴控制参数
y_max = 6e4  # 设置y轴显示的最大值，根据需求调整

# 学术图表设置
pt_number = 30
pt_number_axis = 28
pt_legend = 24

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": pt_number_axis,
        "mathtext.fontset": "stix",
    }  # 字号从12增大到14
)


plt.figure(figsize=(12, 8))
# 使用色环扩展颜色方案
color_cycle = plt.cm.tab10.colors * 2  # 10种基础色重复两次形成20色循环

# 循环绘制所有曲线
for i, (chapter, file) in enumerate(files):
    # 构建带章节的完整路径
    file_path = os.path.join(script_dir, chapter, file)

    # 读取文件头参数（保持不变）
    with open(file_path, "r") as f:
        first_line = f.readline().strip()
        # 修改为同时匹配 Pin/PIN 的表达式
        pin_match = re.search(r"(?i)pin=(\d+)", first_line)
        if pin_match:
            pin_value = pin_match.group(1)
        else:
            raise ValueError(f"未找到PIN参数: {file_path}")

    # 加载数据（保持不变）
    data = np.loadtxt(file_path, comments="#", delimiter="\t")

    # 自动选择颜色（带循环机制）
    line_color = color_cycle[i % len(color_cycle)]

    plt.plot(
        data[:, 0],
        data[:, 1],
        color=line_color,
        linewidth=3.5,  # 修改线宽从1.5→3.0
        label=f"Pin={int(pin_value)/1000}kW",
    )


# 坐标轴标注（调整字号）
plt.xlabel(r"Time (ns)", fontsize=pt_number, labelpad=10)
plt.ylabel(r"Number of particles $[N(t)]$", fontsize=pt_number, labelpad=10)

# 新增y轴范围设置
plt.ylim(top=y_max)  # 仅限制最大值，最小值自动

# 新增科学计数法设置
plt.gca().ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
plt.gca().yaxis.get_offset_text().set_fontsize(pt_number_axis)  # 设置指数字体大小

# 输出设置（调整图例位置和大小）
plt.legend(
    loc="upper left",
    bbox_to_anchor=(0.02, 0.98),  # 左上角坐标
    frameon=True,
    fontsize=pt_legend,  # 新增图例字号设置
)

# 删除以下重复的legend调用

# 输出设置
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
# plt.show()
plt.savefig(f"particle_time_{chapter}.pdf", dpi=300, bbox_inches="tight")
