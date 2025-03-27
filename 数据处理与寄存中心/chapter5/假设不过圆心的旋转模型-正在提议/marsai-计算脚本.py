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


# 初始猜测
initial_guess = [0.5200906874811719 + 3.14 / 4, -5.66, 0.003]

# 优化（增加边界条件约束）
result = least_squares(
    residual, initial_guess, bounds=([-np.inf, -np.inf, 0], [np.inf, np.inf, np.pi / 2])
)
phi_opt, d_opt, theta_opt = result.x  # 添加这行关键解包语句

# 输出结果（增加收敛性检查和残差分析）
print(f"优化状态：{'成功' if result.success else '失败'} (原因：{result.message})")
print(f"残差平方和：{np.sum(result.fun**2):.6f}")
print("\n优化后的参数：")
print(f"φ = {np.degrees(phi_opt):.1f}° ({phi_opt:.4f} rad)")
print(f"d = {d_opt:.4f} mm ({abs(d_opt):.4f} mm 到原点的垂直距离)")
print(f"θ = {theta_opt:.4f} rad ({np.degrees(theta_opt):.1f}°)")

# 旋转轴方程推导（新增部分）
print("\n旋转轴方程 (xOy平面):")
print(
    f"x*cos({np.degrees(phi_opt):.1f}°) + y*sin({np.degrees(phi_opt):.1f}°) = {d_opt:.4f}"
)
print(f"或参数方程形式：")
print(f"x = {d_opt:.4f}*cos({phi_opt:.4f}) - t*sin({phi_opt:.4f})")
print(f"y = {d_opt:.4f}*sin({phi_opt:.4f}) + t*cos({phi_opt:.4f})")
print(f"z = 0 (∀ t ∈ ℝ)")

# 验证预测值
phi_rad = phi_opt
predicted_dz = np.sin(theta_opt) * (d_opt + R * np.sin(alpha_rad - phi_rad))
print("预测的Δz值：", np.round(predicted_dz, 4))
