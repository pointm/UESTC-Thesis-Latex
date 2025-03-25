import math
import matplotlib.pyplot as plt
import numpy as np

# 字体配置
plt.rcParams["font.serif"] = ["SimSun", "Times New Roman"]
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 15
plt.rcParams["axes.unicode_minus"] = False


def qwq_part1():
    ## QWQ的结果
    R = 8.0
    phi = 2.0  # rad
    d = 1.561
    theta = -0.003523  # rad

    ## 修正QWQ的结果
    R = 8.0
    phi = 2.0  # rad
    d = -1.56  # 修正符号
    theta = 0.003523  # 修正为正值

    ## DEEPSEEK结果
    # R = 8.0
    # phi = 5.2325  # rad
    # d = 1.49
    # theta = 0.003691  # rad

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

    # 提取实际测量数据
    angles_deg = [p[0] for p in points]
    actual_dz = [p[1] for p in points]

    # 计算理论值并存储
    computed_dz = []
    print("验证结果：")
    for angle_deg, delta_z in points:
        alpha = math.radians(angle_deg)
        term = d - R * math.cos(alpha - phi)
        computed = math.sin(theta) * term
        computed_dz.append(computed)
        print(f"Angle: {angle_deg}°, 实际Δz: {delta_z:.4f}, 计算Δz: {computed:.4f}")

    # 可视化结果
    plt.figure(figsize=(10, 6))
    plt.plot(angles_deg, computed_dz, "r-", label="理论计算值", marker="o")
    plt.scatter(angles_deg, actual_dz, s=100, label="实际测量值", zorder=3)

    plt.title("Δz 随角度变化对比")
    plt.xlabel("角度 (度)")
    plt.ylabel("Δz (mm)")
    plt.xticks(range(0, 360, 45))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


def qwq_part2():

    # 给定数据点的角度（度）和Δz值
    angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
    dz = np.array([-0.018, 0, 0.021, 0.022, 0.011, -0.014, -0.032, -0.034])

    # 将角度转换为弧度
    angles_rad = np.radians(angles_deg)

    # 构建矩阵A
    cos_angles = np.cos(angles_rad)
    sin_angles = np.sin(angles_rad)
    A = np.array([[1, c, s] for c, s in zip(cos_angles, sin_angles)])

    # 使用最小二乘法求解D、B、C
    x, residuals, rank, s = np.linalg.lstsq(A, dz, rcond=None)
    D, B, C = x

    # 计算sinθ、θ、d和φ
    sin_theta = np.sqrt(B**2 + C**2) / 8  # R=8mm
    theta = np.arcsin(sin_theta)
    d = D / sin_theta
    phi = np.arctan2(
        C, B
    )  # 注意：这里可能需要调整符号，因为公式中的推导可能需要考虑符号

    # 将phi转换为弧度（可能需要调整到正确的象限）
    # 由于B和C的符号，我们手动调整phi的计算
    # 根据推导，phi应为arctan(C/B)的正确象限
    phi = np.arctan2(C, B)

    # 输出结果
    print(f"φ (弧度): {phi:.4f}")
    print(f"d (毫米): {d:.4f}")
    print(f"θ (弧度): {theta:.6f}")

    # 旋转轴的方程参数
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    # 旋转轴的方程形式：cos_phi * x + sin_phi * y = d
    # 由于d是负的，方程可以写成：cos_phi * x + sin_phi * y + |d| =0 ?
    # 但根据公式，正确的方程是：cos_phi * x + sin_phi * y = d
    # 因此方程为：
    # 方程：cos_phi * x + sin_phi * y - d = 0
    equation = f"{cos_phi:.4f}x + {sin_phi:.4f}y - {d:.4f} = 0"

    print(f"旋转轴的方程: {equation}")

    # === 新增可视化代码 ===
    # 计算理论值
    computed_dz = []
    for angle_deg in angles_deg:
        alpha = np.radians(angle_deg)
        term = d - 8 * np.cos(alpha - phi)  # R=8mm
        computed = np.sin(theta) * term
        computed_dz.append(computed)

    # 可视化对比
    plt.figure(figsize=(10, 6))
    plt.plot(angles_deg, computed_dz, "r-", label="理论计算值", marker="o")
    plt.scatter(angles_deg, dz, s=100, label="实际测量值", zorder=3)

    plt.title("Δz 随角度变化对比 (qwq_part2)")
    plt.xlabel("角度 (度)")
    plt.ylabel("Δz (mm)")
    plt.xticks(range(0, 360, 45))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    qwq_part2()
