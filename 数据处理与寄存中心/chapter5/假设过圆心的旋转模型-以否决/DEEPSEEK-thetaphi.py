# DP的预测结果虽说很准确但是实际仿真时候觉得偏心旋转结果一般
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians, degrees

# 字体配置
plt.rcParams["font.serif"] = ["SimSun", "Times New Roman"]
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 15
plt.rcParams["axes.unicode_minus"] = False


def dp_part1():
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


def dp_part2():
    # 输入数据
    angles_deg = np.array([0, 45, 90, 135, 180, 225, 270, 315])
    delta_z = np.array([-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034])

    # 转换为弧度
    alpha = np.deg2rad(angles_deg)

    # 构造设计矩阵
    X = np.column_stack([np.sin(alpha), np.cos(alpha)])

    # 求解线性回归参数
    A, B = np.linalg.lstsq(X, delta_z, rcond=None)[0]

    # 计算偏离角度θ（单位：度）
    theta_rad = np.arctan2(-B, A)
    theta_deg = np.rad2deg(theta_rad) % 360

    # 计算旋转角度φ（单位：度）
    R = 8
    C = np.sqrt(A**2 + B**2)
    phi_rad = np.arcsin(C / R)
    phi_deg = np.rad2deg(phi_rad)

    # 结果输出
    print(f"偏离角度θ：{theta_deg:.2f} 度")
    print(f"旋转角度φ：{phi_deg:.2f} 度")


def dp_part3():

    # 给定数据
    alpha_deg = np.array([0, 45, 90, 135, 180, 225, 270, 315])
    h_observed = np.array([-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034])
    R = 8  # 毫米

    # 构造设计矩阵
    X = np.array(
        [
            [
                np.sin(np.deg2rad(a) / 2),
                np.cos(np.deg2rad(a) / 2),
            ]  # 修正括号闭合，添加逗号分隔元素
            for a in alpha_deg
        ]
    )

    # 最小二乘拟合（保留原有线性解作为初始猜测）
    coeffs, residuals, _, _ = np.linalg.lstsq(X, h_observed, rcond=None)
    C, D = coeffs

    # 新增非线性拟合部分
    from scipy.optimize import curve_fit

    def nonlinear_model(alpha, delta_phi, theta):
        return 2 * R * np.sin((np.deg2rad(alpha) - delta_phi) / 2) * np.sin(theta)

    # 使用线性解作为初始猜测
    A_linear = np.sqrt(C**2 + D**2)
    delta_phi_initial = -2 * np.arctan2(D, C)
    theta_initial = np.arcsin(A_linear / (2 * R))

    # 执行非线性优化
    params_opt, _ = curve_fit(
        nonlinear_model, alpha_deg, h_observed, p0=[delta_phi_initial, theta_initial]
    )
    delta_phi_rad, theta_rad = params_opt

    # 更新计算结果
    delta_phi_deg = np.rad2deg(delta_phi_rad) % 360
    theta_deg = np.rad2deg(theta_rad)

    # 重新计算预测值
    h_predicted = nonlinear_model(alpha_deg, delta_phi_rad, theta_rad)

    # 新增可视化代码
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(alpha_deg, h_observed, "o-", label="实际值", markersize=8)
    plt.plot(alpha_deg, h_predicted, "s--", label="预测值", markersize=6)
    plt.xlabel("旋转角度 α (度)", fontsize=12)
    plt.ylabel("高度差 Δz (mm)", fontsize=12)
    plt.title("实际观测值与模型预测值对比", fontsize=14)
    plt.xticks(np.arange(0, 360, 45))
    plt.legend(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    # 输出结果
    print(f"Δφ = {delta_phi_deg:.2f} 度")
    print(f"θ = {theta_rad:.6f} rad")
    plt.show()  # 显示图表

    print("\n验证预测与实际值对比:")
    for a, h_obs, h_pred in zip(alpha_deg, h_observed, h_predicted):
        print(
            f"α={a}°: 观测h={h_obs:.3f}, 预测h={h_pred:.3f}, 残差={h_obs - h_pred:.3f}"
        )


if __name__ == "__main__":
    dp_part3()
