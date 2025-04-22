import math
import numpy as np
import matplotlib.pyplot as plt

# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix
# 设置字体的大小，
label_size = 16  # xy轴标签的大小
legend_size = 18  # 图例的大小
axis_size = 16  # 坐标轴刻度标签的大小
# ================================

# 参数定义 (单位转换: 1e-3 转换为米)
a = 28.499e-3  # 矩形波导长边
b = 12.624e-3  # 矩形波导短边
frequency_range = np.linspace(7e9, 9e9, 1001)
f = 8.28e9  # 匹配频率
omega = 2 * math.pi * f
c = 3e8  # 光速
epsilon_r = 9.4  # 蓝宝石相对介电常数
mu_11 = 1.841  # 圆波导TE11模特征值
match_l = 8.309249082662044e-3  # 匹配段长度
thickness = 0.6198397534967082e-3  # 窗片厚度

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


# 修改频率响应计算部分
# 新增频率响应计算 ==========================================
s21_results = []
s11_results = []
return_loss = []

for f in frequency_range:
    try:
        # 重新计算频率相关参数
        omega = 2 * math.pi * f
        lambda_ = c / f

        # 重新计算波导参数
        lambda_g_rect = calculate_lambda_g(lambda_, 2 * a)
        lambda_c_circ = (2 * math.pi * R) / mu_11
        lambda_g_circ = lambda_ / math.sqrt(1 - (lambda_ / lambda_c_circ) ** 2)
        gamma = 2 * math.pi / lambda_g_circ  # 当前频率下的传播常数

        # 重新计算电纳BT
        beta = 2 * math.pi / lambda_g_rect
        sum_term = 2 * sum(
            (math.sin(n * phi) ** 2) / (n**3 * phi**2) * delta_2n(2 * n)
            for n in range(1, 6)
        )
        BT = (b / lambda_g_rect) * (
            2 * math.log((Dia**2 - b**2) / (4 * b * Dia))
            + (b / Dia + Dia / b) * math.log((Dia + b) / (Dia - b))
            + sum_term
        )

        # 重新计算阻抗比
        Z_rect = (2 * b / a) * 120 * math.pi / math.sqrt(1 - (c / (2 * a * f)) ** 2)
        Z_circ = 2.02 * 120 * math.pi / math.sqrt(1 - (c / (3.413 * R * f)) ** 2)
        k = Z_circ / Z_rect

        # 使用固定参数计算当前Bd
        Bd = (epsilon_r - 1) * (omega / c) * (lambda_g_circ / lambda_) * thickness

        # 直接计算相位参数
        two_gl = 2 * gamma * match_l  # 直接使用匹配段长度计算相位参数

        # 计算B-C表达式
        BC = (-1j / (2 * k)) * (
            Bd * (BT**2 + 1) * k**2 * (1 - math.cos(two_gl))
            + Bd * (1 + math.cos(two_gl))
            + 4 * BT * k * math.cos(two_gl)
            - 2 * (k * (BT * (Bd + BT * k) + k) - 1) * math.sin(two_gl)
        )

        # 计算S21参数
        S21 = 1 / (1 + 0.25 * abs(BC) ** 2)
        S21_linear = abs(S21)
        S21_db = 20 * math.log10(S21_linear) if S21_linear > 0 else float("-inf")

        # 计算S11和回波损耗
        S11_linear = math.sqrt(abs(1 - S21_linear**2))
        S11_db = 20 * math.log10(S11_linear) if S11_linear > 0 else float("-inf")

        s21_results.append(S21_db)
        s11_results.append(S11_db)
        return_loss.append(-S11_db)

    except Exception as e:
        print(f"频率 {f/1e9} GHz 计算异常: {str(e)}")
        s21_results.append(float("-inf"))
        s11_results.append(float("-inf"))
        return_loss.append(float("inf"))

# 修改可视化部分 ============================================
# 字体配置
plt.rcParams.update(
    {
        "font.family": "SimSun",
        "font.size": 15,
        "axes.unicode_minus": False,
        "mathtext.fontset": "cm",
    }
)

# 图表初始化
fig = plt.figure(figsize=(7.5, 6.5))
ax = fig.add_subplot(111)

# 绘制主曲线
ax.plot(
    frequency_range / 1e9,
    s21_results,
    color="#1f77b4",
    lw=2,
    label=r"$\mathrm{|S_{21}|}$",
)
ax.plot(
    frequency_range / 1e9,
    s11_results,
    color="#d62728",
    ls="--",
    lw=2,
    label=r"$\mathrm{|S_{11}|}$",
)

# 新增缺失变量定义 ========================
freq_ghz = frequency_range / 1e9
s11_array = np.array(s11_results)
mask = s11_array <= -20
# =====================================

# 带宽标注区域
if np.any(mask):
    indices = np.where(mask)[0]
    start_freq = freq_ghz[indices[0]]
    end_freq = freq_ghz[indices[-1]]
    bandwidth = end_freq - start_freq

    # 修正fill_between参数
    ax.fill_between(
        freq_ghz,
        -40,
        s11_array,
        where=mask,
        facecolor="gray",
        alpha=0.3,
        label=f"回波损耗-20dB带宽\n({bandwidth:.2f} GHz)",
    )

    # 修正annotate参数
    ax.annotate(
        f"{bandwidth:.2f} GHz 带宽",
        xy=((start_freq + end_freq) / 2, -22),
        xytext=((start_freq + end_freq) / 2, -18),
        ha="center",
        va="bottom",
        arrowprops=dict(facecolor="black", arrowstyle="->"),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5),
    )

# 样式配置
ax.set(
    xlabel="频率 $\mathrm{(GHz)}$",
    ylabel="幅值 $\mathrm{(dB)}$",
    xlim=(frequency_range[0] / 1e9, frequency_range[-1] / 1e9),
    ylim=(-40, 0),
)

# 新增参数文本框内容 ========================
param_text = (
    f"设计参数:\n"
    f"a = {a*1e3:.3f} mm\n"
    f"b = {b*1e3:.3f} mm\n"
    f"ε_r = {epsilon_r}\n"
    f"t = {thickness*1e3:.3f} mm"
)
# =======================================

# 添加参数框
ax.text(
    0.97,
    0.28,
    param_text,
    transform=ax.transAxes,
    ha="right",
    va="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    fontsize=15,
)

# 输出设置
plt.tight_layout(pad=1.0)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()
