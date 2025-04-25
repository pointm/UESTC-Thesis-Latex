import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import os
import matplotlib.ticker as ticker


def parse_tsv_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # 按参数块分割数据
    blocks = content.split("#Parameters = ")[1:]
    data_dict = {}

    for block in blocks:
        # 解析参数
        params_str, data_str = block.split("\n", 1)
        params = dict(pair.split("=") for pair in params_str.strip("{}").split("; "))

        # 转换为数值类型
        theta = int(float(params["theta"]))
        psi = int(float(params["phi"]))
        realpsi = int(float(params["realphi"]))

        # 读取数据表
        df = pd.read_csv(
            StringIO(data_str.strip()),
            sep="\t",
            comment="#",
            header=None,
            names=["Length_mm", "E_field"],
        )

        # 使用(theta, realpsi)作为唯一标识
        key = (theta, realpsi)
        if key not in data_dict:
            data_dict[key] = []
        data_dict[key].append(df)

    # 合并相同参数的数据
    return {k: pd.concat(v) for k, v in data_dict.items()}


# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix
# 设置字体的大小，
label_size = 20  # xy轴标签的大小
legend_size = 20  # 图例的大小
axis_size = 18  # 坐标轴刻度标签的大小

# 使用示例
filepath = os.path.dirname(os.path.abspath(__file__))
filename = "X频段不同THETAPHI角x电场幅值.txt"
file_path = os.path.join(filepath, filename)
data_groups = parse_tsv_file(file_path)

# 可视化（示例：固定theta，不同psi的比较）
# ==== 用户可配置参数 ====
# 使用元组列表指定要显示的(theta, psi)组合，空列表显示全部数据
# SELECTED_GROUPS = [(0, 0), (3, 90)]  # theta=0°, psi=0°  # theta=3°, psi=90°
# SELECTED_GROUPS = []  # 空的代表全部
SELECTED_GROUPS = [(3, 0), (3, 180)]  #
# ========================

# 修改可视化部分
plt.figure(figsize=(7, 6))
for (theta, psi), df in data_groups.items():
    if not SELECTED_GROUPS or (theta, psi) in SELECTED_GROUPS:
        plt.plot(
            df["Length_mm"],
            df["E_field"],
            label=f"$\\theta$ = {theta}°, $\\psi$ = {psi}°",
            lw=2,
        )


# 启用次要刻度
plt.minorticks_on()

# 自定义次要刻度位置
plt.tick_params(
    axis="both", which="minor", bottom=True, top=False, left=True, right=False
)

# 设置坐标轴刻度标签大小
plt.tick_params(axis="both", which="major", labelsize=axis_size)
plt.tick_params(axis="both", which="minor")

# 设置图例
plt.legend(frameon=False, fontsize=legend_size)

# 获取当前轴，准备设置子刻度
ax = plt.gca()
# 设置X/Y轴次要刻度（修改部分）
ax.xaxis.set_minor_locator(ticker.MultipleLocator(2.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(100))

plt.grid(which="both", linestyle="--", linewidth=0.5)

# 应用字体大小设置
plt.xlabel("x轴坐标 / mm", fontsize=label_size)
plt.ylabel("电场强度/ V/m", fontsize=label_size)
plt.legend(fontsize=legend_size)
plt.tick_params(axis="both", which="major", labelsize=axis_size)  # 坐标轴刻度
plt.tight_layout()
plt.show()
