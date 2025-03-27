# 可视化对比
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# 字体配置
plt.rcParams["font.serif"] = ["SimSun", "Times New Roman"]
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 15
plt.rcParams["axes.unicode_minus"] = False


def dp_part1():
    # 数据点
    angles_deg = np.array([0, 45, 90, 135, 180, 225, 270, 315])
    delta_z = np.array([-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034])

    # 转换为弧度
    alpha = np.deg2rad(angles_deg)
    cos_alpha = np.cos(alpha)
    sin_alpha = np.sin(alpha)

    # 构造矩阵A和向量b
    A = np.column_stack([np.ones_like(alpha), cos_alpha, sin_alpha])
    b = delta_z

    # 最小二乘解
    C0, C1, C2 = np.linalg.lstsq(A, b, rcond=None)[0]

    R = 8  # mm
    # 计算 sin(theta)
    sqrt_C1C2 = np.sqrt(C1**2 + C2**2)
    abs_sin_theta = sqrt_C1C2 / R
    sin_theta = np.sign(C0) * abs_sin_theta  # 符号由C0决定

    # 计算 theta（弧度）
    theta = np.arcsin(sin_theta)

    # 计算 d
    d = C0 / sin_theta

    # 计算 phi（弧度）
    phi = np.arctan2(-C2, -C1)  # 注意符号
    phi = (phi + 2 * np.pi) % (2 * np.pi)  # 转换为0~2π范围

    print(f"估计参数：")
    print(f"φ = {phi:.4f} 弧度（约 {np.rad2deg(phi):.2f} 度）")
    print(f"d = {d:.2f} mm")
    print(f"θ = {theta:.6f} 弧度（约 {np.rad2deg(theta):.4f} 度）")

    # 验证模型预测
    predicted_z = C0 + C1 * cos_alpha + C2 * sin_alpha
    residuals = delta_z - predicted_z
    print("\n残差验证：")
    for i in range(len(delta_z)):
        print(
            f"角度 {angles_deg[i]:3}°: 实际Δz = {delta_z[i]:.3f}, 预测Δz = {predicted_z[i]:.3f}, 残差 = {residuals[i]:.3f}"
        )


def dp_part2():
    # 数据
    alpha_degrees = [0, 45, 90, 135, 180, 225, 270, 315]
    dz = [-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034]

    alpha_radians = np.deg2rad(alpha_degrees)

    # 构建设计矩阵
    X = np.ones((len(alpha_degrees), 3))
    for i in range(len(alpha_degrees)):
        a = alpha_radians[i]
        X[i, 1] = np.cos(a)
        X[i, 2] = np.sin(a)

    Y = np.array(dz)

    # 线性回归求解A, B, C
    coefficients, residuals, _, _ = np.linalg.lstsq(X, Y, rcond=None)
    A, B, C = coefficients

    R = 8.0  # mm

    # 计算参数
    B_sq_C_sq = B**2 + C**2
    sin_theta = -np.sqrt(B_sq_C_sq) / R
    theta = np.arcsin(sin_theta)
    d_param = A / sin_theta
    phi = np.arctan2(C, B)

    # 转换为角度
    theta_deg = np.rad2deg(theta)
    phi_deg = np.rad2deg(phi)

    # 结果输出
    print(f"估计参数：")
    print(f"φ = {phi:.4f} rad ({phi_deg:.2f}°)")
    print(f"d = {d_param:.4f} mm")
    print(f"θ = {theta:.4f} rad ({theta_deg:.2f}°)")

    # 旋转轴方程
    print("\n旋转轴方程：")
    print(f"{np.cos(phi):.4f} x + {np.sin(phi):.4f} y = {d_param:.4f}")

    # === 新增可视化代码 ===
    # 计算理论值
    computed_dz = [
        np.sin(theta) * (d_param - R * np.cos(np.deg2rad(angle) - phi))
        for angle in alpha_degrees
    ]

    plt.figure(figsize=(8, 5))
    plt.plot(alpha_degrees, computed_dz, "r-", marker="o", label="理论计算值")
    plt.scatter(alpha_degrees, dz, s=100, zorder=3, label="实际测量值")

    # plt.title("Δz 角度分布对比 (dp_part2)")
    plt.xlabel("角度 (度)")
    plt.ylabel("Δz (mm)")
    plt.xticks(range(0, 360, 45))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


def dp_part3():
    # 这是在改变公式之后的第一个线性拟合结果，不是很好。
    # 数据
    alpha_deg = np.array([0, 45, 90, 135, 180, 225, 270, 315])
    delta_z = np.array([-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034])

    # 转换为弧度并计算特征
    alpha_rad = np.deg2rad(alpha_deg)
    sin_alpha = np.sin(alpha_rad)
    cos_alpha = np.cos(alpha_rad)
    X = np.column_stack([np.ones(8), sin_alpha, cos_alpha])

    # 线性回归
    coefficients, *_ = np.linalg.lstsq(X, delta_z, rcond=None)
    A, B, C = coefficients
    R = 8.0  # mm

    # 计算参数
    B_sq_plus_C_sq = B**2 + C**2
    sin_theta = np.sqrt(B_sq_plus_C_sq) / R
    theta = np.arcsin(sin_theta)
    phi = np.arctan2(-C, B)
    d = A / sin_theta

    print("phi (rad):", phi)
    print("phi (degrees):", np.degrees(phi))
    print("d (mm):", d)
    print("theta (rad):", theta)
    print("theta (degrees):", np.degrees(theta))


def dp_part4():
    # 改变模型之后的非线性拟合结果，结果都一样的（悲
    # 数据
    alpha_deg = np.array([0, 45, 90, 135, 180, 225, 270, 315])
    delta_z = np.array([-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034])

    def model_func(alpha_deg, phi, d, theta):
        R = 8.0
        alpha_rad = np.deg2rad(alpha_deg)
        term = d + R * np.sin(alpha_rad - phi)
        return np.sin(theta) * term

    popt, _ = curve_fit(model_func, alpha_deg, delta_z, p0=[1.290, 0.082, 0.00358])
    phi_opt, d_opt, theta_opt = popt

    print("优化后参数：")
    print("phi (rad):", phi_opt)
    print("phi (degrees):", np.degrees(phi_opt))
    print("d (mm):", d_opt)
    print("theta (rad):", theta_opt)
    print("theta (degrees):", np.degrees(theta_opt))


if __name__ == "__main__":
    dp_part3()
