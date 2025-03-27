# 看不懂QWQ在做什么，但是貌似很厉害的样子，仿真结果拟合得一般但是勉强能看吧
import numpy as np
from scipy.optimize import least_squares, minimize  # 添加minimize导入
import matplotlib.pyplot as plt


# 字体配置
plt.rcParams["font.serif"] = ["SimSun", "Times New Roman"]
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 15
plt.rcParams["axes.unicode_minus"] = False
# 新增方法选择开关
METHOD = "linear"  # 可选 'linear' 或 'nonlinear'

# 公共数据集（保持原数据不变）
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


def optimize_nonlinear_method():
    """非线性最小二乘法优化方法（原主要算法）"""
    # 保持原处理逻辑不变
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
        residual,
        initial_guess,
        bounds=([-np.pi, 0], [np.pi, 2 * np.pi]),  # 修改边界范围
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


def optimize_linear_method():
    """线性矩阵解法（新增第二种算法）"""
    # 数据准备
    angles_deg = [angle for angle, _ in points]
    dz = [dz for _, dz in points]
    angles_rad = np.radians(angles_deg)

    # 原矩阵解法核心逻辑
    A_matrix = np.array([[np.sin(angle), np.cos(angle)] for angle in angles_rad])
    b = np.array(dz)
    A_val, B_val = np.linalg.lstsq(A_matrix, b, rcond=None)[0]

    # 计算结果
    theta_rad = np.arctan2(-B_val, A_val)
    theta_deg = np.degrees(theta_rad) % 360
    sin_phi = np.sqrt(A_val**2 + B_val**2) / 8
    phi_rad = np.arcsin(sin_phi)
    phi_deg = np.degrees(phi_rad)

    # 输出结果
    print(f"\n旋转轴偏离角度θ = {theta_deg:.1f}°")
    print(f"旋转角度φ = {phi_deg:.2f}°")

    # 计算残差
    predicted_dz = A_val * np.sin(angles_rad) + B_val * np.cos(angles_rad)
    residuals = dz - predicted_dz
    print("\n预测Δz与实际Δz的残差：")
    for angle, residual in zip(angles_deg, residuals):
        print(f"角度{angle}°: 残差 = {residual:.4f} mm")


def new_method():
    # 数据点
    alpha_deg = [0, 45, 90, 135, 180, 225, 270, 315]
    h_values = [-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034]

    # 转换角度为弧度
    alpha_rad = np.deg2rad(alpha_deg)
    R = 8  # 半径

    # 目标函数：计算残差平方和
    def objective(params):
        delta_phi, theta = params  # 单位：弧度
        predicted_h = R * np.sin(theta) * np.sin((alpha_rad - delta_phi))
        residuals = h_values - predicted_h
        return np.sum(residuals**2)

    # 初始猜测（Δφ=135度，θ=0.1度）
    initial_guess = np.deg2rad([135, 0.1])

    # 进行优化
    result = minimize(objective, initial_guess, method="BFGS")

    # 提取结果（转换为角度）
    delta_phi_opt = np.rad2deg(result.x[0])
    theta_opt = np.rad2deg(result.x[1])

    print(f"旋转轴的偏移角度 Δφ = {delta_phi_opt:.1f}°")
    print(f"旋转轴的倾斜角度 θ = {result.x[1]:.5f} rad")

    # 新增可视化部分
    plt.figure(figsize=(6.5, 5))
    # 计算预测值
    predicted_h = 2 * R * np.sin(result.x[1]) * np.sin((alpha_rad - result.x[0]) / 2)
    # 绘制测量值
    plt.scatter(alpha_deg, h_values, label="测量值", marker="o", color="red")
    # 绘制预测值
    plt.scatter(
        alpha_deg, predicted_h, label="预测值", marker="x", color="blue", linewidths=1.5
    )

    plt.xlabel("旋转角度α (度)")
    plt.ylabel("Δz (mm)")
    # plt.title("测量值与预测值对比")
    plt.legend()
    plt.grid(True)
    plt.xticks(np.arange(0, 360, 45))
    plt.show()


if __name__ == "__main__":
    new_method()
