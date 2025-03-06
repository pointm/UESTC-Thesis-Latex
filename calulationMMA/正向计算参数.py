import math
import numpy as np
import matplotlib.pyplot as plt

# 新增中文字体配置 ================
plt.rcParams["font.sans-serif"] = ["SimHei"]  # Windows系统字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
# ================================

# 参数定义 (单位转换: 1e-3 转换为米)
a = 10.668e-3  # 矩形波导长边
b = 4.3188e-3  # 矩形波导短边
f = 19.65e9  # 匹配频率
omega = 2 * math.pi * f
c = 3e8  # 光速
epsilon_r = 9.4  # 蓝宝石相对介电常数
mu_11 = 1.841  # 圆波导TE11模特征值

# 圆波导等效直径计算
Dia = math.sqrt(a**2 + b**2)
R = Dia / 2

# 自由空间波长
lambda_ = c / f

# 矩形波导参数计算
lambda_c_rect = 2 * a


def calculate_lambda_g(lambda_, lambda_c):
    """计算波导工作波长"""
    return lambda_ / math.sqrt(1 - (lambda_ / lambda_c) ** 2)


lambda_g_rect = calculate_lambda_g(lambda_, lambda_c_rect)

# 圆波导参数计算
lambda_c_circ = (2 * math.pi * R) / mu_11
lambda_g_circ = calculate_lambda_g(
    lambda_, lambda_c_circ
)  # 如果也需要封装可以复用该函数
lambda_g_circ = lambda_ / math.sqrt(1 - (lambda_ / lambda_c_circ) ** 2)

print(f"矩形波导的截止波长: {lambda_c_rect*1000:.2f}mm")
print(f"工作波长: {lambda_g_rect*1000:.2f}mm")
print(f"圆波导截止波长: {lambda_c_circ*1000:.2f}mm")
print(f"圆波导工作波长: {lambda_g_circ*1000:.2f}mm")

# 计算电纳BT
beta = 2 * math.pi / lambda_g_rect
phi = (math.pi * b) / Dia


def delta_2n(n):
    return 1 / math.sqrt(1 - (beta * Dia / (2 * math.pi * n)) ** 2) - 1


sum_term = 2 * sum(
    (math.sin(n * phi) ** 2) / (n**3 * phi**2) * delta_2n(2 * n) for n in range(1, 6)
)

BT = (b / lambda_g_rect) * (
    2 * math.log((Dia**2 - b**2) / (4 * b * Dia))
    + (b / Dia + Dia / b) * math.log((Dia + b) / (Dia - b))
    + sum_term
)
print(f"等效电纳 B_T = {BT:.4f}")

# 计算特性阻抗比
Z_rect = (2 * b / a) * 120 * math.pi / math.sqrt(1 - (c / (2 * a * f)) ** 2)
Z_circ = 2.02 * 120 * math.pi / math.sqrt(1 - (c / (3.413 * R * f)) ** 2)
k = Z_circ / Z_rect
print(f"归一化圆波导特性阻抗比 k = {k:.4f}")

# 计算窗片最大厚度
Bd_max = math.sqrt((1 + BT**2) ** 2 * k**4 + 2 * (BT**2 - 1) * k**2 + 1) / k
t_max = Bd_max / ((epsilon_r - 1) * (omega / c) * (lambda_g_circ / lambda_))
print(f"窗片厚度最大值: {t_max*1000:.2f}mm")


# 解二次方程的函数
def solve_tan_gamma_l(Bd):
    A = k * (Bd * (BT**2 + 1) * k - 2 * BT)
    B = 2 - 2 * k * (BT * (Bd + BT * k) + k)
    C = Bd + 2 * BT * k

    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        return []
    return [
        (-B + math.sqrt(discriminant)) / (2 * A),
        (-B - math.sqrt(discriminant)) / (2 * A),
    ]


# 生成Bd范围并求解
Bd_values = np.linspace(0.01, Bd_max, 60)
real_solutions = []
positive_solutions = []  # 新增正根存储

for Bd in Bd_values:
    roots = solve_tan_gamma_l(Bd)
    for root in roots:
        real_solutions.append((Bd, root))
        # 添加正根过滤条件
        if root > 0:
            positive_solutions.append((Bd, root))
# 可视化（在原可视化代码后添加正根可视化）
plt.figure(figsize=(10, 6))
# 原所有解可视化
# 可视化
x = [sol[0] for sol in real_solutions]
y = [sol[1] for sol in real_solutions]
plt.scatter(x, y, c="red", s=10, alpha=0.3, label="所有解")
# 新增正根可视化
x_pos = [sol[0] for sol in positive_solutions]
y_pos = [sol[1] for sol in positive_solutions]
plt.scatter(x_pos, y_pos, c="blue", s=30, label="正根解")

plt.xlabel("Bd")
plt.ylabel("tan(Γl)")
plt.title("实数解分布（蓝色为有效正根）")
plt.legend()
plt.grid(True)
plt.show()

# 新处理逻辑 ==============================================
gamma = 2 * math.pi / lambda_g_circ

# 修改为存储元组的列表
pair_list = []  # 元素格式为 (t(mm), l(mm))

for bd, tan_gl in positive_solutions:
    # 计算窗片厚度t
    t = bd / ((epsilon_r - 1) * (omega / c) * (lambda_g_circ / lambda_))

    # 计算传播长度l
    gl_radians = math.atan(tan_gl)
    if gl_radians < 0:
        gl_radians += math.pi
    l = gl_radians / gamma

    # 将两个值封装为元组存入列表
    pair_list.append((t * 1000, l * 1000))  # 同时转换毫米单位

# 新可视化窗口 ============================================
plt.figure(figsize=(12, 6))
ax1 = plt.gca()  # 获取当前坐标轴

# 绘制物理长度（左轴）
sc = ax1.scatter(
    [x[0] for x in pair_list],
    [x[1] for x in pair_list],
    c="blue",
    s=30,
    alpha=0.6,
    label="物理长度",
)
ax1.set_xlabel("窗片厚度 t (mm)")
ax1.set_ylabel("传播长度 l (mm)", color="blue")

# 创建右轴显示电长度
ax2 = ax1.twinx()
# 计算电长度（l/λ_g） λ_g单位已转换为mm
electrical_lengths = [
    (l / 1000) / (lambda_g_circ) for _, l in pair_list
]  # 单位转换为米后计算
ax2.scatter(
    [x[0] for x in pair_list],
    electrical_lengths,
    c="red",
    s=30,
    alpha=0.6,
    marker="x",
    label="电长度",
)
ax2.set_ylabel("电长度 l/λ_g", color="red")

plt.title("窗片厚度与传播长度关系（红×为电长度）")
plt.grid(True)
plt.tight_layout()

# 合并图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc="best")

plt.show()
