# 看不懂QWQ在做什么，但是貌似很厉害的样子，仿真结果拟合得一般但是勉强能看吧
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

# 用户提供的数据点（角度和Δz）
points = [
    (0, -0.018),
    (45, 0.000),
    (90, 0.021),
    (135, 0.022),
    (180, 0.011),
    (225, -0.014),
    (270, -0.032),
    (315, -0.034),
]

# 将角度转换为弧度
alphas = [np.deg2rad(angle) for angle, _ in points]
dz_values = [dz for _, dz in points]


def residual(params):
    theta, phi = params
    res = []
    for alpha, dz in zip(alphas, dz_values):
        predicted = 8 * np.sin(theta) * np.sin(phi - alpha)
        res.append(predicted - dz)
    return res


# 初始猜测（θ=0.18°, φ=225°）
initial_theta = np.deg2rad(0.18)
initial_phi = np.deg2rad(225)
initial_guess = [initial_theta, initial_phi]

# 使用最小二乘法优化
result = least_squares(
    residual, initial_guess, bounds=([-np.pi, 0], [np.pi, 2 * np.pi])  # 修改边界范围
)

theta_opt, phi_opt = result.x
theta_deg = np.rad2deg(theta_opt)
phi_deg = np.rad2deg(phi_opt)

print(f"Optimized theta: {theta_opt:.6f} rad")  # 修改为直接输出弧度值
print(f"Optimized phi: {phi_deg:.6f}°")  # 保持phi角度输出不变

# 计算优化后的预测值
predicted_dz = []
for alpha in alphas:
    pred = 8 * np.sin(theta_opt) * np.sin(phi_opt - alpha)
    predicted_dz.append(pred)

# 绘制结果
angles = [angle for angle, _ in points]
plt.figure(figsize=(10, 6))
plt.scatter(angles, dz_values, label="Measured Δz", color="blue")
plt.scatter(angles, predicted_dz, label="Predicted Δz", color="red", marker="x")
plt.xlabel("Angle (degrees)")
plt.ylabel("Δz (mm)")
plt.title("Measured vs Predicted Δz Values")
plt.legend()
plt.grid(True)
plt.show()
