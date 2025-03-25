# DP的预测结果虽说很准确但是实际仿真时候觉得偏心旋转结果一般
import numpy as np
from math import cos, sin, radians, degrees

# 输入数据
angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
delta_z = [-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034]

# 转换为弧度
phi = [radians(deg) for deg in angles_deg]

R = 8.0  # 半径 (mm)

# 构造矩阵 X 和 Y
X = []
for angle in phi:
    x = R * cos(angle)
    y = R * sin(angle)
    X.append([x, y, 1])

Y = np.array(delta_z)

# 最小二乘法求解系数 a, b, c
coefficients, residuals, _, _ = np.linalg.lstsq(X, Y, rcond=None)
a, b, c = coefficients

# 计算旋转角度
cos_theta = 1 / np.sqrt(a**2 + b**2 + 1)
theta_rad = np.arccos(cos_theta)
theta_deg = degrees(theta_rad)

# 旋转轴方程
print(f"旋转轴方程：{a:.6f}x + {b:.6f}y + {c:.6f} = 0，位于 z=0 平面")
print(f"旋转角度：{theta_rad:.6f} 弧度")

# 计算预测值并与实际值对比
print("\n角度 | 实际Δz (mm) | 预测Δz (mm)")
print("----------------------------------")
for i in range(len(angles_deg)):
    x = X[i][0]
    y = X[i][1]
    predicted = a * x + b * y + c
    print(f"{angles_deg[i]:3}° | {delta_z[i]:10.3f} | {predicted:10.3f}")
