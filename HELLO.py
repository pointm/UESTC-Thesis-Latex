# ========================

# ... 保持中间原有代码不变 ...

# 修改可视化部分
plt.figure(figsize=(12, 6))
for (theta, phi), df in data_groups.items():
    # 执行筛选逻辑：当SELECTED_GROUPS为空时显示全部，否则匹配指定组合
    if not SELECTED_GROUPS or (theta, phi) in SELECTED_GROUPS:
        plt.plot(df["Length_mm"], df["E_field"], label=f"θ={theta}°, φ={phi}°")

# ... 保持后续绘图代码不变 ...
