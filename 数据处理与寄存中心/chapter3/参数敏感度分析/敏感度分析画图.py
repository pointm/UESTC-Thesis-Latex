import skrf as rf
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix
# 设置字体的大小，
label_size = 23  # xy轴标签的大小
legend_size = 20  # 图例的大小
axis_size = 20  # 坐标轴刻度标签的大小
# 预设配置字典（修改部分）
configs = {
    "TA": {
        "legend_name": "ta",
        "s2p_file_name": [
            "X窗片敏感度-TA_15.92.s2p",
            "X窗片敏感度-TA_16.03.s2p",
            "X窗片敏感度-TA_16.36.s2p",
        ],
        "x_minor_step": 0.5e9,
        "y_minor_step": 5,
        "figsize": (6, 5.5),
    },
    "TB": {
        "legend_name": "tb",
        "s2p_file_name": [
            "X窗片敏感度-TB_10.14.s2p",
            "X窗片敏感度-TB_10.61.s2p",
            "X窗片敏感度-TB_12.22.s2p",
        ],
        "x_minor_step": 0.5e9,
        "y_minor_step": 5,
        "figsize": (6, 5.5),
    },
    "WR": {
        "legend_name": "wr",
        "s2p_file_name": [
            "X窗片敏感度-WR_10.65.s2p",
            "X窗片敏感度-WR_11.49.s2p",
            "X窗片敏感度-WR_12.06.s2p",
        ],
        "x_minor_step": 0.5e9,
        "y_minor_step": 5,
        "figsize": (6, 5.5),
    },
    "WT": {
        "legend_name": "wt",
        "s2p_file_name": [
            "X窗片敏感度-WT_0.87.s2p",
            "X窗片敏感度-WT_0.91.s2p",
            "X窗片敏感度-WT_0.98.s2p",
        ],
        "x_minor_step": 0.5e9,
        "y_minor_step": 5,
        "figsize": (6, 5.5),
    },
    "TRH": {
        "legend_name": "trh",
        "s2p_file_name": [
            "X敏感度-TRH_1.47.s2p",
            "X敏感度-TRH_1.69.s2p",
            "X敏感度-TRH_1.77.s2p",
        ],
        "x_minor_step": 0.5e9,
        "y_minor_step": 5,
        "figsize": (6, 5.5),
    },
}

# 通过修改这里切换配置 ↓
config_selector = "TRH"
selected_config = configs[config_selector]

# 加载TOUCHSTONE数据（修改部分）- 改为加载全部三个文件
networks = [
    rf.Network(os.path.join(script_dir, fname))
    for fname in selected_config["s2p_file_name"]
]

# 绘制三条 S11 曲线（修改部分）
# 在循环外部先提取所有参数值并排序
param_values = [
    float(fname.split(f"{selected_config['legend_name'].upper()}_")[1].split(".s2p")[0])
    for fname in selected_config["s2p_file_name"]
]
sorted_values = sorted(param_values)
min_val, max_val = sorted_values[0], sorted_values[-1]

# 在循环内部修改判断逻辑 ▼▼▼
for network, s2p_file_name in zip(networks, selected_config["s2p_file_name"]):
    # 获取图例名称（从配置中动态获取）
    legend_name = selected_config["legend_name"]
    # 提取参数值（支持任意前缀格式）
    param_value = s2p_file_name.split(f"{legend_name.upper()}_")[1].split(".s2p")[0]

    # 生成LaTeX格式标签（使用配置中的legend_name）
    label = rf"$\mathrm{{{legend_name}}}={param_value}\ \mathrm{{mm}}$"

    # 设置线型（保持原有逻辑）
    current_value = float(param_value)  # 转换为浮点数比较

    # 动态判断极值设置线型
    line_style = "--" if current_value in (min_val, max_val) else "-"

    network.s11.plot_s_db(
        label=label,
        lw=2,
        linestyle=line_style,
    )


# 设置坐标轴标签和标题
plt.xlabel("频率/ GHz", fontsize=label_size)
plt.ylabel("幅值/ dB", fontsize=label_size)

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
# plt.legend(
#     frameon=False, fontsize=legend_size, bbox_to_anchor=(0.5, 0.5)
# )  # 遮住时候用，没遮住不用

# 获取当前轴，准备设置子刻度
ax = plt.gca()
# 设置X/Y轴次要刻度（修改部分）
ax.xaxis.set_minor_locator(ticker.MultipleLocator(selected_config["x_minor_step"]))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(selected_config["y_minor_step"]))

plt.grid(which="both", linestyle="--", linewidth=0.5)
# 显示图表
plt.tight_layout()
plt.show()
