import numpy as np
import matplotlib.pyplot as plt

# 数据输入（从原文件复制）
angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
delta_z = [-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034]

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

# 可视化部分
plt.figure(figsize=(6, 4.5))
plt.scatter(angles_deg, delta_z, marker="x", color="blue", label="Δz测量值")

# 添加数据标签
for angle, dz in zip(angles_deg, delta_z):
    plt.text(
        angle,
        dz + 0.001,
        f"{dz:.3f}",
        ha="center",
        va="bottom",
        fontsize=axis_size,
        color="blue",
        fontfamily="Times New Roman",
    )

# 坐标轴设置
x_min = min(angles_deg) - 25
x_max = max(angles_deg) + 25
plt.xlim(x_min, x_max)
y_min = min(delta_z) - 0.007
y_max = max(delta_z) + 0.007
plt.ylim(y_min, y_max)
plt.xlabel("角度 / 度", fontsize=label_size, fontfamily="SimSun")
plt.ylabel("Δz / mm", fontsize=label_size)
plt.xticks(np.arange(0, 360, 45), fontsize=axis_size)
plt.yticks(fontsize=axis_size)
plt.grid(True)
plt.legend(fontsize=legend_size)
plt.tight_layout()
plt.show()
