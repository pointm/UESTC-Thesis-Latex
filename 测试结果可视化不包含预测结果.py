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
        fontsize=axis_size,  # 修改字体大小参数
        color="darkred",
        fontfamily="Times New Roman",
    )

# 坐标轴设置
plt.xlabel("角度（度）", fontsize=label_size, fontfamily="SimSun")
plt.ylabel("Δz (mm)", fontsize=label_size)
plt.xticks(np.arange(0, 360, 45), fontsize=axis_size)
plt.yticks(fontsize=axis_size)
plt.grid(True)
plt.legend(fontsize=legend_size)
