import numpy as np
from scipy.optimize import least_squares

# 数据
alpha_deg = np.array([0, 45, 90, 135, 180, 225, 270, 315])
alpha_rad = np.radians(alpha_deg)
dz = np.array([-0.018, 0.000, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034])
R = 8


# 残差函数
def residual(params):
    phi, d, theta = params
    predicted = np.sin(theta) * (d + R * np.sin(alpha_rad - phi))
    return predicted - dz


# 初始猜测（φ=45°, d=-5.66, θ=0.003）
initial_guess = [np.radians(45), -5.66, 0.003]

# 优化
result = least_squares(residual, initial_guess)
phi_opt, d_opt, theta_opt = result.x

# 输出结果
print(f"优化后的参数：")
print(f"φ = {np.degrees(phi_opt):.1f}° ({phi_opt:.4f} rad)")
print(f"d = {d_opt:.4f} mm")
print(f"θ = {theta_opt:.4f} rad ({np.degrees(theta_opt):.1f}°)")

# 旋转轴方程和方向向量
phi_rad = phi_opt
direction_vector = np.array([-np.sin(phi_rad), np.cos(phi_rad), 0])
print(f"旋转轴方向向量：{direction_vector}")

# 验证预测值
predicted_dz = np.sin(theta_opt) * (d_opt + R * np.sin(alpha_rad - phi_rad))
print("预测的Δz值：", np.round(predicted_dz, 4))
