import math

R = 8.0  # 半径（毫米）
wt = 1.035  # 厚度（毫米）
z_center = wt / 2.0  # 顶面圆心的z坐标

# 旋转轴线参数
P0_x = 0.0
P0_y = 0.0055 / 0.003203  # 计算P₀的y坐标
P0_z = 0.0

# 方向向量的原始分量
v_x = 0.003203
v_y = 0.001834
v_z = 0.0

# 计算单位方向向量
v_length = math.sqrt(v_x**2 + v_y**2)
u_x = v_x / v_length
u_y = v_y / v_length
u_z = 0.0

theta_rotation = 0.003691  # 旋转角度（弧度）

angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
angles_rad = [math.radians(d) for d in angles_deg]

results = []

for angle in angles_rad:
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    # 当前点的坐标
    Q_x = R * cos_theta
    Q_y = R * sin_theta
    Q_z = z_center

    # 计算Q-P₀的向量
    delta_x = Q_x - P0_x
    delta_y = Q_y - P0_y
    delta_z = Q_z - P0_z

    # 计算叉乘的z分量
    term_z = u_x * delta_y - u_y * delta_x

    delta_z_val = theta_rotation * term_z
    results.append(delta_z_val)

# 输出结果
for i in range(len(angles_deg)):
    print(f"θ={angles_deg[i]}°: Δz = {results[i]:.4f} mm")
