import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 用户数据点
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

# 转换角度为弧度
alphas = np.deg2rad([angle for angle, _ in points])
dz_values = [dz for _, dz in points]


# 改进模型：包含二次项（sin(2θ)）
# 添加模型参数
R = 8.0  # 圆柱半径 (mm)
wt = 1.035  # 窗片厚度 (mm)


def residual(params):
    theta, phi = params
    res = []
    for alpha, dz in zip(alphas, dz_values):
        # 新Δz公式包含半径和厚度参数
        delta = R * np.tan(theta) * np.sin(phi - alpha) - (wt / 2) * (
            np.tan(theta) ** 2
        ) * (np.cos(phi - alpha) ** 2)
        res.append(delta - dz)
    return res


# 初始猜测（应包含θ和φ两个参数）
initial_theta = np.deg2rad(0.18)  # 初始θ猜测（0.18度转弧度）
# 调整初始猜测的φ值为等效角度
initial_phi = np.deg2rad(-135)  # 225°等效于-135°

initial_guess = [initial_theta, initial_phi]  # 仅包含两个参数的初始值

# 使用最小二乘法优化（保持边界约束）
result = least_squares(
    residual, initial_guess, bounds=([-np.pi, -np.pi], [np.pi, np.pi])
)

# 正确解包优化结果（两个参数）
theta_opt, phi_opt = result.x

# 删除以下旧参数解包
# A_opt, B_opt, C_opt = result.x

# 更新结果输出部分
residual_sq = np.sum(result.fun**2)
print("优化结果：")
print(f"旋转轴倾角θ: {np.rad2deg(theta_opt):.6f}°")
print(f"旋转轴方位角φ: {np.rad2deg(phi_opt) % 360:.6f}°")
print(f"残差平方和: {residual_sq:.6f}")

# 绘制结果
angles = [angle for angle, _ in points]
# 更新后的预测值计算（替换第90-92行）
predicted_dz = [
    R * np.tan(theta_opt) * np.sin(phi_opt - alpha)
    - (wt / 2) * (np.tan(theta_opt) ** 2) * (np.cos(phi_opt - alpha) ** 2)
    for alpha in alphas
]

plt.figure(figsize=(10, 6))
plt.scatter(angles, dz_values, label="实测Δz", color="blue", zorder=5)
plt.scatter(
    angles,
    predicted_dz,
    label="预测Δz（改进模型）",
    color="orange",
    marker="x",
    s=100,
    zorder=5,
)
# 修改结果输出部分
print(f"优化结果：")
print(f"旋转轴倾角θ: {np.rad2deg(theta_opt):.4f}°")
print(f"旋转轴方位角φ: {np.rad2deg(phi_opt) % 360:.2f}°")
print(f"窗片半径R: {R} mm")
print(f"窗片厚度wt: {wt} mm")

# 修改绘图标签
plt.xlabel("测量角度（度）")
plt.ylabel("z坐标差Δz (mm)")
plt.title(f"圆柱窗片旋转模型拟合 (R={R}mm, wt={wt}mm)")
plt.xlabel("角度（度）")
plt.ylabel("Δz（mm）")
plt.title("改进模型与实测对比（包含二次项）")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()
