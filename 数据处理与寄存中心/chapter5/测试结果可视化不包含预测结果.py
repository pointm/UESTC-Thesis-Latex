import numpy as np
import matplotlib.pyplot as plt

# 数据输入（从原文件复制）
angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
delta_z = [-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034]

# 字体配置
plt.rcParams["font.serif"] = ["SimSun", "Times New Roman"]
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 15
plt.rcParams["axes.unicode_minus"] = False

# 可视化部分
plt.figure(figsize=(5, 4))
plt.scatter(angles_deg, delta_z, c="r", label="实际Δz")

# 添加数据标签
for angle, dz in zip(angles_deg, delta_z):
    plt.text(
        angle,
        dz + 0.001,
        f"{dz:.3f}",
        ha="center",
        va="bottom",
        fontsize=12,
        color="darkred",
        fontfamily="Times New Roman",
    )

# 坐标轴设置
x_min = min(angles_deg) - 20
x_max = max(angles_deg) + 20
plt.xlim(x_min, x_max)
y_min = min(delta_z) - 0.007
y_max = max(delta_z) + 0.007
plt.ylim(y_min, y_max)
# plt.title("角度-Δz关系散点图", fontsize=14, fontfamily="SimSun")
plt.xlabel("角度（度）", fontsize=12, fontfamily="SimSun")
plt.ylabel("Δz (mm)", fontsize=12)
plt.xticks(np.arange(0, 360, 45), fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()
